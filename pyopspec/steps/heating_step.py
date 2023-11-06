class HeatingStep():
    """
    """

    def __init__(self, pressure:float, flow_rates:dict[str,float], heating_rate:float, target_temperature:float):
        """
        """
        self.pressure = pressure
        self.flow_rates = flow_rates
        self.heating_rate = heating_rate
        self.target_temperature = target_temperature
