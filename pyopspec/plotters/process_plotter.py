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
    Class for plotting data from activation and activity measurement experiments.
    """

    def __init__(self, furnace_controller:FurnaceController, mass_flow_controllers:dict[str, MassFlowController], pressure_controller:PressureController|None, chromatograph:Chromatograph|None):
        """
        Initialize base class, instance variables and start non blocking plotter in a separate process.

        parameters
        ----------
        furnace_controller:OwenTPM101
            furnace controller to get information about current temperature
        mass_flow_controllers:list[BronkhorstF201CV]
            list of mass flow controllers to get information about current flow rates
        gases:list[str]
            list of gases used for process, which will be added as legend to plot
        chromatograph:ChromatecCrystal5000|None
            chromatograph to get information about analysis start time
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
        self._gases = gases
        self._chromatograph = chromatograph
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        self._plotter = NonBlockingPlotter()
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        This method is invoked when thread is started. While thread is running get temperature, chromatograph and flow rate data and send these data through multiprocessing pipe to non blocking plotter. Send None to plotter, when thread is not running.
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            temperature_point, chromatograph_point, flow_rate_points = self._collect_data()
            self._collector_pipe.send((temperature_point, chromatograph_point, flow_rate_points))
            time.sleep(10)
        self._collector_pipe.send((None, None, None))

    def stop(self):
        """
        Stop this thread.
        """
        self._running = False

    def _collect_data(self) -> tuple[Point, Point|None, list[Point]]:
        """
        Get data about current temperature, time from the beginning of the chromatographic analysis and current gas flow rates.

        returns
        -------
        temperature_point:Point
            time and furnace temperature
        chromatograph_point:Point|None
            time from the beginning of the chromatographic analysis or None if chromatograph is not used or if current chromatograph working status is not analysis
        flow_rate_points:list[Point]
            list of times and flow rates for all mass flow controllers
        """
        t = (time.time() - self._start_time) / 60.0
        T = self._furnace_controller.get_temperature()
        temperature_point = Point(x=t, y=T, label='temperature')
        chromatograph_point = None
        if self._chromatograph is not None:
            try:
                t = round((time.time() - self._start_time) / 60.0, 2) - round(self._chromatograph.get_analysis_time(), 2)
                chromatograph_point = Point(x=t, y=None, label='chromatograms')
            except ChromatographStateException:
                pass
        flow_rate_points = []
        for mfc, gas in zip(self._mfcs, self._gases):
            t = (time.time() - self._start_time) / 60.0
            fr = mfc.get_flow_rate()
            flow_rate_point = Point(x=t, y=fr, label=gas)
            flow_rate_points.append(flow_rate_point)
        return (temperature_point, chromatograph_point, flow_rate_points)
