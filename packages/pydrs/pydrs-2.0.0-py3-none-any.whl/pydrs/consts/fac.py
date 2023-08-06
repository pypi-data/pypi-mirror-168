# FAC ACDC
list_acdc_soft_interlocks = []

list_acdc_hard_interlocks = [
    "CapBank Overvoltage",
    "Rectifier Overvoltage",
    "Rectifier Undervoltage",
    "Rectifier Overcurrent",
    "Welded Contactor Fault",
    "Opened Contactor Fault",
    "IIB Input Stage Interlock",
    "IIB Command Interlock",
]

list_acdc_iib_is_interlocks = [
    "Rectifier Overvoltage",
    "Input Overcurrent",
    "IGBT Overtemperature",
    "IGBT Overtemperature HW",
    "Driver Overvoltage",
    "Driver Overcurrent",
    "Top Driver Error",
    "Bottom Driver Error",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

list_acdc_iib_is_alarms = [
    "Rectifier Overvoltage",
    "Input Overcurrent",
    "IGBT Overtemperature",
    "Driver Overvoltage",
    "Driver Overcurrent",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

list_acdc_iib_cmd_interlocks = [
    "Capbank Overvoltage",
    "Output Overvoltage",
    "External Boards Overvoltage",
    "Auxiliary Board Overcurrent",
    "IDB Board Overcurrent",
    "Rectifier Inductor Overtemperature",
    "Rectifier Heat-Sink Overtemperature",
    "AC Mains Overcurrent",
    "Emergency Button",
    "AC Mains Undervoltage",
    "AC Mains Overvoltage",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

list_acdc_iib_cmd_alarms = [
    "Capbank Overvoltage",
    "Output Overvoltage",
    "External Boards Overvoltage",
    "Auxiliary Board Overcurrent",
    "IDB Board Overcurrent",
    "Rectifier Inductor Overtemperature",
    "Rectifier Heat-Sink Overtemperature",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

# FAC DCDC
list_dcdc_soft_interlocks = [
    "DCCT 1 Fault",
    "DCCT 2 Fault",
    "DCCT High Difference",
    "Load Feedback 1 Fault",
    "Load Feedback 2 Fault",
]

list_dcdc_hard_interlocks = [
    "Load Overcurrent",
    "CapBank Overvoltage",
    "CapBank Undervoltage",
    "IIB Interlock",
    "External Interlock",
    "Rack Interlock",
]

list_dcdc_iib_interlocks = [
    "Input Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "IGBT 1 Overtemperature",
    "IGBT 1 Overtemperature HW",
    "IGBT 2 Overtemperature",
    "IGBT 2 Overtemperature HW",
    "Driver Overvoltage",
    "Driver 1 Overcurrent",
    "Driver 2 Overcurrent",
    "Top Driver 1 Error",
    "Bottom Driver 1 Error",
    "Top Driver 2 Error",
    "Bottom Driver 2 Error",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

list_dcdc_iib_alarms = [
    "Input Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "IGBT 1 Overtemperature",
    "IGBT 2 Overtemperature",
    "Driver Overvoltage",
    "Driver 1 Overcurrent",
    "Driver 2 Overcurrent",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

# FAC-2S AC/DC
list_2s_acdc_soft_interlocks = []
list_2s_acdc_hard_interlocks = [
    "CapBank Overvoltage",
    "Rectifier Overvoltage",
    "Rectifier Undervoltage",
    "Rectifier Overcurrent",
    "Welded Contactor Fault",
    "Opened Contactor Fault",
    "IIB Input Stage Interlock",
    "IIB Command Interlock",
]

list_2s_acdc_iib_is_interlocks = list_acdc_iib_is_interlocks
list_2s_acdc_iib_cmd_interlocks = list_acdc_iib_cmd_interlocks
list_2s_acdc_iib_is_alarms = list_acdc_iib_is_alarms
list_2s_acdc_iib_cmd_alarms = list_acdc_iib_cmd_alarms

# FAC-2S DC/DC
list_2s_dcdc_soft_interlocks = [
    "DCCT 1 Fault",
    "DCCT 2 Fault",
    "DCCT High Difference",
    "Load Feedback 1 Fault",
    "Load Feedback 2 Fault",
]

list_2s_dcdc_hard_interlocks = [
    "Load Overcurrent",
    "Module 1 CapBank Overvoltage",
    "Module 2 CapBank Overvoltage",
    "Module 1 CapBank Undervoltage",
    "Module 2 CapBank Undervoltage",
    "IIB Mod 1 Itlk",
    "IIB Mod 2 Itlk",
    "External Interlock",
    "Rack Interlock",
]

list_2s_dcdc_iib_interlocks = list_dcdc_iib_interlocks
list_2s_dcdc_iib_alarms = list_dcdc_iib_alarms

# FAC-2P4S AC/DC
list_2p4s_acdc_hard_interlocks = [
    "CapBank Overvoltage",
    "Rectifier Overvoltage",
    "Rectifier Undervoltage",
    "Rectifier Overcurrent",
    "Welded Contactor Fault",
    "Opened Contactor Fault",
    "IIB Input Stage Interlock",
    "IIB Command Interlock",
]

list_2p4s_acdc_iib_is_interlocks = list_acdc_iib_is_interlocks
list_2p4s_acdc_iib_cmd_interlocks = list_acdc_iib_cmd_interlocks
list_2p4s_acdc_iib_is_alarms = list_acdc_iib_is_alarms
list_2p4s_acdc_iib_cmd_alarms = list_acdc_iib_cmd_alarms

# FAC-2P4S DC/DC
list_2p4s_dcdc_soft_interlocks = [
    "DCCT 1 Fault",
    "DCCT 2 Fault",
    "DCCT High Difference",
    "Load Feedback 1 Fault",
    "Load Feedback 2 Fault",
    "Arm 1 Overcurrent",
    "Arm 2 Overcurrent",
    "Arms High Difference",
    "Complementary PS Interlock",
]

list_2p4s_dcdc_hard_interlocks = [
    "Load Overcurrent",
    "Module 1 CapBank Overvoltage",
    "Module 2 CapBank Overvoltage",
    "Module 3 CapBank Overvoltage",
    "Module 4 CapBank Overvoltage",
    "Module 5 CapBank Overvoltage",
    "Module 6 CapBank Overvoltage",
    "Module 7 CapBank Overvoltage",
    "Module 8 CapBank Overvoltage",
    "Module 1 CapBank Undervoltage",
    "Module 2 CapBank Undervoltage",
    "Module 3 CapBank Undervoltage",
    "Module 4 CapBank Undervoltage",
    "Module 5 CapBank Undervoltage",
    "Module 6 CapBank Undervoltage",
    "Module 7 CapBank Undervoltage",
    "Module 8 CapBank Undervoltage",
    "IIB 1 Itlk",
    "IIB 2 Itlk",
    "IIB 3 Itlk",
    "IIB 4 Itlk",
    "IIB 5 Itlk",
    "IIB 6 Itlk",
    "IIB 7 Itlk",
    "IIB 8 Itlk",
]

list_2p4s_dcdc_iib_interlocks = list_dcdc_iib_interlocks
list_2p4s_dcdc_iib_alarms = list_dcdc_iib_alarms

# FAC DCDC EMA
list_dcdc_ema_soft_interlocks = ["DCCT Fault", "Load Feedback Fault"]

list_dcdc_ema_hard_interlocks = [
    "Load Overcurrent",
    "DCLink Overvoltage",
    "DCLink Undervoltage",
    "Emergency Button",
    "Load Waterflow",
    "Load Overtemperature",
    "IIB Itlk",
]

list_dcdc_ema_iib_interlocks = [
    "Input Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "IGBT 1 Overtemperature",
    "IGBT 1 Overtemperature HW",
    "IGBT 2 Overtemperature",
    "IGBT 2 Overtemperature HW",
    "Driver Overvoltage",
    "Driver 1 Overcurrent",
    "Driver 2 Overcurrent",
    "Top Driver 1 Error",
    "Bottom Driver 1 Error",
    "Top Driver 2 Error",
    "Bottom Driver 2 Error",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

list_dcdc_ema_iib_alarms = [
    "Input Overvoltage",
    "Input Overcurrent",
    "Output Overcurrent",
    "IGBT 1 Overtemperature",
    "IGBT 2 Overtemperature",
    "Driver Overvoltage",
    "Driver 1 Overcurrent",
    "Driver 2 Overcurrent",
    "Inductors Overtemperature",
    "Heat-Sink Overtemperature",
    "Ground Leakage Overcurrent",
    "Board IIB Overtemperature",
    "Module Overhumidity",
]

# FAC-2P ACDC
list_2p_acdc_imas_soft_interlocks = []

list_2p_acdc_imas_hard_interlocks = [
    "CapBank Overvoltage",
    "Rectifier Overcurrent",
    "AC Mains Contactor Fault",
    "Module A Interlock",
    "Module B Interlock",
    "DCDC Interlock",
]

# FAC-2P DCDC
list_2p_dcdc_imas_soft_interlocks = []

list_2p_dcdc_imas_hard_interlocks = [
    "Load Overcurrent",
    "Module 1 CapBank_Overvoltage",
    "Module 2 CapBank_Overvoltage",
    "Module 1 CapBank_Undervoltage",
    "Module 2 CapBank_Undervoltage",
    "Arm 1 Overcurrent",
    "Arm 2 Overcurrent",
    "Arms High_Difference",
    "ACDC Interlock",
]

bsmp_acdc = {
    "v_capacitor_bank": {"addr": 33, "format": "f", "size": 4, "egu": "V"},
    "i_out_rectifier": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "duty_cycle": {"addr": 35, "format": "f", "size": 4, "egu": "p.u."},
    "i_input_is_iib": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "v_input_is_iib": {"addr": 37, "format": "f", "size": 4, "egu": "V"},
    "temp_igbt_is_iib": {"addr": 38, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_is_iib": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "i_driver_is_iib": {"addr": 40, "format": "f", "size": 4, "egu": "A"},
    "temp_inductor_is_iib": {"addr": 41, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_is_iib": {"addr": 42, "format": "f", "size": 4, "egu": "°C"},
    "temp_board_is_iib": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "rh_is_iib": {"addr": 44, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_is": {"addr": 45, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_is": {"addr": 46, "format": "I", "size": 4, "egu": ""},
    "v_output_cmd_iib": {"addr": 47, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_cmd_iib": {"addr": 48, "format": "f", "size": 4, "egu": "V"},
    "temp_rect_inductor_cmd_iib": {"addr": 49, "format": "f", "size": 4, "egu": "°C"},
    "temp_rect_heatsink_cmd_iib": {"addr": 50, "format": "f", "size": 4, "egu": "°C"},
    "v_ext_boards_cmd_iib": {"addr": 51, "format": "f", "size": 4, "egu": "V"},
    "i_aux_board_cmd_iib": {"addr": 52, "format": "f", "size": 4, "egu": "A"},
    "i_idb_board_cmd_iib": {"addr": 53, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_cmd_iib": {"addr": 54, "format": "f", "size": 4, "egu": "A"},
    "temp_board_cmd_iib": {"addr": 55, "format": "f", "size": 4, "egu": "°C"},
    "rh_cmd_iib": {"addr": 56, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_cmd": {"addr": 57, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_cmd": {"addr": 58, "format": "I", "size": 4, "egu": ""},
}

bsmp_dcdc = {
    "i_load_mean": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "i_load1": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "i_load2": {"addr": 35, "format": "f", "size": 4, "egu": "A"},
    "v_capacitor_bank": {"addr": 36, "format": "f", "size": 4, "egu": "V"},
    "duty_cycle": {"addr": 37, "format": "f", "size": 4, "egu": "p.u."},
    "v_input_iib": {"addr": 38, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib": {"addr": 39, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib": {"addr": 40, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib": {"addr": 41, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib": {"addr": 42, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib": {"addr": 44, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib": {"addr": 45, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib": {"addr": 46, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib": {"addr": 47, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_iib": {"addr": 48, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib": {"addr": 49, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib": {"addr": 50, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks": {"addr": 51, "format": "I", "size": 4, "egu": ""},
    "iib_alarms": {"addr": 52, "format": "I", "size": 4, "egu": ""},
    "ps_alarms": {"addr": 53, "format": "I", "size": 4, "egu": ""},
}

bsmp_dcdc_ema = {
    "i_load": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "v_dclink": {"addr": 34, "format": "f", "size": 4, "egu": "V"},
    "duty_cycle": {"addr": 35, "format": "f", "size": 4, "egu": "p.u."},
    "v_input_iib": {"addr": 36, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib": {"addr": 37, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib": {"addr": 38, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib": {"addr": 39, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib": {"addr": 40, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib": {"addr": 41, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib": {"addr": 42, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib": {"addr": 43, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib": {"addr": 44, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib": {"addr": 45, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_iib": {"addr": 46, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib": {"addr": 47, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib": {"addr": 48, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks": {"addr": 49, "format": "f", "size": 4, "egu": ""},
    "iib_alarms": {"addr": 50, "format": "f", "size": 4, "egu": ""},
    "ps_alarms": {"addr": 51, "format": "I", "size": 4, "egu": ""},
}

bsmp_2s_acdc = {
    "v_capacitor_bank": {"addr": 33, "format": "f", "size": 4, "egu": "V"},
    "i_out_rectifier": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "duty_cycle": {"addr": 35, "format": "f", "size": 4, "egu": "p.u."},
    "i_input_is_iib": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "v_input_is_iib": {"addr": 37, "format": "f", "size": 4, "egu": "V"},
    "temp_igbt_is_iib": {"addr": 38, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_is_iib": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "i_driver_is_iib": {"addr": 40, "format": "f", "size": 4, "egu": "A"},
    "temp_inductor_is_iib": {"addr": 41, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_is_iib": {"addr": 42, "format": "f", "size": 4, "egu": "°C"},
    "temp_board_is_iib": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "rh_is_iib": {"addr": 44, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_is": {"addr": 45, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_is": {"addr": 46, "format": "I", "size": 4, "egu": ""},
    "v_output_cmd_iib": {"addr": 47, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_cmd_iib": {"addr": 48, "format": "f", "size": 4, "egu": "V"},
    "temp_rect_inductor_cmd_iib": {"addr": 49, "format": "f", "size": 4, "egu": "°C"},
    "temp_rect_heatsink_cmd_iib": {"addr": 50, "format": "f", "size": 4, "egu": "°C"},
    "v_ext_boards_cmd_iib": {"addr": 51, "format": "f", "size": 4, "egu": "V"},
    "i_aux_board_cmd_iib": {"addr": 52, "format": "f", "size": 4, "egu": "A"},
    "i_idb_board_cmd_iib": {"addr": 53, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_cmd_iib": {"addr": 54, "format": "f", "size": 4, "egu": "A"},
    "temp_board_cmd_iib": {"addr": 55, "format": "f", "size": 4, "egu": "°C"},
    "rh_cmd_iib": {"addr": 56, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_cmd": {"addr": 57, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_cmd": {"addr": 58, "format": "I", "size": 4, "egu": ""},
}

bsmp_2s_dcdc = {
    "i_load_mean": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "i_load1": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "i_load2": {"addr": 35, "format": "f", "size": 4, "egu": "A"},
    "v_capbank_1": {"addr": 36, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_2": {"addr": 37, "format": "f", "size": 4, "egu": "V"},
    "duty_cycle_1": {"addr": 38, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_2": {"addr": 39, "format": "f", "size": 4, "egu": "p.u."},
    "v_input_iib_1": {"addr": 40, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib_1": {"addr": 41, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib_1": {"addr": 42, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib_1": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib_1": {"addr": 44, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib_1": {"addr": 45, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib_1": {"addr": 46, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib_1": {"addr": 47, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib_1": {"addr": 48, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib_1": {"addr": 49, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib_1": {"addr": 50, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib_1": {"addr": 51, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_1": {"addr": 52, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_1": {"addr": 53, "format": "I", "size": 4, "egu": ""},
    "v_input_iib_2": {"addr": 54, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib_2": {"addr": 55, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib_2": {"addr": 56, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib_2": {"addr": 57, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib_2": {"addr": 58, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib_2": {"addr": 59, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib_2": {"addr": 60, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib_2": {"addr": 61, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib_2": {"addr": 62, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib_2": {"addr": 63, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib_2": {"addr": 64, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib_2": {"addr": 65, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_2": {"addr": 66, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_2": {"addr": 67, "format": "I", "size": 4, "egu": ""},
    "ps_alarms": {"addr": 68, "format": "I", "size": 4, "egu": ""},
}

bsmp_2p_acdc_imas = {
    "v_capacitor_bank": {"addr": 33, "format": "f", "size": 4, "egu": "V"},
    "i_out_rectifier": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "duty_cycle": {"addr": 35, "format": "f", "size": 4, "egu": "p.u."},
}

bsmp_2p_dcdc_imas = {
    "i_load": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "i_load_error": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "i_arm_1": {"addr": 35, "format": "f", "size": 4, "egu": "A"},
    "i_arm_2": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "i_arms_diff": {"addr": 37, "format": "f", "size": 4, "egu": "A"},
    "v_capbank_1": {"addr": 38, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_2": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "duty_cycle_1": {"addr": 40, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_2": {"addr": 41, "format": "f", "size": 4, "egu": "p.u."},
    "duty_diff": {"addr": 42, "format": "f", "size": 4, "egu": "p.u."},
}

bsmp_2p4s_acdc = {
    "v_capacitor_bank": {"addr": 33, "format": "f", "size": 4, "egu": "V"},
    "i_out_rectifier": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "duty_cycle": {"addr": 35, "format": "f", "size": 4, "egu": "p.u."},
    "i_input_is_iib": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "v_input_is_iib": {"addr": 37, "format": "f", "size": 4, "egu": "V"},
    "temp_igbt_is_iib": {"addr": 38, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_is_iib": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "i_driver_is_iib": {"addr": 40, "format": "f", "size": 4, "egu": "A"},
    "temp_inductor_is_iib": {"addr": 41, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_is_iib": {"addr": 42, "format": "f", "size": 4, "egu": "°C"},
    "temp_board_is_iib": {"addr": 43, "format": "f", "size": 4, "egu": "°C"},
    "rh_is_iib": {"addr": 44, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_is": {"addr": 45, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_is": {"addr": 46, "format": "I", "size": 4, "egu": ""},
    "v_output_cmd_iib": {"addr": 47, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_cmd_iib": {"addr": 48, "format": "f", "size": 4, "egu": "V"},
    "temp_rect_inductor_cmd_iib": {"addr": 49, "format": "f", "size": 4, "egu": "°C"},
    "temp_rect_heatsink_cmd_iib": {"addr": 50, "format": "f", "size": 4, "egu": "°C"},
    "v_ext_boards_cmd_iib": {"addr": 51, "format": "f", "size": 4, "egu": "V"},
    "i_aux_board_cmd_iib": {"addr": 52, "format": "f", "size": 4, "egu": "A"},
    "i_idb_board_cmd_iib": {"addr": 53, "format": "f", "size": 4, "egu": "A"},
    "i_leakage_cmd_iib": {"addr": 54, "format": "f", "size": 4, "egu": "A"},
    "temp_board_cmd_iib": {"addr": 55, "format": "f", "size": 4, "egu": "°C"},
    "rh_cmd_iib": {"addr": 56, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_cmd": {"addr": 57, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_cmd": {"addr": 58, "format": "I", "size": 4, "egu": ""},
}

bsmp_2p4s_dcdc = {
    "i_load_mean": {"addr": 33, "format": "f", "size": 4, "egu": "A"},
    "i_load1": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "i_load2": {"addr": 35, "format": "f", "size": 4, "egu": "A"},
    "i_arm_1": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "i_arm_2": {"addr": 37, "format": "f", "size": 4, "egu": "A"},
    "v_capbank_1": {"addr": 38, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_2": {"addr": 39, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_3": {"addr": 40, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_4": {"addr": 41, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_5": {"addr": 42, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_6": {"addr": 43, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_7": {"addr": 44, "format": "f", "size": 4, "egu": "V"},
    "v_capbank_8": {"addr": 45, "format": "f", "size": 4, "egu": "V"},
    "duty_cycle_1": {"addr": 46, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_2": {"addr": 47, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_3": {"addr": 48, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_4": {"addr": 49, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_5": {"addr": 50, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_6": {"addr": 51, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_7": {"addr": 52, "format": "f", "size": 4, "egu": "p.u."},
    "duty_cycle_8": {"addr": 53, "format": "f", "size": 4, "egu": "p.u."},
    "v_input_iib_a": {"addr": 54, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib_a": {"addr": 55, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib_a": {"addr": 56, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib_a": {"addr": 57, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib_a": {"addr": 58, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib_a": {"addr": 59, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib_a": {"addr": 60, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib_a": {"addr": 61, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib_a": {"addr": 62, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib_a": {"addr": 63, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib_a": {"addr": 64, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib_a": {"addr": 65, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_a": {"addr": 66, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_a": {"addr": 67, "format": "I", "size": 4, "egu": ""},
    "v_input_iib_b": {"addr": 68, "format": "f", "size": 4, "egu": "V"},
    "i_input_iib_b": {"addr": 69, "format": "f", "size": 4, "egu": "A"},
    "i_output_iib_b": {"addr": 70, "format": "f", "size": 4, "egu": "A"},
    "temp_igbts_1_iib_b": {"addr": 71, "format": "f", "size": 4, "egu": "°C"},
    "temp_igbts_2_iib_b": {"addr": 72, "format": "f", "size": 4, "egu": "°C"},
    "temp_inductor_iib_b": {"addr": 73, "format": "f", "size": 4, "egu": "°C"},
    "temp_heatsink_iib_b": {"addr": 74, "format": "f", "size": 4, "egu": "°C"},
    "v_driver_iib_b": {"addr": 75, "format": "f", "size": 4, "egu": "V"},
    "i_driver_1_iib_b": {"addr": 76, "format": "f", "size": 4, "egu": "A"},
    "i_driver_2_iib_b": {"addr": 77, "format": "f", "size": 4, "egu": "A"},
    "temp_board_iib_b": {"addr": 78, "format": "f", "size": 4, "egu": "°C"},
    "rh_iib_b": {"addr": 79, "format": "f", "size": 4, "egu": "%"},
    "iib_interlocks_b": {"addr": 80, "format": "I", "size": 4, "egu": ""},
    "iib_alarms_b": {"addr": 81, "format": "I", "size": 4, "egu": ""},
    "ps_alarms": {"addr": 82, "format": "I", "size": 4, "egu": ""},
}
