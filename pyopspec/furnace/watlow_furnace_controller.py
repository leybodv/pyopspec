import time

from pywatlow.watlow import Watlow

from .logging import get_logger
from .furnace_controller import FurnaceController
from .exceptions import *

class WatlowFurnaceController(FurnaceController):
    """
    """

    def __init__(self, serial_number:str, port:str, logfilename:str, address:int=1):
        """
        """
        self._serial_number = serial_number
        self._watlow_protocol = Watlow(port=port, address=address)
        self._connected = False
        self._logger = get_logger(name=self.__class__.__name__, logfilename=logfilename)

    def connect(self):
        """
        """
#Next line throws this exception
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "C:\Users\GC\AppData\Local\Programs\Python\Python312\Lib\site-packages\pywatlow\watlow.py", line 325, in readParam
#    output = self._parseResponse(response)
#                                 ^^^^^^^^
#UnboundLocalError: cannot access local variable 'response' where it is not associated with a value
        #device_sn = self._watlow_protocol.readParam(param=1032, data_type=str)
        #if self._serial_number != device_sn:
        #    raise WrongDeviceException(f'Trying to connect device with S/N {self._serial_number} to the device with S/N {device_sn}')
        self._connected = True
        display_units_code = self._read_param(protocol=self._watlow_protocol, param=3005, data_type=int)
        self._display_temperature_units = '°C' if display_units_code == 15 else '°F'
        ramp_rate_units_code = self._read_param(protocol=self._watlow_protocol, param=7015, data_type=int)
        self._ramp_rate_units = 'min' if ramp_rate_units_code == 57 else 'h'
        setpoint_farenheit = self._read_param(protocol=self._watlow_protocol, param=7001, data_type=float)
        self._logger.debug(f'{setpoint_farenheit = }')
        setpoint = self._farenheit_to_celsius(setpoint_farenheit) #pyright: ignore[reportOptionalSubscript]
        measure = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float)) #pyright: ignore[reportOptionalSubscript]
        self._logger.info(f'Connected to furnace {self._serial_number}. Current setpoint value: {setpoint}°C. Current measured value: {measure}°C')

    def set_ramp_rate(self, ramp_rate:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        response = self._watlow_protocol.writeParam(param=7017, value=self._c_per_min_to_watlow_unit(ramp_rate), data_type=float)
        if self._display_temperature_units != '°C':
            raise NotSupportedException(f'Display units in °F are not supported. Change them to °C, or test pywatlow behavior and change the code accordingly')
        #if self._ramp_rate_units != 'min': #they are in hours actually
            #raise NotSupportedException(f'Ramp units in hours are not supported. Change them to minutes, or test pywatlow behavior and change the code accordingly')
        if response['error'] is not None: #pyright: ignore[reportOptionalSubscript]
            raise WatlowProtocolException(f'Error occured while setting heating rate: {response["error"]}') #pyright: ignore[reportOptionalSubscript]
        self._logger.info(f'Ramp rate parameter have been set to {ramp_rate}{self._display_temperature_units}/{self._ramp_rate_units}')

    def set_temperature(self, temperature:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        response = self._watlow_protocol.write(value=self._celsius_to_farenheit(temperature))
        if response['error'] is not None: #pyright: ignore[reportOptionalSubscript]
            raise WatlowProtocolException(f'Error occured while setting temperature: {response["error"]}') #pyright: ignore[reportOptionalSubscript]
        self._logger.info(f'The setpoint value of furnace controller with S/N {self._serial_number} has been set to {temperature}°C')

    def get_temperature(self) -> float:
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        measure = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float))
        self._logger.debug(f'Measured temperature on furnace controller with S/N {self._serial_number}: {measure}{self._display_temperature_units}')
        return measure

    def heat_up_to(self, target_temperature:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        measure = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float))
        if measure >= target_temperature:
            self._logger.warning(f'Trying to heat up to the temperature {target_temperature}{self._display_temperature_units}, which is lower current temperature {measure}{self._display_temperature_units}')
        response = self._watlow_protocol.write(value=self._celsius_to_farenheit(target_temperature))
        if response['error'] is not None: #pyright: ignore[reportOptionalSubscript]
            raise WatlowProtocolException(f'Error occured while setting temperature: {response["error"]}') #pyright: ignore[reportOptionalSubscript]
        self._logger.info(f'The setpoint value of furnace controller with S/N {self._serial_number} has been set to {target_temperature}°C')
        while True:
            current_temperature = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float))
            if current_temperature >= target_temperature * 0.99:
                break
            time.sleep(60)
        self._logger.info(f'Finished heating of the furnace with furnace controller {self._serial_number}')

    def cool_down_to(self, target_temperature:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        measure = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float))
        if measure <= target_temperature:
            self._logger.warning(f'Trying to cool down to the temperature {target_temperature}{self._display_temperature_units}, which is higher then current temperature {measure}{self._display_temperature_units}')
        response = self._watlow_protocol.write(value=self._celsius_to_farenheit(target_temperature))
        if response['error'] is not None: #pyright: ignore[reportOptionalSubscript]
            raise WatlowProtocolException(f'Error occured while setting temperature: {response["error"]}') #pyright: ignore[reportOptionalSubscript]
        self._logger.info(f'The setpoint value of furnace controller with S/N {self._serial_number} has been set to {target_temperature}°C')
        while True:
            current_temperature = self._farenheit_to_celsius(self._read_param(protocol=self._watlow_protocol, param=4001, data_type=float))
            if current_temperature <= target_temperature * 1.01 or current_temperature <= 35:
                break
            time.sleep(60)
        self._logger.info(f'Finished cooling of the furnace with furnace controller {self._serial_number}')

    def _read_param(self, protocol:Watlow, param:int, data_type) -> int|float:
        """
        """
        parameter = protocol.readParam(param=param, data_type=data_type)
        if parameter is not None:
            if parameter['error'] is not None:
                msg = f'Error occured while reading parameter: {parameter["error"]}'
                self._logger.error(msg=msg)
                raise WatlowProtocolException(msg)
            else:
                return parameter['data']
        else:
            msg = 'Read None parameter'
            self._logger.error(msg=msg)
            raise WatlowProtocolException(msg)

    def _farenheit_to_celsius(self, farenheit:float) -> float:
        """
        """
        return 5 * (farenheit - 32) / 9

    def _celsius_to_farenheit(self, celsius:float) -> float:
        """
        """
        return 9 * celsius / 5 +32

    def _c_per_min_to_watlow_unit(self, heating_rate_in_c:float) -> float:
        """
        """
        return heating_rate_in_c * 36 / 20
