import multiprocessing
import multiprocessing.connection
import time
import threading

from pyopspec.furnace.furnace_controller import FurnaceController
from pyopspec.mass_flow_controller.mass_flow_controller import MassFlowController
from pyopspec.pressure_controller.pressure_controller import PressureController
from pyopspec.plotters.non_blocking_plotter import NonBlockingPlotter
from pyopspec.plotters.point import Point

class DataCollectorPlotter(threading.Thread):
    """
    """

    def __init__(self, furnace_controller:FurnaceController, mass_flow_controllers:dict[str, MassFlowController], pressure_controller:PressureController|None):
        """
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
        self._pressure_controller = pressure_controller
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        self._plotter = NonBlockingPlotter()
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            temperature_point, flow_rate_points, pressure_point = self._collect_data()
            self._collector_pipe.send((temperature_point, flow_rate_points, pressure_point))
            time.sleep(1)
        self._collector_pipe.send((None, None, None))

    def stop(self):
        """
        """
        self._running = False

    def _collect_data(self) -> tuple[Point, list[Point], Point|None]:
        """
        """
        t = (time.time() - self._start_time) / 60.0
        T = self._furnace_controller.get_temperature()
        temperature_point = Point(x=t, y=T, label='temperature')
        flow_rate_points = []
        for gas in self._mfcs:
            t = (time.time() - self._start_time) / 60.0
            fr = self._mfcs[gas].get_flow_rate()
            flow_rate_point = Point(x=t, y=fr, label=gas)
            flow_rate_points.append(flow_rate_point)
        if self._pressure_controller is not None:
            t = (time.time() - self._start_time) / 60.0
            P = self._pressure_controller.get_pressure()
            pressure_point = Point(x=t, y=P, label='pressure')
        else:
            pressure_point = None
        return (temperature_point, flow_rate_points, pressure_point)
