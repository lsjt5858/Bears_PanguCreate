"""
数据生成器核心逻辑
"""
import random
import uuid as uuid_lib
from datetime import datetime, timedelta

DATA_TYPES = [
    {"id": "uuid", "name": "UUID", "icon": "🔑", "category": "identifier"},
    {"id": "number", "name": "数字", "icon": "🔢", "category": "identifier"},
    {"id": "string", "name": "随机字符串", "icon": "📝", "category": "identifier"},
    {"id": "boolean", "name": "布尔值", "icon": "✓", "category": "identifier"},
    {"id": "chineseName", "name": "中文姓名", "icon": "👤", "category": "personal"},
    {"id": "englishName", "name": "英文姓名", "icon": "👤", "category": "personal"},
    {"id": "email", "name": "邮箱", "icon": "📧", "category": "personal"},
    {"id": "chinesePhone", "name": "中国手机号", "icon": "📱", "category": "personal"},
    {"id": "phone", "name": "国际手机号", "icon": "📞", "category": "personal"},
    {"id": "chineseIdCard", "name": "身份证号", "icon": "🪪", "category": "personal"},
    {"id": "age", "name": "年龄", "icon": "🎂", "category": "personal"},
    {"id": "gender", "name": "性别", "icon": "⚧", "category": "personal"},
    {"id": "chineseAddress", "name": "中国地址", "icon": "📍", "category": "address"},
    {"id": "province", "name": "省份", "icon": "🗺️", "category": "address"},
    {"id": "city", "name": "城市", "icon": "🏙️", "category": "address"},
    {"id": "zipcode", "name": "邮编", "icon": "📮", "category": "address"},
    {"id": "date", "name": "日期", "icon": "📅", "category": "datetime"},
    {"id": "datetime", "name": "日期时间", "icon": "🕐", "category": "datetime"},
    {"id": "timestamp", "name": "时间戳", "icon": "⏱️", "category": "datetime"},
    {"id": "bankCard", "name": "银行卡号", "icon": "💳", "category": "finance"},
    {"id": "amount", "name": "金额", "icon": "💰", "category": "finance"},
    {"id": "url", "name": "URL", "icon": "🔗", "category": "internet"},
    {"id": "ip", "name": "IPv4", "icon": "🌐", "category": "internet"},
    {"id": "ipv6", "name": "IPv6", "icon": "🌐", "category": "internet"},
    {"id": "mac", "name": "MAC地址", "icon": "📶", "category": "internet"},
    {"id": "domain", "name": "域名", "icon": "🌍", "category": "internet"},
    {"id": "company", "name": "公司名称", "icon": "🏢", "category": "company"},
    {"id": "jobTitle", "name": "职位", "icon": "💼", "category": "company"},
    {"id": "paragraph", "name": "段落", "icon": "📄", "category": "text"},
    {"id": "sentence", "name": "句子", "icon": "💬", "category": "text"},
    {"id": "word", "name": "词语", "icon": "📝", "category": "text"},
]

# 数据源
SURNAMES = ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴", "徐", "孙", "马", "胡", "朱", "郭", "何", "罗", "高", "林"]
GIVEN_NAMES = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英", "华", "慧"]
ENGLISH_FIRST_NAMES = ["James", "John", "Robert", "Michael", "David", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]
ENGLISH_LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
PROVINCES = ["北京市", "上海市", "广东省", "江苏省", "浙江省", "山东省", "河南省", "四川省", "湖北省", "湖南省", "福建省", "安徽省", "河北省", "陕西省", "辽宁省"]
CITIES = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "重庆", "苏州", "天津", "青岛", "长沙", "郑州"]
DISTRICTS = ["朝阳区", "海淀区", "浦东新区", "天河区", "南山区", "江干区", "鼓楼区", "武侯区", "江汉区", "雁塔区"]
STREETS = ["中山路", "人民路", "解放路", "建设路", "和平路", "文化路", "科技路", "创新大道", "学院路", "商业街"]
COMPANY_SUFFIXES = ["科技有限公司", "网络科技有限公司", "信息技术有限公司", "电子商务有限公司", "软件开发有限公司", "数据服务有限公司", "智能科技有限公司", "云计算有限公司"]
COMPANY_PREFIXES = ["华", "中", "东", "南", "北", "新", "创", "智", "云", "数", "信", "科", "盛", "通", "达", "恒", "博"]
JOB_TITLES = ["高级工程师", "产品经理", "项目经理", "技术总监", "运营经理", "市场经理", "人力资源经理", "财务经理", "销售经理", "测试工程师", "前端工程师", "后端工程师", "全栈工程师", "数据分析师", "UI设计师"]
GENDERS = ["男", "女"]
WORDS = ["测试", "数据", "系统", "平台", "服务", "管理", "开发", "技术", "产品", "项目"]
SENTENCES = ["这是一个用于测试的示例数据。", "系统正在处理相关请求。", "数据已成功生成并保存。", "用户信息已更新完成。", "订单处理中，请稍候。"]
EMAIL_DOMAINS = ["gmail.com", "163.com", "qq.com", "outlook.com", "company.com"]
PHONE_PREFIXES = ["138", "139", "150", "151", "152", "158", "159", "186", "187", "188"]
AREA_CODES = ["110101", "310101", "440106", "330102", "320102"]


def generate_value(data_type: str):
    """根据类型生成随机值"""
    generators = {
        "uuid": lambda: str(uuid_lib.uuid4()),
        "chineseName": lambda: random.choice(SURNAMES) + random.choice(GIVEN_NAMES),
        "englishName": lambda: f"{random.choice(ENGLISH_FIRST_NAMES)} {random.choice(ENGLISH_LAST_NAMES)}",
        "email": lambda: f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))}@{random.choice(EMAIL_DOMAINS)}",
        "chinesePhone": lambda: random.choice(PHONE_PREFIXES) + str(random.randint(10000000, 99999999)),
        "phone": lambda: f"+1 {random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "chineseIdCard": lambda: f"{random.choice(AREA_CODES)}{random.randint(1970, 2005)}{str(random.randint(1, 12)).zfill(2)}{str(random.randint(1, 28)).zfill(2)}{random.randint(100, 999)}{random.randint(0, 9)}",
        "age": lambda: random.randint(18, 65),
        "gender": lambda: random.choice(GENDERS),
        "number": lambda: random.randint(1, 100000),
        "string": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10)),
        "boolean": lambda: random.choice([True, False]),
        "date": lambda: f"{random.randint(2020, 2024)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}",
        "datetime": lambda: f"{random.randint(2020, 2024)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)} {str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}",
        "timestamp": lambda: str(int((datetime.now() - timedelta(days=random.randint(0, 365))).timestamp() * 1000)),
        "chineseAddress": lambda: f"{random.choice(PROVINCES)}{random.choice(CITIES)}{random.choice(DISTRICTS)}{random.choice(STREETS)}{random.randint(1, 999)}号",
        "province": lambda: random.choice(PROVINCES),
        "city": lambda: random.choice(CITIES),
        "zipcode": lambda: str(random.randint(100000, 999999)),
        "url": lambda: f"https://{random.choice(['example', 'test', 'demo'])}.{random.choice(['com', 'net', 'org'])}/{random.choice(['api', 'user', 'data'])}",
        "ip": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "ipv6": lambda: ":".join([f"{random.randint(0, 65535):04x}" for _ in range(8)]),
        "mac": lambda: ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)]),
        "domain": lambda: f"{random.choice(['example', 'test', 'demo', 'sample'])}.{random.choice(['com', 'net', 'org', 'io', 'cn'])}",
        "bankCard": lambda: random.choice(["6222", "6227", "6228", "9558", "6216"]) + ''.join([str(random.randint(0, 9)) for _ in range(12)]),
        "amount": lambda: f"¥{random.randint(100, 99999) + random.random():.2f}",
        "company": lambda: random.choice(COMPANY_PREFIXES) + random.choice(COMPANY_PREFIXES) + random.choice(COMPANY_SUFFIXES),
        "jobTitle": lambda: random.choice(JOB_TITLES),
        "paragraph": lambda: "".join([random.choice(SENTENCES) for _ in range(random.randint(3, 5))]),
        "sentence": lambda: random.choice(SENTENCES),
        "word": lambda: random.choice(WORDS),
    }
    
    generator = generators.get(data_type)
    return generator() if generator else ""


def generate_mock_data(fields: list, count: int) -> list:
    """生成模拟数据"""
    result = []
    for _ in range(count):
        record = {}
        for field in fields:
            record[field["name"]] = generate_value(field["type"])
        result.append(record)
    return result
