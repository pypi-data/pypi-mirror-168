# FBP
soft_interlocks = ["Heat-Sink Overtemperature"]

hard_interlocks = [
    "Load Overcurrent",
    "Load Overvoltage",
    "DCLink Overvoltage",
    "DCLink Undervoltage",
    "DCLink Relay Fault",
    "DCLink Fuse Fault",
    "MOSFETs Driver Fault",
    "Welded Relay Fault",
]

# FBP DC-Link
dclink_hard_interlocks = [
    "Power_Module_1_Fault",
    "Power_Module_2_Fault",
    "Power_Module_3_Fault",
    "Total_Output_Overvoltage",
    "Power_Module_1_Overvoltage",
    "Power_Module_2_Overvoltage",
    "Power_Module_3_Overvoltage",
    "Total_Output_Undervoltage",
    "Power_Module_1_Undervoltage",
    "Power_Module_2_Undervoltage",
    "Power_Module_3_Undervoltage",
    "Smoke_Detector",
    "External_Interlock",
]

bsmp = {
    "i_load": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "v_load": {"addr": 34, "format": "f", "size": 4, "egu": "V"},
    "v_dclink": {"addr": 35, "format": "f", "size": 4, "egu": "V"},
    "temp_switches": {"addr": 36, "format": "f", "size": 4, "egu": "°C"},
    "duty_cycle": {"addr": 37, "format": "f", "size": 4, "egu": "%"},
    "ps_alarms": {"addr": 38, "format": "I", "size": 4, "egu": ""},
    "reserved": {"addr": 39, "format": "7s", "size": 7, "egu": ""},
    "ps_status_1": {"addr": 46, "format": "H", "size": 2, "egu": ""},
    "ps_status_2": {"addr": 47, "format": "H", "size": 2, "egu": ""},
    "ps_status_3": {"addr": 48, "format": "H", "size": 2, "egu": ""},
    "ps_status_4": {"addr": 49, "format": "H", "size": 2, "egu": ""},
    "ps_setpoint_1": {"addr": 50, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_setpoint_2": {"addr": 51, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_setpoint_3": {"addr": 52, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_setpoint_4": {"addr": 53, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_reference_1": {"addr": 54, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_reference_2": {"addr": 55, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_reference_3": {"addr": 56, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_reference_4": {"addr": 57, "format": "f", "size": 4, "egu": "A / V / %"},
    "ps_soft_interlocks_1": {"addr": 58, "format": "I", "size": 4, "egu": ""},
    "ps_soft_interlocks_2": {"addr": 59, "format": "I", "size": 4, "egu": ""},
    "ps_soft_interlocks_3": {"addr": 60, "format": "I", "size": 4, "egu": ""},
    "ps_soft_interlocks_4": {"addr": 61, "format": "I", "size": 4, "egu": ""},
    "ps_hard_interlocks_1": {"addr": 62, "format": "I", "size": 4, "egu": ""},
    "ps_hard_interlocks_2": {"addr": 63, "format": "I", "size": 4, "egu": ""},
    "ps_hard_interlocks_3": {"addr": 64, "format": "I", "size": 4, "egu": ""},
    "ps_hard_interlocks_4": {"addr": 65, "format": "I", "size": 4, "egu": ""},
    "i_load_1": {"addr": 66, "format": "f", "size": 4, "egu": "A"},
    "i_load_2": {"addr": 67, "format": "f", "size": 4, "egu": "A"},
    "i_load_3": {"addr": 68, "format": "f", "size": 4, "egu": "A"},
    "i_load_4": {"addr": 69, "format": "f", "size": 4, "egu": "A"},
    "ps_alarms_1": {"addr": 70, "format": "I", "size": 4, "egu": ""},
    "ps_alarms_2": {"addr": 71, "format": "I", "size": 4, "egu": ""},
    "ps_alarms_3": {"addr": 72, "format": "I", "size": 4, "egu": ""},
    "ps_alarms_4": {"addr": 73, "format": "I", "size": 4, "egu": ""},
}

bsmp_dclink = {
    "modules_status": {"addr": 33, "format": "I", "size": 4, "egu": ""},
    "v_out": {"addr": 34, "format": "f", "size": 4, "egu": "V"},
    "v_out_1": {"addr": 35, "format": "f", "size": 4, "egu": "V"},
    "v_out_2": {"addr": 36, "format": "f", "size": 4, "egu": "V"},
    "v_out_3": {"addr": 37, "format": "f", "size": 4, "egu": "V"},
    "dig_pot_tap": {"addr": 38, "format": "B", "size": 1, "egu": "%"},
}
