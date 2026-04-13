#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTP 扩展模块安装文件
用于：pip install -e . 或 python setup_config.py install
"""

from setuptools import setup, Extension
import pybind11
import os
import platform

# 编译配置
system = platform.system()

# 根据不同平台设置编译参数
if system == 'Windows':
    include_dirs = [
        'fw_vnpy_ctp/api/include/ctp',
        'fw_vnpy_ctp/api/include',
        'fw_vnpy_ctp/api/vnctp',
        pybind11.get_include(),
    ]
    library_dirs = ['fw_vnpy_ctp/api/libs']
    md_libraries = ['thostmduserapi_se']
    td_libraries = ['thosttraderapi_se']
    extra_compile_args = ['/MT', '/utf-8']
    extra_link_args = []
elif system == 'Darwin':  # macOS
    import os
    # 获取当前目录的绝对路径
    current_dir = os.path.abspath('.')
    api_dir = os.path.join(current_dir, 'fw_vnpy_ctp', 'api')
    
    include_dirs = [
        'fw_vnpy_ctp/api/include/mac/ctp',
        'fw_vnpy_ctp/api/include/ctp',
        'fw_vnpy_ctp/api/include',
        'fw_vnpy_ctp/api/vnctp',
        pybind11.get_include(),
    ]
    library_dirs = ['.', 'fw_vnpy_ctp/api']
    # 在 macOS 上，直接链接到实际的二进制文件
    md_libraries = []
    td_libraries = []
    extra_compile_args = ['-std=c++11', '-mmacosx-version-min=10.9']
    # 使用绝对路径设置 rpath 和链接库
    extra_link_args = [
        f'-Wl,-rpath,{api_dir}',
        os.path.join(api_dir, 'thostmduserapi_se.framework', 'Versions', 'A', 'thostmduserapi_se'),
        os.path.join(api_dir, 'thosttraderapi_se.framework', 'Versions', 'A', 'thosttraderapi_se')
    ]
else:  # Linux
    include_dirs = [
        'fw_vnpy_ctp/api/include/ctp',
        'fw_vnpy_ctp/api/include',
        'fw_vnpy_ctp/api/vnctp',
        pybind11.get_include(),
    ]
    library_dirs = ['fw_vnpy_ctp/api']
    md_libraries = ['thostmduserapi_se']
    td_libraries = ['thosttraderapi_se']
    extra_compile_args = ['-std=c++11']
    extra_link_args = ['-Wl,-rpath,./fw_vnpy_ctp/api']

# 编译配置
ext_modules = []

# 根据平台创建不同的扩展模块
if system == 'Darwin':  # macOS
    # 在 macOS 上，两个扩展模块使用相同的库文件
    ext_modules.append(Extension(
        'fw_vnpy_ctp.api.vnctpmd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctpmd/vnctpmd.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ))
    ext_modules.append(Extension(
        'fw_vnpy_ctp.api.vnctptd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctptd/vnctptd.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ))
else:
    # 在 Windows 和 Linux 上，分别指定不同的库
    ext_modules.append(Extension(
        'fw_vnpy_ctp.api.vnctpmd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctpmd/vnctpmd.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=md_libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ))
    ext_modules.append(Extension(
        'fw_vnpy_ctp.api.vnctptd',
        sources=['fw_vnpy_ctp/api/vnctp/vnctptd/vnctptd.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=td_libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ))

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