import configparser
import datetime
import logging
import struct
import os
import platform
from ctypes import *
from os.path import dirname
from pathlib import Path
import faulthandler
from collections import defaultdict
from datetime import datetime
import atexit
import signal
import logging

# config file variables
DBOPTIONS = "dboptions"
LOGGING = "logging"
LOGLEVEL = "loglevel"
LOGFILE = "logfile"
LOGFILENAME = "pyconnector.log"
READTIMEOUT = "readtimeout"
WRITETIMEOUT = "writetimeout"
RECONNECTTIMEOUT = "reconnecttimeout"
KEY = "key"
HANDSHAKE = "handshake"
TRANSPORT = "transport"
ENABLE_FAULTHANDLER = "enable_faulthandler"
CHARACTERENCODING = "encoding"
DATEFORMAT = "dateformat"
FAME = "fame"
PYTHON_CONNECTOR_FILE_NAME = "python_connector.config"
CHLILOGGING = "chli_log_enable"
CHLILOGGINGFILE = "chli_log_path"

BOOL_ARRAY = {-1: "TRUE", 0: "FALSE"}

CONFIG_OPTIONS = [DBOPTIONS, LOGGING, LOGLEVEL, LOGFILE, READTIMEOUT, WRITETIMEOUT, RECONNECTTIMEOUT, KEY,
                  HANDSHAKE, TRANSPORT, ENABLE_FAULTHANDLER, CHARACTERENCODING, DATEFORMAT, FAME,
                  PYTHON_CONNECTOR_FILE_NAME, CHLILOGGING, CHLILOGGINGFILE]

env_var_fame_chli_file = "FAME_CHLI_FILE"
env_var_fame = "FAME"
env_var_fame_path = "FAME_PATH"
env_var_fame_temp = "FAME_TEMP"
env_var_temp = "TEMP"
env_var_tmp = "TMP"

DEFAULT_KEY = "37254F07EDB1CF4D6C8705274583C9GE"

HANDSHAKE_ALWAYS = "ALWAYS"
HANDSHAKE_BEST = "BEST"
HANDSHAKE_NEVER = "NEVER"

module = 'PYTHON_CONNECTOR'

VT_EMPTY = 0
VT_NULL = 1
VT_I2 = 2
VT_I4 = 3
VT_R4 = 4
VT_R8 = 5
VT_CY = 6
VT_DATE = 7
VT_BSTR = 8
VT_DISPATCH = 9
VT_ERROR = 10
VT_BOOL = 11
VT_VARIANT = 12
VT_UNKNOWN = 13
VT_DECIMAL = 14
VT_I1 = 16
VT_UI1 = 17
VT_UI2 = 18
VT_UI4 = 19
VT_I8 = 20
VT_UI8 = 21
VT_INT = 22
VT_UINT = 23
VT_VOID = 24
VT_HRESULT = 25
VT_PTR = 26
VT_SAFEARRAY = 27
VT_CARRAY = 28
VT_USERDEFINED = 29
VT_LPSTR = 30
VT_LPWSTR = 31
VT_RECORD = 36
VT_INT_PTR = 37
VT_UINT_PTR = 38
VT_FILETIME = 64
VT_BLOB = 65
VT_STREAM = 66
VT_STORAGE = 67
VT_STREAMED_OBJECT = 68
VT_STORED_OBJECT = 69
VT_BLOB_OBJECT = 70
VT_CF = 71
VT_CLSID = 72
VT_VERSIONED_STREAM = 73
VT_BSTR_BLOB = 0xfff
VT_VECTOR = 0x1000
VT_ARRAY = 0x2000
VT_BYREF = 0x4000
VT_RESERVED = 0x8000
VT_ILLEGAL = 0xffff
VT_ILLEGALMASKED = 0xfff
VT_TYPEMASK = 0xfff

def f(obj):
    for k, v in obj.__dict__.items():
        print("k=", k, " v=", v)
        if hasattr(v, '__dict__'):
            f(v)


def iswritable(dir):
    try:
        tmp_prefix = "testwrite"
        count = 0
        filename = os.path.join(dir, tmp_prefix)
        while (os.path.exists(filename)):
            filename = "{}.{}".format(os.path.join(dir, tmp_prefix), count)
            count = count + 1
        f = open(filename, "w")
        f.close()
        os.remove(filename)
        return True
    except Exception as ex:
        raise


def FAMEConvertToDateTime2(datetimevalue, datetimeformat=None):
    try:
        seconds = (datetimevalue - 25569) * 86400.0
        if datetimeformat is None:
            return datetime.utcfromtimestamp(seconds)
        else:
            return datetime.utcfromtimestamp(seconds).strftime(datetimeformat)
    except Exception as ex:
        logger.exception("converttodatetime2: %s", ex)
        raise


def floatToTime(fh):
    timeconve = fh*24
    h = int(timeconve)
    timeconve = (timeconve - h)*60
    m = int(timeconve)
    timeconve = (timeconve - m) * 60
    s = int(timeconve)
    timeconve = (timeconve - s) * 1000 * 1000
    ms = int(round(timeconve))
    if ms > 999999:
        ms = 0
        s = s + 1
    if s > 59:
        s = 0
        m = m + 1
    if m > 59:
        m = 0
        h = h + 1


    return (
        h,
        m,
        s,
        ms
    )


def FAMEConvertToDateTime(datetimevalue, datetimeformat=None):
    try:
        idatetimevalue = int(datetimevalue)
        if datetimevalue < 0:
            if datetimevalue.is_integer() is False:
                idatetimevalue = idatetimevalue - 1
            rawdt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + idatetimevalue - 2)
        else:
            rawdt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + idatetimevalue - 2)
        hour, minute, second, msecond = floatToTime(datetimevalue % 1)
        rawdt = rawdt.replace(hour=hour, minute=minute, second=second, microsecond=msecond)
        if datetimeformat is None:
            #return rawdt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            return rawdt.isoformat(sep=' ', timespec='milliseconds')

        else:
            return rawdt.strftime(datetimeformat)

    except Exception as ex:
        logger.exception("converttodatetime: %s", ex)
        raise


def gettempfilepath():
    try:
        tempfilepath = None
        for env_var in [env_var_fame_temp, env_var_temp, env_var_tmp]:
            tempfilepath = os.getenv((env_var))
            if tempfilepath is not None and iswritable(tempfilepath) is True:
                return tempfilepath
            else:
                tempfilepath = None

        if tempfilepath is None:
            tempfilepath = os.getcwd()
            return tempfilepath

    except Exception as ex:
        raise


def ptr2d_to_mat(ptr, nrows, cols, row_array):
    try:
        i = 0
        j = 0
        k = 0
        l = 0
        elements = defaultdict(list)
        #for i in range(nrows * cols):
        while i < (nrows * cols):
            if l == row_array[k]:
                k = k + 1
                i = nrows * k
                l = 0

            value = float('nan')
            if VT_EMPTY == ptr[i].vt:
                pass
            if VT_ERROR == ptr[i].vt:
                value = "N/A"
            if VT_BOOL == ptr[i].vt:
                value = BOOL_ARRAY[ptr[i].boolVal]
            elif VT_DATE == ptr[i].vt:
                # value = ptr[i].date
                # value = datetime.strptime(ptr[i].date, '%d%b%Y').date()
                value = FAMEConvertToDateTime(ptr[i].date)
            elif VT_R4 == ptr[i].vt:
                value = ptr[i].fltVal
            elif VT_R8 == ptr[i].vt:
                value = ptr[i].dblVal
            elif VT_I4 == ptr[i].vt:
                value = ptr[i].lVal
            elif VT_BSTR == ptr[i].vt:
                bytearray_data = bytearray()
                bytearray_data.extend(map(ord, ptr[i].bstrVal))
                value = bytearray_data.decode(getproperty("encoding"),'ignore')

            if i % nrows != 0:
                elements[j].append(value)
            else:
                j = j + 1
                elements[j].append(value)
            i = i + 1
            l = l + 1
        return elements
    except Exception as ex:
        logger.exception("ptr2d_to_mat: %s", ex)
        raise


class tagSAFEARRAYBOUND(Structure):
    _fields_ = [
        ('cElements', c_ulong),
        ('lBound', c_long)
    ]


class tagSAFEARRAY(Structure):
    _fields_ = [
        ('cDims', c_ushort),
        ('cColumns', c_ushort),
        ('fFeatures', c_ushort),
        ('cbElements', c_ulong),
        ('cLocks', c_ulong),
        ('pvData', c_void_p),
        ('rgsabound', POINTER(tagSAFEARRAYBOUND))
    ]


class tagVARIANTUNION(Union):
    _fields_ = [
        ('llVal', c_longlong),
        ('lVal', c_long),
        ('bVal', c_ubyte),
        ('iVal', c_short),
        ('fltVal', c_float),
        ('dblVal', c_double),
        ('boolVal', c_short),
        ('scode', c_long),
        ('date', c_double),
        ('bstrVal', c_wchar_p),
        ('parray', POINTER(tagSAFEARRAY))
    ]


class _tagVARIANT(Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("vt", c_ushort),
        ("wReserved1", c_ushort),
        ("wReserved2", c_ushort),
        ("wReserved3", c_ushort),
        ("u", tagVARIANTUNION)
    ]


class _VARIANT_NAME_1(Union):
    _anonymous_ = ("tvs",)
    _fields_ = [
        ("tvs", _tagVARIANT)
    ]


class tagVARIANT(Structure):
    _anonymous_ = ("vn1",)
    _fields_ = [
        ("vn1", _VARIANT_NAME_1)
    ]


# def free_library(handle):
#     kernel32 = WinDLL('kernel32', use_last_error=True)
#     kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
#     kernel32.FreeLibrary(handle)

def loadinstance():
    try:
        dll_name = "chliwrap.dll"
        dll_path = os.getcwd()
        dll_name_path = dll_path + slash + dll_name
        if os.path.exists(dll_name_path):
            pass
        else:
            dll_path = dirname(dirname(dll_name_path))
            dll_name_path = dll_path + slash + dll_name

        # dll_name_path = dll_name
        global handle

        handle = cdll.LoadLibrary(dll_name_path)
        assert handle.__class__.__name__ == 'CDLL'
        assert handle._name == str(dll_name_path)
        # time.sleep(20)
        instanceloaded = True

    except Exception as ex:
        logger.exception("loadinstance: %s", ex)
        raise


def startinstance():
    try:
        initdataretptr = POINTER(tagVARIANT)
        startInstance = handle.startInstance
        startInstance.argtypes = None
        startInstance.restype = initdataretptr
        initData = startInstance()
        if (initData.contents.vt == VT_ERROR):
            raise Exception(initData.contents.bstrVal)
        del initData
    except Exception as ex:
        logger.exception("startinstance: %s", ex)
        raise


def exit_handler():
    # print("My application is ending!")
    # exitretptr = POINTER(tagVARIANT)
    exit_instance = handle.exitInstance
    exit_instance.argtypes = None
    exit_instance.restype = None
    exit_instance()
    # free_library(handle._handle)
    # exitretptr = exit_instance()
    # if (exitretptr.contents.vt == VT_ERROR):
    #    print("error=", exitretptr.contents.vt.bstrVal)


atexit.register(exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGABRT, exit_handler)
# signal.signal(signal.SIGKILL, exit_handler)
signal.signal(signal.SIGSEGV, exit_handler)
# signal.signal(signal.SIGTRAP, exit_handler)
signal.signal(signal.SIGFPE, exit_handler)
# signal.signal(signal.SIGTRAP, exit_handler)
# signal.signal(signal.SIGHUP, exit_handler)

class Properties(dict):
    property_dict = {}

    def __init__(self):
        self.read_parameter_file()
        if self.property_dict[ENABLE_FAULTHANDLER]:
            # fame_path = str(os.environ.get(env_var_fame))
            faultfile = gettempfilepath()
            faultfile += slash + 'fault_%s.log' % str(os.getpid())
            f = open(faultfile, 'w')
            faulthandler.enable(file=f, all_threads=True)

    def read_parameter_file(self):
        global logger
        config_parser = configparser.ConfigParser()
        config_file_path = os.getcwd()
        debug_str1 = None
        debug_str2 = None

        config_file_path += slash + PYTHON_CONNECTOR_FILE_NAME
        debug_str1 = config_file_path + " is set to " + config_file_path

        config_file = Path(config_file_path)
        if config_file.is_file():
            debug_str2 = str(config_file) + " is present"
        else:
            debug_str2 = str(config_file) + " is NOT present"
            # print("config file does not exist or directory with same name exists")
            ## need to optimize this code along with
            logfile = gettempfilepath()
            logfile += slash + LOGFILENAME
            fw = open(logfile, 'a+')
            fw.close()

            self.property_dict[LOGFILE] = logfile
            self.property_dict[LOGLEVEL] = "INFO"
            logging.basicConfig(filename=self.property_dict[LOGFILE], filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d f%H:%M:%S',
                                level=self.property_dict[LOGLEVEL])

            logger = logging.getLogger(module)

            logger.info("Logging starts...")
            logger.info("config file path set to %s", config_file_path)
            logger.info("config file set to %s", config_file)

            logger.info("%s", debug_str1)
            logger.info("%s", debug_str2)

            self.property_dict[ENABLE_FAULTHANDLER] = False
            self.property_dict[READTIMEOUT] = 60
            self.property_dict[WRITETIMEOUT] = 60
            self.property_dict[RECONNECTTIMEOUT] = 0
            self.property_dict[HANDSHAKE] = HANDSHAKE_BEST
            self.property_dict[TRANSPORT] = HANDSHAKE_NEVER
            self.property_dict[KEY] = DEFAULT_KEY
            self.property_dict[CHARACTERENCODING] = "cp1252"
            self.property_dict[DATEFORMAT] = None
            self.property_dict[CHLILOGGING] = False
            self.property_dict[CHLILOGGINGFILE] = None

            for k, v in self.property_dict.items():
                if k != KEY:
                    logger.info("properties %s %s", k, v)

            return

        config_parser.read(config_file)

        loglevel = config_parser.get(LOGGING, LOGLEVEL, fallback='WARNING')
        if loglevel.upper() in ("WARNING", "DEBUG", "ERROR", "CRITICAL", "INFO"):
            self.property_dict[LOGLEVEL] = loglevel
        else:
            self.property_dict[LOGLEVEL] = "INFO"

        enable_faulthandler = config_parser.get(LOGGING, ENABLE_FAULTHANDLER, fallback="false")
        if enable_faulthandler.upper() == "TRUE":
            self.property_dict[ENABLE_FAULTHANDLER] = True
        else:
            self.property_dict[ENABLE_FAULTHANDLER] = False

        logfile = config_parser.get(LOGGING, LOGFILE, fallback=None)
        if logfile is None:
            logfile = os.getcwd() + slash + LOGFILENAME
            fw = open(logfile, 'a+')
            fw.close()
        else:
            pass

        self.property_dict[LOGFILE] = logfile
        logging.basicConfig(filename=self.property_dict[LOGFILE], filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d f%H:%M:%S',
                            level=self.property_dict[LOGLEVEL])
        # logging.getLogger(module).addHandler(logging.StreamHandler())
        logger = logging.getLogger(module)

        logger.info("Logging starts...")
        logger.info("config file path set to %s", config_file_path)
        logger.info("config file set to %s", config_file)

        logger.info("%s", debug_str1)
        logger.info("%s", debug_str2)

        enable_chli_logging = config_parser.get(LOGGING, CHLILOGGING, fallback="false")
        if enable_chli_logging.upper() == "TRUE":
            self.property_dict[CHLILOGGING] = True
        else:
            self.property_dict[CHLILOGGING] = False

        chlilogfile = config_parser.get(LOGGING, CHLILOGGINGFILE, fallback=None)
        if chlilogfile is None:
            pass
        else:
            self.property_dict[CHLILOGGINGFILE] = chlilogfile

        rtimeout = config_parser.get(DBOPTIONS, READTIMEOUT, fallback=60)
        # if rtimeout is not None and rtimeout.isdigit():
        if rtimeout is not None and (isinstance(rtimeout, int) or isinstance(rtimeout, float) or rtimeout.isdigit()):
            self.property_dict[READTIMEOUT] = rtimeout
        else:
            self.property_dict[READTIMEOUT] = 60

        wtimeout = config_parser.get(DBOPTIONS, WRITETIMEOUT, fallback=60)
        if wtimeout is not None and wtimeout.isdigit():
            self.property_dict[WRITETIMEOUT] = wtimeout
        else:
            self.property_dict[WRITETIMEOUT] = 60

        rctimeout = config_parser.get(DBOPTIONS, RECONNECTTIMEOUT, fallback=0)
        if rctimeout is not None and rctimeout.isdigit():
            self.property_dict[RECONNECTTIMEOUT] = rctimeout
        else:
            self.property_dict[RECONNECTTIMEOUT] = 0

        hshake = config_parser.get(DBOPTIONS, HANDSHAKE, fallback=HANDSHAKE_BEST)
        if hshake is not None and hshake in (HANDSHAKE_ALWAYS, HANDSHAKE_NEVER, HANDSHAKE_BEST):
            self.property_dict[HANDSHAKE] = hshake
        else:
            self.property_dict[HANDSHAKE] = HANDSHAKE_BEST

        tport = config_parser.get(DBOPTIONS, TRANSPORT, fallback=HANDSHAKE_NEVER)
        if tport is not None and tport in (HANDSHAKE_ALWAYS, HANDSHAKE_NEVER, HANDSHAKE_BEST):
            self.property_dict[TRANSPORT] = tport
        else:
            self.property_dict[TRANSPORT] = HANDSHAKE_NEVER

        ekey = config_parser.get(DBOPTIONS, KEY, fallback=DEFAULT_KEY)
        if ekey is not None:
            self.property_dict[KEY] = ekey
        else:
            self.property_dict[KEY] = DEFAULT_KEY

        characterencoding = config_parser.get(DBOPTIONS, CHARACTERENCODING, fallback="utf-8")
        if characterencoding is not None:
            self.property_dict[CHARACTERENCODING] = characterencoding
        else:
            self.property_dict[CHARACTERENCODING] = "cp1252"

        dateformat = config_parser.get(DBOPTIONS, DATEFORMAT, fallback=None)
        if dateformat is not None:
            self.property_dict[DATEFORMAT] = dateformat
        else:
            self.property_dict[DATEFORMAT] = None

        logger.info("config file path %s", config_file_path)
        for k, v in self.property_dict.items():
            if k != KEY:
                logger.info("properties %s %s", k, v)

    def getProperty(self, propname):
        return self.property_dict[propname]

    def setProperty(self, propname, value):
        self.property_dict[propname] = value

    def has_key(self, k):
        if k in self.property_dict:
            return True
        else:
            return False
# elements = defaultdict(list)
# def setdate1(expression, startDate, endDate, numRecords):
#     set_date(expression.encode(), startDate, endDate, numRecords)

def FAMESetProperty(key_option, value_option):
    if key_option in CONFIG_OPTIONS:
        properties.setProperty(key_option, value_option)
        setfameoption(key_option, value_option)
    else:
        return


def getproperty(key_option):
    return properties.getProperty(key_option)


def setfameoption(setkey, setvalue):
    try:
        set_fameoption = handle.setFameOption
        set_fameoption.argtypes = [tagVARIANT, tagVARIANT]
        set_fameoption.restype = None

        fame_option_key = tagVARIANT()
        fame_option_key.vn1.tvs.vt = VT_BSTR
        fame_option_key.vn1.tvs.u.bstrVal = c_wchar_p(setkey)

        fame_option_value = tagVARIANT()
        fame_option_value.vn1.tvs.vt = VT_BSTR
        fame_option_value.vn1.tvs.u.bstrVal = c_wchar_p(setvalue)

        set_fameoption(fame_option_key, fame_option_value)


    except Exception as ex:
        logger.exception("setfameoption: %s", ex)
        raise



try:
    os_type = (platform.system()).lower()
    slash = None
    # fame_path = str(os.environ.get(env_var_fame))
    if os_type == 'windows':
        slash = '\\'
    else:
        slash = '/'

    bit = 8 * struct.calcsize("P")
    handle = None
    logger = None
    global instanceloaded
    instanceloaded = False
    instancestarted = False
    properties = Properties()
    if instanceloaded is False:
        loadinstance()

except Exception as ex:
    raise


def cleandata(data):
    try:
        cleanVarPtr = POINTER(tagVARIANT)
        clean_data = handle.clean_data
        clean_data.argtypes = [cleanVarPtr]
        clean_data.restype = None
        clean_data(data)
    except Exception as ex:
        logger.exception("cleandata: %s", ex)
        raise


def setdate(frequency, startdate, enddate, numpriods):
    try:
        set_date = handle.set_date
        datevarptr = POINTER(tagVARIANT)
        # set_date.argtypes = [c_wchar_p, startDate, endDate, c_long]
        set_date.argtypes = [c_char_p, c_char_p, c_char_p, c_long]
        set_date.restype = datevarptr
        datedata = set_date(frequency.encode(), startdate.encode(), enddate.encode(), numpriods)
        if (datedata.contents.vt == VT_ERROR):
            raise Exception(datedata.contents.bstrVal)
        cleandata(datedata)
        del datedata
    except Exception as ex:
        logger.exception("setdate: %s", ex)
        raise


def getdata(expression, includeHeading, isAcross, isReversed):
    try:
        retValptr = tagVARIANT()
        VarPtr = POINTER(tagVARIANT)
        retVal = POINTER(tagVARIANT)
        get_data = handle.get_data
        get_data.argtypes = [c_char_p, c_short, c_short, c_short, retVal]
        get_data.restype = VarPtr
        dictData = get_data(expression.encode(), includeHeading, isAcross, isReversed, byref(retValptr))
        if (dictData.contents.vt == VT_ERROR):
            raise Exception(dictData.contents.bstrVal)
        w = cast(dictData.contents.vn1.tvs.u.parray.contents.rgsabound, POINTER(tagSAFEARRAYBOUND))
        maxrowvalue = 0
        columns = dictData.contents.vn1.tvs.u.parray.contents.cColumns
        row_array = []
        for column in range(columns):
            row_array.append(w[column].cElements)
            if maxrowvalue < w[column].cElements:
                maxrowvalue = w[column].cElements

        raw_data = cast(dictData.contents.vn1.tvs.u.parray.contents.pvData, POINTER(tagVARIANT))
        outptr = ptr2d_to_mat(raw_data, maxrowvalue + 1, columns, row_array)
        cleandata(dictData)
        del dictData
        return outptr

    except Exception as ex:
        logger.exception("getdata: %s", ex)
        raise


def FAMEData(expression, startdate, enddate, numrecords, frequency, across, heading, ireversed):
    isAcross = 0
    includeHeading = 0
    isReversed = 0
    try:
        global instancestarted
        if instancestarted is False:
            startinstance()
            instancestarted = True

        if (across[0]).lower() == 'a':
            isAcross = 0
        else:
            isAcross = 0

        if (heading[0]).lower() == "n":
            includeHeading = 0
        else:
            includeHeading = 1

        if (ireversed[0]).lower() == "r":
            isReversed = 1
        else:
            isReversed = 0

        retValptr = tagVARIANT()
        VarPtr = POINTER(tagVARIANT)
        retVal = POINTER(tagVARIANT)
        get_data_all = handle.get_data_all
        get_data_all.argtypes = [c_char_p, c_char_p, c_char_p, c_long, c_char_p, c_short, c_short, c_short, retVal]
        get_data_all.restype = VarPtr
        dictData = get_data_all(expression.encode(), startdate.encode(), enddate.encode(), numrecords, frequency.encode(),
                                isAcross, includeHeading, isReversed, byref(retValptr))
        if (dictData.contents.vt == VT_ERROR):
            raise Exception(dictData.contents.bstrVal)
        w = cast(dictData.contents.vn1.tvs.u.parray.contents.rgsabound, POINTER(tagSAFEARRAYBOUND))
        maxrowvalue = 0
        columns = dictData.contents.vn1.tvs.u.parray.contents.cColumns
        row_array = []
        for column in range(columns):
            row_array.append(w[column].cElements)
            if maxrowvalue < w[column].cElements:
                maxrowvalue = w[column].cElements

        #if includeHeading == 1:
        #    maxrowvalue = maxrowvalue + 1

        raw_data = cast(dictData.contents.vn1.tvs.u.parray.contents.pvData, POINTER(tagVARIANT))
        outptr = ptr2d_to_mat(raw_data, maxrowvalue, columns, row_array)
        cleandata(dictData)
        del dictData
        return outptr

    except Exception as ex:
        logger.exception("FAMEData: %s", ex)
        raise