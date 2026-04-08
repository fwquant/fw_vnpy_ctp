#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTP 扩展模块安装文件
用于：pip install -e . 或 python setup.py install
"""

from setuptools import setup, Extension
import pybind11
import os

# 编译配置
ext_modules = [
    Extension(
        'vnpy_ctp.api.vnctpmd',
        sources=['vnpy_ctp/api/vnctp/vnctpmd/vnctpmd.cpp'],
        include_dirs=[
            'vnpy_ctp/api/include',
            'vnpy_ctp/api/vnctp',
            pybind11.get_include(),
        ],
        library_dirs=['vnpy_ctp/api/libs'],
        libraries=['thostmduserapi_se'],
        extra_compile_args=['/MT', '/utf-8'] if os.name == 'nt' else [],  # 添加 /utf-8
    ),
    Extension(
        'vnpy_ctp.api.vnctptd',
        sources=['vnpy_ctp/api/vnctp/vnctptd/vnctptd.cpp'],
        include_dirs=[
            'vnpy_ctp/api/include',
            'vnpy_ctp/api/vnctp',
            pybind11.get_include(),
        ],
        library_dirs=['vnpy_ctp/api/libs'],
        libraries=['thosttraderapi_se'],
        extra_compile_args=['/MT', '/utf-8'] if os.name == 'nt' else [],  # 添加 /utf-8
    ),
]

setup(
    name='vnpy_ctp',
    version='6.7.11.4',
    description='VN.PY CTP Gateway',
    author='VN.PY Team',
    license='MIT',
    ext_modules=ext_modules,
    zip_safe=False,
    packages=['vnpy_ctp', 'vnpy_ctp.api', 'vnpy_ctp.gateway'],
    package_dir={
        'vnpy_ctp': 'vnpy_ctp',
        'vnpy_ctp.api': 'vnpy_ctp/api',
        'vnpy_ctp.gateway': 'vnpy_ctp/gateway',
    },
    package_data={
        'vnpy_ctp.api': ['*.dll', '*.pyd', '*.so'],
    },
    python_requires='>=3.7',
    install_requires=[
        'vnpy>=3.0.0',
        'pybind11>=2.10.0',
    ],
)