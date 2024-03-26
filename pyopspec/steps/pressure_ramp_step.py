class PressureRampStep():
    """
    """

    def __init__(self, pressure:float, pressure_ramp_rate:float, flow_rates:dict[str,float]):
        """
        params
        ------
            pressure:float
                pressure in the device units
            ramp_rate:float
                pressure increase/decrease rate in <pressure device units>/min
            flow_rates:dict[str,float]
                flow_rates of gases
        """
        self.pressure = pressure
        self.pressure_ramp_rate = pressure_ramp_rate
        self.flow_rates = flow_rates
