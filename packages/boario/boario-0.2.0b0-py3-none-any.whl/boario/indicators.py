# BoARIO : The Adaptative Regional Input Output model in python.
# Copyright (C) 2022  Samuel Juhel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

from typing import Union
from boario.simulation import Simulation
import numpyencoder
import json
import pathlib
import numpy as np
import pandas as pd
import itertools
from boario.utils import misc
import dask.dataframe as da
from boario import logger

__all__ = ['Indicators']

def df_from_memmap(memmap:np.memmap, indexes:dict) -> pd.DataFrame:
    a = pd.DataFrame(memmap, columns=pd.MultiIndex.from_product([indexes["regions"], indexes["sectors"]]))
    a['step'] = a.index
    return a

def stock_df_from_memmap(memmap:np.memmap, indexes:dict, timesteps:int, timesteps_simulated:int) -> pd.DataFrame:
    a = pd.DataFrame(memmap.reshape(timesteps*indexes["n_sectors"],-1), index=pd.MultiIndex.from_product([timesteps, indexes["sectors"]], names=['step', 'stock of']), columns=pd.MultiIndex.from_product([indexes["regions"], indexes["sectors"]]))
    a = a.loc[pd.IndexSlice[:timesteps_simulated,:]]
    return a

class Indicators(object):

    record_files_list = ["classic_demand_record",
                         "final_demand_unmet_record",
                         "iotable_X_max_record",
                         "iotable_XVA_record",
                         "limiting_stocks_record",
                         "overprodvector_record",
                         "rebuild_demand_record",
                         "rebuild_prod_record"
                         ]

    params_list = ["simulated_params", "simulated_events"]

    def __init__(self, data_dict:dict, include_crash:bool = False) -> None:
        logger.info("Instanciating indicators")
        print(data_dict['events'])
        super().__init__()
        if not include_crash:
            if data_dict["has_crashed"]:
                raise RuntimeError("Simulation crashed and include_crash is False, I won't compute indicators")
        steps = [i for i in range(data_dict["n_temporal_units_to_sim"])]

        if "stocks" in data_dict:
            stock_treatement = True
        else:
            stock_treatement = False

        self.prod_df = pd.DataFrame(data_dict["prod"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region','sector']))
        self.prodmax_df = pd.DataFrame(data_dict["prodmax"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        self.overprod_df = pd.DataFrame(data_dict["overprod"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        self.c_demand_df = pd.DataFrame(data_dict["c_demand"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        self.r_demand_df = pd.DataFrame(data_dict["r_demand"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        self.r_prod_df = pd.DataFrame(data_dict["r_prod"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        fd_unmet_df = pd.DataFrame(data_dict["fd_unmet"], columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        if stock_treatement:
            stocks_df = pd.DataFrame(data_dict["stocks"].reshape(data_dict["n_temporal_units_to_sim"]*data_dict["n_sectors"],-1),
                                     index=pd.MultiIndex.from_product([steps, data_dict["sectors"]], names=['step', 'stock of']),
                                     columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
            stocks_df = stocks_df.loc[pd.IndexSlice[:data_dict["n_temporal_units_simulated"],:]]
        else:
            stocks_df = None
        self.prod_df = self.prod_df.rename_axis('step')
        self.prodmax_df = self.prodmax_df.rename_axis('step')
        self.overprod_df = self.overprod_df.rename_axis('step')
        self.c_demand_df = self.c_demand_df.rename_axis('step')
        self.r_demand_df = self.r_demand_df.rename_axis('step')
        self.r_prod_df = self.r_prod_df.rename_axis('step')
        self.fd_unmet_df = fd_unmet_df.rename_axis('step')

        if stock_treatement:
            stocks_df = stocks_df.replace([np.inf, -np.inf], np.nan).dropna(how='all')
            stocks_df = stocks_df.astype(np.float32)
            stocks_df = stocks_df.groupby('stock of').pct_change().fillna(0).add(1).groupby('stock of').cumprod().sub(1) #type: ignore
            stocks_df = stocks_df.melt(ignore_index=False).rename(columns={'variable_0':'region','variable_1':'sector', 'variable_2':'stock of'})
            stocks_df = stocks_df.reset_index()
            stocks_df['step'] = stocks_df['step'].astype("uint16")
            stocks_df['stock of'] = stocks_df['stock of'].astype("category")
            stocks_df['region'] = stocks_df['region'].astype("category")
            stocks_df['sector'] = stocks_df['sector'].astype("category")
        self.df_stocks = stocks_df
        del stocks_df

        self.df_loss = self.fd_unmet_df.melt(ignore_index=False).rename(columns={'variable_0':'region','variable_1':'fd_cat', 'value':'fdloss'}).reset_index()

        self.df_limiting = pd.DataFrame(data_dict["limiting_stocks"].reshape(data_dict["n_temporal_units_to_sim"]*data_dict["n_sectors"],-1),
                                        index=pd.MultiIndex.from_product([steps, data_dict["sectors"]], names=['step', 'stock of']),
                                        columns=pd.MultiIndex.from_product([data_dict["regions"], data_dict["sectors"]], names=['region', 'sector']))
        self.aff_regions = []
        for e in data_dict["events"]:
            self.aff_regions.append(e['aff_regions'])

        self.aff_regions = list(misc.flatten(self.aff_regions))

        self.aff_sectors = []
        for e in data_dict["events"]:
            self.aff_sectors.append(e['aff_sectors'])
        self.aff_sectors = list(misc.flatten(self.aff_sectors))

        self.rebuilding_sectors = []
        for e in data_dict["events"]:
            self.rebuilding_sectors.append(e['rebuilding_sectors'].keys())
            self.rebuilding_sectors = list(misc.flatten(self.rebuilding_sectors))

        if 'r_dmg' in data_dict['events'][0]:
            gdp_dmg_share = data_dict['events'][0]['r_dmg']
        else:
            gdp_dmg_share = -1.
        self.indicators = {
            "region" : self.aff_regions,
            "gdp_dmg_share" : gdp_dmg_share,
            "tot_fd_unmet": "unset",
            "aff_fd_unmet": "unset",
            "rebuild_durations": "unset",
            "shortage_b": False,
            "shortage_date_start": "unset",
            "shortage_date_end": "unset",
            "shortage_date_max": "unset",
            "shortage_ind_max": "unset",
            "shortage_ind_mean": "unset",
            "10_first_shortages_(step,region,sector,stock_of)": "unset",
            "prod_gain_tot": "unset",
            "prod_lost_tot": "unset",
            "prod_gain_unaff": "unset",
            "prod_lost_unaff": "unset",
            "psi" : data_dict['params']['psi_param'],
            "inv_tau" : data_dict['params']['inventory_restoration_tau'],
            "n_temporal_units_to_sim" : data_dict['n_temporal_units_simulated'],
            "has_crashed" : data_dict['has_crashed'],
        }
        self.storage = (pathlib.Path(data_dict['results_storage'])/'indicators.json').resolve()
        self.storage_path = (pathlib.Path(data_dict['results_storage'])).resolve()
        self.save_dfs()

    @classmethod
    def from_model(cls, sim : Simulation, include_crash:bool = False):
        data_dict = {}
        data_dict['params'] = sim.params
        data_dict["n_temporal_units_to_sim"] = sim.n_temporal_units_to_sim
        data_dict["n_temporal_units_simulated"] = sim.n_temporal_units_simulated
        data_dict["has_crashed"] = sim.has_crashed
        data_dict["regions"] = sim.model.regions
        data_dict["sectors"] = sim.model.sectors
        with (pathlib.Path(sim.params["results_storage"])/".simulated_events.json").open() as f:
            events = json.load(f)

        data_dict["events"] = events
        data_dict["prod"] = sim.model.production_evolution
        data_dict["prodmax"] = sim.model.production_cap_evolution
        data_dict["overprod"] = sim.model.overproduction_evolution
        data_dict["c_demand"] = sim.model.classic_demand_evolution
        data_dict["r_demand"] = sim.model.rebuild_demand_evolution
        data_dict["r_prod"] = sim.model.rebuild_production_evolution
        data_dict["fd_unmet"] = sim.model.final_demand_unmet_evolution
        if sim.params['register_stocks']:
            data_dict["stocks"] = sim.model.stocks_evolution
        data_dict["limiting_stocks"] = sim.model.limiting_stocks_evolution
        return cls(data_dict, include_crash)

    @classmethod
    def from_storage_path(cls, storage_path:str, params=None, include_crash:bool = False) -> Indicators:
        return cls(cls.dict_from_storage_path(storage_path, params=params), include_crash)

    @classmethod
    def from_folder(cls, folder: Union[str, pathlib.Path], indexes_file: Union[str, pathlib.Path], include_crash:bool = False) -> Indicators:
        data_dict = {}
        if not isinstance(indexes_file, pathlib.Path):
            indexes_file = pathlib.Path(indexes_file)
            if not indexes_file.exists():
                raise FileNotFoundError(str("File does not exist:"+str(indexes_file)))
        if not isinstance(folder, pathlib.Path):
            folder = pathlib.Path(folder)
            if not folder.exists():
                raise FileNotFoundError(str("Directory does not exist:"+str(folder)))
        with indexes_file.open() as f:
            indexes = json.load(f)

        params_file = {f.stem : f for f in folder.glob("*.json")}
        absentee = [f for f in cls.params_list if f not in params_file.keys()]
        if absentee != []:
            raise FileNotFoundError("Some of the required parameters files not found (looked for {} in {}".format(cls.params_list,folder))

        record_files = [f for f in folder.glob("*record") if f.is_file()]
        absentee = [f for f in cls.record_files_list if f not in [fn.name for fn in record_files]]
        if absentee != []:
            raise FileNotFoundError("Some of the required records are not there : {}".format(absentee))

        with params_file['simulated_params'].open('r') as f:
            params = json.load(f)

        with params_file['simulated_events'].open('r') as f:
            events = json.load(f)

        if "has_crashed" in params:
            data_dict["has_crashed"] = params["has_crashed"]
        else:
            data_dict["has_crashed"] = False
        results_path = data_dict["results_storage"] = folder.absolute()
        t = data_dict["n_temporal_units_to_sim"] = params['n_temporal_units_to_sim']
        data_dict['params'] = params
        data_dict["n_temporal_units_simulated"] = params['n_temporal_units_simulated']
        data_dict["regions"] = indexes["regions"]
        data_dict["n_regions"] = indexes["n_regions"]
        data_dict["sectors"] = indexes["sectors"]
        data_dict["n_sectors"] = indexes["n_sectors"]
        data_dict["events"] = events
        data_dict["prod"] = np.memmap(results_path/"iotable_XVA_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["prodmax"] = np.memmap(results_path/"iotable_X_max_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["overprod"] = np.memmap(results_path/"overprodvector_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["c_demand"] = np.memmap(results_path/"classic_demand_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["r_demand"] = np.memmap(results_path/"rebuild_demand_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["r_prod"] = np.memmap(results_path/"rebuild_prod_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["fd_unmet"] = np.memmap(results_path/"final_demand_unmet_record", mode='r+', dtype='float64',shape=(t,indexes['n_regions']*indexes['n_sectors']))
        data_dict["limiting_stocks"] = np.memmap(results_path/"limiting_stocks_record", mode='r+', dtype='bool',shape=(t*indexes['n_sectors'],indexes['n_industries']))
        if params['register_stocks']:
            if not (results_path/"stocks_record").exists():
                raise FileNotFoundError("Stocks record file was not found {}".format(results_path/"stocks_record"))
            data_dict["stocks"] = np.memmap(results_path/"stocks_record", mode='r+', dtype='float64',shape=(t*indexes['n_sectors'],indexes['n_industries']))
        return cls(data_dict, include_crash)


    @classmethod
    def dict_from_storage_path(cls, storage_path:Union[str,pathlib.Path], params=None) -> dict:
        data_dict = {}
        if not isinstance(storage_path, pathlib.Path):
            storage_path = pathlib.Path(storage_path)
            assert storage_path.exists(), str("Directory does not exist:"+str(storage_path))
        if params is not None:
            simulation_params = params
        else:
            with (storage_path/"simulated_params.json").open() as f:
                simulation_params = json.load(f)
        if (storage_path/simulation_params['results_storage']/"simulated_params.json").exists():
            with (storage_path/simulation_params['results_storage']/"simulated_params.json").open() as f:
                simulation_params = json.load(f)
        with (storage_path/simulation_params['results_storage']/"indexes.json").open() as f:
            indexes = json.load(f)
        with (storage_path/simulation_params['results_storage']/"simulated_events.json").open() as f:
            events = json.load(f)
        t = simulation_params["n_temporal_units_to_sim"]
        if indexes['fd_cat'] is None:
            indexes['fd_cat'] = np.array(["Final demand"])
        results_path = storage_path/pathlib.Path(simulation_params['results_storage'])
        if "has_crashed" in simulation_params:
            data_dict["has_crashed"] = simulation_params["has_crashed"]
        data_dict['params'] = simulation_params
        data_dict["results_storage"] = results_path
        data_dict["n_temporal_units_to_sim"] = t
        data_dict["n_temporal_units_simulated"] = simulation_params['n_temporal_units_simulated']
        data_dict["regions"] = indexes["regions"]
        data_dict["n_regions"] = indexes["n_regions"]
        data_dict["sectors"] = indexes["sectors"]
        data_dict["n_sectors"] = indexes["n_sectors"]
        data_dict["events"] = events
        data_dict["prod"] = np.memmap(results_path/"iotable_XVA_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["prodmax"] = np.memmap(results_path/"iotable_X_max_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["overprod"] = np.memmap(results_path/"overprodvector_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["c_demand"] = np.memmap(results_path/"classic_demand_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["r_demand"] = np.memmap(results_path/"rebuild_demand_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["r_prod"] = np.memmap(results_path/"rebuild_prod_record", mode='r+', dtype='float64',shape=(t,indexes['n_industries']))
        data_dict["fd_unmet"] = np.memmap(results_path/"final_demand_unmet_record", mode='r+', dtype='float64',shape=(t,indexes['n_regions']*indexes['n_sectors']))
        if simulation_params['register_stocks']:
            data_dict["stocks"] = np.memmap(results_path/"stocks_record", mode='r+', dtype='float64',shape=(t*indexes['n_sectors'],indexes['n_industries']))
        data_dict["limiting_stocks"] = np.memmap(results_path/"limiting_stocks_record", mode='r+', dtype='bool',shape=(t*indexes['n_sectors'],indexes['n_industries']))
        return data_dict

    def calc_top_failing_sect(self):
        pass

    def calc_tot_fd_unmet(self):
        self.indicators['tot_fd_unmet'] = self.df_loss['fdloss'].sum()

    def calc_aff_fd_unmet(self):
        #TODO: check this
        self.indicators['aff_fd_unmet'] = self.df_loss[self.df_loss.region.isin(self.aff_regions)]['fdloss'].sum()

    def calc_rebuild_durations(self):
        rebuilding = self.r_demand_df.reset_index().melt(id_vars ="step", var_name=['region','sector'], value_name="rebuild_demand").groupby('step').sum().ne(0).rebuild_demand.to_numpy()
        self.indicators['rebuild_durations'] = [ sum( 1 for _ in group ) for key, group in itertools.groupby( rebuilding ) if key ]

    def calc_recovery_duration(self):
        pass

    def calc_general_shortage(self):
        #TODO: replace hard values by soft.
        a = self.df_limiting.T.stack(level=0)
        #a.index = a.index.rename(['step','sector', 'region']) #type: ignore
        b = a.sum(axis=1).groupby(['step','region','sector']).sum()/8
        c = b.groupby(['step','region']).sum()/8
        c = c.groupby('step').sum()/6
        if not c.ne(0).any():
            self.indicators['shortage_b'] = False
        else:
            self.indicators['shortage_b'] = True
            shortage_date_start = c.ne(0.0).argmax()
            self.indicators['shortage_date_start'] = shortage_date_start
            shortage_date_end = c.iloc[shortage_date_start:].eq(0).argmax()+shortage_date_start
            self.indicators['shortage_date_end'] = shortage_date_end
            self.indicators['shortage_date_max'] = c.argmax()
            self.indicators['shortage_ind_max'] = c.max()
            self.indicators['shortage_ind_mean'] = c.iloc[shortage_date_start:shortage_date_end].mean()

    def calc_first_shortages(self):
        a = self.df_limiting.stack([0,1]) #type: ignore
        a = a.swaplevel(1,2).swaplevel(2,3)
        b = a[a]
        b = b[:10]
        res = list(b.index) #type:ignore
        self.indicators['10_first_shortages_(step,region,sector,stock_of)'] = res

    def calc_tot_prod_change(self):
        df2=self.prod_df.copy()
        #df2.columns=df2.columns.droplevel(0)
        prod_chg = df2 - df2.iloc[0,:]
        prod_chg = prod_chg.round(6)
        prod_chg_sect = prod_chg.sum()
        self.prod_chg_region = pd.concat([prod_chg_sect.loc[pd.IndexSlice[:,self.rebuilding_sectors]].groupby('region').sum(),prod_chg_sect.loc[prod_chg_sect.index.difference(prod_chg_sect.loc[pd.IndexSlice[:,self.rebuilding_sectors]].index)].groupby('region').sum()], keys=['rebuilding', 'non-rebuilding'], names=['sectors affected'])
        self.prod_chg_region = pd.DataFrame({(self.storage_path.parent.name,self.storage_path.name):self.prod_chg_region}).T
        self.prod_chg_region.to_json(self.storage_path/"prod_chg.json", indent=4, orient='split')

        self.indicators['prod_gain_tot'] = prod_chg.mul(prod_chg.gt(0)).sum().sum()
        self.indicators['prod_lost_tot'] = prod_chg.mul(~prod_chg.gt(0)).sum().sum() * (-1)
        prod_chg = prod_chg.drop(self.aff_regions, axis=1)
        self.indicators['prod_gain_unaff'] = prod_chg.mul(prod_chg.gt(0)).sum().sum()
        self.indicators['prod_lost_unaff'] = prod_chg.mul(~prod_chg.gt(0)).sum().sum() * (-1)
        tmp = prod_chg_sect.sort_values(ascending=False,key=abs).head(5).to_dict()
        self.indicators['top_5_sector_chg'] = {str(k): v for k, v in tmp.items()}

    def update_indicators(self):
        logger.info("(Re)computing all indicators")
        self.calc_tot_fd_unmet()
        self.calc_aff_fd_unmet()
        self.calc_rebuild_durations()
        self.calc_recovery_duration()
        self.calc_general_shortage()
        self.calc_tot_prod_change()
        self.calc_fd_loss_region()
        self.calc_first_shortages()

    def write_indicators(self):
        logger.info("Writing indicators to json")
        #self.update_indicators()
        with self.storage.open('w') as f:
            json.dump(self.indicators, f, cls=numpyencoder.NumpyEncoder)

    def calc_fd_loss_region(self):
        df2 = self.df_loss.set_index(['step','region','sector']).unstack([1,2])
        df2 = df2.round(6).sum()
        self.df_loss_region = pd.concat([df2.loc[pd.IndexSlice[:,:,self.rebuilding_sectors]].groupby('region').sum(),df2.loc[df2.index.difference(df2.loc[pd.IndexSlice[:,:,self.rebuilding_sectors]].index)].groupby('region').sum()], keys=['rebuilding', 'non-rebuilding'], names=['sectors affected'])
        self.df_loss_region = pd.DataFrame({(self.storage_path.parent.name,self.storage_path.name):self.df_loss_region}).T
        self.df_loss_region.to_json(self.storage_path/"fd_loss.json", indent=4, orient='split')

    def save_dfs(self):
        logger.info("Saving computed dataframe to results folder")
        self.prod_df.to_parquet(self.storage_path/"prod_df.parquet")
        self.prodmax_df.to_parquet(self.storage_path/"prodmax_df.parquet")
        self.overprod_df.to_parquet(self.storage_path/"overprod_df.parquet")
        self.fd_unmet_df.to_parquet(self.storage_path/"fd_unmet_df.parquet")
        self.c_demand_df.to_parquet(self.storage_path/"c_demand_df.parquet")
        self.r_demand_df.to_parquet(self.storage_path/"r_demand_df.parquet")
        self.df_loss.to_parquet(self.storage_path/"treated_df_loss.parquet")
        if self.df_stocks is not None:
            ddf = da.from_pandas(self.df_stocks, chunksize=10000000)
            ddf.to_parquet(self.storage_path/"treated_df_stocks.parquet", engine="pyarrow")
        if self.df_limiting is not None:
            #ddf_l = da.from_pandas(self.df_limiting, chunksize=10000000)
            #ddf_l = ddf_l.melt(ignore_index=False).rename(columns={'variable_0':'region','variable_1':'sector', 'variable_2':'stock of'})
            #ddf_l = ddf_l.reset_index()
            #ddf_l['step'] = ddf_l['step'].astype("uint16")
            #ddf_l['stock of'] = ddf_l['stock of'].astype("category")
            #ddf_l['region'] = ddf_l['region'].astype("category")
            #ddf_l['sector'] = ddf_l['sector'].astype("category")
            self.df_limiting.to_parquet(self.storage_path/"treated_df_limiting.parquet", engine="pyarrow")
        #self.df_limiting.to_feather(self.storage_path/"treated_df_limiting.feather")
