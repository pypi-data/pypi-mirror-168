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
import json
import pathlib
import pymrio
import numpy as np
from nptyping import NDArray

from boario import logger
from boario.event import *
from pymrio.core.mriosystem import IOSystem

__all__ = ["ARIOBaseModel","INV_THRESHOLD","VALUE_ADDED_NAMES","VA_idx", "lexico_reindex"]

INV_THRESHOLD = 0 #20 #temporal_units

VALUE_ADDED_NAMES = ['VA', 'Value Added', 'value added',
                        'factor inputs', 'factor_inputs', 'Factors Inputs',
                        'Satellite Accounts', 'satellite accounts', 'satellite_accounts',
                     'satellite']

VA_idx = np.array(['Taxes less subsidies on products purchased: Total',
       'Other net taxes on production',
       "Compensation of employees; wages, salaries, & employers' social contributions: Low-skilled",
       "Compensation of employees; wages, salaries, & employers' social contributions: Medium-skilled",
       "Compensation of employees; wages, salaries, & employers' social contributions: High-skilled",
       'Operating surplus: Consumption of fixed capital',
       'Operating surplus: Rents on land',
       'Operating surplus: Royalties on resources',
       'Operating surplus: Remaining net operating surplus'], dtype=object)

def lexico_reindex(mrio: pymrio.IOSystem) -> pymrio.IOSystem:
    """Reindex IOSystem lexicographicaly

    Sort indexes and columns of the dataframe of a ``pymrio`` `IOSystem <https://pymrio.readthedocs.io/en/latest/intro.html>` by
    lexical order.

    Parameters
    ----------
    mrio : pymrio.IOSystem
        The IOSystem to sort

    Returns
    -------
    pymrio.IOSystem
        The sorted IOSystem


    """

    mrio.Z = mrio.Z.reindex(sorted(mrio.Z.index), axis=0)
    mrio.Z = mrio.Z.reindex(sorted(mrio.Z.columns), axis=1)
    mrio.Y = mrio.Y.reindex(sorted(mrio.Y.index), axis=0)
    mrio.Y = mrio.Y.reindex(sorted(mrio.Y.columns), axis=1)
    mrio.x = mrio.x.reindex(sorted(mrio.x.index), axis=0) #type: ignore
    mrio.A = mrio.A.reindex(sorted(mrio.A.index), axis=0)
    mrio.A = mrio.A.reindex(sorted(mrio.A.columns), axis=1)

    return mrio

class ARIOBaseModel(object):
    r"""The core of an ARIO3 model.  Handles the different arrays containing the mrio tables.

    A ARIOBaseModel wrap all the data and functions used in the core of the most basic version of the ARIO
    model (based on Hallegatte2013 and Guan2020).

    Attributes
    ----------

    results_storage : pathlib.Path
                      The path where the results of the simulation are stored.
    regions : numpy.ndarray of str
              An array of the regions of the model.
    n_regions : int
                The number :math:`m` of regions.
    sectors : numpy.ndarray of str
              An array of the sectors of the model.
    n_sectors : int
                The number :math:`n` of sectors.
    fd_cat : numpy.ndarray of str
             An array of the final demand categories of the model (``["Final demand"]`` if there is only one)
    n_fd_cat : int
               The numbers of final demand categories.
    monetary_unit : int
                    monetary unit prefix (i.e. if the tables unit is 10^6 € instead of 1 €, it should be set to 10^6).
    temporal_units_by_step : int
                     The number of temporal_units between each step. (Current version of the model was not tested with values other than `1`).
    year_to_temporal_unit_factor : int
                               Kinda deprecated, should be equal to `temporal_units_by_step`.
    rebuild_tau : int
                  Rebuilding characteristic time :math:`\tau_{\textrm{REBUILD}}` (see :ref:`boario-math`).
    overprod_max : float
                   Maximum factor of overproduction :math:`\alpha^{\textrm{max}}` (default should be 1.25).
    overprod_tau : float
                   Characteristic time of overproduction :math:`\tau_{\alpha}` in ``temporal_units_by_step`` (default should be 365 days).
    overprod_base : float
                    Base value of overproduction factor :math:`\alpha^{b}` (Default to 1.0).
    inv_duration : numpy.ndarray of int
                   Array :math:`\mathbf{s}` of size :math:`n` (sectors), setting for each input the initial number of ``temporal_units_by_step`` of stock for the input. (see :ref:`boario-math`).
    restoration_tau : numpy.ndarray of int
                      Array of size :math:`n` setting for each inputs its characteristic restoration time :math:`\tau_{\textrm{INV}}` in ``temporal_units_by_step``. (see :ref:`boario-math`).
    Z_0 : numpy.ndarray of float
          2-dim square matrix array :math:`\ioz` of size :math:`(n \times m, n \times m)` representing the intermediate (transaction) matrix (see :ref:`boario-math-init`).
    Z_C : numpy.ndarray of float
          2-dim matrix array :math:`\ioz^{\sectorsset}` of size :math:`(n, n \times m)` representing the intermediate (transaction) matrix aggregated by inputs (see :ref:`here <boario-math-z-agg>`).
    Z_distrib : numpy.ndarray of float
                :math:`\ioz` normalised by :math:`\ioz^{\sectorsset}`, i.e. representing for each input the share of the total ordered transiting from an industry to another (see :ref:`here <boario-math-z-agg>`).
    Y_0 : numpy.ndarray of float
          2-dim array :math:`\ioy` of size :math:`(n \times m, m \times \text{number of final demand categories})` representing the final demand matrix.
    X_0 : numpy.ndarray of float
          Array :math:`\iox(0)` of size :math:`n \times m` representing the initial gross production.
    gdp_df : pandas.DataFrame
             Dataframe of the total GDP of each region of the model
    VA_0 : numpy.ndarray of float
           Array :math:`\iov` of size :math:`n \times m` representing the total value added for each sectors.
    tech_mat : numpy.ndarray
               2-dim array :math:`\ioa` of size :math:`(n \times m, n \times m)` representing the technical coefficients matrix
    overprod : numpy.ndarray
               Array of size :math:`n \times m` representing the overproduction coefficients vector :math:`\mathbf{\alpha}(t)`.
    Raises
    ------
    RuntimeError
        A RuntimeError can occur when data is inconsistent (negative stocks for
        instance)
    ValueError
    NotImplementedError
    """

    def __init__(self,
                 pym_mrio: IOSystem,
                 mrio_params: dict,
                 simulation_params: dict,
                 results_storage: pathlib.Path
                 ) -> None:

        logger.debug("Initiating new ARIOBaseModel instance")
        super().__init__()

        ################ Parameters variables #######################
        logger.info("IO system metadata :\n{}".format(str(pym_mrio.meta)))
        logger.info("Simulation parameters:\n{}".format(json.dumps(simulation_params, indent=4)))
        pym_mrio = lexico_reindex(pym_mrio)
        self.mrio_params:dict = mrio_params
        self.main_inv_dur = mrio_params['main_inv_dur']

        results_storage = results_storage.absolute()
        self.results_storage:pathlib.Path = results_storage
        logger.info("Results storage is: {}".format(self.results_storage))
        self.regions = np.array(sorted(list(pym_mrio.get_regions()))) #type: ignore
        self.n_regions = len(pym_mrio.get_regions()) #type: ignore
        self.sectors = np.array(sorted(list(pym_mrio.get_sectors()))) #type: ignore
        self.n_sectors = len(pym_mrio.get_sectors()) #type: ignore
        try:
            self.fd_cat = np.array(sorted(list(pym_mrio.get_Y_categories()))) #type: ignore
            self.n_fd_cat = len(pym_mrio.get_Y_categories()) #type: ignore
        except KeyError:
            self.n_fd_cat = 1
            self.fd_cat = np.array(["Final demand"])
        except IndexError:
            self.n_fd_cat= 1
            self.fd_cat = np.array(["Final demand"])
        self.monetary_unit = mrio_params['monetary_unit']
        logger.info("Monetary unit from params is: %s", self.monetary_unit)
        logger.info("Monetary unit from loaded mrio is: %s", pym_mrio.unit.unit.unique()[0])
        #self.psi = simulation_params['psi_param']
        self.n_temporal_units_by_step = simulation_params['temporal_units_by_step']
        self.iotable_year_to_temporal_unit_factor = simulation_params['year_to_temporal_unit_factor'] # 365 for yearly IO tables
        if self.iotable_year_to_temporal_unit_factor != 365:
            logger.warning("iotable_to_daily_step_factor is not set to 365 (days). This should probably not be the case if the IO tables you use are on a yearly basis.")
        self.steply_factor =  self.n_temporal_units_by_step / self.iotable_year_to_temporal_unit_factor
        self.rebuild_tau = self.n_temporal_units_by_step / simulation_params['rebuild_tau']
        self.overprod_max = simulation_params['alpha_max']
        self.overprod_tau = self.n_temporal_units_by_step / simulation_params['alpha_tau']
        self.overprod_base = simulation_params['alpha_base']
        inv = mrio_params['inventories_dict']
        inventories = [ np.inf if inv[k]=='inf' else inv[k] for k in sorted(inv.keys())]
        self.inv_duration = np.array(inventories)  / self.n_temporal_units_by_step
        if (self.inv_duration <= 1).any() :
            logger.warning("At least one product has inventory duration lower than the numbers of temporal units in one step ({}), model will set it to 2 by default, but you should probably check this !".format(self.n_temporal_units_by_step))
            self.inv_duration[self.inv_duration <= 1] = 2
        #################################################################


        ######## INITIAL MRIO STATE (in step temporality) ###############
        self._matrix_id = np.eye(self.n_sectors)
        self._matrix_I_sum = np.tile(self._matrix_id, self.n_regions)
        self.Z_0 = pym_mrio.Z.to_numpy()
        self.Z_C = (self._matrix_I_sum @ self.Z_0)
        with np.errstate(divide='ignore',invalid='ignore'):
            self.Z_distrib = (np.divide(self.Z_0,(np.tile(self.Z_C, (self.n_regions, 1)))))
        self.Z_distrib = np.nan_to_num(self.Z_distrib)
        self.Z_0 = (pym_mrio.Z.to_numpy() * self.steply_factor)
        self.Y_0 = (pym_mrio.Y.to_numpy() * self.steply_factor)
        self.X_0 = (pym_mrio.x.T.to_numpy().flatten() * self.steply_factor) #type: ignore
        value_added = (pym_mrio.x.T - pym_mrio.Z.sum(axis=0))
        value_added = value_added.reindex(sorted(value_added.index), axis=0) #type: ignore
        value_added = value_added.reindex(sorted(value_added.columns), axis=1)
        value_added[value_added < 0] = 0.0
        self.gdp_df = value_added.groupby('region',axis=1).sum()
        self.VA_0 = (value_added.to_numpy().flatten())
        self.tech_mat = ((self._matrix_I_sum @ pym_mrio.A).to_numpy()) #type: ignore #to_numpy is not superfluous !
        kratio = mrio_params['capital_ratio_dict']
        kratio_ordered = [kratio[k] for k in sorted(kratio.keys())]
        self.kstock_ratio_to_VA = np.tile(np.array(kratio_ordered),self.n_regions)
        if value_added.ndim > 1:
            self.gdp_share_sector = (self.VA_0 / value_added.sum(axis=0).groupby('region').transform('sum').to_numpy())
        else:
            self.gdp_share_sector = (self.VA_0 / value_added.groupby('region').transform('sum').to_numpy())
        self.gdp_share_sector = self.gdp_share_sector.flatten()
        self.matrix_share_thresh = self.Z_C > np.tile(self.X_0, (self.n_sectors, 1)) * 0.00001 # [n_sectors, n_regions*n_sectors]
        #################################################################

        ####### SIMULATION VARIABLES ####################################
        self.overprod = np.full((self.n_regions * self.n_sectors), self.overprod_base, dtype=np.float64)
        with np.errstate(divide='ignore',invalid='ignore'):
            self.matrix_stock = ((np.tile(self.X_0, (self.n_sectors, 1)) * self.tech_mat) * self.inv_duration[:,np.newaxis])
        self.matrix_stock = np.nan_to_num(self.matrix_stock,nan=np.inf, posinf=np.inf)
        self.matrix_stock_0 = self.matrix_stock.copy()
        self.matrix_orders = self.Z_0.copy()
        self.production = self.X_0.copy()
        self.production_cap = self.X_0.copy()
        self.intmd_demand = self.Z_0.copy()
        self.final_demand = self.Y_0.copy()
        self.rebuilding_demand = None
        self.total_demand = np.zeros(shape = self.X_0.shape)
        self.rebuild_demand = np.zeros(shape = np.concatenate([self.Z_0,self.Y_0],axis=1).shape)
        # self.prod_max_toward_rebuilding = None
        self.kapital_lost = np.zeros(self.production.shape)
        self.order_type = simulation_params['order_type']
        #################################################################

        ################## SIMULATION TRACKING VARIABLES ################
        self.in_shortage = False
        self.had_shortage = False
        self.production_evolution = np.memmap(results_storage/"iotable_XVA_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.production_evolution.fill(np.nan)
        self.production_cap_evolution = np.memmap(results_storage/"iotable_X_max_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.production_cap_evolution.fill(np.nan)
        self.classic_demand_evolution = np.memmap(results_storage/"classic_demand_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.classic_demand_evolution.fill(np.nan)
        self.rebuild_demand_evolution = np.memmap(results_storage/"rebuild_demand_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.rebuild_demand_evolution.fill(np.nan)
        self.rebuild_stock_evolution = np.memmap(results_storage/"rebuild_demand_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.rebuild_stock_evolution.fill(np.nan)
        self.overproduction_evolution = np.memmap(results_storage/"overprodvector_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.overproduction_evolution.fill(np.nan)
        self.final_demand_unmet_evolution = np.memmap(results_storage/"final_demand_unmet_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.final_demand_unmet_evolution.fill(np.nan)
        self.rebuild_production_evolution = np.memmap(results_storage/"rebuild_prod_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors*self.n_regions))
        self.rebuild_production_evolution.fill(np.nan)
        if simulation_params['register_stocks']:
            self.stocks_evolution = np.memmap(results_storage/"stocks_record", dtype='float64', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors, self.n_sectors*self.n_regions))
            self.stocks_evolution.fill(np.nan)
        self.limiting_stocks_evolution = np.memmap(results_storage/"limiting_stocks_record", dtype='bool', mode="w+", shape=(simulation_params['n_temporal_units_to_sim'], self.n_sectors, self.n_sectors*self.n_regions))
        #############################################################################

        #### POST INIT ####
        self.write_index(results_storage/"indexes.json")

    def update_system_from_events(self, events: list[Event]) -> None:
        """Update MrioSystem variables according to given list of events

        Compute kapital loss for each industry affected as the sum of their total rebuilding demand (to each rebuilding sectors and for each events). This information is stored as a 1D array ``kapital_lost`` of size :math:`n \time m`.
        Also compute the total rebuilding demand.

        Parameters
        ----------
        events : 'list[Event]'
            List of events (as Event objects) to consider.


        """
        self.update_kapital_lost(events)
        self.calc_tot_rebuild_demand(events)

    def calc_rebuild_house_demand(self, events:list[Event]) -> np.ndarray :
        r"""Compute rebuild demand for final demand

        Compute and return rebuilding final demand for the given list of events
        by summing the final_demand_rebuild member of each event. Only events
        tagged as rebuildable are accounted for. The shape of the array
        returned is the same as the final demand member (``Y_0`` | :math:`\ioy`) of the calling
        MrioSystem.

        Parameters
        ----------
        events : 'list[Event]'
            A list of Event objects

        Returns
        -------
        np.ndarray
            An array of same shape as Y_0, containing the sum of all currently
            rebuildable final demand stock from all events in the given list.

        Notes
        -----

        Currently the model wasn't tested with such a rebuilding demand. Only intermediate demand is considered.
        """
        rebuildable_events = np.array([e.final_demand_rebuild for e in events if e.rebuildable])
        if rebuildable_events.size == 0:
            return np.zeros(shape = self.Y_0.shape)
        ret = np.add.reduce(rebuildable_events)
        return ret

    def calc_rebuild_firm_demand(self, events:'list[Event]') -> np.ndarray :
        r"""Compute rebuild demand for intermediate demand

        Compute and return rebuilding intermediate demand for the given list of events
        by summing the industry_rebuild member of each event. Only events
        tagged as rebuildable are accounted for. The shape of the array
        returned is the same as the intermediate demand member (``Z_0`` | :math:`\ioz`) of the calling
        MrioSystem.

        Parameters
        ----------
        events : 'list[Event]'
            A list of Event objects

        Returns
        -------
        np.ndarray
            An array of same shape as Z_0, containing the sum of all currently
            rebuildable intermediate demand stock from all events in the given list.
        """
        rebuildable_events = np.array([e.industry_rebuild for e in events if e.rebuildable])
        if rebuildable_events.size == 0:
            return np.zeros(shape = self.Z_0.shape)
        ret = np.add.reduce(rebuildable_events)
        return ret

    def calc_tot_rebuild_demand(self, events:'list[Event]') -> None:
        """Compute and update total rebuild demand.

        Compute and update total rebuilding demand for the given list of events. Only events
        tagged as rebuildable are accounted for.

        TODO: ADD MATH

        Parameters
        ----------
        events : 'list[Event]'
            A list of Event objects

        separate_rebuilding: 'bool'
            A boolean specifying if demand should be treated as a whole (true) or under the characteristic time/proportional scheme strategy.
        """
        ret =  np.concatenate([self.calc_rebuild_house_demand(events),self.calc_rebuild_firm_demand(events)],axis=1)
        #if not separate_rebuilding:
        #    ret *= self.rebuild_tau
        self.rebuild_demand = ret

    def calc_production_cap(self):
        r"""Compute and update production capacity.

        Compute and update production capacity from possible kapital damage and overproduction.

        .. math::

            x^{Cap}_{f}(t) = \alpha_{f}(t) (1 - \Delta_{f}(t)) x_{f}(t)

        Raises
        ------
        ValueError
            Raised if any industry has negative production (probably from kapital loss too high)
        """
        self.production_cap = self.X_0.copy()
        productivity_loss = np.zeros(shape=self.kapital_lost.shape)
        k_stock = (self.VA_0 * self.kstock_ratio_to_VA)
        np.divide(self.kapital_lost, k_stock, out=productivity_loss, where=k_stock!=0)
        if (productivity_loss > 0.).any():
            if (productivity_loss > 1.).any():
                np.minimum(productivity_loss, 1.0, out=productivity_loss)
                logger.warning("Productivity loss factor was found greater than 1.0 on at least on industry (meaning more kapital damage than kapital stock)")
            self.production_cap = self.production_cap * (1 - productivity_loss)
        if (self.overprod > 1.0).any():
            self.production_cap = self.production_cap * self.overprod
        if (self.production_cap < 0).any() :
            raise ValueError("Production capacity was found negative for at least on industry")

    def calc_prod_reqby_demand(self, events:'list[Event]', separate_rebuilding:bool=False ) -> None :
        """Computes and updates total demand

        Update total rebuild demand (and apply rebuilding characteristic time
        if ``separate_rebuilding`` is False, then sum/reduce rebuilding, orders
        and final demand together and accordingly update vector of total
        demand.

        Parameters
        ----------
        events : 'list[Event]'
            List of Event to consider for rebuilding demand.
        separate_rebuilding : bool
            A boolean specifying if rebuilding demand should be treated as a whole (true) or under the characteristic time/proportional scheme strategy.
        Returns
        -------
        None

        """
        self.calc_tot_rebuild_demand(events)
        if not separate_rebuilding:
            dmg_demand_restorable = self.rebuild_demand * self.rebuild_tau
        else:
            dmg_demand_restorable = None # rebuild demand is treated elsewhere in this case
        prod_reqby_demand = self.matrix_orders.sum(axis=1) + self.final_demand.sum(axis=1)
        if dmg_demand_restorable is not None:
            prod_reqby_demand += dmg_demand_restorable.sum(axis=1)
        assert not (prod_reqby_demand < 0).any()
        self.total_demand = prod_reqby_demand

    def calc_production(self, current_temporal_unit:int) -> np.NDArray:
        r"""Compute and update actual production

        1. Compute ``production_opt`` and ``inventory_constraints`` as :

        .. math::
           :nowrap:

                \begin{alignat*}{4}
                      \iox^{\textrm{Opt}}(t) &= (x^{\textrm{Opt}}_{f}(t))_{f \in \firmsset} &&= \left ( \min \left ( d^{\textrm{Tot}}_{f}(t), x^{\textrm{Cap}}_{f}(t) \right ) \right )_{f \in \firmsset} && \text{Optimal production}\\
                      \mathbf{\ioinv}^{\textrm{Cons}}(t) &= (\omega^{\textrm{Cons},f}_p(t))_{\substack{p \in \sectorsset\\f \in \firmsset}} &&=
                    \begin{bmatrix}
                        \tau^{1}_1 & \hdots & \tau^{p}_1 \\
                        \vdots & \ddots & \vdots\\
                        \tau^1_n & \hdots & \tau^{p}_n
                    \end{bmatrix}
                    \odot \begin{bmatrix} \iox^{\textrm{Opt}}(t)\\ \vdots\\ \iox^{\textrm{Opt}}(t) \end{bmatrix} \odot \ioa^{\sectorsset} && \text{Inventory constraints} \\
                    &&&= \begin{bmatrix}
                        \tau^{1}_1 x^{\textrm{Opt}}_{1}(t) a_{11} & \hdots & \tau^{p}_1 x^{\textrm{Opt}}_{p}(t) a_{1p}\\
                        \vdots & \ddots & \vdots\\
                        \tau^1_n x^{\textrm{Opt}}_{1}(t) a_{n1} & \hdots & \tau^{p}_n x^{\textrm{Opt}}_{p}(t) a_{np}
                    \end{bmatrix} && \\
                \end{alignat*}

        2. If stocks do not meet ``inventory_constraints`` for any inputs, then decrease production accordingly :

        .. math::
           :nowrap:

                \begin{alignat*}{4}
                    \iox^{a}(t) &= (x^{a}_{f}(t))_{f \in \firmsset} &&= \left \{ \begin{aligned}
                                                           & x^{\textrm{Opt}}_{f}(t) & \text{if $\omega_{p}^f(t) \geq \omega^{\textrm{Cons},f}_p(t)$}\\
                                                           & x^{\textrm{Opt}}_{f}(t) \cdot \min_{p \in \sectorsset} \left ( \frac{\omega^s_{p}(t)}{\omega^{\textrm{Cons,f}}_p(t)} \right ) & \text{if $\omega_{p}^f(t) < \omega^{\textrm{Cons},f}_p(t)$}
                                                           \end{aligned} \right. \quad &&
                \end{alignat*}

        Also warns in log if such shortages happen.


        Parameters
        ----------
        current_temporal_unit : int
            current step number

        """
        #1.
        production_opt = np.fmin(self.total_demand, self.production_cap)
        inventory_constraints = self.calc_inventory_constraints(production_opt)
        #2.
        if (stock_constraint := (self.matrix_stock < inventory_constraints) * self.matrix_share_thresh).any():
            if not self.in_shortage:
                logger.info('At least one industry entered shortage regime. (step:{})'.format(current_temporal_unit))
            self.in_shortage = True
            self.had_shortage = True
            production_ratio_stock = np.ones(shape=self.matrix_stock.shape)
            np.divide(self.matrix_stock, inventory_constraints, out=production_ratio_stock, where=(self.matrix_share_thresh * (inventory_constraints!=0)))
            production_ratio_stock[production_ratio_stock > 1] = 1
            if (production_ratio_stock < 1).any():
                production_max = np.tile(production_opt, (self.n_sectors, 1)) * production_ratio_stock
                assert not (np.min(production_max,axis=0) < 0).any()
                self.production = np.min(production_max, axis=0)
            else:
                assert not (production_opt < 0).any()
                self.production = production_opt
        else:
            if self.in_shortage:
                self.in_shortage = False
                logger.info('All industries exited shortage regime. (step:{})'.format(current_temporal_unit))
            assert not (production_opt < 0).any()
            self.production = production_opt
        return stock_constraint

    def calc_inventory_constraints(self, production:np.ndarray) -> np.ndarray :
        """Compute inventory constraint (no psi parameter)

        See :meth:`calc_production`.

        Parameters
        ----------
        production : np.ndarray
            production vector

        Returns
        -------
        np.ndarray
            A boolean NDArray `stock_constraint` of the same shape as ``matrix_stock`` (ie `(n_sectors,n_regions*n_sectors)`), with ``True`` for any input not meeting the inventory constraints.

        """

        inventory_constraints = (np.tile(production, (self.n_sectors, 1)) * self.tech_mat)
        tmp = np.tile(np.nan_to_num(self.inv_duration, posinf=0.)[:,np.newaxis],(1,self.n_regions*self.n_sectors))
        return inventory_constraints * tmp

    def distribute_production(self,
                              current_temporal_unit: int, events: 'list[Event]',
                              scheme:str='proportional', separate_rebuilding:bool=False) -> list[Event]:
        r"""Production distribution module

    #. Computes rebuilding demand for each rebuildable events (applying the `rebuild_tau` characteristic time)

    #. Creates/Computes total demand matrix (Intermediate + Final + Rebuild)

    #. Assesses if total demand is greater than realized production, hence requiring rationning

    #. Distributes production proportionally to demand such that :

        .. math::
           :nowrap:

               \begin{alignat*}{4}
                   &\ioorders^{\textrm{Received}}(t) &&= \left (\frac{o_{ff'}(t)}{d^{\textrm{Tot}}_f(t)} \cdot x^a_f(t) \right )_{f,f'\in \firmsset}\\
                   &\ioy^{\textrm{Received}}(t) &&= \left ( \frac{y_{f,c}}{d^{\textrm{Tot}}_f(t)}\cdot x^a_f(t) \right )_{f\in \firmsset, c \in \catfdset}\\
                   &\Damage^{\textrm{Repaired}}(t) &&= \left ( \frac{\gamma_{f,c}}{d^{\textrm{Tot}}_f(t)} \cdot x^a_f(t) \right )_{f\in \firmsset, c \in \catfdset}\\
               \end{alignat*}

        Where :

        - :math:`\ioorders^{\textrm{Received}}(t)` is the received orders matrix,

        - :math:`\ioy^{\textrm{Received}}(t)` is the final demand received matrix,

        - :math:`\Damage^{\textrm{Repared}}(t)` is the rebuilding/repair achieved matrix,

        - :math:`d^{\textrm{Tot}}_f(t)` is the total demand to industry :math:`f`,

        - :math:`x^a_f(t)` is :math:`f`'s realized production,

        - :math:`o_{ff'}(t)` is the quantity of product ordered by industry :math:`f'` to industry :math:`f`,

        - :math:`y_{fc}(t)` is the quantity of product ordered by household :math:`c` to industry :math:`f`,

        - :math:`\gamma_{fc}(t)` is the repaired/rebuilding demand ordered to :math:`f`.

    #. Updates stocks matrix. (Only if `np.allclose(stock_add, stock_use).all()` is false)

        .. math::
           :nowrap:

               \begin{alignat*}{4}
                   &\ioinv(t+1) &&= \ioinv(t) + \left ( \mathbf{I}_{\textrm{sum}} \cdot \ioorders^{\textrm{Received}}(t) \right ) - \left ( \colvec{\iox^{\textrm{a}}(t)}{\iox^{\textrm{a}}(t)} \odot \ioa^{\sectorsset} \right )\\
               \end{alignat*}

        Where :

        - :math:`\ioinv` is the inventory matrix,
        - :math:`\mathbf{I}_{\textrm{sum}}` is a row summation matrix,
        - :math:`\ioa^{\sectorsset}` is the (input not specific to region) technical coefficients matrix.

    #. Computes final demand not met due to rationing and write it.

    #. Updates rebuilding demand for each event (by substracting distributed production)

    Parameters
    ----------
    current_temporal_unit : int
        Current temporal unit (day|week|... depending on parameters) (required to write the final demand not met)
    events : 'list[Event]'
        Simulation events list
    scheme : str
        Placeholder for future distribution scheme
    separate_rebuilding : bool
        Currently unused.

    Returns
    -------
    list[Event]
        The list of events to remove from current events (as they are totally rebuilt)

    Raises
    ------
    RuntimeError
        If negative values are found in places there's should not be any
    ValueError
        If an attempt to run an unimplemented distribution scheme is tried

"""
        if scheme != 'proportional':
            raise ValueError("Scheme %s not implemented"% scheme)

        ## 1. Calc demand from rebuilding requirements (with characteristic time rebuild_tau)
        n_events = len([e for e in events])
        n_events_reb = len([e for e in events if e.rebuildable])
        tot_rebuilding_demand_summed = np.zeros(self.X_0.shape)
        tot_rebuilding_demand = np.zeros(shape=(self.n_sectors*self.n_regions, (self.n_sectors*self.n_regions+self.n_regions*self.n_fd_cat),n_events))
        if n_events_reb >0:
           for e_id, e in enumerate(events):
               if e.rebuildable:
                   rebuilding_demand = np.concatenate([e.industry_rebuild,e.final_demand_rebuild],axis=1)
                   rebuilding_demand_summed = np.add.reduce(rebuilding_demand,axis=1)
                   tot_rebuilding_demand[:,:,e_id] = rebuilding_demand * self.rebuild_tau
                   tot_rebuilding_demand_summed += rebuilding_demand_summed * self.rebuild_tau

        ## 2. Concat to have total demand matrix (Intermediate + Final + Rebuild)
        tot_demand = np.concatenate([self.matrix_orders, self.final_demand, np.expand_dims(tot_rebuilding_demand_summed,1)], axis=1)
        ## 3. Does production meet total demand
        rationning_required = (self.production - tot_demand.sum(axis=1))<(-1/self.monetary_unit)
        rationning_mask = np.tile(rationning_required[:,np.newaxis],(1,tot_demand.shape[1]))
        demand_share = np.full(tot_demand.shape,0.0)
        tot_dem_summed = np.expand_dims(np.sum(tot_demand, axis=1, where=rationning_mask),1)
        # Get demand share
        np.divide(tot_demand, tot_dem_summed, where=(tot_dem_summed!=0), out=demand_share)
        distributed_production = tot_demand.copy()
        # 4. distribute production proportionally to demand
        np.multiply(demand_share, np.expand_dims(self.production,1), out=distributed_production, where=rationning_mask)
        intmd_distribution = distributed_production[:,:self.n_sectors * self.n_regions]
        # Stock use is simply production times technical coefs
        stock_use = np.tile(self.production, (self.n_sectors,1)) * self.tech_mat
        if (stock_use < 0).any() :
            raise RuntimeError("Stock use contains negative values, this should not happen")
        # 5. Restock is the production from each supplier, summed.
        stock_add = self._matrix_I_sum @ intmd_distribution
        if (stock_add < 0).any():
            raise RuntimeError("stock_add (restocking) contains negative values, this should not happen")
        if not np.allclose(stock_add, stock_use):
            self.matrix_stock = self.matrix_stock - stock_use + stock_add
            if (self.matrix_stock < 0).any():
                self.matrix_stock.dump(self.results_storage/"matrix_stock_dump.pkl")
                logger.error("Negative values in the stocks, matrix has been dumped in the results dir : \n {}".format(self.results_storage/"matrix_stock_dump.pkl"))
                raise RuntimeError("stock_add (restocking) contains negative values, this should not happen")

        # 6. Compute final demand not met due to rationing
        final_demand_not_met = self.final_demand - distributed_production[:,self.n_sectors*self.n_regions:(self.n_sectors*self.n_regions + self.n_fd_cat*self.n_regions)]
        final_demand_not_met = final_demand_not_met.sum(axis=1)
        # avoid -0.0 (just in case)
        final_demand_not_met[final_demand_not_met==0.] = 0.
        self.write_final_demand_unmet(current_temporal_unit, final_demand_not_met)

        # 7. Compute production delivered to rebuilding
        rebuild_prod = distributed_production[:,(self.n_sectors*self.n_regions + self.n_fd_cat*self.n_regions):].copy().flatten()
        self.write_rebuild_prod(current_temporal_unit,rebuild_prod) #type: ignore
        tot_rebuilding_demand_shares = np.zeros(shape=tot_rebuilding_demand.shape)
        tot_rebuilding_demand_broad = np.broadcast_to(tot_rebuilding_demand_summed[:,np.newaxis,np.newaxis],tot_rebuilding_demand.shape)
        np.divide(tot_rebuilding_demand,tot_rebuilding_demand_broad, where=(tot_rebuilding_demand_broad!=0), out=tot_rebuilding_demand_shares)
        rebuild_prod_broad = np.broadcast_to(rebuild_prod[:,np.newaxis,np.newaxis],tot_rebuilding_demand.shape)
        rebuild_prod_distributed = np.zeros(shape=tot_rebuilding_demand.shape)
        np.multiply(tot_rebuilding_demand_shares,rebuild_prod_broad,out=rebuild_prod_distributed)
        # update rebuilding demand
        events_to_remove = []
        for e_id, e in enumerate(events):
            e.industry_rebuild -= rebuild_prod_distributed[:,:self.n_sectors*self.n_regions,e_id]
            e.final_demand_rebuild -= rebuild_prod_distributed[:,self.n_sectors*self.n_regions:,e_id]
            if (e.industry_rebuild < (10/self.monetary_unit)).all() and (e.final_demand_rebuild < (10/self.monetary_unit)).all():
                events_to_remove.append(e)
        return events_to_remove

    def calc_orders(self, events:list[Event]) -> None:
        """TODO describe function

        :param stocks_constraints:
        :type stocks_constraints:
        :returns:

        """
        self.calc_prod_reqby_demand(events)
        production_opt = np.fmin(self.total_demand, self.production_cap)
        matrix_stock_goal = np.tile(production_opt, (self.n_sectors, 1)) * self.tech_mat
        # Check this !
        matrix_stock_gap = matrix_stock_goal * 0
        with np.errstate(invalid='ignore'):
            matrix_stock_goal *= self.inv_duration[:,np.newaxis]
        if np.allclose(self.matrix_stock, matrix_stock_goal):
            #debug_logger.info("Stock replenished ?")
            pass
        else:
            matrix_stock_gap[np.isfinite(matrix_stock_goal)] = (matrix_stock_goal[np.isfinite(matrix_stock_goal)] - self.matrix_stock[np.isfinite(self.matrix_stock)])
        assert (not np.isnan(matrix_stock_gap).any()), "NaN in matrix stock gap"
        matrix_stock_gap[matrix_stock_gap < 0] = 0
        # matrix_stock_gap = np.expand_dims(self.restoration_tau, axis=1) * matrix_stock_gap
        matrix_stock_gap += (np.tile(self.production, (self.n_sectors, 1)) * self.tech_mat)
        if self.order_type == "alt":
            prod_ratio = np.divide(self.production,self.X_0, where=self.X_0!=0)
            Z_prod = self.Z_0 * prod_ratio[:, np.newaxis]
            Z_Cprod = np.tile(self._matrix_I_sum @ Z_prod,(self.n_regions,1))
            out=np.zeros(shape=Z_prod.shape)
            np.divide(Z_prod,Z_Cprod,out=out, where=Z_Cprod!=0)
            tmp = (np.tile(matrix_stock_gap, (self.n_regions, 1)) * out)
        else:
            tmp = (np.tile(matrix_stock_gap, (self.n_regions, 1)) * self.Z_distrib)
        assert not (tmp < 0).any()
        self.matrix_orders = tmp

    def update_kapital_lost(self, events:list[Event]) -> None:
        self.__update_kapital_lost(events)

    def __update_kapital_lost(self, events:list[Event]
                              ) -> None:
        tot_industry_rebuild_demand = np.add.reduce(np.array([e.industry_rebuild for e in events]))

        self.kapital_lost = tot_industry_rebuild_demand.sum(axis=0)

    def calc_overproduction(self) -> None:
        scarcity = np.full(self.production.shape, 0.0)
        scarcity[self.total_demand!=0] = (self.total_demand[self.total_demand!=0] - self.production[self.total_demand!=0]) / self.total_demand[self.total_demand!=0]
        scarcity[np.isnan(scarcity)] = 0
        overprod_chg = (((self.overprod_max - self.overprod) * (scarcity) * self.overprod_tau) + ((self.overprod_base - self.overprod) * (scarcity == 0) * self.overprod_tau)).flatten()
        self.overprod += overprod_chg
        self.overprod[self.overprod < 1.] = 1.

    def check_stock_increasing(self, current_temporal_unit:int):
        tmp = np.full(self.matrix_stock.shape,0.0)
        mask = np.isfinite(self.matrix_stock_0)
        np.subtract(self.matrix_stock,self.matrix_stock_0, out=tmp, where=mask)
        check_1 = tmp > 0.0
        tmp = np.full(self.matrix_stock.shape,0.0)
        np.subtract(self.stocks_evolution[current_temporal_unit], self.stocks_evolution[current_temporal_unit-1], out=tmp, where=mask)
        check_2 = (tmp >= 0.0)
        return (check_1 & check_2).all()

    def check_production_eq_strict(self):
        return ((np.isclose(self.production, self.X_0)) | np.greater(self.production, self.X_0)).all()

    def check_production_eq_soft(self, current_temporal_unit:int, period:int = 10) -> bool:
        return self.check_monotony(self.production_evolution, current_temporal_unit, period)

    def check_stocks_monotony(self, current_temporal_unit:int, period:int = 10) -> bool:
        return self.check_monotony(self.stocks_evolution, current_temporal_unit, period)

    def check_initial_equilibrium(self)-> bool:
        return (np.allclose(self.production, self.X_0) and np.allclose(self.matrix_stock, self.matrix_stock_0))

    def check_equilibrium_soft(self, current_temporal_unit:int):
        return (self.check_stock_increasing(current_temporal_unit) and self.check_production_eq_strict)

    def check_equilibrium_monotony(self, current_temporal_unit:int, period:int=10) -> bool:
        return self.check_production_eq_soft(current_temporal_unit, period) and self.check_stocks_monotony(current_temporal_unit, period)

    def check_monotony(self, x, current_temporal_unit:int, period:int = 10) -> bool:
        return np.allclose(x[current_temporal_unit], x[current_temporal_unit-period], atol=0.0001)

    def check_crash(self, prod_threshold : float=0.80) -> int:
        """Check for economic crash

        This method look at the production vector and returns the number of
        industries which production is less than a certain share (default 20%) of the starting
        production.

        Parameters
        ----------
        prod_threshold : float, default: 0.8
            An industry is counted as 'crashed' if its current production is less than its starting production times (1 - `prod_threshold`).


        """
        tmp = np.full(self.production.shape, 0.0)
        checker = np.full(self.production.shape, 0.0)
        mask = self.X_0 != 0
        np.subtract(self.X_0, self.production, out=tmp, where=mask)
        np.divide(tmp, self.X_0, out=checker, where=mask)
        return np.where(checker >= prod_threshold)[0].size

    def reset_module(self,
                 simulation_params: dict,
                 ) -> None:
        # Reset OUTPUTS
        self.reset_record_files(simulation_params['n_temporal_units_to_sim'], simulation_params['register_stocks'])
        # Reset variable attributes
        self.kapital_lost = np.zeros(self.production.shape)
        self.overprod = np.full((self.n_regions * self.n_sectors), self.overprod_base, dtype=np.float64)
        with np.errstate(divide='ignore',invalid='ignore'):
            self.matrix_stock = ((np.tile(self.X_0, (self.n_sectors, 1)) * self.tech_mat) * self.inv_duration[:,np.newaxis])
        self.matrix_stock = np.nan_to_num(self.matrix_stock,nan=np.inf, posinf=np.inf)
        self.matrix_stock_0 = self.matrix_stock.copy()
        self.matrix_orders = self.Z_0.copy()
        self.production = self.X_0.copy()
        self.production_cap = self.X_0.copy()
        self.intmd_demand = self.Z_0.copy()
        self.final_demand = self.Y_0.copy()
        self.rebuilding_demand = None
        self.prod_max_toward_rebuilding = None

    def update_params(self, new_params:dict) -> None:
        """Update the parameters of the model.

        Replace each parameters with given new ones.

        .. warning::
            Be aware this method calls :meth:`~boario.model_base.reset_record_files`, which resets the memmap files located in the results directory !

        Parameters
        ----------
        new_params : dict
            Dictionary of new parameters to use.

        """
        self.n_temporal_units_by_step = new_params['temporal_units_by_step']
        self.iotable_year_to_temporal_unit_factor = new_params['year_to_temporal_unit_factor']
        self.rebuild_tau = new_params['rebuild_tau']
        self.overprod_max = new_params['alpha_max']
        self.overprod_tau = new_params['alpha_tau']
        self.overprod_base = new_params['alpha_base']
        if self.results_storage != pathlib.Path(new_params['output_dir']+"/"+new_params['results_storage']):
            self.results_storage = pathlib.Path(new_params['output_dir']+"/"+new_params['results_storage'])
        self.reset_record_files(new_params['n_temporal_units_to_sim'], new_params['register_stocks'])

    def reset_record_files(self, n_temporal_units:int, reg_stocks: bool) -> None:
        """Reset results memmaps

        This method creates/resets the :class:`memmaps <numpy.memmap>` arrays used to track
        production, demand, overproduction, etc.

        Parameters
        ----------
        n_steps : int
            number of steps of the simulation (memmaps size are predefined)
        reg_stocks : bool
            If true, create/reset the stock memmap (which can be huge)

        """
        self.production_evolution = np.memmap(self.results_storage/"iotable_XVA_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.production_cap_evolution = np.memmap(self.results_storage/"iotable_X_max_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.classic_demand_evolution = np.memmap(self.results_storage/"classic_demand_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.rebuild_demand_evolution = np.memmap(self.results_storage/"rebuild_demand_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.overproduction_evolution = np.memmap(self.results_storage/"overprodvector_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.final_demand_unmet_evolution = np.memmap(self.results_storage/"final_demand_unmet_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        self.rebuild_production_evolution = np.memmap(self.results_storage/"rebuild_prod_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors*self.n_regions))
        if reg_stocks:
            self.stocks_evolution = np.memmap(self.results_storage/"stocks_record", dtype='float64', mode="w+", shape=(n_temporal_units, self.n_sectors, self.n_sectors*self.n_regions))
        self.limiting_stocks_evolution = np.memmap(self.results_storage/"limiting_stocks_record", dtype='bool', mode="w+", shape=(n_temporal_units, self.n_sectors, self.n_sectors*self.n_regions))


    def write_production(self, current_temporal_unit:int) -> None:
        self.production_evolution[current_temporal_unit] = self.production

    def write_production_max(self, current_temporal_unit:int) -> None:
        self.production_cap_evolution[current_temporal_unit] = self.production_cap

    def write_classic_demand(self, current_temporal_unit:int) -> None:
         self.classic_demand_evolution[current_temporal_unit] = self.matrix_orders.sum(axis=1) + self.final_demand.sum(axis=1)

    def write_rebuild_demand(self, current_temporal_unit:int) -> None:
        to_write = np.full(self.n_regions*self.n_sectors,0.0)
        if (r_dem := self.rebuild_demand) is not None:
            self.rebuild_demand_evolution[current_temporal_unit] = r_dem.sum(axis=1)
        else:
            self.rebuild_demand_evolution[current_temporal_unit] = to_write

    def write_rebuild_prod(self, current_temporal_unit:int, rebuild_prod_agg:np.ndarray) -> None:
        self.rebuild_production_evolution[current_temporal_unit] = rebuild_prod_agg

    def write_overproduction(self, current_temporal_unit:int) -> None:
        self.overproduction_evolution[current_temporal_unit] = self.overprod

    def write_final_demand_unmet(self, current_temporal_unit:int, final_demand_unmet:np.ndarray) -> None:
        self.final_demand_unmet_evolution[current_temporal_unit] = final_demand_unmet

    def write_stocks(self, current_temporal_unit:int) -> None:
        self.stocks_evolution[current_temporal_unit] = self.matrix_stock

    def write_limiting_stocks(self, current_temporal_unit:int,
                              limiting_stock:NDArray) -> None:
        self.limiting_stocks_evolution[current_temporal_unit] = limiting_stock

    def write_index(self, index_file:Union[str,pathlib.Path]) -> None:
        """Write the indexes of the different dataframes of the model in a json file.

        In order to easily rebuild the dataframes from the 'raw' data, this
        method create a JSON file with all columns and indexes names, namely :

        * regions names
        * sectors names
        * final demand categories
        * number of regions, sectors and industries (regions * sectors)

        Parameters
        ----------
        index_file : pathlib.Path
            Path to the file to save the indexes.
        """

        indexes= {
            "regions":list(self.regions),
            "sectors":list(self.sectors),
            "fd_cat":list(self.fd_cat),
            "n_sectors":self.n_sectors,
            "n_regions":self.n_regions,
            "n_industries":self.n_sectors*self.n_regions
        }
        if isinstance(index_file,str):
            index_file=pathlib.Path(index_file)
        with index_file.open('w') as f:
            json.dump(indexes,f)

    def change_inv_duration(self, new_dur:int, old_dur:int=None) -> None:
        if old_dur is None:
            old_dur = self.main_inv_dur
        old_dur = float(old_dur) / self.n_temporal_units_by_step
        new_dur = float(new_dur) / self.n_temporal_units_by_step
        logger.info("Changing (main) inventories duration from {} steps to {} steps (there are {} temporal units by step so duration is {})".format(old_dur, new_dur, self.n_temporal_units_by_step, new_dur*self.n_temporal_units_by_step))
        self.inv_duration = np.where(self.inv_duration==old_dur, new_dur, self.inv_duration)
