#!/usr/bin/env python3
"""The core for pydrs, from which all child classes are based"""
import csv
import math
import os
import struct
import time
from typing import Union

from .consts import (
    COM_CREATE_BSMP_GROUP,
    COM_FUNCTION,
    COM_GET_BSMP_GROUP_LIST,
    COM_GET_BSMP_GROUP_VARS,
    COM_READ_BSMP_GROUP_VALUES,
    COM_READ_VAR,
    COM_REQUEST_CURVE,
    COM_SEND_WFM_REF,
    COM_WRITE_VAR,
    DP_MODULE_MAX_COEFF,
    NUM_MAX_COEFFS_DSP,
    WRITE_DOUBLE_SIZE_PAYLOAD,
    WRITE_FLOAT_SIZE_PAYLOAD,
    common,
    dsp_classes_names,
    fac,
    fap,
    fbp,
    num_blocks_curves_fax,
    num_blocks_curves_fbp,
    num_coeffs_dsp_modules,
    num_dsp_modules,
    size_curve_block,
    type_format,
    type_size,
)
from .utils import (
    double_to_hex,
    float_list_to_hex,
    float_to_hex,
    format_list_size,
    get_logger,
    index_to_hex,
    size_to_hex,
    uint32_to_hex,
)
from .validation import SerialError, SerialErrPckgLen, SerialInvalidCmd

logger = get_logger(name=__file__)


class BaseDRS:
    """Base class, originates all communication child classes"""

    def __init__(self):
        self.slave_addr = 1
        self.var_group_index: int = None

        self.vars_size_cache = {}

    def __exit__(self, _, _1, _2):
        self.disconnect()

    def connect(self):
        """Creates communication bus object and connects"""
        pass

    def disconnect(self):
        """Disconnects current communication bus"""
        pass

    def is_open(self) -> bool:
        """Returns whether or not the current communication bus is open (or equivalent terminology)"""
        pass

    def _transfer(self, msg: str, size: int) -> bytes:
        """Sends then receives data from target DRS device."""
        return b""

    def _transfer_write(self, msg: str):
        """Transfers data to target DRS device"""
        pass

    def reset_input_buffer(self):
        """Resets input buffer for the given communication protocol"""
        pass

    @property
    def timeout(self) -> float:
        """Communication bus timeout"""
        pass

    @timeout.setter
    def timeout(self, new_timeout: float):
        pass

    @property
    def slave_addr(self) -> int:
        """Power supply address in the serial network"""
        return struct.unpack("B", self._slave_addr.encode())[0]

    @slave_addr.setter
    def slave_addr(self, address: int):
        self._slave_addr = struct.pack("B", address).decode("ISO-8859-1")

    def read_var(self, var_id: str, size: int) -> bytes:
        """Reads a variable with a given ID

        Parameters
        -------
        var_id
            Variable ID
        size
            Variable size

        Returns
        -------
        bytes
            Raw variable response"""
        self.reset_input_buffer()
        return self._transfer(COM_READ_VAR + var_id, size)

    # BSMP entity calls

    def _create_bsmp_group(self, group: list) -> bytes:
        """Creates BSMP group from the variables described in `group`

        Parameters
        -------
        group
            List of variables to include in new group

        Returns
        -------
        bytes
            UDC response"""
        str_group = "".join(f"{index_to_hex(i)}" for i in group)
        return self._transfer(
            f"{COM_CREATE_BSMP_GROUP}{size_to_hex(len(group))}{str_group}", 5
        )

    def _get_bsmp_groups(self) -> list:
        """Gets list of BSMP variable groups with variables contained in them.

        Returns
        -------
        list
            List of variable groups, each containing all variables in the group"""
        var_group_amount = self._transfer(f"{COM_GET_BSMP_GROUP_LIST}\x00\x00", 0)[4]
        var_groups = []

        for i in range(0, var_group_amount):
            try:
                var_groups.append(self._get_bsmp_group_vars(i))
            except SerialError:
                pass

        return var_groups

    def _get_bsmp_group_vars(self, group: int) -> list:
        """Gets list of BSMP variables contained in a group

        Parameters
        -------
        group
            Variable group index

        Returns
        -------
        list
            List of variables contained in group"""
        bsmp_vars = self._transfer(
            f"{COM_GET_BSMP_GROUP_VARS}\x00\x01{index_to_hex(group)}", 0
        )
        return [i for i in bsmp_vars[4:-1]]

    def turn_on(self) -> bytes:
        """Turns on power supply

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("turn_on"))
        )
        return self._transfer(send_packet, 6)

    def turn_off(self) -> bytes:
        """Turns off power supply

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("turn_off"))
        )
        return self._transfer(send_packet, 6)

    def open_loop(self) -> bytes:
        """Opens the control loop

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("open_loop"))
        )
        return self._transfer(send_packet, 6)

    def close_loop(self) -> bytes:
        """Closes the control loop

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("closed_loop"))
        )
        return self._transfer(send_packet, 6)

    def reset_interlocks(self) -> bytes:
        """Resets interlocks on connected DRS device

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("reset_interlocks"))
        )
        return self._transfer(send_packet, 6)

    @staticmethod
    def _parse_status(status: int) -> dict:
        return {
            "state": common.op_modes[(status & 0b0000000000001111)],
            "open_loop": (status & 0b0000000000010000) >> 4,
            "interface": (status & 0b0000000001100000) >> 5,
            "active": (status & 0b0000000010000000) >> 7,
            "model": common.ps_models[(status & 0b0001111100000000) >> 8],
            "unlocked": (status & 0b0010000000000000) >> 13,
        }

    def read_ps_status(self) -> dict:
        """Gets power supply status

        Returns
        -------
        dict
            Containing `state`, `open_loop` (whether control loop is open), `interface`, `active`, power supply `model`, `unlocked` (represents UDC lock status)"""
        reply_msg = self.read_var(index_to_hex(common.vars.index("ps_status")), 7)
        val = struct.unpack("BBHHB", reply_msg)
        return self._parse_status(val[3])

    def set_ps_name(self, ps_name: str):
        """Sets power supply name

        Parameters
        -------
        ps_name
            New power supply name"""
        for n in range(len(ps_name)):
            self.set_param("PS_Name", n, float(ord(ps_name[n])))
        for i in range(n + 1, 64):
            self.set_param("PS_Name", i, float(ord(" ")))

    def get_ps_name(self) -> str:
        """Gets power supply name

        Returns
        -------
        str
            Power supply name"""
        ps_name = ""
        for n in range(64):
            ps_name += chr(int(self.get_param("PS_Name", n)))
            if ps_name[-3:] == "   ":
                ps_name = ps_name[: n - 2]
                break
        return ps_name

    def set_slowref(self, setpoint: float) -> bytes:
        """Sets new slow reference (setpoint) value

        Parameters
        -------
        setpoint
            Slowref setpoint value

        Returns
        -------
        bytes
            UDC response
        """
        payload_size = size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = float_to_hex(setpoint)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref"))
            + hex_setpoint
        )
        return self._transfer(send_packet, 6)

    def set_slowref_fbp(
        self, iRef1: int = 0, iRef2: int = 0, iRef3: int = 0, iRef4: int = 0
    ) -> bytes:
        """Sets slowref setpoint value for FBP power supplies"""
        # TODO: Take int list instead?
        payload_size = size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = float_to_hex(iRef1)
        hex_iRef2 = float_to_hex(iRef2)
        hex_iRef3 = float_to_hex(iRef3)
        hex_iRef4 = float_to_hex(iRef4)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref_fbp"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        return self._transfer(send_packet, 6)

    def set_slowref_readback_mon(self, setpoint: float) -> bytes:
        """Sets slowref reference value and returns current readback"""
        payload_size = size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = float_to_hex(setpoint)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref_readback_mon"))
            + hex_setpoint
        )
        reply_msg = self._transfer(send_packet, 9)
        val = struct.unpack("BBHfB", reply_msg)
        return val[3]

    def set_slowref_fbp_readback_mon(
        self, iRef1: int = 0, iRef2: int = 0, iRef3: int = 0, iRef4: int = 0
    ) -> list:
        """Sets slowref reference value for FBP power supplies and returns current readback"""
        # TODO: Take int list instead?
        payload_size = size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = float_to_hex(iRef1)
        hex_iRef2 = float_to_hex(iRef2)
        hex_iRef3 = float_to_hex(iRef3)
        hex_iRef4 = float_to_hex(iRef4)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref_fbp_readback_mon"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        try:
            reply_msg = self._transfer(send_packet, 21)
            val = struct.unpack("BBHffffB", reply_msg)
            return [val[3], val[4], val[5], val[6]]
        except (SerialErrPckgLen, SerialInvalidCmd):
            return reply_msg

    def set_slowref_readback_ref(self, setpoint: float) -> float:
        """Sets slowref reference value and returns reference current"""
        payload_size = size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = float_to_hex(setpoint)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref_readback_ref"))
            + hex_setpoint
        )
        reply_msg = self._transfer(send_packet, 9)
        val = struct.unpack("BBHfB", reply_msg)
        return val[3]

    def set_slowref_fbp_readback_ref(
        self, iRef1: int = 0, iRef2: int = 0, iRef3: int = 0, iRef4: int = 0
    ) -> Union[bytes, list]:
        """Sets slowref reference value for FBP power supplies and returns reference current"""
        # TODO: Take int list instead?
        payload_size = size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = float_to_hex(iRef1)
        hex_iRef2 = float_to_hex(iRef2)
        hex_iRef3 = float_to_hex(iRef3)
        hex_iRef4 = float_to_hex(iRef4)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_slowref_fbp_readback_ref"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        try:
            reply_msg = self._transfer(send_packet, 21)
            val = struct.unpack("BBHffffB", reply_msg)
            return [val[3], val[4], val[5], val[6]]
        except (SerialErrPckgLen, SerialInvalidCmd):
            return reply_msg

    def set_param(self, param_id: Union[str, int], n: int, value: float) -> tuple:
        """Set parameter

        Parameters
        -------
        param_id
            Parameter ID either as its human readable name or BSMP ID
        n
            Index for arrays of variables
        value
            Value to set

        Returns
        -------
        tuple
            Value alongside parameter hex value"""
        # TODO: Turn into property?
        payload_size = size_to_hex(
            1 + 2 + 2 + 4
        )  # Payload: ID + param id + [n] + value
        if isinstance(param_id, str):
            hex_id = double_to_hex(common.params[param_id]["id"])
        if isinstance(param_id, int):
            hex_id = double_to_hex(param_id)
        hex_n = double_to_hex(n)
        hex_value = float_to_hex(value)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_param"))
            + hex_id
            + hex_n
            + hex_value
        )

        reply_msg = self._transfer(send_packet, 6)
        return reply_msg, hex_value

    def get_param(self, param_id: Union[int, str], n=0, return_floathex=False):
        """Get parameter

        Parameters
        -------
        param_id
            Parameter ID either as its human readable name or BSMP ID
        n
            Index for arrays of variables
        return_floathex
            Return hexadecimal representation of float alongside float value

        Returns
        -------
        list
            Value alongside reply message (if `return_floathex` is true)
        float
            Parameter value (if `return_floathex` is false)
        """
        # Payload: ID + param id + [n]
        payload_size = size_to_hex(1 + 2 + 2)
        if isinstance(param_id, str):
            hex_id = double_to_hex(common.params[param_id]["id"])
        if isinstance(param_id, int):
            hex_id = double_to_hex(param_id)
        hex_n = double_to_hex(n)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("get_param"))
            + hex_id
            + hex_n
        )
        self.reset_input_buffer()
        try:
            reply_msg = self._transfer(send_packet, 9)
            val = struct.unpack("BBHfB", reply_msg)
            if return_floathex:
                return [val[3], reply_msg[4:8]]
            else:
                return val[3]
        except SerialInvalidCmd:
            return float("nan")

    def save_param_eeprom(
        self, param_id: Union[int, str], n: int = 0, type_memory: int = 2
    ) -> bytes:
        """Save parameter to EEPROM

        Parameters
        -------
        param_id
            Parameter ID, either as its name or numeric ID
        n
            Index to save (in arrays)
        type_memory
            Type of memory to save to. 1 for BID, 2 for EEPROM.

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(
            1 + 2 + 2 + 2
        )  # Payload: ID + param id + [n] + memory type
        if isinstance(param_id, str):
            hex_id = double_to_hex(common.params[param_id]["id"])
        if isinstance(param_id, int):
            hex_id = double_to_hex(param_id)
        hex_n = double_to_hex(n)
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("save_param_eeprom"))
            + hex_id
            + hex_n
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def load_param_eeprom(
        self, param_id: str, n: int = 0, type_memory: int = 2
    ) -> bytes:
        """Load parameter from EEPROM"""
        payload_size = size_to_hex(
            1 + 2 + 2 + 2
        )  # Payload: ID + param id + [n] + memory type
        if isinstance(param_id, str):
            hex_id = double_to_hex(common.params[param_id]["id"])
        if isinstance(param_id, int):
            hex_id = double_to_hex(param_id)
        hex_n = double_to_hex(n)
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("load_param_eeprom"))
            + hex_id
            + hex_n
            + hex_type
        )
        reply_msg = self._transfer(send_packet, 6)
        return reply_msg

    def save_param_bank(self, type_memory: int = 2) -> bytes:
        """Saves all paremeter values loaded into memory to BID/EEPROM

        Parameters
        -------
        type_memory
            Memory to save to. 1 for BID, 2 for EEPROM"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("save_param_bank"))
            + hex_type
        )

        # User defined timeout is temporarily changed to a "safe" value to prevent lockups
        old_timeout = self.timeout
        self.timeout = 10
        ret = self._transfer(send_packet, 6)
        self.timeout = old_timeout
        return ret

    def load_param_bank(self, type_memory: int = 2) -> bytes:
        """Loads all parameter values from EEPROM/BID to memory

        Parameters
        -------
        type_memory
            Memory to save to. 1 for BID, 2 for EEPROM"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("load_param_bank"))
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def set_param_bank(self, param_file: str) -> list:
        """Writes content of file to parameter bank

        Parameters
        -------
        param_file
            Path to parameter bank file

        Returns
        -------
        list
            Written parameter bank values"""
        ps_param_list = {}
        with open(param_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                ps_param_list[str(row[0])] = row[1:]

        for param in ps_param_list.keys():
            if param == "PS_Name":
                # print(str(param[0]) + "[0]: " + str(param[1]))
                self.set_ps_name(str(ps_param_list[param][0]))
            else:
                for n in range(64):
                    try:
                        # print(str(param[0]) + "[" + str(n) + "]: " + str(param[n + 1]))
                        _, param_hex = self.set_param(
                            param, n, float(ps_param_list[param][n])
                        )
                        ps_param_list[param][n] = [
                            ps_param_list[param][n],
                            param_hex.encode("latin-1"),
                        ]
                    except Exception:
                        break
        return ps_param_list
        # self.save_param_bank()

    def read_csv_param_bank(self, param_csv_file: str):
        """Reads parameter bank from CSV file"""
        csv_param_list = {}
        with open(param_csv_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                csv_param_list[str(row[0])] = row[1:]

        for param in csv_param_list.keys():
            if param == "PS_Name":
                csv_param_list[param] = str(csv_param_list[param][0])
            else:
                param_values = []
                for n in range(64):
                    try:
                        param_values.append(float(csv_param_list[param][n]))
                    except Exception:
                        break
                csv_param_list[param] = param_values

        return csv_param_list

    def get_param_bank(
        self,
        list_param: list = None,
        timeout: float = 0.5,
        return_floathex: bool = False,
    ) -> list:
        """Gets parameter bank values loaded into memory

        Parameters
        -------
        list_param
            List of parameters to read (all, by default)
        timeout
            Timeout for this operation. Since this operation might take longer than usual,
            setting a different timeout is recommended
        print_modules
            Print parameter bank values
        return_floathex
            Include hexadecimal representation of floats in returned value
        """
        if list_param is None:
            list_param = common.params.keys()

        timeout_old = self.timeout
        param_bank = {}

        for param_name in list_param:
            param_row = []
            for n in range(64):
                p = None
                if param_name == "PS_Name":
                    param_row.append(self.get_ps_name())
                    self.timeout = timeout
                    break

                p = self.get_param(param_name, n, return_floathex=return_floathex)

                if not isinstance(p, list):
                    if math.isnan(p):
                        break
                param_row.append(p)
                # if(print_modules):
                # print(param_name + "[" + str(n) + "]: " + str(p))

            param_bank[param_name] = param_row

        self.timeout = timeout_old

        return param_bank

    @staticmethod
    def store_param_bank_csv(bank: dict, filename: str):
        """Saves parameter bank to CSV file

        Parameters
        -------
        bank
            Parameter bank to be stored
        filename
            Location of output file"""
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            for param, val in bank.items():
                writer.writerow([param] + [val])

    def enable_onboard_eeprom(self):
        """Enables onboard EEPROM"""
        self.set_param("Enable_Onboard_EEPROM", 0, 0)
        self.save_param_eeprom("Enable_Onboard_EEPROM", 0, 2)

    def disable_onboard_eeprom(self):
        """Disables onboard EEPROM"""
        self.set_param("Enable_Onboard_EEPROM", 0, 1)
        self.save_param_eeprom("Enable_Onboard_EEPROM", 0, 2)

    def set_dsp_coeffs(
        self,
        dsp_class: int,
        dsp_id: int,
        coeffs_list: list = None,
    ) -> bytes:
        if coeffs_list is None:
            coeffs_list = [0] * 12

        coeffs_list_full = format_list_size(coeffs_list, NUM_MAX_COEFFS_DSP)
        payload_size = size_to_hex(1 + 2 + 2 + 4 * NUM_MAX_COEFFS_DSP)
        hex_dsp_class = double_to_hex(dsp_class)
        hex_dsp_id = double_to_hex(dsp_id)
        hex_coeffs = float_list_to_hex(coeffs_list_full)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_dsp_coeffs"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_coeffs
        )
        return self._transfer(send_packet, 6), hex_coeffs[: 4 * len(coeffs_list)]

    def get_dsp_coeff(
        self, dsp_class: int, dsp_id: int, coeff: int, return_floathex=False
    ) -> Union[tuple, float]:
        """Get DSP coefficient values"""
        payload_size = size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = double_to_hex(dsp_class)
        hex_dsp_id = double_to_hex(dsp_id)
        hex_coeff = double_to_hex(coeff)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("get_dsp_coeff"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_coeff
        )
        self.reset_input_buffer()
        reply_msg = self._transfer(send_packet, 9)
        val = struct.unpack("BBHfB", reply_msg)

        if return_floathex:
            return val[3], reply_msg[4:8]

        return val[3]

    def save_dsp_coeffs_eeprom(
        self, dsp_class: int, dsp_id: int, type_memory: int = 2
    ) -> bytes:
        """Save DSP coefficients to EEPROM"""
        payload_size = size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = double_to_hex(dsp_class)
        hex_dsp_id = double_to_hex(dsp_id)
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("save_dsp_coeffs_eeprom"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def load_dsp_coeffs_eeprom(
        self, dsp_class: int, dsp_id: int, type_memory: int = 2
    ) -> bytes:
        """Load DSP coefficient values from EEPROM into memory"""
        payload_size = size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = double_to_hex(dsp_class)
        hex_dsp_id = double_to_hex(dsp_id)
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("load_dsp_coeffs_eeprom"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def save_dsp_modules_eeprom(self, type_memory: int = 2) -> bytes:
        """Save DSP module configuration to EEPROM"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("save_dsp_modules_eeprom"))
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def load_dsp_modules_eeprom(self, type_memory: int = 2) -> bytes:
        """Loads DSP modules from EEPROM to memory"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = double_to_hex(type_memory)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("load_dsp_modules_eeprom"))
            + hex_type
        )
        return self._transfer(send_packet, 6)

    def reset_udc(self):
        """Resets UDC"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("reset_udc"))
        )
        try:
            self._transfer_write(send_packet)
        except SerialErrPckgLen:
            return

    def run_bsmp_func(self, id_func: int) -> bytes:
        """Runs a given BSMP function

        Parameters
        -------
        id_func
            Numeric ID for BSMP function

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = COM_FUNCTION + payload_size + index_to_hex(id_func)
        return self._transfer(send_packet, 6)

    def run_bsmp_func_all_ps(
        self,
        p_func,
        add_list: list,
        arg=None,
        delay: float = 0.5,
        print_reply: bool = True,
    ):
        old_add = self.slave_addr
        for add in add_list:
            self.slave_addr = add
            if arg is None:
                r = p_func()
            else:
                r = p_func(arg)
            if print_reply:
                print("\n Add " + str(add))
                print(r)
            time.sleep(delay)
        self.slave_addr = old_add

    def cfg_source_scope(self, p_source: int) -> bytes:
        payload_size = size_to_hex(1 + 4)  # Payload: ID + p_source
        hex_op_mode = uint32_to_hex(p_source)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("cfg_source_scope"))
            + hex_op_mode
        )
        return self._transfer(send_packet, 6)

    def cfg_freq_scope(self, freq: float) -> bytes:
        payload_size = size_to_hex(1 + 4)  # Payload: ID + freq
        hex_op_mode = float_to_hex(freq)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("cfg_freq_scope"))
            + hex_op_mode
        )
        return self._transfer(send_packet, 6)

    def cfg_duration_scope(self, duration: float) -> bytes:
        payload_size = size_to_hex(1 + 4)  # Payload: ID + duration
        hex_op_mode = float_to_hex(duration)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("cfg_duration_scope"))
            + hex_op_mode
        )
        return self._transfer(send_packet, 6)

    def enable_scope(self) -> bytes:
        """Enables scope

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("enable_scope"))
        )
        return self._transfer(send_packet, 6)

    def disable_scope(self) -> bytes:
        """Disables scope

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("disable_scope"))
        )
        return self._transfer(send_packet, 6)

    def get_scope_vars(self) -> dict:
        return {
            "frequency": self.read_bsmp_variable(25, "float"),
            "duration": self.read_bsmp_variable(26, "float"),
            "source_data": self.read_bsmp_variable(27, "uint32_t"),
        }

    def sync_pulse(self) -> bytes:
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("sync_pulse"))
        )
        return self._transfer(send_packet, 6)

    def select_op_mode(self, op_mode: int) -> bytes:
        """Select operation mode

        Parameters
        -------
        op_mode
            Operation mode (check BSMP specification for power supplies for more information)

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + enable
        hex_op_mode = double_to_hex(common.op_modes.index(op_mode))
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("select_op_mode"))
            + hex_op_mode
        )
        return self._transfer(send_packet, 6)

    def set_serial_termination(self, term_enable: int) -> bytes:
        """Set serial termination state"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + enable
        hex_enable = double_to_hex(term_enable)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_serial_termination"))
            + hex_enable
        )
        return self._transfer(send_packet, 6)

    def set_command_interface(self, interface: int) -> bytes:
        payload_size = size_to_hex(1 + 2)  # Payload: ID + enable
        hex_interface = double_to_hex(interface)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_command_interface"))
            + hex_interface
        )
        return self._transfer(send_packet, 6)

    def unlock_udc(self, password: int) -> bytes:
        """Unlocks UDC, enables password protected commands to be ran

        Parameters
        -------
        password
            Password

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + password
        hex_password = double_to_hex(password)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("unlock_udc"))
            + hex_password
        )
        return self._transfer(send_packet, 6)

    def lock_udc(self, password: int) -> bytes:
        """Locks UDC, disables password protected commands

        Parameters
        -------
        password
            Password

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + password
        hex_password = double_to_hex(password)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("lock_udc"))
            + hex_password
        )
        return self._transfer(send_packet, 6)

    def reset_counters(self) -> bytes:
        """Resets counters"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("reset_counters"))
        )
        return self._transfer(send_packet, 6)

    def cfg_siggen(
        self,
        sig_type: int,
        num_cycles: int,
        freq: float,
        amplitude: float,
        offset: float,
        aux0: float,
        aux1: float,
        aux2: float,
        aux3: float,
    ) -> bytes:
        """"""
        # TODO: take aux as list?
        payload_size = size_to_hex(1 + 2 + 2 + 4 + 4 + 4 + 4 * 4)
        hex_sig_type = double_to_hex(common.sig_gen_types.index(sig_type))
        hex_num_cycles = double_to_hex(num_cycles)
        hex_freq = float_to_hex(freq)
        hex_amplitude = float_to_hex(amplitude)
        hex_offset = float_to_hex(offset)
        hex_aux0 = float_to_hex(aux0)
        hex_aux1 = float_to_hex(aux1)
        hex_aux2 = float_to_hex(aux2)
        hex_aux3 = float_to_hex(aux3)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("cfg_siggen"))
            + hex_sig_type
            + hex_num_cycles
            + hex_freq
            + hex_amplitude
            + hex_offset
            + hex_aux0
            + hex_aux1
            + hex_aux2
            + hex_aux3
        )
        return self._transfer(send_packet, 6)

    def set_siggen(self, freq: float, amplitude: float, offset: float) -> bytes:
        """Updates signal generator parameters in continuous operation.
        Amplitude and offset are updated instantaneously, frequency is
        updated on the next 1 second update cycle. *This function cannot be
        applied in trapezoidal mode.

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1 + 4 + 4 + 4)
        hex_freq = float_to_hex(freq)
        hex_amplitude = float_to_hex(amplitude)
        hex_offset = float_to_hex(offset)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("set_siggen"))
            + hex_freq
            + hex_amplitude
            + hex_offset
        )
        return self._transfer(send_packet, 6)

    def enable_siggen(self) -> bytes:
        """Enables signal generator

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("enable_siggen"))
        )
        return self._transfer(send_packet, 6)

    def disable_siggen(self) -> bytes:
        """Disables signal generator

        Returns
        -------
        bytes
            UDC response"""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("disable_siggen"))
        )
        return self._transfer(send_packet, 6)

    def cfg_wfmref(
        self,
        idx: int,
        sync_mode: int,
        frequency: float,
        gain: float = 1.0,
        offset: int = 0,
    ) -> bytes:
        """"""
        payload_size = size_to_hex(
            1 + 2 + 2 + 4 + 4 + 4
        )  # Payload: ID + idx + sync_mode + frequency + gain + offset
        hex_idx = double_to_hex(idx)
        hex_mode = double_to_hex(sync_mode)
        hex_freq = float_to_hex(frequency)
        hex_gain = float_to_hex(gain)
        hex_offset = float_to_hex(offset)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("cfg_wfmref"))
            + hex_idx
            + hex_mode
            + hex_freq
            + hex_gain
            + hex_offset
        )
        return self._transfer(send_packet, 6)

    def select_wfmref(self, idx: int) -> bytes:
        """Selects index in current waveform, loads waveform into
        wfmref_data."""
        payload_size = size_to_hex(1 + 2)  # Payload: ID + idx
        hex_idx = double_to_hex(idx)
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("select_wfmref"))
            + hex_idx
        )
        return self._transfer(send_packet, 6)

    def reset_wfmref(self) -> bytes:
        """Resets WfmRef, next sync pulse takes index back to the
        waveform's start."""
        payload_size = size_to_hex(1)  # Payload: ID
        send_packet = (
            COM_FUNCTION
            + payload_size
            + index_to_hex(common.functions.index("reset_wfmref"))
        )
        return self._transfer(send_packet, 6)

    def get_wfmref_vars(self, curve_id: int):
        return {
            "curve_id": curve_id,
            "length": (
                self.read_bsmp_variable(20 + curve_id * 3, "uint32_t")
                - self.read_bsmp_variable(19 + curve_id * 3, "uint32_t")
            )
            / 2
            + 1,
            "index": (
                self.read_bsmp_variable(21 + curve_id * 3, "uint32_t")
                - self.read_bsmp_variable(19 + curve_id * 3, "uint32_t")
            )
            / 2
            + 1,
            "wfmref_selected": self.read_bsmp_variable(14, "uint16_t"),
            "sync_mode": self.read_bsmp_variable(15, "uint16_t"),
            "frequency": self.read_bsmp_variable(16, "float"),
            "gain": self.read_bsmp_variable(17, "float"),
            "offset": self.read_bsmp_variable(18, "float"),
        }

    @staticmethod
    def store_dsp_modules_bank_csv(bank: dict, filename: str):
        """Saves DSP parameter bank to CSV file

        Parameters
        -------
        bank
            Parameter bank to be stored
        filename
            Output filename
        """
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            for dsp_module, values in bank.items():
                for i, coef in enumerate(values["coeffs"]):
                    writer.writerow([dsp_module, values["class"], i] + coef)

    def read_csv_file(self, filename: str, type: str = "float") -> list:
        """Utility function to translate CSV file to list

        Parameters
        -------
        filename
            File location
        type
            Type to consider for the variables in the file, determines whether or not a parsed float or a string is returned in the list

        Returns
        -------
        list
            List of rows
        """
        csv_list = []
        with open(filename, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if type == "float":
                    row_converted = float(row[0])
                elif type in ("string", "str"):
                    row_converted = str(row[0])
                csv_list.append(row_converted)
        return csv_list

    """
    ======================================================================
                Métodos de Leitura de Valores das Variáveis BSMP
    O retorno do método são os valores double/float da respectiva variavel
    ======================================================================
    """

    def read_bsmp_variable(self, id_var: int, type_var: str) -> Union[float, int]:
        """Reads a BSMP variable

        Parameters
        -------
        id_var
            Variable's numeric ID
        type_var
            Type of variable to read (float, uint8_t, uint16_t, uint32_t)

        Returns
        -------
        float
            Variable value (if given type was float)
        int
            Variable value (if given type was an integer of any length)
        """
        reply_msg = self.read_var(index_to_hex(id_var), type_size[type_var])
        val = struct.unpack(type_format[type_var], reply_msg)
        return val[3]

    def read_bsmp_variable_gen(self, id_var: int, size_bytes: int) -> bytes:
        return self.read_var(index_to_hex(id_var), size_bytes + 5)

    def read_udc_arm_version(self) -> str:
        reply_msg = self.read_var(index_to_hex(3), 133)
        val = struct.unpack("16s", reply_msg[4:20])
        return val[0].decode("utf-8")

    def read_udc_c28_version(self) -> str:
        reply_msg = self.read_var(index_to_hex(3), 133)
        val = struct.unpack("16s", reply_msg[20:36])
        return val[0].decode("utf-8")

    def read_udc_version(self) -> dict:
        """Gets UDC's ARM and DSP firmware version

        Returns
        -------
        dict
            Dictionary containing both ARM and DSP firmware versions"""
        return {"arm": self.read_udc_arm_version(), "c28": self.read_udc_c28_version()}

    """
    ======================================================================
                Métodos de Escrita de Valores das Variáveis BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    """

    def Write_sigGen_Freq(self, float_value):
        # TODO: Fix method name
        hex_float = float_to_hex(float_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_FLOAT_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("sigGen_Freq"))
            + hex_float
        )
        return self._transfer(send_packet, 5)

    def Write_sigGen_Amplitude(self, float_value):
        # TODO: Fix method name
        hex_float = float_to_hex(float_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_FLOAT_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("sigGen_Amplitude"))
            + hex_float
        )
        return self._transfer(send_packet, 5)

    def Write_sigGen_Offset(self, float_value):
        # TODO: Fix method name
        hex_float = float_to_hex(float_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_FLOAT_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("sigGen_Offset"))
            + hex_float
        )
        return self._transfer(send_packet, 5)

    def Write_sigGen_Aux(self, float_value):
        # TODO: Fix method name
        hex_float = float_to_hex(float_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_FLOAT_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("sigGen_Aux"))
            + hex_float
        )
        return self._transfer(send_packet, 5)

    def Write_dp_ID(self, double_value):
        # TODO: Fix method name
        hex_double = double_to_hex(double_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_DOUBLE_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("dp_ID"))
            + hex_double
        )
        return self._transfer(send_packet, 5)

    def Write_dp_Class(self, double_value):
        # TODO: Fix method name
        hex_double = double_to_hex(double_value)
        send_packet = (
            COM_WRITE_VAR
            + WRITE_DOUBLE_SIZE_PAYLOAD
            + index_to_hex(common.vars.index("dp_Class"))
            + hex_double
        )
        return self._transfer(send_packet, 5)

    def Write_dp_Coeffs(self, list_float):
        # TODO: Fix method name
        hex_float_list = []
        # list_full = list_float[:]

        # while(len(list_full) < self.dp_module_max_coeff):
        #    list_full.append(0)

        list_full = [0 for i in range(DP_MODULE_MAX_COEFF)]
        list_full[: len(list_float)] = list_float[:]

        for float_value in list_full:
            hex_float = float_to_hex(float(float_value))
            hex_float_list.append(hex_float)
        str_float_list = "".join(hex_float_list)
        payload_size = size_to_hex(
            1 + 4 * DP_MODULE_MAX_COEFF
        )  # Payload: ID + 16floats
        send_packet = (
            COM_WRITE_VAR
            + payload_size
            + index_to_hex(common.vars.index("dp_Coeffs"))
            + str_float_list
        )
        return self._transfer(send_packet, 5)

    # Methods for writing curves

    def send_wfmref_curve(self, block_idx: int, data) -> bytes:
        # TODO: Could use list comprehension in val
        block_hex = size_to_hex(block_idx)
        val = []
        for k in range(0, len(data)):
            val.append(float_to_hex(float(data[k])))
        payload_size = size_to_hex((len(val) * 4) + 3)
        curve_hex = "".join(val)
        send_packet = (
            COM_SEND_WFM_REF
            + payload_size
            + index_to_hex(common.curves.index("wfmRef_Curve"))
            + block_hex
            + curve_hex
        )
        return self._transfer(send_packet, 5)

    def recv_wfmref_curve(self, block_idx: int) -> list:
        # TODO: Will always fail, wfmRef_Curve is not in list
        block_hex = size_to_hex(block_idx)
        payload_size = size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            COM_REQUEST_CURVE
            + payload_size
            + index_to_hex(common.curves.index("wfmRef_Curve"))
            + block_hex
        )
        # Address+Command+Size+ID+Block_idx+data+checksum
        recv_msg = self._transfer(send_packet, 1 + 1 + 2 + 1 + 2 + 8192 + 1)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.append(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer(self) -> list:
        raise NotImplementedError
        """
        # TODO: Will always fail, samplesBuffer is not in list
        block_hex = size_to_hex(0)
        payload_size = size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            COM_REQUEST_CURVE
            + payload_size
            + index_to_hex(common.curves.index("samplesBuffer"))
            + block_hex
        )
        # Address+Command+Size+ID+Block_idx+data+checksum
        recv_msg = self._transfer(send_packet, 1 + 1 + 2 + 1 + 2 + 16384 + 1)
        val = []
        try:
            for k in range(7, len(recv_msg) - 1, 4):
                val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        except Exception:
            pass
        """

    def send_full_wfmref_curve(self, block_idx: int, data) -> bytes:
        # TODO: Will always fail, fullwfmRef_Curve is not in list
        raise NotImplementedError
        block_hex = size_to_hex(block_idx)
        val = []
        for k in range(0, len(data)):
            val.append(float_to_hex(float(data[k])))
        payload_size = size_to_hex(len(val) * 4 + 3)
        curve_hex = "".join(val)
        send_packet = (
            COM_SEND_WFM_REF
            + payload_size
            + index_to_hex(common.curves.index("fullwfmRef_Curve"))
            + block_hex
            + curve_hex
        )
        return self._transfer(send_packet, 5)

    def recv_full_wfmref_curve(self, block_idx: int) -> list:
        # TODO: Will always fail, fullwfmRef_Curve is not in list
        raise NotImplementedError
        block_hex = size_to_hex(block_idx)
        payload_size = size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            COM_REQUEST_CURVE
            + payload_size
            + index_to_hex(common.curves.index("fullwfmRef_Curve"))
            + block_hex
        )
        recv_msg = self._transfer(send_packet, 1 + 1 + 2 + 1 + 2 + 16384 + 1)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.append(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer_blocks(self, block_idx: int) -> list:
        # TODO: Will always fail, samplesBuffer_blocks is not in list
        raise NotImplementedError
        block_hex = size_to_hex(block_idx)
        payload_size = size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            COM_REQUEST_CURVE
            + payload_size
            + index_to_hex(common.curves.index("samplesBuffer_blocks"))
            + block_hex
        )
        # t0 = time.time()
        # Address+Command+Size+ID+Block_idx+data+checksum
        recv_msg = self._transfer(send_packet, 1 + 1 + 2 + 1 + 2 + 1024 + 1)
        # print(time.time()-t0)
        # print(recv_msg)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer_allblocks(self) -> list:
        # TODO: Will fail
        raise NotImplementedError
        buff = []
        # self.DisableSamplesBuffer()
        for i in range(0, 16):
            # t0 = time.time()
            buff.extend(self.recv_samples_buffer_blocks(i))
            # print(time.time()-t0)
        # self.EnableSamplesBuffer()
        return buff

    def read_curve_block(self, curve_id: int, block_id: int) -> list:
        block_hex = size_to_hex(block_id)
        payload_size = size_to_hex(1 + 2)  # Payload: curve_id + block_id
        send_packet = (
            COM_REQUEST_CURVE + payload_size + index_to_hex(curve_id) + block_hex
        )
        # t0 = time.time()
        self.reset_input_buffer()
        # Address+Command+Size+ID+Block_idx+data+checksum
        recv_msg = self._transfer(
            send_packet, 1 + 1 + 2 + 1 + 2 + size_curve_block[curve_id] + 1
        )
        # print(time.time()-t0)
        # print(recv_msg)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def write_curve_block(self, curve_id: int, block_id: int, data) -> bytes:
        block_hex = size_to_hex(block_id)
        val = []
        for k in range(0, len(data)):
            val.append(float_to_hex(float(data[k])))
        payload_size = size_to_hex(len(val) * 4 + 3)
        curve_hex = "".join(val)
        send_packet = (
            COM_SEND_WFM_REF
            + payload_size
            + index_to_hex(curve_id)
            + block_hex
            + curve_hex
        )
        return self._transfer(send_packet, 5)

    def write_wfmref(self, curve: int, data) -> list:
        # curve = list_curv.index('wfmref')
        block_size = int(size_curve_block[curve] / 4)
        # print(block_size)

        blocks = [data[x : x + block_size] for x in range(0, len(data), block_size)]

        ps_status = self.read_ps_status()

        wfmref_selected = self.read_bsmp_variable(14, "uint16_t")

        if (wfmref_selected == curve) and (
            ps_status["state"] == "RmpWfm" or ps_status["state"] == "MigWfm"
        ):
            raise RuntimeError(
                "The specified curve ID is currently selected and PS is on {} state. Choose a different curve ID.".format(
                    ps_status["state"]
                )
            )

        for block_id in range(len(blocks)):
            self.write_curve_block(curve, block_id, blocks[block_id])

        return blocks

    def read_buf_samples_ctom(self) -> list:
        buf = []
        curve_id = common.curves.index("buf_samples_ctom")

        ps_status = self.read_ps_status()
        if ps_status["model"] == "FBP":
            for i in range(num_blocks_curves_fbp[curve_id]):
                buf.extend(self.read_curve_block(curve_id, i))
        else:
            for i in range(num_blocks_curves_fax[curve_id]):
                buf.extend(self.read_curve_block(curve_id, i))

        return buf

    # Auxiliary functions

    def _parse_vars(self, data: bytes, template: dict) -> dict:
        vars_dict = {}
        index = 0

        for key, var in template.items():
            try:
                val = f"{round(struct.unpack(var['format'], data[index:index+var['size']])[0], 3)} {var['egu']}"
            except TypeError:
                val = struct.unpack(var["format"], data[index : index + var["size"]])[0]
            vars_dict[key] = val
            index += var["size"]

        return vars_dict

    def read_vars_common(self, vals: bytes = None) -> dict:
        """Reads common variables for all power supplies

        Parameters
        -------
        vals
            Bytes read from power supply (useful for caching, preventing redundant reads)

        Returns
        -------
        dict
            Dictionary containing common variables"""
        if vals is None:
            vals = self._transfer(
                f"{COM_READ_BSMP_GROUP_VALUES}\x00\x01{index_to_hex(1)}",
                0,
            )[4:]

            if len(vals) < 246:
                raise SerialErrPckgLen(
                    f"Expected at least 246 bytes, received {len(vals)}"
                )
        vars_dict = self._parse_vars(vals, common.bsmp)
        vars_dict["status"] = self._parse_status(int(vars_dict["ps_status"]))

        if vars_dict["status"]["open_loop"] == 0:
            if (
                (vars_dict["status"]["model"] == "FAC_ACDC")
                or (vars_dict["status"]["model"] == "FAC_2S_ACDC")
                or (vars_dict["status"]["model"] == "FAC_2P4S_ACDC")
            ):
                vars_dict["ps_setpoint"] = vars_dict["ps_setpoint"][:-1] + "V"
                vars_dict["ps_reference"] = vars_dict["ps_reference"][:-1] + "V"
        else:
            vars_dict["ps_setpoint"] = vars_dict["ps_setpoint"][:-1] + "%"
            vars_dict["ps_reference"] = vars_dict["ps_reference"][:-1] + "%"

        vars_dict["siggen_type"] = common.sig_gen_types[int(vars_dict["siggen_type"])]
        vars_dict["wfmref_sync_mode"] = common.wfmref_sync_modes[
            int(vars_dict["wfmref_sync_mode"])
        ]
        vars_dict["version"] = {}

        for i, version in enumerate(common.versions):
            var_str = vars_dict["firmware_version"][i * 16 : (i + 1) * 16]

            if b"\x00" in var_str:
                continue

            vars_dict["version"][version] = var_str.decode("UTF-8")
        del vars_dict["firmware_version"]

        return vars_dict

    def _interlock_unknown_assignment(self, active_interlocks, index):
        active_interlocks.append(f"bit {index}: Reserved")

    def _interlock_name_assigned(self, active_interlocks, index, list_interlocks):
        active_interlocks.append(f"bit {index}: {list_interlocks[index]}")

    def _decode_all_interlocks(self, interlocks: list, soft: list, hard: list) -> dict:
        interlocks = [struct.unpack("I", i)[0] for i in interlocks]

        return {
            "soft_interlocks": self.decode_interlocks(interlocks[0], soft),
            "hard_interlocks": self.decode_interlocks(interlocks[1], hard),
        }

    def decode_interlocks(
        self, reg_interlocks: Union[int, str], list_interlocks: list
    ) -> list:
        """Decodes interlocks from a raw interlock readout value

        Parameters
        -------
        reg_interlocks
            Raw interlock value
        list_interlocks
            List mapping each interlock bit to an interlock message

        Returns
        -------
        list
            List of interlocks"""

        active_interlocks = []

        if isinstance(reg_interlocks, str):
            reg_interlocks = int(reg_interlocks)

        if not reg_interlocks:
            return active_interlocks

        for index in range(32):
            if reg_interlocks & (1 << index):
                if index < len(list_interlocks):
                    self._interlock_name_assigned(
                        active_interlocks, index, list_interlocks
                    )
                else:
                    self._interlock_unknown_assignment(active_interlocks, index)

        return active_interlocks

    def _read_vars_generic(
        self, template: dict, soft_ilocks: list, hard_ilocks: list, length: int = None
    ) -> dict:
        index = 0
        if length is None:
            length = 255 + sum([data["size"] for data in template.values()])

        # Dynamically obtaining transfer sizes incurs a 70 uS penalty per execution

        vals = self._transfer(
            f"{COM_READ_BSMP_GROUP_VALUES}\x00\x01{index_to_hex(1)}",
            length,
        )

        # 1 byte for checksum, 246 common variable bytes, 8 interlock bytes

        vars_dict = self.read_vars_common(vals[4:246])
        vals = vals[246:-1]

        vars_dict = {
            **vars_dict,
            **self._decode_all_interlocks(
                [vals[:4], vals[4:8]], soft_ilocks, hard_ilocks
            ),
        }

        index += 8

        return {**vars_dict, **self._parse_vars(vals[8:], template)}

    def read_vars_fbp(self) -> dict:
        """Reads FBP 2S ACDC power supply variables

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        return self._read_vars_generic(
            fbp.bsmp, fbp.soft_interlocks, fbp.hard_interlocks
        )

    def read_vars_fbp_dclink(self) -> dict:
        """Reads FBP DCLink power supply variables

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        return self._read_vars_generic(fbp.bsmp_dclink, [], fbp.dclink_hard_interlocks)

    def read_vars_fac_acdc(self, iib: bool = True) -> dict:
        """Reads FAC ACDC power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fac.bsmp_acdc,
            fac.list_acdc_soft_interlocks,
            fac.list_acdc_hard_interlocks,
        )

        if iib:
            vars_dict["iib_cmd_alarms_raw"] = vars_dict.pop("iib_alarms_cmd")
            vars_dict["iib_cmd_interlocks_raw"] = vars_dict.pop("iib_interlocks_cmd")
            vars_dict["iib_is_alarms_raw"] = vars_dict.pop("iib_alarms_is")
            vars_dict["iib_is_interlocks_raw"] = vars_dict.pop("iib_interlocks_is")

            vars_dict["iib_is_interlocks"] = self.decode_interlocks(
                vars_dict["iib_is_interlocks_raw"],
                fac.list_acdc_iib_is_interlocks,
            )

            vars_dict["iib_is_alarms"] = self.decode_interlocks(
                vars_dict["iib_is_alarms_raw"],
                fac.list_acdc_iib_is_alarms,
            )

            vars_dict["iib_cmd_interlocks"] = self.decode_interlocks(
                vars_dict["iib_cmd_interlocks_raw"],
                fac.list_acdc_iib_cmd_interlocks,
            )

            vars_dict["iib_cmd_alarms"] = self.decode_interlocks(
                vars_dict["iib_cmd_alarms_raw"],
                fac.list_acdc_iib_cmd_alarms,
            )

        return vars_dict

    def read_vars_fac_dcdc(self, iib: bool = True) -> dict:
        """Reads FAC DCDC power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fac.bsmp_dcdc,
            fac.list_dcdc_soft_interlocks,
            fac.list_dcdc_hard_interlocks,
        )

        vars_dict["wfmref_index"] = round(
            (
                float(vars_dict["p_wfmref_end_0"])
                - float(vars_dict["wfmref_offset"].split(" ")[0])
            )
            / 2
            + 1,
            3,
        )

        if iib:
            vars_dict["iib_interlocks_raw"] = vars_dict["iib_interlocks"]
            vars_dict["iib_alarms_raw"] = vars_dict["iib_alarms"]

            vars_dict["iib_interlocks"] = self.decode_interlocks(
                vars_dict["iib_interlocks_raw"],
                fac.list_dcdc_iib_interlocks,
            )

            vars_dict["iib_cmd_alarms"] = self.decode_interlocks(
                vars_dict["iib_alarms_raw"],
                fac.list_dcdc_iib_alarms,
            )

        return vars_dict

    def read_vars_fac_dcdc_ema(self, iib=False) -> dict:
        """Reads FAC DCDC EMA power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fac.bsmp_dcdc_ema,
            fac.list_dcdc_ema_soft_interlocks,
            fac.list_dcdc_ema_hard_interlocks,
        )

        if iib:
            vars_dict["iib_interlocks_raw"] = vars_dict["iib_interlocks"]
            vars_dict["iib_alarms_raw"] = vars_dict["iib_alarms"]

            vars_dict["iib_interlocks"] = self.decode_interlocks(
                vars_dict["iib_interlocks_raw"],
                fac.list_dcdc_ema_iib_interlocks,
            )

            vars_dict["iib_alarms"] = self.decode_interlocks(
                vars_dict["iib_alarms_raw"],
                fac.list_dcdc_ema_iib_alarms,
            )

        return vars_dict

    def _read_fac_2s_acdc_module(self, iib: bool) -> dict:
        vars_dict = self._read_vars_generic(
            fac.bsmp_2s_acdc,
            fac.list_2s_acdc_soft_interlocks,
            fac.list_2s_acdc_hard_interlocks,
            399,
        )

        if iib:
            vars_dict["iib_cmd_alarms_raw"] = vars_dict.pop("iib_alarms_cmd")
            vars_dict["iib_cmd_interlocks_raw"] = vars_dict.pop("iib_interlocks_cmd")
            vars_dict["iib_is_alarms_raw"] = vars_dict.pop("iib_alarms_is")
            vars_dict["iib_is_interlocks_raw"] = vars_dict.pop("iib_interlocks_is")

            vars_dict["iib_is_interlocks"] = self.decode_interlocks(
                vars_dict["iib_is_interlocks_raw"],
                fac.list_2s_acdc_iib_is_interlocks,
            )

            vars_dict["iib_is_alarms"] = self.decode_interlocks(
                vars_dict["iib_is_alarms_raw"], fac.list_2s_acdc_iib_is_alarms
            )

            vars_dict["iib_cmd_interlocks"] = self.decode_interlocks(
                vars_dict["iib_cmd_interlocks_raw"],
                fac.list_2s_acdc_iib_cmd_interlocks,
            )

            vars_dict["iib_cmd_alarms"] = self.decode_interlocks(
                vars_dict["iib_cmd_alarms_raw"], fac.list_2s_acdc_iib_cmd_alarms
            )

        return vars_dict

    def read_vars_fac_2s_acdc(self, iib=False) -> dict:
        """Reads FAC 2S ACDC power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        return self._read_fac_2s_acdc_module(iib)

    def read_vars_fac_2s_dcdc(self, iib=False) -> dict:
        """Reads FAC 2S DCDC power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fac.bsmp_2s_dcdc,
            fac.list_2s_dcdc_soft_interlocks,
            fac.list_2s_dcdc_hard_interlocks,
        )

        if iib:
            for i in range(1, 2):
                vars_dict[f"iib_interlocks_{i}_raw"] = vars_dict[f"iib_interlocks_{i}"]
                vars_dict[f"iib_alarms_{i}_raw"] = vars_dict[f"iib_alarms_{i}"]

                vars_dict[f"iib_interlocks_{i}"] = self.decode_interlocks(
                    vars_dict[f"iib_interlocks_{i}_raw"],
                    fac.list_2s_dcdc_iib_interlocks,
                )

                vars_dict[f"iib_alarms_{i}"] = self.decode_interlocks(
                    vars_dict[f"iib_alarms_{i}_raw"],
                    fac.list_2s_dcdc_iib_alarms,
                )

        return vars_dict

    def read_vars_fac_2p4s_acdc(self, iib=0) -> dict:
        """Reads FAC 2P4S ACDC power supply variables (alias for `read_vars_fac_2s_acdc`)

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables

        """
        return self.read_vars_fac_2s_acdc(iib)

    def read_vars_fac_2p4s_dcdc(self) -> dict:
        """Reads FAC 2P4S DCDC power supply variables

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fac.bsmp_2p4s_dcdc,
            fac.list_2p4s_dcdc_soft_interlocks,
            fac.list_2p4s_dcdc_hard_interlocks,
        )

        for i in ["a", "b"]:
            vars_dict[f"iib_interlocks_{i}_raw"] = vars_dict[f"iib_interlocks_{i}"]
            vars_dict[f"iib_alarms_{i}_raw"] = vars_dict[f"iib_alarms_{i}"]

            vars_dict[f"iib_interlocks_{i}"] = self.decode_interlocks(
                vars_dict[f"iib_interlocks_{i}_raw"], fac.list_2p4s_dcdc_iib_interlocks
            )
            vars_dict[f"iib_alarms_{i}"] = self.decode_interlocks(
                vars_dict[f"iib_alarms_{i}_raw"], fac.list_2p4s_dcdc_iib_alarms
            )

        return vars_dict

    def read_vars_fap(self, iib=True) -> dict:
        """Reads FAP power supply variables

        Parameters
        -------
        iib
            Whether or not IIB interlocks should be parsed and returned alongside other data

        Returns
        -------
        dict
            Dictionary with power supply variables
        """
        vars_dict = self._read_vars_generic(
            fap.bsmp, fap.list_soft_interlocks, fap.list_hard_interlocks
        )

        if iib:
            vars_dict["iib_interlocks_raw"] = vars_dict["iib_interlocks"]
            vars_dict["iib_alarms_raw"] = vars_dict["iib_alarms"]

            vars_dict["iib_interlocks"] = self.decode_interlocks(
                vars_dict["iib_interlocks_raw"], fap.list_iib_interlocks
            )

            vars_dict["iib_alarms"] = self.decode_interlocks(
                vars_dict["iib_alarms_raw"], fap.list_iib_alarms
            )

        return vars_dict

    def read_vars_fap_4p(self) -> dict:
        vars_dict = self._read_vars_generic(
            fap.bsmp_4p, fap.list_4p_soft_interlocks, fap.list_4p_hard_interlocks
        )

        for i in range(1, 4):
            vars_dict[f"iib_interlocks_{i}_raw"] = vars_dict[f"iib_interlocks_{i}"]
            vars_dict[f"iib_alarms_{i}_raw"] = vars_dict[f"iib_alarms_{i}"]

            vars_dict[f"iib_interlocks_{i}"] = (
                self.decode_interlocks(
                    vars_dict[f"iib_interlocks_{i}_raw"],
                    fap.list_4p_iib_interlocks,
                ),
            )

            vars_dict[f"iib_alarms_{i}"] = self.decode_interlocks(
                vars_dict[f"iib_alarms_{i}_raw"],
                fap.list_4p_iib_alarms,
            )

        return vars_dict

    def read_vars_fap_2p2s(self) -> dict:
        vars_dict = self._read_vars_generic(
            fap.bsmp_2p2s, fap.list_2p2s_soft_interlocks, fap.list_2p2s_hard_interlocks
        )

        for i in range(1, 4):
            vars_dict[f"iib_interlocks_{i}_raw"] = vars_dict[f"iib_interlocks_{i}"]
            vars_dict[f"iib_alarms_{i}_raw"] = vars_dict[f"iib_alarms_{i}"]

            vars_dict[f"iib_interlocks_{i}"] = (
                self.decode_interlocks(
                    vars_dict[f"iib_interlocks_{i}_raw"],
                    fap.list_4p_iib_interlocks,
                ),
            )

            vars_dict[f"iib_alarms_{i}"] = self.decode_interlocks(
                vars_dict[f"iib_alarms_{i}_raw"],
                fap.list_4p_iib_alarms,
            )

        return vars_dict

    def read_vars_fap_225A(self) -> dict:
        vars_dict = {
            "load_current": f"{round(self.read_bsmp_variable(33, 'float'), 3)} A",
            "igbt_current_1": f"{round(self.read_bsmp_variable(34, 'float'), 3)} A",
            "igbt_current_2": f"{round(self.read_bsmp_variable(35, 'float'), 3)} A",
            "igbt_duty_cycle_1": f"{round(self.read_bsmp_variable(36, 'float'), 3)} %",
            "igbt_duty_cycle_2": f"{round(self.read_bsmp_variable(37, 'float'), 3)} %",
            "igbt_differential_duty_cycle": f"{round(self.read_bsmp_variable(38, 'float'), 3)} %",
        }

        vars_dict = self._include_interlocks(
            vars_dict,
            fap.list_225A_soft_interlocks,
            fap.list_225A_hard_interlocks,
        )

        return vars_dict

    def read_vars_fac_2p_acdc_imas(self) -> dict:
        """
        Read FAC 2P ACDC IMAS specific power supply variables

        Returns
        -------
        dict
            Dict containing FAC 2P ACDC IMAS variables
        """
        return self._read_vars_generic(
            fac.bsmp_2p_acdc_imas,
            fac.list_2p_acdc_imas_soft_interlocks,
            fac.list_2p_acdc_imas_hard_interlocks,
        )

    def read_vars_fac_2p_dcdc_imas(self, com_add=1) -> dict:
        """
        Read FAC 2P DCDC IMAS specific power supply variables

        Returns
        -------
        dict
            Dict containing FAC 2P DCDC IMAS variables
        """
        return self._read_vars_generic(
            fac.bsmp_2p_dcdc_imas,
            fac.list_2p_dcdc_imas_soft_interlocks,
            fac.list_2p_dcdc_imas_hard_interlocks,
        )

    def check_param_bank(self, param_file: str):
        ps_param_list = []

        # max_sampling_freq = 600000
        # c28_sysclk = 150e6

        with open(param_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                ps_param_list.append(row)

        for param in ps_param_list:
            if (str(param[0]) == "Num_PS_Modules" and param[1] > 4) or (
                str(param[0]) == "Freq_ISR_Controller" and param[1] > 6000000
            ):
                raise AttributeError(f"Invalid {param[0]} : {param[1]}. Maximum is 4")

            for n in range(64):
                try:
                    print(str(param[0]) + "[" + str(n) + "]: " + str(param[n + 1]))
                    print(self.set_param(str(param[0]), n, float(param[n + 1])))
                except Exception:
                    break

    # TODO: Fix siriuspy dependency
    """
    @staticmethod
    def get_default_ramp_waveform(
        interval=500, nrpts=4000, ti=None, fi=None, forms=None
    ):
        from siriuspy.magnet.util import get_default_ramp_waveform

        return get_default_ramp_waveform(interval, nrpts, ti, fi, forms)
    """

    @staticmethod
    def save_ramp_waveform(ramp: dict, filename: str):
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(ramp)

    @staticmethod
    def save_ramp_waveform_col(ramp: dict, filename: str):
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            for val in ramp:
                writer.writerow([val])

    def read_vars_fac_n(self):
        raise NotImplementedError

    def set_buf_samples_freq(self, fs):
        self.set_param("Freq_TimeSlicer", 1, fs)
        self.save_param_eeprom("Freq_TimeSlicer", 1)
        self.reset_udc()

    def calc_pi(self, r_load, l_load, f_bw, v_dclink, send_drs=0, dsp_id=0):
        kp = 2 * 3.1415 * f_bw * l_load / v_dclink
        ki = kp * r_load / l_load
        if send_drs:
            self.set_dsp_coeffs(3, dsp_id, [kp, ki, 0.95, -0.95])
        return {"kp": kp, "ki": ki}

    def config_dsp_modules_drs_fap_tests(self):
        kp_load = 0
        ki_load = 20.95
        kp_share = 0.000032117
        ki_share = 0.0012

        self.set_dsp_coeffs(3, 0, [kp_load, ki_load, 0.6, 0])
        self.set_dsp_coeffs(3, 1, [kp_share, ki_share, 0.0015, -0.0015])
        self.save_dsp_modules_eeprom()

    def set_prbs_sampling_freq(self, freq, type_memory):
        self.set_param("Freq_TimeSlicer", 0, freq)
        self.set_param("Freq_TimeSlicer", 1, freq)
        self.save_param_bank(type_memory)

    def get_dsp_modules_bank(
        self,
        list_dsp_classes=None,
        return_floathex=False,
    ) -> dict:
        """
        Gets DSP modules parameter bank

        Parameters
        -------
        list_dsp_classes
            List of DSP classes to get
        print_modules
            Print prettified dict to terminal
        return_floathex
            Return hexadecimal representation of float alongside float

        Returns
        -------
        dict
            Dict containing DSP modules parameter bank
        """
        if list_dsp_classes is None:
            list_dsp_classes = [1, 2, 3, 4, 5, 6]

        dsp_modules_bank = {}
        for dsp_class in list_dsp_classes:
            dsp_modules_bank[dsp_classes_names[dsp_class]] = {
                "class": dsp_class,
                "coeffs": [[], b""] if return_floathex else [],
            }
            for dsp_id in range(num_dsp_modules[dsp_class]):
                dsp_coeffs = []
                dsp_coeffs_hex = b""
                for dsp_coeff in range(num_coeffs_dsp_modules[dsp_class]):
                    try:
                        coeff, coeff_hex = self.get_dsp_coeff(
                            dsp_class, dsp_id, dsp_coeff, return_floathex=True
                        )
                        if dsp_class == 3 and dsp_coeff == 1:
                            coeff *= self.get_param("Freq_ISR_Controller", 0)
                        dsp_coeffs.append(coeff)
                        dsp_coeffs_hex += coeff_hex
                    except SerialInvalidCmd:
                        if return_floathex:
                            dsp_coeffs.append("nan")
                            dsp_coeffs_hex += b"\x00\x00\x00\x00"
                        else:
                            dsp_modules_bank[dsp_classes_names[dsp_class]][
                                "coeffs"
                            ].append(dsp_coeffs)

                if return_floathex:
                    dsp_modules_bank[dsp_classes_names[dsp_class]]["coeffs"] = [
                        dsp_coeffs,
                        dsp_coeffs_hex,
                    ]
                else:
                    dsp_modules_bank[dsp_classes_names[dsp_class]][
                        "coeffs"
                    ] = dsp_coeffs

        return dsp_modules_bank

    def set_dsp_modules_bank(
        self, dsp_modules_file: str, save_eeprom: bool = False
    ) -> dict:
        """
        Writes DSP modules parameter bank from CSV file to memory

        Parameters
        -------
        dsp_modules_file
            CSV file
        save_eeprom
            Whether or not parameters should be saved to EEPROM as well
        """
        dsp_coeffs = {}
        with open(dsp_modules_file, newline="") as f:
            reader = csv.reader(f)

            for dsp_module in reader:
                if dsp_module[0] not in dsp_coeffs.keys():
                    dsp_coeffs[dsp_module[0]] = {"class": 9, "coeffs": []}
                if not dsp_module == []:
                    if not dsp_module[0][0] == "#":
                        list_coeffs = []
                        dsp_coeffs[dsp_module[0]]["class"] = int(dsp_module[1])

                        for coeff in dsp_module[
                            3 : 3 + num_coeffs_dsp_modules[int(dsp_module[1])]
                        ]:
                            list_coeffs.append(float(coeff))

                        _, hexcoeffs = self.set_dsp_coeffs(
                            int(dsp_module[1]), int(dsp_module[2]), list_coeffs
                        )
                        dsp_coeffs[dsp_module[0]]["coeffs"].append(
                            [list_coeffs, hexcoeffs.encode("latin-1")]
                        )

        if save_eeprom:
            self.save_dsp_modules_eeprom()

        return dsp_coeffs

    @staticmethod
    def read_csv_dsp_modules_bank(dsp_modules_file_csv: str):
        """
        Reads CSV file containing DSP modules parameter banks

        Parameters
        -------
        dsp_modules_file_csv
            CSV file

        Returns
        -------
        dict[dsp_class_name] = {"class":int, "coeffs":[float]}
        """
        dsp_coeffs_from_csv = {}
        with open(dsp_modules_file_csv, newline="") as f:
            reader = csv.reader(f)

            for dsp_module in reader:
                if dsp_module[0] not in dsp_coeffs_from_csv.keys():
                    dsp_coeffs_from_csv[dsp_module[0]] = {"class": 9, "coeffs": []}
                if not dsp_module == []:
                    if not dsp_module[0][0] == "#":
                        list_coeffs = []
                        dsp_coeffs_from_csv[dsp_module[0]]["class"] = int(dsp_module[1])

                        for coeff in dsp_module[
                            3 : 3 + num_coeffs_dsp_modules[int(dsp_module[1])]
                        ]:
                            list_coeffs.append(float(coeff))

                        dsp_coeffs_from_csv[dsp_module[0]]["coeffs"].append(list_coeffs)

        return dsp_coeffs_from_csv

    def select_param_bank(self, cfg_dsp_modules=0):  # noqa: C901

        add = int(
            input(
                "\n Digite o endereco serial atual do controlador a ser configurado: "
            )
        )

        old_add = self.slave_addr
        self.slave_addr = add

        # areas = ["IA", "LA", "PA"]

        ps_models = ["fbp", "fbp_dclink", "fap", "fap_4p", "fap_2p4s", "fac", "fac_2s"]

        # ps_folders = [
        #   "fbp",
        #   "fbp_dclink",
        #   "fap",
        #   "fap",
        # ]

        # la_fap = [
        #   "TB-Fam:PS-B",
        #   "TS-01:PS-QF1A",
        #   "TS-01:PS-QF1B",
        #   "TS-02:PS-QD2",
        #   "TS-02:PS-QF2",
        #   "TS-03:PS-QF3",
        #   "TS-04:PS-QD4A",
        #   "TS-04:PS-QD4B",
        #   "TS-04:PS-QF4",
        # ]

        print("\n Selecione area: \n")
        print("   0: Sala de racks")
        print("   1: Linhas de transporte")
        print("   2: Sala de fontes\n")
        area = int(input(" Digite o numero correspondente: "))

        if area == 0:
            sector = input("\n Digite o setor da sala de racks [1 a 20]: ")

            if int(sector) < 10:
                sector = "0" + sector

            rack = input("\n Escolha o rack em que a fonte se encontra [1/2/3]: ")

            # if (rack != '1') and (rack != '2'):
            if not ((rack == "1") or (rack == "2") or (sector == "09" and rack == "3")):
                print(" \n *** RACK INEXISTENTE ***\n")
                return

            print("\n Escolha o tipo de fonte: \n")
            print("   0: FBP")
            print("   1: FBP-DCLink\n")
            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model == 0:
                crate = "_crate_" + input(
                    "\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : "
                )

            elif ps_model == 1:
                crate = ""

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            file_dir = "../ps_parameters/IA-" + sector + "/" + ps_models[ps_model] + "/"

            file_name = (
                "parameters_"
                + ps_models[ps_model]
                + "_IA-"
                + sector
                + "RaPS0"
                + rack
                + crate
                + ".csv"
            )

            file_path = file_dir + file_name

            print("\n Banco de parametros a ser utilizado: " + file_path)

        elif area == 1:

            print("\n Escolha o tipo de fonte: \n")
            print("   0: FBP")
            print("   1: FBP-DCLink")
            print("   2: FAP\n")

            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model in (0, 1):

                crate = input(
                    "\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : "
                )
                ps_name = "_LA-RaPS06_crate_" + crate

                file_dir = "../ps_parameters/LA/" + ps_models[ps_model] + "/"
                file_name = "parameters_" + ps_models[ps_model] + ps_name + ".csv"
                file_path = file_dir + file_name

            elif ps_model == 2:

                ps_list = []

                file_dir = "../ps_parameters/LA/fap/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print("\n ### Lista de fontes FAP da linha de transporte ### \n")

                for idx, ps in enumerate(ps_list):
                    print("   " + str(idx) + ": " + ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            print("\n Banco de parametros a ser utilizado: " + file_path)

        elif area == 2:
            print("\n Escolha o tipo de fonte: \n")
            print("   0: FAC")
            print("   1: FAP\n")

            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model == 0:

                ps_list = []

                file_dir = "../ps_parameters/PA/fac/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print(
                    "\n ### Lista de bastidores de controle FAC da sala de fontes ### \n"
                )

                for idx, ps in enumerate(ps_list):
                    print(" ", idx, ": ", ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            elif ps_model == 1:

                ps_list = []

                file_dir = "../ps_parameters/PA/fap/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print(
                    "\n ### Lista de bastidores de controle FAP da sala de fontes ### \n"
                )

                for idx, ps in enumerate(ps_list):
                    print(" ", idx, ": ", ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            print("\n Banco de parametros a ser utilizado: " + file_path)

        else:
            print(" \n *** SALA INEXISTENTE ***\n")
            return

        r = input("\n Tem certeza que deseja prosseguir? [Y/N]: ")

        if r.lower() != "y":
            print(" \n *** OPERAÇÃO CANCELADA ***\n")
            return
        self.slave_addr = add

        if ps_model == 0 and cfg_dsp_modules == 1:
            print("\n Enviando parametros de controle para controlador ...")

            dsp_file_dir = (
                "../dsp_parameters/IA-" + sector + "/" + ps_models[ps_model] + "/"
            )

            dsp_file_name = (
                "dsp_parameters_"
                + ps_models[ps_model]
                + "_IA-"
                + sector
                + "RaPS0"
                + rack
                + crate
                + ".csv"
            )

            dsp_file_path = dsp_file_dir + dsp_file_name

            self.set_dsp_modules_bank(dsp_file_path)

            print("\n Gravando parametros de controle na memoria ...")
            time.sleep(1)
            self.save_dsp_modules_eeprom()

        print("\n Enviando parametros de operacao para controlador ...\n")
        time.sleep(1)
        self.set_param_bank(file_path)
        print("\n Gravando parametros de operacao na memoria EEPROM onboard ...")
        self.save_param_bank(2)
        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()
        time.sleep(2)

        print(
            "\n Pronto! Não se esqueça de utilizar o novo endereço serial para se comunicar com esta fonte! :)\n"
        )

        self.slave_addr = old_add

    def get_siggen_vars(self) -> dict:
        reply_msg = self.read_var(index_to_hex(13), 21)
        val = struct.unpack("BBHffffB", reply_msg)

        return {
            "enable": self.read_bsmp_variable(6, "uint16_t"),
            "type": common.sig_gen_types[int(self.read_bsmp_variable(7, "uint16_t"))],
            "num_cycles": self.read_bsmp_variable(8, "uint16_t"),
            "index": self.read_bsmp_variable(9, "float"),
            "frequency": self.read_bsmp_variable(10, "float"),
            "amplitude": self.read_bsmp_variable(11, "float"),
            "offset": self.read_bsmp_variable(12, "float"),
            "aux_params": val[3:7],
        }

    def clear_bid(self, password, clear_ps=True, clear_dsp=True):

        self.unlock_udc(password)
        time.sleep(1)

        if clear_ps:
            # CLEAR PS PARAMETERS
            for param in list(common.params.keys())[:51]:
                for n in range(common.params[param]["n"]):
                    self.set_param(param, n, 0)
            # ARM - Defaults
            self.set_param(common.params["PS_Model"]["id"], 0, 31)
            self.set_param(common.params["Num_PS_Modules"]["id"], 0, 1)
            self.set_param(common.params["RS485_Baudrate"]["id"], 0, 6000000)
            self.set_param(common.params["RS485_Address"]["id"], 0, 1)
            self.set_param(common.params["RS485_Address"]["id"], 1, 30)
            self.set_param(common.params["RS485_Address"]["id"], 2, 30)
            self.set_param(common.params["RS485_Address"]["id"], 3, 30)
            self.set_param(common.params["RS485_Termination"]["id"], 0, 1)
            self.set_param(common.params["Buzzer_Volume"]["id"], 0, 1)

        if clear_dsp:
            # CLEAR DSP PARAMETERS
            for dsp_class in [1, 2, 3, 4, 5, 6]:
                for dsp_id in range(num_dsp_modules[dsp_class]):
                    for _ in range(num_coeffs_dsp_modules[dsp_class]):
                        self.set_dsp_coeffs(dsp_class, dsp_id, [0])

        # Store values into BID
        time.sleep(0.5)
        self.save_param_bank(type_memory=1)
        time.sleep(0.5)
        self.save_dsp_modules_eeprom(type_memory=1)
        time.sleep(0.5)

    def firmware_initialization(self):
        print("\n ### Inicialização de firmware ### \n")

        print("\n Lendo status...")
        print(self.read_ps_status())

        print("\n Lendo versão de firmware...")
        self.read_udc_version()

        print("\n Desbloqueando UDC...")
        print(self.unlock_udc(0xFFFF))

        print("\n Habilitando EEPROM onboard...")
        self.enable_onboard_eeprom()

        print("\n Alterando senha...")
        print(self.set_param("Password", 0, 0xCAFE))
        print(self.save_param_eeprom("Password", 0, 2))

        print("\n Configurando banco de parâmetros...")
        self.select_param_bank()

        print("\n ### Fim da inicialização de firmware ### \n")

    def cfg_hensys_ps_model(self):

        list_files = [
            "fbp_dclink/parameters_fbp_dclink_hensys.csv",
            "fac/parameters_fac_acdc_hensys.csv",
            "fac/parameters_fac_dcdc_hensys.csv",
            "fac/parameters_fac_2s_acdc_hensys.csv",
            "fac/parameters_fac_2s_dcdc_hensys.csv",
            "fac/parameters_fac_2p4s_acdc_hensys.csv",
            "fac/parameters_fac_2p4s_dcdc_hensys.csv",
            "fap/parameters_fap_hensys.csv",
            "fap/parameters_fap_2p2s_hensys.csv",
            "fap/parameters_fap_4p_hensys.csv",
        ]

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(0xCAFE))

        print("\n *** Escolha o modelo de fonte a ser configurado ***\n")
        print(" 0: FBP-DClink")
        print(" 1: FAC-ACDC")
        print(" 2: FAC-DCDC")
        print(" 3: FAC-2S-ACDC")
        print(" 4: FAC-2S-DCDC")
        print(" 5: FAC-2P4S-ACDC")
        print(" 6: FAC-2P4S-DCDC")
        print(" 7: FAP")
        print(" 8: FAP-2P2S")
        print(" 9: FAP-4P")

        model_idx = int(input("\n Digite o índice correspondente: "))
        file_path = "../ps_parameters/development/" + list_files[model_idx]

        print("\n Banco de parametros a ser utilizado: " + file_path)

        r = input("\n Tem certeza que deseja prosseguir? [Y/N]: ")

        if r.lower() != "y":
            print(" \n *** OPERAÇÃO CANCELADA ***\n")
            return

        print("\n Enviando parametros de operacao para controlador ...\n")
        time.sleep(1)
        self.set_param_bank(file_path)

        print("\n Gravando parametros de operacao na memoria EEPROM onboard ...")
        self.save_param_bank(2)
        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()
        time.sleep(2)

        print(
            "\n Pronto! Nao se esqueca de utilizar o novo endereco serial para se comunicar com esta fonte! :)\n"
        )

    def test_bid_board(self, password):

        input(
            "\n Antes de iniciar, certifique-se que o bastidor foi energizado sem a placa BID.\n Para prosseguir, conecte a placa BID a ser testada e pressione qualquer tecla... "
        )

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory=2))

        print("\n Banco de parametros da memoria onboard:\n")

        max_param = common.params["Scope_Source"]["id"]
        param_bank_onboard = []

        for param in common.params.keys()[0:max_param]:
            val = self.get_param(param, 0)
            print(param + ":", val)
            param_bank_onboard.append(val)

        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory=1))

        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()

        time.sleep(3)

        self.read_ps_status()

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory=1))

        self.read_ps_status()

        print("\n Verificando banco de parametros offboard apos reset ... \n")
        try:
            param_bank_offboard = []

            for param in common.params.keys()[0:max_param]:
                val = self.get_param(param, 0)
                print(param, val)
                param_bank_offboard.append(val)

            if param_bank_onboard == param_bank_offboard:
                print("\n Placa BID aprovada!\n")
            else:
                print("\n Placa BID reprovada!\n")

        except Exception:
            print(" Placa BID reprovada!\n")

    def upload_parameters_bid(self, password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory=1))
        time.sleep(1)

        print("\n Salvando banco de parametros na memoria onboard ...")
        print(self.save_param_bank(type_memory=2))
        time.sleep(5)

        print("\n Carregando coeficientes de controle da memoria offboard ...")
        print(self.load_dsp_modules_eeprom(type_memory=1))
        time.sleep(1)

        print("\n Salvando coeficientes de controle na memoria onboard ...\n")
        print(self.save_dsp_modules_eeprom(type_memory=2))

    def download_parameters_bid(self, password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory=2))
        time.sleep(1)

        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory=1))
        time.sleep(5)

        print("\n Carregando coeficientes de controle da memoria onboard ...")
        print(self.load_dsp_modules_eeprom(type_memory=2))
        time.sleep(1)

        print("\n Salvando coeficientes de controle na memoria offboard ...")
        print(self.save_dsp_modules_eeprom(type_memory=1))
