import vnctptd
import inspect

def show_module_details(module):
    print("=" * 50)
    print(f"模块: {module.__name__}")
    print("=" * 50)

    # 遍历所有成员
    for name, member in inspect.getmembers(module):
        # 过滤内置成员
        if name.startswith("_"):
            continue

        # 如果是类
        if inspect.isclass(member):
            print(f"\n📦 类: {name}")
            for m_name, m_func in inspect.getmembers(member):
                if not m_name.startswith("_"):
                    print(f"  - {m_name}")

        # 如果是结构体/字段
        else:
            print(f"\n🔹 其他对象: {name}")

show_module_details(vnctptd)