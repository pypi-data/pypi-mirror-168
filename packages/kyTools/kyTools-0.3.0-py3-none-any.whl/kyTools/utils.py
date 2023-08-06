import os
import platform
import subprocess


def call_gmt(gmt_command: str):
    """
    在Python代码中调用gmt脚本命令
    :param gmt_command: gmt脚本命令
    :return: 无
    """
    this_system = platform.system()

    script_file = "gmt_command.bat"
    if this_system != "Windows":
        script_file = "gmt_command.sh"
    with open(script_file, mode="w", encoding="utf-8") as bat:
        bat.write(gmt_command)
        bat.flush()

        args = ["cmd", "/c", bat.name]
        if this_system != "Windows":
            args = ["bash", bat.name]

        try:
            subprocess.run(args=args)
        except FileNotFoundError:
            raise Exception("gmt 未正确安装，请检查")

    os.remove(bat.name)
