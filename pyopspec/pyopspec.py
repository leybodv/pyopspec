import argparse
import time
import importlib
import importlib.util
import types
import sys
from pathlib import Path

# import pyopspec.process_config as process_config
import pyopspec.config as config
from pyopspec.plotters.process_plotter import DataCollectorPlotter
from pyopspec.data_exporters.data_exporter import DataExporter
from pyopspec.steps.heating_step import HeatingStep
from pyopspec.steps.isothermal_step import IsothermalStep
from pyopspec.steps.cooling_step import CoolingStep
from pyopspec.steps.final_step import FinalStep
from pyopspec.steps.pressure_ramp_step import PressureRampStep
from .exceptions import *

def _import_config(path:Path) -> types.ModuleType:
    """
    """
    config_spec = importlib.util.spec_from_file_location('process_config', path)
    if config_spec is None:
        raise Exception(f'Cannot read config file at {path}')
    config_loader = config_spec.loader
    if config_loader is None:
        raise Exception(f'Cannot read config file at {path}')
    config_module = importlib.util.module_from_spec(config_spec)
    sys.modules['process_config'] = config_module
    config_loader.exec_module(config_module)
    process_config = importlib.import_module('process_config')
    return process_config

def play(args:argparse.Namespace):
    """
    """
    config.pressure_controller.connect()
    for gas in config.mfcs:
        config.mfcs[gas].connect()
    config.furnace.connect()
    config_path = Path(args.config)
    process_config = _import_config(config_path)
    plotter = DataCollectorPlotter(furnace_controller=config.furnace, mass_flow_controllers=config.mfcs, pressure_controller=config.pressure_controller)
    data_exporter = DataExporter(folder_path=process_config.export_folder_path, furnace_controller=config.furnace, mass_flow_controllers=config.mfcs, pressure_controller=config.pressure_controller)
    plotter.start()
    data_exporter.start()
    for step in process_config.steps:
        if isinstance(step, HeatingStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            config.furnace.set_ramp_rate(step.heating_rate)
            config.furnace.heat_up_to(step.target_temperature)
        elif isinstance(step, IsothermalStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            time.sleep(step.time * 60)
        elif isinstance(step, CoolingStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            config.furnace.set_ramp_rate(step.cooling_rate)
            config.furnace.cool_down_to(step.target_temperature)
        elif isinstance(step, PressureRampStep):
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            config.pressure_controller.ramp_pressure(pressure=step.pressure, ramp_rate=step.pressure_ramp_rate)
        elif isinstance(step, FinalStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            plotter.stop()
            data_exporter.stop()
            config.furnace.set_temperature(step.temperature)
        else:
            raise UnknownStepException(f'Unknown step: {step}')

def main():
    """
    """
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=play)
    parser.add_argument('--config', required=True, help='path to config file with the sequence of actions to perform by the program')
    args = parser.parse_args()
    args.func(args)
