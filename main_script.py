import os
import time
import logging
import time
# from temperature_profile import TemperatureProfile
from time import sleep
from threading import Lock
from threading import Event
from pyModbusTCP.client import ModbusClient
from enum import Enum
from temperature_profile import TemperatureProfile

from pyModbusTCP.client import ModbusClient
import constans

# init modbus client
c = ModbusClient(host='192.168.0.8', port=56789, unit_id=1, auto_open=True)


# read 10 bits (= coils) at address 0, store result in coils list


class State(Enum):
    COOLING = 0
    HEATING = 1


class PlantTemperatureSimulator():
    shared_lock = Lock()
    heating_event = Event()
    cooling_event = Event()
    heating_profile = TemperatureProfile('Heating', shared_lock, heating_event, constans.dt_heat, constans.dtime)
    cooling_profile = TemperatureProfile('Cooling', shared_lock, cooling_event, constans.dt_cool, constans.dtime)

    def __init__(self):

        previous_state = State.COOLING.value  # Set initial state
        PlantTemperatureSimulator.heating_profile.start()
        PlantTemperatureSimulator.cooling_profile.start()
        while True:
            #try:
                # dane pobierane
                current_state = (c.read_holding_registers(14))[0]  ## grzanie lub chłodzenie

                pwm = c.read_holding_registers(6)  # PWM


                if previous_state != current_state:
                    if current_state == State.HEATING.value:
                        PlantTemperatureSimulator.cooling_event.clear()
                        PlantTemperatureSimulator.heating_event.set()
                        print(f'Heating...')
                    else:
                        PlantTemperatureSimulator.heating_event.clear()
                        PlantTemperatureSimulator.cooling_event.set()
                        print(f'Cooling...')
                    previous_state = current_state
            #except:
               # print("Oops!  ModbusTCP Error, trying again...")

            #try:
                c.write_single_register(10, int(TemperatureProfile.temperature*256))  ## temperatura odczytana

            #except:
                #print("Oops!  ModbusTCP Error, trying again...")
                sleep(1)


PlantTemperatureSimulator()
