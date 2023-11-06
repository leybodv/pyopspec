from pyopspec.steps.heating_step import HeatingStep
from pyopspec.steps.isothermal_step import IsothermalStep
from pyopspec.steps.cooling_step import CoolingStep
from pyopspec.steps.final_step import FinalStep

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
