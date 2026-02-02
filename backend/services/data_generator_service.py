"""
数据生成服务
负责根据字段配置生成模拟数据
"""
import random
import uuid as uuid_lib
from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import OrderedDict


class DataGeneratorService:
    """数据生成服务"""
    
    # 数据源
    SURNAMES = ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴", "徐", "孙", "马", "胡", "朱", "郭", "何", "罗", "高", "林"]
    GIVEN_NAMES = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英", "华", "慧"]
    ENGLISH_FIRST_NAMES = ["James", "John", "Robert", "Michael", "David", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "William", "Sarah", "Thomas", "Jessica", "Daniel"]
    ENGLISH_LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore"]
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
    
    # 新增数据源
    COUNTRIES = ["中国", "美国", "日本", "英国", "法国", "德国", "加拿大", "澳大利亚", "韩国", "新加坡"]
    COUNTRY_CODES = ["CN", "US", "JP", "GB", "FR", "DE", "CA", "AU", "KR", "SG"]
    WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    CURRENCIES = ["CNY", "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "HKD", "SGD"]
    PROTOCOLS = ["http", "https", "ftp", "ssh", "ws", "wss"]
    HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    HTTP_STATUSES = [200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503]
    DEPARTMENTS = ["研发部", "产品部", "市场部", "销售部", "人力资源部", "财务部", "运营部", "客服部"]
    INDUSTRIES = ["互联网", "金融", "教育", "医疗", "制造业", "零售", "房地产", "物流", "能源", "农业"]
    PRODUCT_CATEGORIES = ["电子产品", "服装鞋帽", "食品饮料", "家居用品", "图书音像", "美妆护肤", "运动户外", "母婴用品"]
    BRANDS = ["Apple", "华为", "小米", "三星", "OPPO", "vivo", "联想", "戴尔", "惠普", "索尼"]
    CAR_BRANDS = ["奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "特斯拉", "比亚迪", "蔚来", "理想"]
    CAR_MODELS = ["E300L", "5系", "A6L", "帕萨特", "凯美瑞", "雅阁", "Model 3", "汉", "ES6", "L9"]
    BLOOD_TYPES = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    UNIVERSITIES = ["清华大学", "北京大学", "复旦大学", "上海交通大学", "浙江大学", "南京大学", "中国科学技术大学", "哈尔滨工业大学"]
    MAJORS = ["计算机科学与技术", "软件工程", "电子信息工程", "通信工程", "自动化", "机械工程", "土木工程", "金融学", "会计学", "市场营销"]
    DEGREES = ["学士", "硕士", "博士"]
    STATUSES = ["active", "inactive", "pending", "completed", "cancelled", "processing"]
    PRIORITIES = ["高", "中", "低"]
    TAGS = ["重要", "紧急", "待处理", "已完成", "测试", "生产", "开发"]
    LANGUAGES = ["zh-CN", "en-US", "ja-JP", "ko-KR", "fr-FR", "de-DE", "es-ES"]
    TIMEZONES = ["Asia/Shanghai", "America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
    FILE_EXTENSIONS = [".jpg", ".png", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".zip", ".mp4", ".mp3"]
    MIME_TYPES = ["image/jpeg", "image/png", "application/pdf", "application/msword", "text/plain", "video/mp4", "audio/mpeg"]
    EMOJIS = ["😀", "😃", "😄", "😁", "😊", "🎉", "🎊", "🎈", "🎁", "❤️", "👍", "🔥", "✨", "🌟", "💯"]
    
    # 自增ID计数器
    _auto_increment_counter = 0

    def __init__(self):
        self._generators = self._init_generators()

    def _get_auto_increment(self) -> int:
        """获取自增ID"""
        DataGeneratorService._auto_increment_counter += 1
        return DataGeneratorService._auto_increment_counter

    def _init_generators(self) -> Dict[str, callable]:
        """初始化生成器映射"""
        return {
            # ==================== 标识符类 ====================
            "uuid": lambda: str(uuid_lib.uuid4()),
            "objectId": lambda: ''.join(random.choices('0123456789abcdef', k=24)),
            "number": lambda: random.randint(1, 100000),
            "float": lambda: round(random.uniform(0, 1000), 2),
            "string": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10)),
            "boolean": lambda: random.choice([True, False]),
            "autoIncrement": lambda: self._get_auto_increment(),
            "hexColor": lambda: f"#{random.randint(0, 0xFFFFFF):06X}",
            "rgbColor": lambda: f"rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})",
            
            # ==================== 个人信息类 ====================
            "chineseName": lambda: random.choice(self.SURNAMES) + random.choice(self.GIVEN_NAMES),
            "englishName": lambda: f"{random.choice(self.ENGLISH_FIRST_NAMES)} {random.choice(self.ENGLISH_LAST_NAMES)}",
            "firstName": lambda: random.choice(self.GIVEN_NAMES),
            "lastName": lambda: random.choice(self.SURNAMES),
            "username": lambda: f"user_{random.randint(10000, 99999)}",
            "password": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%', k=12)),
            "email": lambda: f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))}@{random.choice(self.EMAIL_DOMAINS)}",
            "chinesePhone": lambda: random.choice(self.PHONE_PREFIXES) + str(random.randint(10000000, 99999999)),
            "phone": lambda: f"+1 {random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "chineseIdCard": lambda: f"{random.choice(self.AREA_CODES)}{random.randint(1970, 2005)}{str(random.randint(1, 12)).zfill(2)}{str(random.randint(1, 28)).zfill(2)}{random.randint(100, 999)}{random.randint(0, 9)}",
            "age": lambda: random.randint(18, 65),
            "birthday": lambda: f"{random.randint(1970, 2005)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}",
            "gender": lambda: random.choice(self.GENDERS),
            "avatar": lambda: f"https://avatar.example.com/{random.randint(1, 1000)}.jpg",
            "bio": lambda: random.choice(["热爱编程的开发者", "产品设计师", "全栈工程师", "数据分析专家", "技术爱好者"]),
            
            # ==================== 地址位置类 ====================
            "chineseAddress": lambda: f"{random.choice(self.PROVINCES)}{random.choice(self.CITIES)}{random.choice(self.DISTRICTS)}{random.choice(self.STREETS)}{random.randint(1, 999)}号",
            "province": lambda: random.choice(self.PROVINCES),
            "city": lambda: random.choice(self.CITIES),
            "district": lambda: random.choice(self.DISTRICTS),
            "street": lambda: random.choice(self.STREETS),
            "zipcode": lambda: str(random.randint(100000, 999999)),
            "latitude": lambda: round(random.uniform(-90, 90), 6),
            "longitude": lambda: round(random.uniform(-180, 180), 6),
            "country": lambda: random.choice(self.COUNTRIES),
            "countryCode": lambda: random.choice(self.COUNTRY_CODES),
            
            # ==================== 日期时间类 ====================
            "date": lambda: f"{random.randint(2020, 2024)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}",
            "datetime": lambda: f"{random.randint(2020, 2024)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)} {str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}",
            "timestamp": lambda: str(int((datetime.now() - timedelta(days=random.randint(0, 365))).timestamp() * 1000)),
            "time": lambda: f"{str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}",
            "year": lambda: random.randint(2000, 2024),
            "month": lambda: random.randint(1, 12),
            "weekday": lambda: random.choice(self.WEEKDAYS),
            "isoDate": lambda: f"{random.randint(2020, 2024)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}T{str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}Z",
            
            # ==================== 金融财务类 ====================
            "bankCard": lambda: random.choice(["6222", "6227", "6228", "9558", "6216"]) + ''.join([str(random.randint(0, 9)) for _ in range(12)]),
            "amount": lambda: f"¥{random.randint(100, 99999) + random.random():.2f}",
            "price": lambda: f"¥{random.randint(1, 9999) + random.random():.2f}",
            "currency": lambda: random.choice(self.CURRENCIES),
            "creditCard": lambda: ''.join([str(random.randint(0, 9)) for _ in range(16)]),
            "cvv": lambda: ''.join([str(random.randint(0, 9)) for _ in range(3)]),
            "iban": lambda: f"GB{random.randint(10, 99)} WEST {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(10, 99)}",
            "bitcoin": lambda: '1' + ''.join(random.choices('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', k=33)),
            "ethereum": lambda: '0x' + ''.join(random.choices('0123456789abcdef', k=40)),
            
            # ==================== 互联网类 ====================
            "url": lambda: f"https://{random.choice(['example', 'test', 'demo'])}.{random.choice(['com', 'net', 'org'])}/{random.choice(['api', 'user', 'data'])}",
            "domain": lambda: f"{random.choice(['example', 'test', 'demo', 'sample'])}.{random.choice(['com', 'net', 'org', 'io', 'cn'])}",
            "ip": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
            "ipv6": lambda: ":".join([f"{random.randint(0, 65535):04x}" for _ in range(8)]),
            "mac": lambda: ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)]),
            "userAgent": lambda: f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.0.0 Safari/537.36",
            "port": lambda: random.randint(1024, 65535),
            "protocol": lambda: random.choice(self.PROTOCOLS),
            "slug": lambda: '-'.join(random.choices(self.WORDS, k=3)),
            "httpMethod": lambda: random.choice(self.HTTP_METHODS),
            "httpStatus": lambda: random.choice(self.HTTP_STATUSES),
            
            # ==================== 企业信息类 ====================
            "company": lambda: random.choice(self.COMPANY_PREFIXES) + random.choice(self.COMPANY_PREFIXES) + random.choice(self.COMPANY_SUFFIXES),
            "companyShort": lambda: random.choice(self.COMPANY_PREFIXES) + random.choice(self.COMPANY_PREFIXES),
            "department": lambda: random.choice(self.DEPARTMENTS),
            "jobTitle": lambda: random.choice(self.JOB_TITLES),
            "industry": lambda: random.choice(self.INDUSTRIES),
            "taxId": lambda: f"91{random.randint(100000, 999999)}{random.randint(100000000, 999999999)}",
            "businessLicense": lambda: f"91{random.randint(100000, 999999)}{random.randint(100000000, 999999999)}",
            
            # ==================== 文本内容类 ====================
            "paragraph": lambda: "".join([random.choice(self.SENTENCES) for _ in range(random.randint(3, 5))]),
            "sentence": lambda: random.choice(self.SENTENCES),
            "word": lambda: random.choice(self.WORDS),
            "title": lambda: random.choice(["如何使用数据生成工具", "系统架构设计方案", "产品需求文档", "技术实现方案", "项目进度报告"]),
            "description": lambda: random.choice(["这是一个简短的描述", "用于测试的示例描述", "产品功能说明", "服务介绍"]),
            "content": lambda: "".join([random.choice(self.SENTENCES) for _ in range(random.randint(5, 10))]),
            "hashtag": lambda: f"#{random.choice(self.WORDS)}",
            "emoji": lambda: random.choice(self.EMOJIS),
            
            # ==================== 商品电商类 ====================
            "productName": lambda: f"{random.choice(self.BRANDS)} {random.choice(['手机', '笔记本', '平板', '耳机', '手表'])} {random.choice(['Pro', 'Max', 'Plus', 'Ultra'])}",
            "productCategory": lambda: random.choice(self.PRODUCT_CATEGORIES),
            "sku": lambda: f"SKU-{random.randint(2020, 2024)}-{random.randint(1000, 9999)}",
            "barcode": lambda: ''.join([str(random.randint(0, 9)) for _ in range(13)]),
            "brand": lambda: random.choice(self.BRANDS),
            "rating": lambda: round(random.uniform(3.0, 5.0), 1),
            "stock": lambda: random.randint(0, 10000),
            "discount": lambda: f"{random.randint(5, 50)}%",
            "orderNumber": lambda: f"ORD{datetime.now().strftime('%Y%m%d')}{random.randint(10000, 99999)}",
            "trackingNumber": lambda: f"SF{random.randint(1000000000, 9999999999)}",
            
            # ==================== 社交媒体类 ====================
            "wechat": lambda: f"wx_{random.randint(100000, 999999)}",
            "qq": lambda: str(random.randint(100000000, 999999999)),
            "weibo": lambda: f"@{random.choice(self.SURNAMES)}{random.choice(self.GIVEN_NAMES)}",
            "twitter": lambda: f"@user{random.randint(1000, 9999)}",
            "facebook": lambda: f"facebook.com/user{random.randint(1000, 9999)}",
            "instagram": lambda: f"@user{random.randint(1000, 9999)}",
            "linkedin": lambda: f"linkedin.com/in/user{random.randint(1000, 9999)}",
            "github": lambda: f"github.com/user{random.randint(1000, 9999)}",
            
            # ==================== 文件媒体类 ====================
            "filename": lambda: f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}{random.choice(self.FILE_EXTENSIONS)}",
            "fileExtension": lambda: random.choice(self.FILE_EXTENSIONS),
            "mimeType": lambda: random.choice(self.MIME_TYPES),
            "fileSize": lambda: f"{round(random.uniform(0.1, 100), 2)} MB",
            "imageUrl": lambda: f"https://cdn.example.com/images/{random.randint(1000, 9999)}.jpg",
            "videoUrl": lambda: f"https://cdn.example.com/videos/{random.randint(1000, 9999)}.mp4",
            "audioUrl": lambda: f"https://cdn.example.com/audio/{random.randint(1000, 9999)}.mp3",
            
            # ==================== 车辆交通类 ====================
            "licensePlate": lambda: f"{random.choice(['京', '沪', '粤', '浙', '苏'])}{random.choice(['A', 'B', 'C', 'D'])}{random.randint(10000, 99999)}",
            "vin": lambda: ''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ0123456789', k=17)),
            "carBrand": lambda: random.choice(self.CAR_BRANDS),
            "carModel": lambda: random.choice(self.CAR_MODELS),
            "flightNumber": lambda: f"{random.choice(['CA', 'MU', 'CZ', 'HU'])}{random.randint(1000, 9999)}",
            "trainNumber": lambda: f"{random.choice(['G', 'D', 'C', 'K'])}{random.randint(1, 9999)}",
            
            # ==================== 医疗健康类 ====================
            "bloodType": lambda: random.choice(self.BLOOD_TYPES),
            "height": lambda: f"{random.randint(150, 190)} cm",
            "weight": lambda: f"{random.randint(45, 100)} kg",
            "bmi": lambda: round(random.uniform(18.5, 28.0), 1),
            "temperature": lambda: f"{round(random.uniform(36.0, 37.5), 1)}°C",
            "heartRate": lambda: f"{random.randint(60, 100)} bpm",
            
            # ==================== 教育学术类 ====================
            "university": lambda: random.choice(self.UNIVERSITIES),
            "major": lambda: random.choice(self.MAJORS),
            "degree": lambda: random.choice(self.DEGREES),
            "gpa": lambda: round(random.uniform(2.5, 4.0), 2),
            "studentId": lambda: f"{random.randint(2020, 2024)}{random.randint(100000, 999999)}",
            "course": lambda: random.choice(self.MAJORS),
            
            # ==================== 其他类 ====================
            "status": lambda: random.choice(self.STATUSES),
            "priority": lambda: random.choice(self.PRIORITIES),
            "tag": lambda: random.choice(self.TAGS),
            "category": lambda: random.choice(self.PRODUCT_CATEGORIES),
            "version": lambda: f"{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "language": lambda: random.choice(self.LANGUAGES),
            "timezone": lambda: random.choice(self.TIMEZONES),
            "locale": lambda: random.choice(self.LANGUAGES).replace('-', '_'),
        }

    def generate_value(self, data_type: str, config: Dict[str, Any] = None) -> Any:
        """
        根据类型生成单个随机值
        
        Args:
            data_type: 数据类型
            config: 可选配置参数（用于未来扩展，如范围、格式等）
        
        Returns:
            生成的随机值
        """
        generator = self._generators.get(data_type)
        if generator:
            try:
                return generator()
            except Exception as e:
                print(f"生成 {data_type} 类型数据时出错: {e}")
                return ""
        return ""

    def generate_data(self, fields: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """
        生成模拟数据
        确保字段顺序与输入顺序一致
        
        Args:
            fields: 字段配置列表，每个字段包含 name 和 type
            count: 生成数据条数
        
        Returns:
            生成的数据列表
        """
        if not fields or count <= 0:
            return []
        
        result = []
        # 提取字段名和类型的有序列表
        field_specs = [(f.get("name", ""), f.get("type", "string"), f.get("config", {})) for f in fields]
        
        # 重置自增计数器（每次批量生成时重置）
        DataGeneratorService._auto_increment_counter = 0
        
        for _ in range(count):
            # 按顺序生成每个字段的值
            record = {}
            for field_name, field_type, field_config in field_specs:
                if field_name:  # 确保字段名不为空
                    record[field_name] = self.generate_value(field_type, field_config)
            result.append(record)
        
        return result
    
    def get_supported_types(self) -> List[str]:
        """获取所有支持的数据类型"""
        return list(self._generators.keys())
    
    def is_type_supported(self, data_type: str) -> bool:
        """检查数据类型是否支持"""
        return data_type in self._generators


# 单例实例
data_generator_service = DataGeneratorService()
