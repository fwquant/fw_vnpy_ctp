第N次更新步骤（如果是第一次，请看最后面的《第一次步骤》，当前为后面用得较多次数准备的。）：
1、下载文件，下载需要更新的 SIMNOW api 文件包 https://www.simnow.com.cn/static/apiDownload.action
2、准备    解压后的文件  (MACOS直接替换即可，下面不用管：thostmduserapi_se.framework和thosttraderapi_se.framework)
    复制
    把所有    .dll   文件复制到   fw_vnpy_ctp/api 目录下
    把所有    .h     文件复制到   fw_vnpy_ctp/api/include/ctp 目录下
    把所有    .lib   文件复制到   fw_vnpy_ctp/api/libs 目录下
3、运行        py install.py
    选择 1 菜单 完整构建 (清理 + 编译 + 验证)
    等待编译完成
4、验证        打开pycharm找到 script\run.py 右键点击 运行
    成功运行并能连接到 SIMNOW 交易接口 表示 成功。







第一次步骤：

1、克隆代码：pycharm,菜单，来自版本控制的项目：https://github.com/fwquant/fw_vnpy_ctp.git
2、创建虚拟环境：.venv  并激活
3、下载需要更新的 SIMNOW api 文件包 https://www.simnow.com.cn/static/apiDownload.action
4、解压后的文件
    复制
    把所有    .dll   文件复制到   vnpy_ctp/api 目录下
    把所有    .h     文件复制到   vnpy_ctp/api/include/ctp 目录下
    把所有    .lib   文件复制到   vnpy_ctp/api/libs 目录下
5、安装VNPY,MSVC:
    安装VNPY:
        pip install vnpy
    安装MSVC   :    https://visualstudio.microsoft.com/zh-hans/vs/community/    
    勾选以下几项：    
        使用 C++ 的桌面开发
        MSVC v143 - VS 2022 C++ x64/x86 生成工具
        Windows 11 SDK 或 Windows 10 SDK
    安装完成后，重启操作系统 
6、运行：   py 重新清理编译验证CTP.py   
    输入 1 确认 完整构建 (清理 + 编译 + 验证)
    等待编译完成
7、打开pycharm找到 script\run.py 右键点击 运行


其他资料：
    everything: "C:\Users\DT2025\Downloads\"    path:64_se *.h|*.lib|*.dll
    上面的 "C:\Users\DT2025\Downloads\v6.7.13_20260225" 请换成你解压后的文件路径







说明：
1、  编译脚本：       /fw_vnpy_ctp/install.py
    验证脚本：       /fw_vnpy_ctp/script/run.py
    功能 ：兼容 WINDOWS,MAC。
    
    MACOS
        编译前更新：文件来自 SIMNOW api 文件包中的文件，例 ：https://www.simnow.com.cn/static/apiDownload.action   左边 MACOS 版本的文件 替换下面文件夹
            /fw_vnpy_ctp/fw_vnpy_ctp/api/thostmduserapi_se.framework
            /fw_vnpy_ctp/fw_vnpy_ctp/api/thosttraderapi_se.framework
        编译后的扩展名为.so      
        例 ：/fw_vnpy_ctp/fw_vnpy_ctp/api/vnctptd.cpython-310-darwin.so


    windows
        编译前更新：文件来自 SIMNOW api 文件包中的文件，例 ：https://www.simnow.com.cn/static/apiDownload.action   左边 PC 版本的文件 替换下面文件
            /fw_vnpy_ctp/api/include/ctp/ThostFtdcMdApi.h
            /fw_vnpy_ctp/api/include/ctp/ThostFtdcTraderApi.h
            /fw_vnpy_ctp/api/include/ctp/ThostFtdcUserApiDataType.h
            /fw_vnpy_ctp/api/include/ctp/ThostFtdcUserApiStruct.h


            /fw_vnpy_ctp/fw_vnpy_ctp/api/thosttraderapi_se.dll
            /fw_vnpy_ctp/fw_vnpy_ctp/api/thostmduserapi_se.dll

            /fw_vnpy_ctp/api/libs/thostmduserapi_se.lib
            /fw_vnpy_ctp/api/libs/thosttraderapi_se.lib

        编译后为 .pyd        
            例 ：/fw_vnpy_ctp/fw_vnpy_ctp/api/vnctptd.cpython-310-win_amd64.pyd





