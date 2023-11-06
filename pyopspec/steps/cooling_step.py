class CoolingStep():
    """
    """

    def __init__(self, pressure:float, flow_rates:dict[str,float], cooling_rate:float, target_temperature:float):
        """
        """
        self.pressure = pressure
        self.flow_rates = flow_rates
        self.cooling_rate = cooling_rate
        self.target_temperature = target_temperature
