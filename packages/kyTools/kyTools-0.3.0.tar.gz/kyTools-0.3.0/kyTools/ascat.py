import os
import csv
import json
import math
import zlib
import base64
import struct
import hashlib
import platform
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
import numpy as np


def parse_record_class(index):
    record_class = {0: "Reserved",
                    1: "Main Product Header Record",
                    2: "Secondary Product Header Record",
                    3: "Internal Pointer Record",
                    4: "Global External Auxiliary Data Record",
                    5: "Global Internal Auxiliary Data Record",
                    6: "Variable External Auxiliary Data Record",
                    7: "Variable Internal Auxiliary Data Record",
                    8: "Measurement Data Record"
                    }
    return record_class[index]


def parse_record_subclass(class_id, subclass_id):
    class_name = parse_record_class(class_id)
    ipr = {
        0: "Reserved",
        1: "Main Product Header Record",
        2: "Secondary Product Header Record",
        3: "Internal Pointer Record",
        4: "Global External Auxiliary Data Record",
        5: "Global Internal Auxiliary Data Record",
        6: "Variable External Auxiliary Data Record",
        7: "Variable Internal Auxiliary Data Record",
        8: "Measurement Data Record"
    }
    geadr = {2: ("LSM", "Land Sea Mask File")}
    veadr = {
        1:  ("VEADR-PRC", "Processing parameters file"),
        2:  ("VEADR-INS", "Instrument parameters file"),
        3:  ("VEADR-NTB", "Normalisation Table"),
        5:  ("VEADR-XCL", "Antenna gain patterns file"),
        6:  ("VEADR-OSV", "Orbit State Vector prediction file"),
        7:  ("VEADR-SMC", "Sigma_0 bias correction file"),
        8:  ("VEADR-CURV", "Parameters database file"),
        9:  ("VEADR-CURV-NOISE", "Parameters database file"),
        10: ("VEADR-DRY", "Parameters database file"),
        11: ("VEADR-DRY-NOISE", "Parameters database file"),
        12: ("VEADR-MS-MEAN", "Parameters database file"),
        13: ("VEADR-NONSCAT", "Parameters database file"),
        14: ("VEADR-SLOP", "Parameters database file"),
        15: ("VEADR-SLOP", "Parameters database file"),
        16: ("VEADR-WET", "Parameters database file"),
        17: ("VEADR-WET-NOISE", "Parameters database file"),
    }
    viadr = {
        4: ("VIADR-OA", "Orbit/attitude parameters"),
        6: ("VIADR-VER", "Processor and auxiliary file versions used"),
        7: ("VIADR-VER-SM", "Processor and auxiliary file versions used"),
        8: ("VIADR-GRID", "Only used in SZF products")
    }
    mdr = {
        0: ("MDR-1A", "Level 1A measurement and associated data"),
        1: ("MDR-1B-125", "Only used in SZR products"),
        2: ("MDR-1B-250", "Only used in SZO products"),
        3: ("MDR-1B-FULL", "Only used in SZF products"),
        4: ("MDR-2-SM-125", "Only used in SMR products"),
        5: ("MDR-2-SM-250", "Only used in SMO products")
    }
    subclass = {
        "Main Product Header Record":              {0: "Unspecified"},
        "Secondary Product Header Record":         {1: "Unspecified"},
        "Internal Pointer Record":                 ipr,
        "Global External Auxiliary Data Record":   geadr,
        "Variable External Auxiliary Data Record": veadr,
        "Variable Internal Auxiliary Data Record": viadr,
        "Measurement Data Record":                 mdr
    }
    subclass_name = subclass[class_name][subclass_id]
    return subclass_name


def parse_instrument_group(index):
    instrument_group = {0: "GENERIC",
                        2: "ASCAT"
                        }
    return instrument_group[index]


def parse_short_time(days, ms):
    begin_datetime = datetime(2000, 1, 1, 0, 0, 0)
    return begin_datetime + timedelta(days=days, milliseconds=ms)


def parse_long_time(days, ms, mms):
    begin_datetime = datetime(2000, 1, 1, 0, 0, 0)
    return begin_datetime + timedelta(days=days, milliseconds=ms, microseconds=mms)


def read_grh_and_content(file_p):
    grh_size = 20
    grh_bytes = file_p.read(grh_size)
    grh_type = struct.Struct(">4b I HI HI")
    grh_tuple = grh_type.unpack(grh_bytes)

    grh = {
        "RECORD_CLASS":            (grh_tuple[0], parse_record_class(grh_tuple[0])),
        "INSTRUMENT_GROUP":        (grh_tuple[1], parse_instrument_group(grh_tuple[1])),
        "RECORD_SUBCLASS":         parse_record_subclass(grh_tuple[0], grh_tuple[2]),
        "RECORD_SUBCLASS_VERSION": grh_tuple[3],
        "RECORD_SIZE":             grh_tuple[4],
        "RECORD_START_TIME":       parse_short_time(grh_tuple[5], grh_tuple[6]),
        "RECORD_STOP_TIME":        parse_short_time(grh_tuple[7], grh_tuple[8])
    }

    content_size = grh["RECORD_SIZE"] - grh_size
    content = file_p.read(content_size)
    return grh, content


def unpack_viadr(subclass_name, content):
    types = {
        "VIADR-VER":    struct.Struct(">11b"),
        "VIADR-VER-SM": struct.Struct(">26b"),
        "VIADR-OA":     struct.Struct(">HIH 3q 3q 3i 36i"),
        "VIADR-GRID":   struct.Struct(">HI i 81i 81i 81i 81i")
    }

    unpacked = types[subclass_name].unpack(content)
    viadr_info = {
        "VIADR-OA":     {
            "AC_UTC_TIME":    parse_long_time(unpacked[0], unpacked[1], unpacked[2]),
            "AC_SV_POSITION": np.divide(unpacked[3:6], 1e4),
            "AC_SV_VELOCITY": np.divide(unpacked[6:9], 1e4),
            "ATT_YS_LAW":     np.divide(unpacked[9:12], 1e6),
            "ATT_DIST_LAW":   np.divide(unpacked[12:], 1e6)
        },
        "VIADR-VER":    {
            "PROCESSOR_VERSION1": unpacked[0],
            "PROCESSOR_VERSION2": unpacked[1],
            "PROCESSOR_VERSION3": unpacked[2],
            "PRC_VERSION1":       unpacked[3],
            "PRC_VERSION2":       unpacked[4],
            "INS_VERSION1":       unpacked[5],
            "INS_VERSION2":       unpacked[6],
            "NTB_VERSION1":       unpacked[7],
            "NTB_VERSION2":       unpacked[8],
            "XCL_VERSION1":       unpacked[9],
            "XCL_VERSION2":       unpacked[10]
        },
        "VIADR-VER-SM": {
            "SOMO_PROCESSOR_VERSION1": unpacked[11:12],
            "SOMO_PROCESSOR_VERSION2": unpacked[12:13],
            "SOMO_PROCESSOR_VERSION3": unpacked[13:14],
            "SMC_VERSION1":            unpacked[14:15],
            "SMC_VERSION2":            unpacked[15:16],
            "CURV-VERSION":            unpacked[16:17],
            "CURV-NOISE-VERSION":      unpacked[17:18],
            "DRY-VERSION":             unpacked[18:19],
            "DRY-NOISE-VERSION":       unpacked[19:20],
            "MS-MEAN-VERSION":         unpacked[20:21],
            "NONSCAT-VERSION":         unpacked[21:22],
            "SLOP-VERSION":            unpacked[22:23],
            "SLOP-NOISE-VERSION":      unpacked[23:24],
            "WET-VERSION":             unpacked[24:25],
            "WET-NOISE-VERSION":       unpacked[25:26]
        },
        "VIADR-GRID":   {
            "UTC_LINE_NODES":  parse_short_time(unpacked[0], unpacked[1]),
            "ABS_LINE_NUMBER": unpacked[2],
            "LATITUDE_LEFT":   np.divide(unpacked[3:84], 1e6),
            "LONGITUDE_LEFT":  np.divide(unpacked[84:165], 1e6),
            "LATITUDE_RIGHT":  np.divide(unpacked[165:246], 1e6),
            "LONGITUDE_RIGHT": np.divide(unpacked[246:327], 1e6)
        }
    }
    viadr_info["VIADR-VER-SM"].update(viadr_info["VIADR-VER"])
    return viadr_info[subclass_name]


def unpack_mdr(subclass_name, content):
    b_250 = ">? ? HI i H ? 42? 42i 42i 126i 126H 126H 126h 126I 126? 126b 126H 126H 126H 126H 126H 126H 126H"
    b_125 = b_250.replace("42", "82").replace("126", "246")
    sm_250 = b_250 + "H H 42H 42H 42i 42i 42i 42i 42I 42i 42i 42H 42B 42B 42H 42B 42B 42B 42B 42B"
    sm_125 = sm_250.replace("42", "82").replace("126", '246')
    types = {
        "MDR-1B-250":   struct.Struct(b_250),
        "MDR-1B-125":   struct.Struct(b_125),
        "MDR-1B-FULL":  struct.Struct(">? ? HI H ? B 192i 192H 192h 192i 192i 192H B B B B 192B"),
        "MDR-2-SM-250": struct.Struct(sm_250),
        "MDR-2-SM-125": struct.Struct(sm_125)
    }
    mdr_tuple = types[subclass_name].unpack(content)
    mdr_info = {
        "MDR-1B-250":   {
            "DEGRADED_INST_MDR": mdr_tuple[0],
            "DEGRADED_PROC_MDR": mdr_tuple[1],
            "UTC_LINE_NODES":    parse_short_time(mdr_tuple[2], mdr_tuple[3]),
            "ABS_LINE_NUMBER":   mdr_tuple[4],
            "SAT_TRACK_AZI":     np.divide(mdr_tuple[5], 1e2),
            "AS_DES_PASS":       mdr_tuple[6],
            "SWATH INDICATOR":   mdr_tuple[7:49],
            "LATITUDE":          np.divide(mdr_tuple[49:91], 1e6),
            "LONGITUDE":         np.divide(mdr_tuple[91:133], 1e6),
            "SIGMA0_TRIP":       np.divide(mdr_tuple[133:259], 1e6),
            "KP":                np.divide(mdr_tuple[259:385], 1e4),
            "INC_ANGLE_TRIP":    np.divide(mdr_tuple[385:511], 1e2),
            "AZI_ANGLE_TRIP":    np.divide(mdr_tuple[511:637], 1e2),
            "NUM_VAL_TRIP":      mdr_tuple[637:763],
            "F_KP":              mdr_tuple[763:889],
            "F_USABLE":          mdr_tuple[889:1015],
            "F_F":               np.divide(mdr_tuple[1015:1141], 1e3),
            "F_V":               np.divide(mdr_tuple[1141:1267], 1e3),
            "F_OA":              np.divide(mdr_tuple[1267:1393], 1e3),
            "F_SA":              np.divide(mdr_tuple[1393:1519], 1e3),
            "F_TEL":             np.divide(mdr_tuple[1519:1645], 1e3),
            "F_REF":             np.divide(mdr_tuple[1645:1771], 1e3),
            "F_LAND":            np.divide(mdr_tuple[1771:1897], 1e3)
        },
        "MDR-1B-125":   {
            "DEGRADED_INST_MDR": mdr_tuple[0],
            "DEGRADED_PROC_MDR": mdr_tuple[1],
            "UTC_LINE_NODES":    parse_short_time(mdr_tuple[2], mdr_tuple[3]),
            "ABS_LINE_NUMBER":   mdr_tuple[4],
            "SAT_TRACK_AZI":     np.divide(mdr_tuple[5], 1e2),
            "AS_DES_PASS":       mdr_tuple[6],
            "SWATH INDICATOR":   mdr_tuple[7:89],
            "LATITUDE":          np.divide(mdr_tuple[89:171], 1e6),
            "LONGITUDE":         np.divide(mdr_tuple[171:253], 1e6),
            "SIGMA0_TRIP":       np.divide(mdr_tuple[253:499], 1e6),
            "KP":                np.divide(mdr_tuple[499:745], 1e4),
            "INC_ANGLE_TRIP":    np.divide(mdr_tuple[745:991], 1e2),
            "AZI_ANGLE_TRIP":    np.divide(mdr_tuple[991:1237], 1e2),
            "NUM_VAL_TRIP":      mdr_tuple[1237:1483],
            "F_KP":              mdr_tuple[1483:1729],
            "F_USABLE":          mdr_tuple[1729:1975],
            "F_F":               np.divide(mdr_tuple[1975:2221], 1e3),
            "F_V":               np.divide(mdr_tuple[2221:2467], 1e3),
            "F_OA":              np.divide(mdr_tuple[2467:2713], 1e3),
            "F_SA":              np.divide(mdr_tuple[2713:2959], 1e3),
            "F_TEL":             np.divide(mdr_tuple[2959:3205], 1e3),
            "F_REF":             np.divide(mdr_tuple[3205:3451], 1e3),
            "F_LAND":            np.divide(mdr_tuple[3451:3697], 1e3)
        },
        "MDR-1B-FULL":  {
            "DEGRADED_INST_MDR": mdr_tuple[0],
            "DEGRADED_PROC_MDR": mdr_tuple[1],
            "UTC_LOCALISATION":  parse_short_time(mdr_tuple[2], mdr_tuple[3]),
            "SAT_TRACK_AZI":     np.divide(mdr_tuple[4], 1e2),
            "AS_DES_PASS":       mdr_tuple[5],
            "BEAM_NUMBER":       mdr_tuple[6],
            "SIGMA0_FULL":       np.divide(mdr_tuple[6:198], 1e6),
            "INC_ANGLE_FULL":    np.divide(mdr_tuple[198:390], 1e2),
            "AZI_ANGLE_FULL":    np.divide(mdr_tuple[390:582], 1e2),
            "LATITUDE_FULL":     np.divide(mdr_tuple[582:774], 1e6),
            "LONGITUDE_FULL":    np.divide(mdr_tuple[774:966], 1e6),
            "LAND_FRAC":         np.divide(mdr_tuple[966:1158], 1e2),
            "FLAGFIELD_RF1":     mdr_tuple[1158],
            "FLAGFIELD_RF2":     mdr_tuple[1159],
            "FLAGFIELD_PL":      mdr_tuple[1160],
            "FLAGFIELD_GEN1":    mdr_tuple[1161],
            "FLAGFIELD_GEN2":    mdr_tuple[1162]
        },
        "MDR-2-SM-250": {
            "WARP_NRT_VERSION":          mdr_tuple[1897:1898],
            "PARAM_DB_VERSION":          mdr_tuple[1898:1899],
            "SOIL_MOISTURE":             np.divide(mdr_tuple[1899:1941], 1e2),
            "SOIL_MOISTURE_ERROR":       np.divide(mdr_tuple[1941:1983], 1e2),
            "SIGMA40":                   np.divide(mdr_tuple[1983:2025], 1e6),
            "SIGMA40_ERROR":             np.divide(mdr_tuple[2025:2067], 1e6),
            "SLOPE40":                   np.divide(mdr_tuple[2067:2109], 1e6),
            "SLOPE40_ERROR":             np.divide(mdr_tuple[2109:2151], 1e6),
            "SOIL_MOISTURE_SENSITIVITY": np.divide(mdr_tuple[2151:2193], 1e6),
            "DRY_BACKSCATTER":           np.divide(mdr_tuple[2193:2235], 1e6),
            "WET_BACKSCATTER":           np.divide(mdr_tuple[2235:2277], 1e6),
            "MEAN_SURF_SOIL_MOISTURE":   np.divide(mdr_tuple[2277:2319], 1e2),
            "RAINFALL_FLAG":             mdr_tuple[2319:2361],
            "CORRECTION_FLAGS":          mdr_tuple[2361:2403],
            "PROCESSING_FLAGS":          mdr_tuple[2403:2445],
            "AGGREGATED_QUALITY_FLAG":   mdr_tuple[2445:2487],
            "SNOW_COVER_PROBABILITY":    mdr_tuple[2487:2529],
            "FROZEN_SOIL_PROBABILITY":   mdr_tuple[2529:2571],
            "INUNDATION_OR_WETLAND":     mdr_tuple[2571:2613],
            "TOPOGRAPHICAL_COMPLEXITY":  mdr_tuple[2613:2655]
        },
        "MDR-2-SM-125": {
            "WARP_NRT_VERSION":          mdr_tuple[3697:3698],
            "PARAM_DB_VERSION":          mdr_tuple[3698:3699],
            "SOIL_MOISTURE":             np.divide(mdr_tuple[3699:3781], 1e2),
            "SOIL_MOISTURE_ERROR":       np.divide(mdr_tuple[3781:3863], 1e2),
            "SIGMA40":                   np.divide(mdr_tuple[2863:3945], 1e6),
            "SIGMA40_ERROR":             np.divide(mdr_tuple[3945:4027], 1e6),
            "SLOPE40":                   np.divide(mdr_tuple[4027:4109], 1e6),
            "SLOPE40_ERROR":             np.divide(mdr_tuple[4109:4191], 1e6),
            "SOIL_MOISTURE_SENSITIVITY": np.divide(mdr_tuple[4191:4273], 1e6),
            "DRY_BACKSCATTER":           np.divide(mdr_tuple[4273:4355], 1e6),
            "WET_BACKSCATTER":           np.divide(mdr_tuple[4355:4437], 1e6),
            "MEAN_SURF_SOIL_MOISTURE":   np.divide(mdr_tuple[4437:4519], 1e2),
            "RAINFALL_FLAG":             mdr_tuple[4519:4601],
            "CORRECTION_FLAGS":          mdr_tuple[4601:4683],
            "PROCESSING_FLAGS":          mdr_tuple[4683:4765],
            "AGGREGATED_QUALITY_FLAG":   mdr_tuple[4765:4847],
            "SNOW_COVER_PROBABILITY":    mdr_tuple[4847:4929],
            "FROZEN_SOIL_PROBABILITY":   mdr_tuple[4929:5011],
            "INUNDATION_OR_WETLAND":     mdr_tuple[5011:5093],
            "TOPOGRAPHICAL_COMPLEXITY":  mdr_tuple[5093:5175]
        }
    }
    mdr_info["MDR-2-SM-250"].update(mdr_info["MDR-1B-250"])
    mdr_info["MDR-2-SM-125"].update(mdr_info["MDR-1B-125"])
    return mdr_info[subclass_name]


class Reader:
    def __init__(self, filename: str):
        self.__product_level = None
        self.__header = {"mphr": {}, "sphr": {}}
        self.__pointer = []
        self.__gad = {"geadr": [], "giadr": []}
        self.__vad = {"veadr": [], "viadr": []}
        self.__body = {"mdr": {}}
        with open(filename, "rb") as nat:
            self.__parse_header(nat)

            self.__parse_pointer(nat)

            # 格式版本判断，及时停止，以免读取Body时出错
            file_main_ver = self.__header["mphr"]["FORMAT_MAJOR_VERSION"]
            file_ver_2 = self.__header["mphr"]["FORMAT_MINOR_VERSION"]
            if file_main_ver != "12" and file_ver_2 != "0":
                raise Exception("次文件版本的内容作者还未整合，请联系程序作者")

            self.__parse_gad(nat)
            #
            self.__parse_vad(nat)
            #
            self.__parse_mdr(nat)

    def __parse_header(self, file_p):
        grh, content_bytes = read_grh_and_content(file_p)
        content = content_bytes.decode().replace(" ", "")

        mphr_content = dict(item.split("=") for item in content.splitlines())
        self.__header["mphr"] = mphr_content
        self.__product_level = mphr_content["PROCESSING_LEVEL"]

        if self.__header["mphr"]["TOTAL_SPHR"] != "0":
            grh, content_bytes = read_grh_and_content(file_p)
            content = content_bytes.decode().replace(" ", "")
            sphr_content = dict(item.split("=") for item in content.splitlines())
            self.__header["sphr"] = sphr_content

    def __parse_pointer(self, file_p):
        ipr_type = struct.Struct(">3bI")
        ipr_count = self.__header["mphr"]["TOTAL_IPR"]
        for i in range(int(ipr_count)):
            grh, content_bytes = read_grh_and_content(file_p)

            unpacked = ipr_type.unpack(content_bytes)

            body = {
                "TARGET_RECORD_CLASS":     parse_record_class(unpacked[0]),
                "TARGET_INSTRUMENT_GROUP": parse_instrument_group(unpacked[1]),
                "TARGET_RECORD_SUBCLASS":  parse_record_subclass(unpacked[0], unpacked[2]),
                "TARGET_RECORD_OFFSET":    unpacked[3]
            }

            self.__pointer.append(body)

    def __parse_gad(self, file_p):
        geadr_count = self.__header["mphr"]["TOTAL_GEADR"]
        giadr_count = self.__header["mphr"]["TOTAL_GIADR"]
        for i in range(int(geadr_count)):
            grh, content_bytes = read_grh_and_content(file_p)
            self.__gad["geadr"].append(content_bytes.decode().strip())

        for i in range(int(giadr_count)):
            grh, content_bytes = read_grh_and_content(file_p)
            self.__gad["giadr"].append(content_bytes.decode().strip())

    def __parse_vad(self, file_p):
        veadr_count = self.__header["mphr"]["TOTAL_VEADR"]
        for i in range(int(veadr_count)):
            grh, content_bytes = read_grh_and_content(file_p)
            self.__vad["veadr"].append(content_bytes.decode().strip())

        viadr_count = self.__header["mphr"]["TOTAL_VIADR"]
        for i in range(int(viadr_count)):
            grh, content_bytes = read_grh_and_content(file_p)
            viadr = unpack_viadr(grh["RECORD_SUBCLASS"][0], content_bytes)
            self.__vad["viadr"].append(viadr)

    def __parse_mdr(self, file_p):
        mdr_contents = {}
        line_number = int(self.__header["mphr"]["TOTAL_MDR"])
        for i in range(line_number):
            grh, content_bytes = read_grh_and_content(file_p)

            subclass_name = grh["RECORD_SUBCLASS"][0]

            mdr_content = unpack_mdr(subclass_name, content_bytes)

            try:
                col_number = len(mdr_content["SWATH INDICATOR"])
            except KeyError:
                col_number = len(mdr_content["SIGMA0_FULL"])

            key_shape = {
                1:              (1, line_number, 1),
                col_number:     (1, line_number, col_number),
                col_number * 3: (3, line_number, col_number)
            }

            for key, item in mdr_content.items():
                item = np.array(item)
                shape = key_shape[item.size]
                if i == 0:
                    mdr_contents[key] = np.empty(shape=shape, dtype=item.dtype)
                if shape[0] == 3:
                    item = item.reshape((3, col_number), order="F")
                mdr_contents[key][:, i, :] = item
        self.__body["mdr"] = mdr_contents

    # ------------------------public 接口 ----------------------
    def get_mphr(self):
        return self.__header["mphr"]

    def get_sphr(self):
        return self.__header["sphr"]

    def get_pointer(self):
        return self.__pointer

    def get_gad(self):
        return self.__gad

    def get_veadr(self):
        return self.__vad["veadr"]

    def get_viadr(self):
        return self.__vad["viadr"]

    def get_mdr(self):
        return self.__body["mdr"]

    def get_product_level(self):
        return self.__product_level

    def get_datasets_name(self):
        return self.__body["mdr"].keys()


# ======================= Downloader 模块 ====================

def file_right(file_path, file_md5) -> bool:
    """
    验证该文件是否存在，且是否下载完成（md5匹配）

    :param file_path: 文件的路径
    :param file_md5: 文件的真实 md5
    :return: True or False
    """
    md5_returned = ""
    if os.path.exists(file_path):
        with open(file_path, mode="rb") as file_check:
            md5_returned = hashlib.md5(file_check.read()).hexdigest()
    return file_md5 == md5_returned


def set_aria2c():
    """
    返回自带的aria2c.exe的绝对路径

    :return: 自带的aria2c.exe的绝对路径
    """
    system = platform.system()
    if system == "Windows":
        filepath = os.path.dirname(__file__)
        aria2c_path = os.path.join(filepath, "aria2c.exe")
    else:
        p = subprocess.run(["which", "aria2c"], capture_output=True)
        aria2c_path = p.stdout.decode().strip()
        if aria2c_path == "":
            print("aria2c 未安装，请先安装.")
            raise Exception("aria2c 未安装，无法下载")
    print("使用", aria2c_path, "下载")
    return aria2c_path


class Downloader:
    def __init__(self, product_id: str):
        self._key = None
        self._bbox = None
        self._token = None
        self._filelist = []
        self._secret = None
        self._dt_end = None
        self._pi = product_id
        self._dt_start = None
        self._save_path = None
        self._search_url = None
        self._token_start = None
        self._token_expires = None
        self._filelist_save = None
        self._total_file_count = None

    def set_credentials(self, key: str, secret: str):
        self._key = key
        self._secret = secret

    def set_regions(self, bbox: list):
        self._bbox = ",".join(map(str, bbox))

    def set_temporal(self, dt_begin: datetime, dt_end: datetime):
        self._dt_start = dt_begin
        self._dt_end = dt_end

    def set_save_path(self, save_to):
        self._save_path = save_to

    def launch(self):
        print("开始检索")
        session_code = self.__session_encode()
        self._filelist_save = os.path.join(self._save_path, f"filelist-{session_code}.csv")
        if not os.path.exists(self._filelist_save):
            self.__search()
            self.__save_search_result()
        else:
            print("检测到可用的文件列表，将跳过在线检索")
        print("开始下载")
        self.__download()

    def __make_url(self, si):
        params = {"si":    si, "c": 500, "pi": self._pi, "bbox": self._bbox, "format": "json",
                  "dtend": self._dt_end.isoformat(), "dtstart": self._dt_start.isoformat()
                  }
        params = urllib.parse.urlencode(params)
        self._search_url = f"https://api.eumetsat.int/data/search-products/os?{params}"

    def __request_filelist(self):
        print(self._search_url)
        req = urllib.request.urlopen(self._search_url)
        if req.status != 200:
            raise Exception("请求失败")
        return_json = json.loads(req.read())
        self._total_file_count = int(return_json["properties"]["totalResults"])
        for feature in return_json["features"]:
            fileinfo = {"文件名":   feature["id"] + ".zip",
                        "下载链接": feature["properties"]["links"]["data"][0]["href"],
                        "md5":      feature["properties"]["extraInformation"]["md5"]
                        }
            self._filelist.append(fileinfo)

    def __save_search_result(self):
        with open(self._filelist_save, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["文件名", "下载链接", "md5"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self._filelist)

    def __session_encode(self):
        crc32 = zlib.crc32(f"{self._pi}{self._dt_start}{self._dt_end}{self._bbox}".encode())
        return crc32

    def __run_aria2c(self, aria2c_exe, download_link):
        subprocess.run(
            [aria2c_exe, "-c", '--allow-overwrite=true', "-x5", '-d', self._save_path,
             "--download-result=hide", f'--header=Authorization: Bearer {self._token}',
             download_link])

    def __search(self):
        this_page, start_index = 1, 0
        while True:
            print(f"正在检索第 {this_page} 页")
            self.__make_url(start_index), self.__request_filelist()
            if this_page == 1:
                total_pages = math.ceil(self._total_file_count / 500)
                print(f"共检索到 {self._total_file_count} 个目标文件。将分为 {total_pages} 页检索")
            print("已完成第", this_page, "页的信息检索")
            this_page += 1
            start_index += 500
            if start_index > self._total_file_count:
                break

    def __download(self):
        start = datetime.now()
        result_file = open(self._filelist_save, newline="", encoding="utf-8")
        lines = list(csv.DictReader(result_file))
        self._total_file_count = len(lines)

        self.__update_token()
        print("Token:", self._token)

        print("开始下载".center(30, "="))
        aria2c = set_aria2c()
        for i, line in enumerate(lines):
            print(f" 第 {i + 1} 个，共 {self._total_file_count} 个 ".center(50, "x"))
            if file_right(os.path.join(self._save_path, line["文件名"]), line["md5"]):
                print("文件已存在，跳过：", line["文件名"])
                continue
            if (datetime.now() - self._token_start).seconds > self._token_expires:
                self.__update_token()
            self.__run_aria2c(aria2c, line["下载链接"])
        print("所有下载已完成，耗时", datetime.now() - start)

    def __update_token(self):
        base64str = base64.b64encode(f"{self._key}:{self._secret}".encode()).decode()
        url = "https://api.eumetsat.int/token"
        data = b"grant_type=client_credentials"
        header = {"Authorization": f"Basic {base64str}"}
        req = urllib.request.Request(url, data=data, headers=header)

        with urllib.request.urlopen(req) as f:
            json_obj = json.loads(f.read())
            print(json_obj)
            self._token = json_obj["access_token"]
            self._token_expires = int(json_obj["expires_in"])
            self._token_start = datetime.now()
