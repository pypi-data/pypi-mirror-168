# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-target', 'armeb', '-DDEBUG=1', '-fpack-struct', '-EB']
# WORD_SIZE is: 4
# POINTER_SIZE is: 4
# LONGDOUBLE_SIZE is: 8
#
import ctypes




uint8_t = ctypes.c_uint8

# values for enumeration 'c__EA_cmd_type_t'
c__EA_cmd_type_t__enumvalues = {
    165: 'CMD_READ',
    90: 'CMD_WRITE',
}
CMD_READ = 165
CMD_WRITE = 90
c__EA_cmd_type_t = ctypes.c_int # enum
cmd_type_t = c__EA_cmd_type_t
cmd_type_t__enumvalues = c__EA_cmd_type_t__enumvalues

# values for enumeration 'c__EA_debug_error_t'
c__EA_debug_error_t__enumvalues = {
    0: 'DEBUG_ERROR_NONE',
    1: 'DEBUG_ERROR_FRONTEND',
    2: 'DEBUG_ERROR_I2C_BUSY',
}
DEBUG_ERROR_NONE = 0
DEBUG_ERROR_FRONTEND = 1
DEBUG_ERROR_I2C_BUSY = 2
c__EA_debug_error_t = ctypes.c_int # enum
debug_error_t = c__EA_debug_error_t
debug_error_t__enumvalues = c__EA_debug_error_t__enumvalues

# values for enumeration 'c__EA_debug_cmd_t'
c__EA_debug_cmd_t__enumvalues = {
    0: 'DEBUG_CMD_SET_CELL_MV',
    1: 'DEBUG_CMD_SET_PACK_CA',
    2: 'DEBUG_CMD_SET_PACK_CV',
    3: 'DEBUG_CMD_SET_NTC_DK',
    4: 'DEBUG_CMD_SET_MANUAL_ENABLE',
    5: 'DEBUG_CMD_DUMP_REGS',
}
DEBUG_CMD_SET_CELL_MV = 0
DEBUG_CMD_SET_PACK_CA = 1
DEBUG_CMD_SET_PACK_CV = 2
DEBUG_CMD_SET_NTC_DK = 3
DEBUG_CMD_SET_MANUAL_ENABLE = 4
DEBUG_CMD_DUMP_REGS = 5
c__EA_debug_cmd_t = ctypes.c_int # enum
debug_cmd_t = c__EA_debug_cmd_t
debug_cmd_t__enumvalues = c__EA_debug_cmd_t__enumvalues
class struct_c__SA_debug_cmd_set_cell_mv_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('cell_num', ctypes.c_ubyte),
    ('cell_mv', ctypes.c_uint16),
     ]

debug_cmd_set_cell_mv_t = struct_c__SA_debug_cmd_set_cell_mv_t
class struct_c__SA_debug_cmd_set_ntc_dk_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('ntc_num', ctypes.c_ubyte),
    ('ntc_dk', ctypes.c_uint16),
     ]

debug_cmd_set_ntc_dk_t = struct_c__SA_debug_cmd_set_ntc_dk_t
class struct_c__SA_debug_cmd_set_pack_ca_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('pack_ca', ctypes.c_int16),
     ]

debug_cmd_set_pack_ca_t = struct_c__SA_debug_cmd_set_pack_ca_t
class struct_c__SA_debug_cmd_set_pack_cv_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('pack_cv', ctypes.c_int16),
     ]

debug_cmd_set_pack_cv_t = struct_c__SA_debug_cmd_set_pack_cv_t
class struct_c__SA_debug_cmd_set_manual_enable_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('manual_enable', ctypes.c_ubyte),
     ]

debug_cmd_set_manual_enable_t = struct_c__SA_debug_cmd_set_manual_enable_t
class union_c__UA_debug_cmd_union_t(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('cell_mv', debug_cmd_set_cell_mv_t),
    ('ntc_dk', debug_cmd_set_ntc_dk_t),
    ('pack_ca', debug_cmd_set_pack_ca_t),
    ('pack_cv', debug_cmd_set_pack_cv_t),
    ('manual_enable', debug_cmd_set_manual_enable_t),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

debug_cmd_union_t = union_c__UA_debug_cmd_union_t
class struct_c__SA_debug_cmd_packet_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('cmd', ctypes.c_ubyte),
    ('u', debug_cmd_union_t),
     ]

debug_cmd_packet_t = struct_c__SA_debug_cmd_packet_t
class struct_c__SA_debug_t(ctypes.BigEndianStructure):
    _pack_ = True # source:False
    _fields_ = [
    ('error_code', ctypes.c_ubyte),
    ('chip_id', ctypes.c_byte),
    ('cell_cnt', ctypes.c_ubyte),
    ('cell_max_idx', ctypes.c_ubyte),
    ('cell_0_raw', ctypes.c_uint16),
    ('adc_gain', ctypes.c_uint16),
    ('adc_offset', ctypes.c_ubyte),
    ('ohms_raw', ctypes.c_uint16),
    ('cc_raw', ctypes.c_int16),
    ('cc_cfg', ctypes.c_ubyte),
    ('t0', ctypes.c_ubyte),
    ('t1', ctypes.c_ubyte),
    ('t2', ctypes.c_ubyte),
    ('protect_active', ctypes.c_ubyte),
    ('balance_active', ctypes.c_ubyte),
     ]

debug_t = struct_c__SA_debug_t
debug_info = struct_c__SA_debug_t # Variable struct_c__SA_debug_t
debug_manual_values = None # Variable ctypes.c_ubyte
__all__ = \
    ['CMD_READ', 'CMD_WRITE', 'DEBUG_CMD_DUMP_REGS',
    'DEBUG_CMD_SET_CELL_MV', 'DEBUG_CMD_SET_MANUAL_ENABLE',
    'DEBUG_CMD_SET_NTC_DK', 'DEBUG_CMD_SET_PACK_CA',
    'DEBUG_CMD_SET_PACK_CV', 'DEBUG_ERROR_FRONTEND',
    'DEBUG_ERROR_I2C_BUSY', 'DEBUG_ERROR_NONE', 'c__EA_cmd_type_t',
    'c__EA_debug_cmd_t', 'c__EA_debug_error_t', 'cmd_type_t',
    'cmd_type_t__enumvalues', 'debug_cmd_packet_t',
    'debug_cmd_set_cell_mv_t', 'debug_cmd_set_manual_enable_t',
    'debug_cmd_set_ntc_dk_t', 'debug_cmd_set_pack_ca_t',
    'debug_cmd_set_pack_cv_t', 'debug_cmd_t',
    'debug_cmd_t__enumvalues', 'debug_cmd_union_t', 'debug_error_t',
    'debug_error_t__enumvalues', 'debug_info', 'debug_manual_values',
    'debug_t', 'struct_c__SA_debug_cmd_packet_t',
    'struct_c__SA_debug_cmd_set_cell_mv_t',
    'struct_c__SA_debug_cmd_set_manual_enable_t',
    'struct_c__SA_debug_cmd_set_ntc_dk_t',
    'struct_c__SA_debug_cmd_set_pack_ca_t',
    'struct_c__SA_debug_cmd_set_pack_cv_t', 'struct_c__SA_debug_t',
    'uint8_t', 'union_c__UA_debug_cmd_union_t']
