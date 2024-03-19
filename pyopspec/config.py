from datetime import datetime

from pyopspec.pressure_controller.bronkhorst_pressure_controller import BronkhorstPressureController
from pyopspec.mass_flow_controller.bronkhorst_mass_flow_controller import BronkhorstMassFlowController
from pyopspec.furnace.watlow_furnace_controller import WatlowFurnaceController

logfilename=f'./pyopspec_logs/{datetime.now():%Y%m%d_%H%M%S}.log'
pressure_controller = BronkhorstPressureController(
                                                    port='COM6',
                                                    serial_number='M22202037R',
                                                    logfilename=logfilename,
                                                    address=59,
                                                  )

mfcs = {
        'Ar':BronkhorstMassFlowController(
                                           port='COM6',
                                           serial_number='M21222867K',
                                           logfilename=logfilename,
                                           address=15,
                                         ),
        'CO2':BronkhorstMassFlowController(
                                           port='COM6',
                                           serial_number='M21222867G',
                                           logfilename=logfilename,
                                           address=10,
                                         ),
        'CO':BronkhorstMassFlowController(
                                           port='COM6',
                                           serial_number='M21222867B',
                                           logfilename=logfilename,
                                           address=100,
                                         ),
        'H2':BronkhorstMassFlowController(
                                           port='COM6',
                                           serial_number='M21222867I',
                                           logfilename=logfilename,
                                           address=13,
                                         ),
        'N2':BronkhorstMassFlowController(
                                           port='COM6',
                                           serial_number='M21222867J',
                                           logfilename=logfilename,
                                           address=14,
                                         ),
      }

furnace = WatlowFurnaceController(serial_number='12345', port='COM3', logfilename=logfilename)
