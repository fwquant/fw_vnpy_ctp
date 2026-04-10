#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTP 扩展模块安装文件
用于：pip install -e . 或 python setup_config.py install
"""

from setuptools import setup, Extension
import pybind11
import os

# 编译配置
ext_modules = [
    Extension(
        'fw_vnpy_ctp.api.vnctpmd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctpmd/vnctpmd.cpp'],
        include_dirs=[
            'fw_vnpy_ctp/api/include/ctp',      # CTP 头文件目录
            'fw_vnpy_ctp/api/include',          # 备用目录
            'fw_vnpy_ctp/api/vnctp',
            pybind11.get_include(),
        ],
        library_dirs=['fw_vnpy_ctp/api/libs'],
        libraries=['thostmduserapi_se'],
        extra_compile_args=['/MT', '/utf-8'] if os.name == 'nt' else [],
        # 注意：不要添加 runtime_library_dirs，MSVC 不支持
    ),
    Extension(
        'fw_vnpy_ctp.api.vnctptd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctptd/vnctptd.cpp'],
        include_dirs=[
            'fw_vnpy_ctp/api/include/ctp',
            'fw_vnpy_ctp/api/include',
            'fw_vnpy_ctp/api/vnctp',
            pybind11.get_include(),
        ],
        library_dirs=['fw_vnpy_ctp/api/libs'],
        libraries=['thosttraderapi_se'],
        extra_compile_args=['/MT', '/utf-8'] if os.name == 'nt' else [],
    ),
]

setup(
    name='fw_vnpy_ctp',
    version='6.7.11.4',
    description='VN.PY CTP Gateway',
    author='VN.PY Team',
    license='MIT',
    ext_modules=ext_modules,
    zip_safe=False,
    packages=['fw_vnpy_ctp', 'fw_vnpy_ctp.api', 'fw_vnpy_ctp.gateway'],
    package_dir={
        'fw_vnpy_ctp': 'fw_vnpy_ctp',
        'fw_vnpy_ctp.api': 'fw_vnpy_ctp/api',
        'fw_vnpy_ctp.gateway': 'fw_vnpy_ctp/gateway',
    },
    package_data={
        'fw_vnpy_ctp.api': ['*.dll', '*.pyd', '*.so'],
    },
    python_requires='>=3.7',
    install_requires=[
        'vnpy>=3.0.0',
        'pybind11>=2.10.0',
    ],
)