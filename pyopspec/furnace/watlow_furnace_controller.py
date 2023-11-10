import time

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
        display_units_code = self._watlow_protocol.readParam(param=3005, data_type=int)['data']
        self._display_temperature_units = '°C' if display_units_code == 15 else '°F'
        ramp_rate_units_code = self._watlow_protocol.readParam(param=7015, data_type=int)
        self._ramp_rate_units = 'min' if ramp_rate_units_code == 57 else 'h'
        setpoint = self._farenheit_to_celsius(self._watlow_protocol.readSetpoint()['data'])
        measure = self._farenheit_to_celsius(self._watlow_protocol.read()['data'])
        self._logger.info(f'Connected to furnace {self._serial_number}. Current setpoint value: {setpoint}°C. Current measured value: {measure}°C')

    def set_heating_rate(self, heating_rate:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        response = self._watlow_protocol.writeParam(param=7017, value=self._c_per_min_to_watlow_unit(heating_rate), data_type=float)
        if self._display_temperature_units != '°C':
            raise NotSupportedException(f'Display units in °F are not supported. Change them to °C, or test pywatlow behavior and change the code accordingly')
        if self._ramp_rate_units != 'min':
            raise NotSupportedException(f'Ramp units in hours are not supported. Change them to minutes, or test pywatlow behavior and change the code accordingly')
        if response['error'] is not None:
            raise WatlowProtocolException(f'Error occured while setting heating rate: {response['error']}')
        self._logger.info(f'Heating rate parameter have been set to {heating_rate}{self._display_temperature_units}/{self._ramp_rate_units}')

    def heat_up_to(self, target_temperature:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        response = self._watlow_protocol.write(value=self._celsius_to_farenheit(target_tamperature))
        if response['error'] is not None:
            raise WatlowProtocolException(f'Error occured while setting temperature: {response['error']}')
        self._logger.info(f'The setpoint value of furnace controller with S/N {self._serial_number} has been set to {target_temperature}°C')
        while True:
            current_temperature = self._farenheit_to_celsius(self._watlow_protocol.read()['data'])
            if current_temperature >= target_temperature * 0.99:
                break
            time.sleep(60)
        self._logger.info(f'Finished heating of the furnace with furnace controller {self._serial_number}')

    def _farenheit_to_celsius(self, farenheit:float) -> float:
        """
        """
        return 5 * (farenheit - 32) / 9

    def _c_per_min_to_watlow_unit(self, heating_rate_in_c:float) -> float:
        """
        """
        return heating_rate_in_c * 36 / 20
