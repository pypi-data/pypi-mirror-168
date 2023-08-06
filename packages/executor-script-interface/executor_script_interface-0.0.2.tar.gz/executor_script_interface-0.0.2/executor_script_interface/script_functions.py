import logging
from enum import Enum

class VariableType(Enum):
    PRESSURE = 1
    VOLTAGE = 2
    CURRENT = 3
    PACK_TEMPERATURE = 4
    AMBIENT_TEMPERATURE = 5

class CodesysMachineState():
    OPERATIONAL = int()
    OPERATIONAL_WITH_LOW_SOC = int()
    OPERATIONAL_DISCHARGE_NOT_ALLOWED = int()
    OPERATIONAL_WITH_HIGH_SOC = int()
    OPERATIONAL_CHARGE_NOT_ALLOWED = int()
    OPERATIONAL_RANGE = range(0)
    ALARM_RANGE = range(0)

class OpcTag():
    MACHINE_STATE = None

def log_info(msg: str) -> None:
    logging.info("### executor script: {}".format(msg))

class ScriptFunctions(object):
    def __init__(self) -> None:
        self.result = (False, "Script is not initialized")
        self.emulator = EmulatorFunctions()
        self.imu_sim = ImuSimFunctions()

    def script_pass(self) -> None:
        log_info("{} - {}: {}".format(ScriptFunctions.__name__, self.script_pass.__name__, locals()))

    def script_fail(self) -> None:
        log_info("{} - {}: {}".format(ScriptFunctions.__name__, self.script_fail.__name__, locals()))
        raise Exception("Failure!")

    def wait_for_machine_state_in_range(self, valid_machine_states: range, timeout_secs=60) -> None:
        log_info("{} - {}: {}".format(ScriptFunctions.__name__, self.wait_for_machine_state_in_range.__name__, locals()))

    def sleep(self, seconds: float):
        log_info("{} - {}: {}".format(ScriptFunctions.__name__, self.sleep.__name__, locals()))

class EmulatorFunctions(object):
    def __init__(self) -> None:
        pass

    def send(self, command_string: str):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.send.__name__, locals()))

    def enable_con(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.enable_con.__name__, locals()))

    def disable_con(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.disable_con.__name__, locals()))

    def set_con(self, value):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_con.__name__, locals()))

    def read_con(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_con.__name__, locals()))

    def enable_module(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.enable_module.__name__, locals()))

    def disable_module(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.disable_module.__name__, locals()))

    def set_module(self, target, value):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_module.__name__, locals()))

    def read_module(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_module.__name__, locals()))

    def read_module_current(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_module_current.__name__, locals()))

    def read_module_24v(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_module_24v.__name__, locals()))

    def read_module_3v3(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_module_3v3.__name__, locals()))

    def read_pressure_voltage(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_pressure_voltage.__name__, locals()))

    def read_pressure(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_pressure.__name__, locals()))

    def set_pressure(self, value):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_pressure.__name__, locals()))

    def read_current_voltage(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_current_voltage.__name__, locals()))

    def read_current(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_current.__name__, locals()))

    def set_current(self, target, value):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_current.__name__, locals()))

    def read_temp_voltage(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_temp_voltage.__name__, locals()))

    def read_temp(self, target):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_temp.__name__, locals()))

    def set_temp(self, target, value):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_temp.__name__, locals()))

    def set_contactor(self, value, scale=1.0):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.set_contactor.__name__, locals()))

    def read_contactor(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_contactor.__name__, locals()))

    def reinit(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.reinit.__name__, locals()))

    def status(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.status.__name__, locals()))

    def read_external_5v_pressure(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_external_5v_pressure.__name__, locals()))

    def read_external_5v_current(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_external_5v_current.__name__, locals()))

    def read_global_5v(self):
        log_info("{} - {}: {}".format(EmulatorFunctions.__name__, self.read_global_5v.__name__, locals()))

class ImuSimFunctions(object):
    def __init__(self) -> None:
        pass

    def initialize(self) -> None:
        log_info("{} - {}: {}".format(ImuSimFunctions.__name__, self.initialize.__name__, locals()))

    def get_variable_value(self, var_type: VariableType, node_id: int) -> float:
        log_info("{} - {}: {}".format(ImuSimFunctions.__name__, self.get_variable_value.__name__, locals()))

    def set_variable_value(self, var_type: VariableType, value: float, node_id: int):
        log_info("{} - {}: {}".format(ImuSimFunctions.__name__, self.set_variable_value.__name__, locals()))

    def ramp_variable(self, var_type: VariableType, target: float, delta_minute: float, reference_node: int, valid_machine_states: range) -> None:
        log_info("{} - {}: {}".format(ImuSimFunctions.__name__, self.ramp_variable.__name__, locals()))