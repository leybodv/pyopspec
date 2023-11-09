from pyopspec.pressure_controller.bronkhorst_pressure_controller import BronkhorstPressureController
from pyopspec.mass_flow_controller.bronkhorst_mass_flow_controller import BronkhorstMassFlowController

pressure_controller = BronkhorstPressureController(
                                                    port='',
                                                    serial_number='',
                                                    address=0,
                                                  )

mfcs = {
        'Ar':BronkhorstMassFlowController(
                                            port= ,
                                            serial_number= ,
                                            address= ,
                                         ),
        'CO':BronkhorstMassFlowController(
                                            port= ,
                                            serial_number= ,
                                            address= ,
                                         ),
        }

furnace = WatlowFurnaceController()
