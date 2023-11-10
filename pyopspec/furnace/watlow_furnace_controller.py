from pywatlow.watlow import Watlow

class WatlowFurnaceController():
    """
    """

    def __init__(self, serial_number:str, port:str, address:int=1):
        """
        """
        self._serial_number = serial_number
        self._watlow_protocol = Watlow(port=port, address=address)
        self._connected = False
        raise NotImplementedError()

    def connect(self):
        """
        """
        device_sn = self._watlow_protocol.readParam(param=1032, data_type=str)
        if self._serial_number != device_sn:
            raise WrongDeviceException(f'Trying to connect device with S/N {self._serial_number} to the device with S/N {device_sn}')
        self._connected = True
        setpoint = self._farenheit_to_celsius(self._watlow_protocol.readSetpoint()['data'])
        measure = self._farenheit_to_celsius(self._watlow_protocol.read()['data'])
        self._logger.info(f'Connected to furnace {self._serial_number}. Current setpoint value: {setpoint}°C. Current measured value: {measure}°C')

    def _farenheit_to_celsius(self, farenheit:float) -> float:
        """
        """
        return 5 * (farenheit - 32) / 9
