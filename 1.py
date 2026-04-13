from fw_vnpy_ctp.api import MdApi, TdApi

# 测试创建 API 实例
md_api = MdApi()
td_api = TdApi()

# 测试获取 API 版本（如果支持）
if hasattr(md_api, 'GetApiVersion'):
    print(f"API 版本: {md_api.GetApiVersion()}")

print("✅ API 实例创建成功！")
