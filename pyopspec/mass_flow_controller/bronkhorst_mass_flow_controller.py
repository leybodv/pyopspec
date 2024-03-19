import propar

from .mass_flow_controller import MassFlowController
from .exceptions import *
from .logging import get_logger

class BronkhorstMassFlowController(MassFlowController):
    """
    """

    def __init__(self, port:str, serial_number:str, logfilename:str, address:int=1):
        """
        """
        self._port = port
        self._serial_number = serial_number
        self._address = address
        self._propar_instrument = propar.instrument(comport=self._port, address=self._address)
        self._connected = False
        self._logger = get_logger(self.__class__.__name__, logfilename=logfilename)

    def connect(self):
        """
        """
        instrument_sn = self._propar_instrument.readParameter(dde_nr=92)
        if self._serial_number != instrument_sn:
            raise WrongDeviceException(f'Trying to connect device with S/N {self._serial_number} to the device with S/N {instrument_sn}')
        self._connected = True
        self._propar_instrument.wink()
        self._max_controlled_flowrate = self._propar_instrument.readParameter(dde_nr=21)
        self._flowrate_unit = self._propar_instrument.readParameter(dde_nr=129)
        self._calibration_fluid_name = self._propar_instrument.readParameter(dde_nr=25)
        self._calibration_inlet_pressure = self._propar_instrument.readParameter(dde_nr=178)
        self._calibration_outlet_pressure = self._propar_instrument.readParameter(dde_nr=179)
        setpoint = self._propar_instrument.readParameter(dde_nr=206)
        measure = self._propar_instrument.readParameter(dde_nr=205)
        self._logger.info(f'Connected to mass flow controller {self._serial_number}. Current calibration: {self._calibration_fluid_name}, inlet {self._calibration_inlet_pressure} bar(a), outlet {self._calibration_outlet_pressure} bar(a). Max controlled flow rate: {self._max_controlled_flowrate} {self._flowrate_unit}. Current setpoint value: {setpoint} {self._flowrate_unit}. Current measured value: {measure} {self._flowrate_unit}')

    def set_flow_rate(self, flow_rate:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        if flow_rate > self._max_controlled_flowrate: #pyright: ignore[reportGeneralTypeIssues]
            raise OutOfDeviceCapacityException(f'Trying to set flow rate {flow_rate} {self._flowrate_unit} on a device with max capacity of {self._max_controlled_flowrate} {self._flowrate_unit}')
        self._propar_instrument.writeParameter(dde_nr=206, data=flow_rate)
        self._logger.info(f'Set flow rate of {self._serial_number} to {flow_rate} {self._flowrate_unit}')

    def get_flow_rate(self) -> float:
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        measure = self._propar_instrument.readParameter(dde_nr=205)
        self._logger.debug(f'Current flow rate on mass flow controller {self._serial_number}: {measure} {self._flowrate_unit}')
        return measure #pyright: ignore[reportGeneralTypeIssues]
