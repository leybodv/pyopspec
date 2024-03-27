from pyopspec.steps.heating_step import HeatingStep
from pyopspec.steps.isothermal_step import IsothermalStep
from pyopspec.steps.cooling_step import CoolingStep
from pyopspec.steps.pressure_ramp_step import PressureRampStep
from pyopspec.steps.final_step import FinalStep

export_folder_path = './exported_data'

steps = [
            HeatingStep(
                pressure=1,
                flow_rates={
                                'Ar' :15,
                                'H2' :5,
                                'CO' :0,
                                'CO2':0,
                            },
                heating_rate=1,
                target_temperature=445),
            IsothermalStep(
                pressure=1,
                flow_rates={
                                'Ar' :15,
                                'H2' :5,
                                'CO' :0,
                                'CO2':0,
                            },
                time=120),
            CoolingStep(
                pressure=1,
                flow_rates={
                                'Ar' :20,
                                'H2' :0,
                                'CO' :0,
                                'CO2':0,
                            },
                cooling_rate=1,
                target_temperature=276),
            PressureRampStep(
                # change gas flow rates
                # ramp pressure at a specified rate
                pressure=5, # new setpoint value of pressure
                pressure_ramp_rate=1, # pressure increase/decrease ramp rate in bar/min
                flow_rates={ # flow rates in ml.n/min
                                'Ar' :20,
                                'H2' :0,
                                'CO' :0,
                                'CO2':0,
                            },),
            FinalStep(
                pressure=3,
                flow_rates={
                                'Ar' :5,
                                'H2' :5,
                                'CO' :5,
                                'CO2':5,
                            },
                temperature=276),
        ]
