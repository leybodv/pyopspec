import multiprocessing.connection

import matplotlib.pyplot as plt

from pyopspec.plotters.data import Data

class NonBlockingPlotter():
    """
    """

    def __init__(self):
        """
        """
        self._temperatures = Data(label='temperature')
        self._flow_rates = None
        self._pressures = None

    def __call__(self, pipe:multiprocessing.connection.Connection):
        """
        """
        self._pipe = pipe
        self._fig, (self._temperature_ax, self._flow_rates_ax) = plt.subplots(nrows=1, ncols=2)
        self._pressure_ax = self._temperature_ax.twinx()
        self._fig.set_tight_layout(True) #pyright: ignore[reportGeneralTypeIssues]
        self._setup_temperature_ax()
        self._setup_pressure_ax()
        self._setup_flow_rates_ax()
        timer = self._fig.canvas.new_timer(interval=5000)
        timer.add_callback(self._call_back)
        timer.start()
        plt.show()

    def _call_back(self) -> bool:
        """
        """
        while self._pipe.poll():
            data = self._pipe.recv()
            temperature_point = data[0]
            flow_rate_points = data[1]
            pressure_point = data[2]
            if temperature_point is None:
                return False
            else:
                self._temperatures.add_point(temperature_point)
                if pressure_point is not None:
                    if self._pressures is None:
                        self._pressures = Data(label='pressure')
                    self._pressures.add_point(pressure_point)
                if self._flow_rates is None:
                    self._flow_rates = []
                    for flow_rate_point in flow_rate_points:
                        self._flow_rates.append(Data(label=flow_rate_point.get_label()))
                for flow_rate_point, flow_rate in zip(flow_rate_points, self._flow_rates):
                    flow_rate.add_point(flow_rate_point)
                self._temperature_ax.clear()
                self._flow_rates_ax.clear()
                self._pressure_ax.clear()
                self._setup_temperature_ax()
                self._setup_pressure_ax()
                self._setup_flow_rates_ax()
                lines_temperature_pressure = []
                line, = self._temperature_ax.plot(self._temperatures.get_x(), self._temperatures.get_y(), color='red', linewidth=1, linestyle=':', label=self._temperatures.get_label())
                lines_temperature_pressure.append(line)
                if self._pressures is not None:
                    line, = self._pressure_ax.plot(self._pressures.get_x(), self._pressures.get_y(), color='blue', linewidth=1, linestyle=':', label=self._pressures.get_label())
                    lines_temperature_pressure.append(line)
                for flow_rate in self._flow_rates:
                    self._flow_rates_ax.plot(flow_rate.get_x(), flow_rate.get_y(), linewidth=1, linestyle=':', label=flow_rate.get_label())
                self._temperature_ax.legend(handles=lines_temperature_pressure)
                self._flow_rates_ax.legend()
        self._fig.canvas.draw()
        return True

    def _setup_temperature_ax(self):
        """
        """
        self._temperature_ax.set_xlabel('Time, min')
        self._temperature_ax.set_ylabel('Temperature, °C')

    def _setup_pressure_ax(self):
        """
        """
        self._pressure_ax.set_ylabel('Pressure, bar(a)')

    def _setup_flow_rates_ax(self):
        """
        """
        self._flow_rates_ax.set_ylabel('Flow rate, n.ml/min')
