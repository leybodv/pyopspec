import propar

class BronkhorstPressureController():
    """
    """

    def __init__(self):
        """
        """
        raise NotImplementedError()

    def connect(self):
        """
        """
        self._propar_instrument = propar.instrument(comport=self._port, address=self._address)
        if self._propar_instrument.readParameter(92) != self._serial_number:
            raise WrongDeviceException()
        self._connected = True
        max_controlled_pressure = self._propar_instrument.readParameter(21)
        pressure_unit = self._propar_instrument.readParameter(129)
        setpoint = self._propar_instrument.readParameter(206)
        measure = self._propar_instrument.readParameter(205)
        self._logger.info(f'Connected to pressure controller. Max controlled pressure: {max_controlled_pressure} {pressure_unit}. Current setpoint value: {setpoint} {pressure_unit}. Current measured value: {measure} {pressure_unit}')
