import threading
import time
from pathlib import Path

from pyopspec.furnace.furnace_controller import FurnaceController
from pyopspec.mass_flow_controller.mass_flow_controller import MassFlowController
from pyopspec.pressure_controller.pressure_controller import PressureController

class DataExporter(threading.Thread):
    """
    """

    def __init__(self, folder_path:str, furnace_controller:FurnaceController, mass_flow_controllers:dict[str, MassFlowController], pressure_controller:PressureController):
        """
        """
        super().__init__(daemon=False)
        self._folder = Path(folder_path).absolute()
        self._folder.mkdir(parents=True, exist_ok=True)
        with self._folder.joinpath('temperature.txt').open(mode='w') as f:
            f.write(f'Time, min\tTemperature, °C\n')
        for gas in mass_flow_controllers:
            with self._folder.joinpath(f'{gas}.txt').open(mode='w') as f:
                f.write(f'Time, min\tFlow Rate, ml/min\n')
        with self._folder.joinpath('pressure.txt').open(mode='w') as f:
            f.write(f'Time, min\tPressure, bar\n')
        self._furnace_controller = furnace_controller
        self._mass_flow_controllers = mass_flow_controllers
        self._pressure_controller = pressure_controller

    def run(self):
        """
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            t = (time.time() - self._start_time) / 60.0
            T = self._furnace_controller.get_temperature()
            with self._folder.joinpath('temperature.txt').open(mode='a') as f:
                f.write(f'{t}\t{T}\n')
            for gas in self._mass_flow_controllers:
                t = (time.time() - self._start_time) / 60.0
                f = self._mass_flow_controllers[gas].get_flow_rate()
                with self._folder.joinpath(f'{gas}.txt').open(mode='a') as file:
                    file.write(f'{t}\t{f}\n')
            t = (time.time() - self._start_time) / 60.0
            p = self._pressure_controller.get_pressure()
            with self._folder.joinpath('pressure.txt').open(mode='a') as f:
                f.write(f'{t}\t{p}\n')
            time.sleep(1)

    def stop(self):
        """
        """
        self._running = False
