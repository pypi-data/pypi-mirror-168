import numpy as np

from datetime import datetime
from benedict.dicts import benedict as Benedict

from mosartwmpy.config.parameters import Parameters
from mosartwmpy.state.state import State
from mosartwmpy.grid.grid import Grid
from mosartwmpy.reservoirs.istarf import istarf_release


def reservoir_release(state: State, grid: Grid, config: Benedict, parameters: Parameters, current_time: datetime):
    # compute release from reservoirs

    # if ISTARF enabled, use new module; else use old module
    if config.get('water_management.reservoirs.enable_istarf'):
        istarf_release(state, grid, config, parameters, current_time)

    else:
        month = current_time.month
        # if it's the start of the operational year for the reservoir, set it's start of op year storage to the current storage
        state.reservoir_storage_operation_year_start = np.where(
            state.reservoir_month_start_operations == month,
            state.reservoir_storage,
            state.reservoir_storage_operation_year_start
        )
        regulation_release(state, grid, config, parameters, current_time)
        storage_targets(state, grid, config, parameters, current_time)


def regulation_release(state, grid, config, parameters, current_time):
    # compute the expected monthly release based on Biemans (2011)
    
    # initialize to the average flow
    state.reservoir_release = grid.reservoir_streamflow_schedule.mean(dim='month').values
    
    # TODO what is k
    k = state.reservoir_storage_operation_year_start / (
            parameters.reservoir_regulation_release_parameter * grid.reservoir_storage_capacity)
    
    # TODO what is factor
    factor = np.where(
        grid.reservoir_runoff_capacity > parameters.reservoir_runoff_capacity_parameter,
        (2.0 / grid.reservoir_runoff_capacity) ** 2.0,
        0
    )
    
    # release is some combination of prerelease, average flow in the time period, and total average flow
    state.reservoir_release = np.where(
        np.logical_or(grid.reservoir_use_electricity, grid.reservoir_use_irrigation),
        np.where(
            grid.reservoir_runoff_capacity <= 2.0,
            k * grid.reservoir_prerelease_schedule.sel({'month': current_time.month}).values,
            k * factor * grid.reservoir_prerelease_schedule.sel({
                'month': current_time.month}).values + (1 - factor) * grid.reservoir_streamflow_schedule.sel({
                    'month': current_time.month}).values
        ),
        np.where(
            grid.reservoir_runoff_capacity <= 2.0,
            k * grid.reservoir_streamflow_schedule.mean(dim='month').values,
            k * factor * grid.reservoir_streamflow_schedule.mean(
                dim='month').values + (1 - factor) * grid.reservoir_streamflow_schedule.sel({
                    'month': current_time.month}).values
        )
    )


def storage_targets(state: State, grid: Grid, config: Benedict, parameters: Parameters, current_time: datetime) -> None:
    """Define the necessary drop in storage based on the reservoir storage targets at the start of the month.

    Args:
        state (State): the model state
        grid (Grid): the model grid
        config (Config): the model configuration
        parameters (Parameters): the model parameters
        current_time (datetime): the current simulation time
    """

    # TODO the logic here is really hard to follow... can it be simplified or made more readable?

    # if flood control active and has a flood control start
    flood_control_condition = (grid.reservoir_use_flood_control > 0) & (state.reservoir_month_flood_control_start > 0)
    # modify release in order to maintain a certain storage level
    month_condition = state.reservoir_month_flood_control_start <= state.reservoir_month_flood_control_end
    total_condition = flood_control_condition & (
        (month_condition &
        (current_time.month >= state.reservoir_month_flood_control_start) &
        (current_time.month < state.reservoir_month_flood_control_end)) |
        (np.logical_not(month_condition) &
        (current_time.month >= state.reservoir_month_flood_control_start) |
        (current_time.month < state.reservoir_month_flood_control_end))
    )
    drop = 0 * state.reservoir_month_flood_control_start
    n_month = 0 * drop
    for m in np.arange(1, 13):
        m_and_condition = (m >= state.reservoir_month_flood_control_start) & (m < state.reservoir_month_flood_control_end)
        m_or_condition = (m >= state.reservoir_month_flood_control_start) | (m < state.reservoir_month_flood_control_end)
        drop = np.where(
            (month_condition & m_and_condition) | (np.logical_not(month_condition) & m_or_condition),
            np.where(
                grid.reservoir_streamflow_schedule.sel({'month': m}).values >= grid.reservoir_streamflow_schedule.mean(dim='month').values,
                drop + 0,
                drop + np.abs(grid.reservoir_streamflow_schedule.mean(dim='month').values - grid.reservoir_streamflow_schedule.sel({'month': m}).values)
            ),
            drop
        )
        n_month = np.where(
            (month_condition & m_and_condition) | (np.logical_not(month_condition) & m_or_condition),
            n_month + 1,
            n_month
        )
    state.reservoir_release = np.where(
        total_condition & (n_month > 0),
        state.reservoir_release + drop / n_month,
        state.reservoir_release
    )
    # now need to make sure it will fill up but issue with spilling in certain hydro-climate conditions
    month_condition = state.reservoir_month_flood_control_end <= state.reservoir_month_start_operations
    first_condition = flood_control_condition & month_condition & (
        (current_time.month >= state.reservoir_month_flood_control_end) &
        (current_time.month < state.reservoir_month_start_operations)
    )
    second_condition = flood_control_condition & np.logical_not(month_condition) & (
        (current_time.month >= state.reservoir_month_flood_control_end) |
        (current_time.month < state.reservoir_month_start_operations)
    )
    state.reservoir_release = np.where(
        (state.reservoir_release > grid.reservoir_streamflow_schedule.mean(dim='month').values) & (first_condition | second_condition),
        grid.reservoir_streamflow_schedule.mean(dim='month').values,
        state.reservoir_release
    )
