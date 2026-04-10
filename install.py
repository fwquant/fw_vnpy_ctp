#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTP 扩展模块统一编译工具
支持：编译、清理、验证、交互式菜单
"""

import subprocess
import sys
import os
import shutil
import glob
import re
from datetime import datetime


def print_step(step, message):
    """打印步骤信息"""
    print(f"\n[ {step} ] {message}")


def print_success(message):
    """打印成功信息"""
    print(f"✓ {message}")


def print_error(message):
    """打印错误信息"""
    print(f"✗ {message}")


def print_info(message):
    """打印信息"""
    print(f"➜ {message}")


def print_title(message):
    """打印标题"""
    print(f"\n{'=' * 60}")
    print(f"{message.center(60)}")
    print(f"{'=' * 60}")


def clean_build_files():
    """清理编译文件"""
    print_step("1/4", "清理旧文件")

    dirs_to_clean = [
        'build',
        'fw_vnpy_ctp.egg-info',
        'fw_vnpy_ctp/api/__pycache__',
        'fw_vnpy_ctp/__pycache__',
        'fw_vnpy_ctp/gateway/__pycache__',
    ]

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print_info(f"删除目录: {dir_name}")

    # 删除所有 .pyd 文件
    pyd_files = glob.glob("fw_vnpy_ctp/api/*.pyd")
    for f in pyd_files:
        os.remove(f)
        print_info(f"删除文件: {os.path.basename(f)}")

    print_success("清理完成")
    return True


def compile_extensions():
    """编译扩展模块"""
    print_step("2/4", "编译 C++ 扩展模块")

    # 使用 Popen 实时显示输出，过滤乱码
    process = subprocess.Popen(
        [sys.executable, "setup_config.py", "build_ext", "--inplace"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=False  # 以字节模式处理
    )

    # 编译进度标志
    compile_started = False
    link_started = False
    current_file = ""

    for line_bytes in process.stdout:
        # 解码为字符串，尝试多种编码
        line = None
        for encoding in ['gbk', 'utf-8', 'ascii']:
            try:
                line = line_bytes.decode(encoding, errors='strict')
                break
            except:
                continue

        if line is None:
            line = line_bytes.decode('gbk', errors='ignore')

        # 过滤掉乱码行（包含常见乱码字符的行）
        garbage_patterns = [
            '鏂囦欢', '寮', '鍛戒护', 'Warning', 'warning C',
            '姝ｅ湪', '鍒涘缓', '鐢熸垚', '杩炴帴', '宸插紑濮'
        ]

        skip_line = False
        for pattern in garbage_patterns:
            if pattern in line:
                skip_line = True
                break

        if skip_line:
            continue

        # 提取有用的信息
        line = line.strip()
        if not line:
            continue

        # 显示编译进度
        if 'cl.exe' in line and '/c' in line:
            # 提取正在编译的源文件
            match = re.search(r'([\w]+\.cpp)', line)
            if match:
                current_file = match.group(1)
                if not compile_started:
                    print_info("正在编译源文件...")
                    compile_started = True
                print(f"  编译: {current_file}")

        elif 'link.exe' in line:
            if not link_started:
                print_info("正在链接生成扩展模块...")
                link_started = True

        elif 'Creating library' in line or '生成代码' in line:
            # 跳过这些信息
            continue

        elif 'build_ext' in line or 'running build_ext' in line:
            print_info("开始构建扩展模块...")

        elif 'building' in line and 'extension' in line:
            print_info(f"构建目标: {line}")

        elif 'error' in line.lower() or 'failed' in line.lower():
            # 显示错误信息
            print_error(line)

        elif 'success' in line.lower() or 'completed' in line.lower():
            print_success(line)

    process.wait()

    if process.returncode != 0:
        print_error(f"编译失败，错误码: {process.returncode}")
        return False

    print_success("编译完成")
    return True


def copy_pyd_files():
    """复制编译好的 .pyd 文件"""
    print_step("3/4", "安装扩展模块")

    # 查找编译输出目录
    build_dirs = []
    if os.path.exists('build'):
        for item in os.listdir('build'):
            if item.startswith('lib.win-amd64-cpython'):
                build_dirs.append(os.path.join('build', item, 'fw_vnpy_ctp', 'api'))

    if not build_dirs:
        print_error("未找到编译输出文件")
        return False

    copied = False
    for src_dir in build_dirs:
        if os.path.exists(src_dir):
            for file in os.listdir(src_dir):
                if file.endswith('.pyd'):
                    src = os.path.join(src_dir, file)
                    dst = os.path.join('fw_vnpy_ctp/api', file)
                    shutil.copy2(src, dst)
                    print_info(f"复制: {file}")
                    copied = True

    if copied:
        print_success("安装完成")
        return True
    else:
        print_error("未找到 .pyd 文件")
        return False


def get_ctp_version():
    """从头文件中获取 CTP API 版本"""
    version_file = "fw_vnpy_ctp/api/include/ThostFtdcUserApiStruct.h"
    if not os.path.exists(version_file):
        return None

    try:
        with open(version_file, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()

            # 查找版本号
            patterns = [
                r'#define\s+USER_API_VERSION\s+"([^"]+)"',
                r'#define\s+API_VERSION\s+"([^"]+)"',
                r'USER_API_VERSION\s+"([^"]+)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)

            # 如果找不到，尝试查找日期版本
            date_pattern = r'(\d{8})'
            dates = re.findall(date_pattern, content)
            if dates:
                return f"CTP API ({dates[0]})"

        return "未知版本"
    except:
        return "无法读取"


def get_ctp_version():
    """从头文件中获取 CTP API 版本"""
    version_file = "fw_vnpy_ctp/api/include/ThostFtdcUserApiStruct.h"
    if not os.path.exists(version_file):
        return None

    try:
        with open(version_file, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()

            # 查找版本号
            patterns = [
                r'#define\s+USER_API_VERSION\s+"([^"]+)"',
                r'#define\s+API_VERSION\s+"([^"]+)"',
                r'USER_API_VERSION\s+"([^"]+)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)

            # 如果找不到，尝试查找日期版本
            date_pattern = r'(\d{8})'
            dates = re.findall(date_pattern, content)
            if dates:
                return f"CTP API ({dates[0]})"

        return "未知版本"
    except:
        return "无法读取"


def verify_import():
    """验证模块导入"""
    print_step("4/4", "验证模块")

    # 确保当前目录在路径最前面
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir in sys.path:
        sys.path.remove(current_dir)
    sys.path.insert(0, current_dir)

    # 移除可能干扰的模块
    modules_to_remove = ['_fw_vnpy_ctp_editable_loader', 'fw_vnpy_ctp', 'fw_vnpy_ctp.api']
    for module in modules_to_remove:
        if module in sys.modules:
            del sys.modules[module]

    try:
        # 注意：是 TdApi 不是 TradeApi
        from fw_vnpy_ctp.api import MdApi, TdApi
        import fw_vnpy_ctp

        print_success("✅ MdApi 导入成功")
        print_success("✅ TdApi 导入成功")

        # 获取版本信息
        print(f"\n{'=' * 50}")
        print("📦 模块详细信息:")
        print(f"{'=' * 50}")

        # 1. 包版本
        try:
            version = fw_vnpy_ctp.__version__
            print(f"  📌 包版本: {version}")
        except AttributeError:
            # 尝试从 setup_config.py 读取
            setup_file = "setup_config.py"
            if os.path.exists(setup_file):
                with open(setup_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
                    if match:
                        print(f"  📌 包版本: {match.group(1)}")
                    else:
                        print(f"  ⚠️ 包版本: 未知")
            else:
                print(f"  ⚠️ 包版本: 未知")

        # 2. CTP API 版本
        ctp_version = get_ctp_version()
        if ctp_version:
            print(f"  📌 CTP API 版本: {ctp_version}")

        # 3. 尝试获取 API 运行时版本
        try:
            # 创建临时实例获取版本
            md_api = MdApi()
            if hasattr(md_api, 'GetApiVersion'):
                api_version = md_api.GetApiVersion()
                print(f"  📌 API 运行时版本: {api_version}")
        except Exception as e:
            pass

        # 4. 模块文件路径
        print(f"\n  📁 模块路径:")
        print(f"    MdApi: {MdApi.__module__}")
        print(f"    TdApi: {TdApi.__module__}")

        # 5. 查找扩展文件详情
        import glob
        pyd_files = glob.glob("fw_vnpy_ctp/api/*.pyd") + glob.glob("fw_vnpy_ctp/api/*.so")
        if pyd_files:
            print(f"\n  🔧 扩展文件:")
            for f in sorted(pyd_files):
                file_stat = os.stat(f)
                file_size = file_stat.st_size / 1024
                mod_time = datetime.fromtimestamp(file_stat.st_mtime)
                mod_time_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"    📄 {os.path.basename(f)}")
                print(f"      大小: {file_size:.1f} KB")
                print(f"      修改: {mod_time_str}")

        # 6. 系统信息
        print(f"\n  💻 系统信息:")
        print(f"    Python: {sys.version.split()[0]}")
        print(f"    平台: {sys.platform}")
        if sys.platform == 'win32':
            print(f"    架构: {'64位' if sys.maxsize > 2 ** 32 else '32位'}")

        # 7. 依赖库检查
        print(f"\n  📚 依赖检查:")

        # pybind11
        try:
            import pybind11
            print(f"    ✅ pybind11: {pybind11.__version__}")
        except ImportError:
            print(f"    ❌ pybind11: 未安装")

        # vnpy
        try:
            import vnpy
            print(f"    ✅ vnpy: {vnpy.__version__}")
        except ImportError:
            print(f"    ❌ vnpy: 未安装")

        # numpy (可选)
        try:
            import numpy
            print(f"    ✅ numpy: {numpy.__version__}")
        except ImportError:
            print(f"    ⚠️ numpy: 未安装 (可选)")

        print(f"{'=' * 50}")

        return True

    except ImportError as e:
        print_error(f"❌ 导入失败: {e}")

        # 检查文件是否存在（注意不要重复导入 glob）
        import glob
        pyd_files = glob.glob("fw_vnpy_ctp/api/*.pyd")
        if pyd_files:
            print(f"\n📁 找到 .pyd 文件: {[os.path.basename(f) for f in pyd_files]}")
        else:
            print("\n⚠️ 未找到 .pyd 文件，编译可能未完成")

        # 检查 __init__.py 内容
        init_file = "fw_vnpy_ctp/api/__init__.py"
        if os.path.exists(init_file):
            print(f"\n📄 检查 {init_file}:")
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"  {content.strip()}")

        print("\n🔍 可能原因:")
        print("  1. 编译未完成或失败")
        print("  2. __init__.py 中未正确导出 TdApi")
        print("  3. DLL 文件缺失")
        print("  4. Python 版本不匹配")
        return False


def show_help():
    """显示帮助信息"""
    print_title("CTP 扩展模块编译工具")
    print("""
使用方法:
    python build.py --all       清理、编译、验证（推荐）
    python build.py --clean     仅清理
    python build.py --build     仅编译
    python build.py --verify    仅验证

交互式菜单:
    python build.py             显示交互式菜单

注意:
    - 需要已安装 Visual Studio Build Tools
    - 需要已安装 pybind11: pip install pybind11
    - 编译前确保虚拟环境已激活
""")


def show_menu():
    """显示交互式菜单"""
    print_title("CTP 扩展模块编译工具")
    print("\n请选择操作:")
    print("  [1] 完整构建 (清理 + 编译 + 验证)")
    print("  [2] 仅清理")
    print("  [3] 仅编译")
    print("  [4] 仅验证")
    print("  [5] 显示帮助")
    print("  [0] 退出")
    print()


def interactive_mode():
    """交互式模式"""
    while True:
        show_menu()
        choice = input("请输入选项 [0-5]: ").strip()

        if choice == '0':
            print_info("退出程序")
            break
        elif choice == '1':
            do_full_build()
        elif choice == '2':
            do_clean_only()
        elif choice == '3':
            do_build_only()
        elif choice == '4':
            do_verify_only()
        elif choice == '5':
            show_help()
            input("\n按 Enter 键继续...")
        else:
            print_error("无效选项，请重新输入")

        print()


def do_full_build():
    """完整构建流程"""
    print_title("开始完整构建")

    success = True
    if not clean_build_files():
        success = False
    if success and not compile_extensions():
        success = False
    if success and not copy_pyd_files():
        success = False
    if success and not verify_import():
        success = False

    print_title("构建结果")
    if success:
        print_success("CTP 模块已就绪！")
        print("\n现在可以:")
        print("  python -c \"from fw_vnpy_ctp.api import MdApi, TdApi\"")
    else:
        print_error("构建失败，请检查错误信息")
        print("\n常见问题:")
        print("  1. 确保已安装 Visual Studio Build Tools")
        print("  2. 确保已安装 pybind11: pip install pybind11")
        print("  3. 检查 CTP API 文件是否完整")

    input("\n按 Enter 键继续...")


def do_clean_only():
    """仅清理"""
    print_title("清理编译文件")
    clean_build_files()
    input("\n按 Enter 键继续...")


def do_build_only():
    """仅编译"""
    print_title("编译扩展模块")
    if compile_extensions() and copy_pyd_files():
        print_success("编译完成")
    else:
        print_error("编译失败")
    input("\n按 Enter 键继续...")


def do_verify_only():
    """仅验证"""
    print_title("验证模块")
    verify_import()
    input("\n按 Enter 键继续...")


def main():
    """主函数"""
    import os
    print("当前工作目录:", os.getcwd())
    args = sys.argv[1:]

    # 无参数时进入交互式菜单
    if not args:
        interactive_mode()
        return 0

    # 处理命令行参数
    if '--help' in args or '-h' in args:
        show_help()
        return 0

    success = True

    if '--all' in args:
        print_title("开始完整构建")
        if not clean_build_files():
            success = False
        if success and not compile_extensions():
            success = False
        if success and not copy_pyd_files():
            success = False
        if success and not verify_import():
            success = False
    else:
        if '--clean' in args:
            success = clean_build_files() and success
        if '--build' in args:
            success = compile_extensions() and copy_pyd_files() and success
        if '--verify' in args:
            success = verify_import() and success

    # 输出最终结果
    print_title("操作结果")
    if success:
        print_success("操作成功！")
    else:
        print_error("操作失败，请检查错误信息")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
