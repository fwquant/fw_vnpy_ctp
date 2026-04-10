import os
import sys

# 添加 DLL 路径
api_path = r"D:\GIT\github\fwquant\fw_vnpy_ctp\fw_vnpy_ctp\api"
os.add_dll_directory(api_path)

# 直接导入测试
import vnctpmd
print("✓ vnctpmd 导入成功")

from fw_vnpy_ctp.api import MdApi
print("✓ MdApi 导入成功")