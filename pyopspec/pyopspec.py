import argparse
import time

import pyopspec.process_config as process_config
import pyopspec.config as config
from pyopspec.plotters.process_plotter import DataCollectorPlotter

def play(args:argparse.Namespace):
    """
    """
    config.pressure_controller.connect()
    for gas in config.mfcs:
        config.mfcs[gas].connect()
    config.furnace.connect()
    plotter = DataCollectorPlotter()
    plotter.start()
    for step in process_config.steps:
        if isinstance(step, HeatingStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            config.furnace.set_heating_rate(step.heating_rate)
            config.furnace.heat_up_to(step.target_temperature)
        elif isinstance(step, IsothermalStep):
            config.pressure_controller.set_pressure(step.pressure)
            for gas in step.flow_rates:
                config.mfcs[gas].set_flow_rate(step.flow_rates[gas])
            time.sleep(step.time * 60)
        elif isinstance(step, CoolingStep):
            raise NotImplementedError()
        elif isinstance(step, FinalStep):
            raise NotImplementedError()
        else:
            raise Exception()

def main():
    """
    """
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=play)
    parser.add_argument('--config', required=True, help='path to config file with the sequence of actions to perform by the program')
    args = parser.parse_args()
    args.func(args)
