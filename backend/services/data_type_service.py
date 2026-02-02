"""
数据类型服务
管理所有支持的数据类型
"""
from typing import List, Dict, Any, Optional


class DataTypeService:
    """数据类型服务"""
    
    # 所有支持的数据类型（大幅扩展）
    DATA_TYPES = [
        # ==================== 标识符类 ====================
        {"id": "uuid", "name": "UUID", "icon": "🔑", "category": "identifier", "description": "通用唯一识别码"},
        {"id": "objectId", "name": "ObjectId", "icon": "🔑", "category": "identifier", "description": "MongoDB ObjectId"},
        {"id": "number", "name": "随机数字", "icon": "🔢", "category": "identifier", "description": "随机整数"},
        {"id": "float", "name": "浮点数", "icon": "🔢", "category": "identifier", "description": "随机小数"},
        {"id": "string", "name": "随机字符串", "icon": "📝", "category": "identifier", "description": "随机字母数字组合"},
        {"id": "boolean", "name": "布尔值", "icon": "✓", "category": "identifier", "description": "true/false"},
        {"id": "autoIncrement", "name": "自增ID", "icon": "🔢", "category": "identifier", "description": "从1开始自增"},
        {"id": "hexColor", "name": "十六进制颜色", "icon": "🎨", "category": "identifier", "description": "#RRGGBB格式"},
        {"id": "rgbColor", "name": "RGB颜色", "icon": "🎨", "category": "identifier", "description": "rgb(r,g,b)格式"},
        
        # ==================== 个人信息类 ====================
        {"id": "chineseName", "name": "中文姓名", "icon": "👤", "category": "personal", "description": "随机中文姓名"},
        {"id": "englishName", "name": "英文姓名", "icon": "👤", "category": "personal", "description": "随机英文姓名"},
        {"id": "firstName", "name": "名", "icon": "👤", "category": "personal", "description": "名字"},
        {"id": "lastName", "name": "姓", "icon": "�", "category": "personal", "description": "姓氏"},
        {"id": "username", "name": "用户名", "icon": "�", "category": "personal", "description": "随机用户名"},
        {"id": "password", "name": "密码", "icon": "�", "categoryr": "personal", "description": "随机密码"},
        {"id": "email", "name": "邮箱", "icon": "📧", "category": "personal", "description": "随机邮箱地址"},
        {"id": "chinesePhone", "name": "中国手机号", "icon": "�", "category": "personal", "description": "13x/15x/18x开头"},
        {"id": "phone", "name": "国际手机号", "icon": "�", "category": "personal", "description": "国际格式手机号"},
        {"id": "chineseIdCard", "name": "身份证号", "icon": "🪪", "category": "personal", "description": "18位身份证号"},
        {"id": "age", "name": "年龄", "icon": "�", "category": "personal", "description": "随机年龄"},
        {"id": "birthday", "name": "生日", "icon": "�", "catoegory": "personal", "description": "出生日期"},
        {"id": "gender", "name": "性别", "icon": "⚧", "category": "personal", "description": "男/女"},
        {"id": "avatar", "name": "头像URL", "icon": "🖼️", "category": "personal", "description": "随机头像链接"},
        {"id": "bio", "name": "个人简介", "icon": "📝", "category": "personal", "description": "个人描述"},
        
        # ==================== 地址位置类 ====================
        {"id": "chineseAddress", "name": "中国地址", "icon": "�", "category": "address", "description": "完整中文地址"},
        {"id": "province", "name": "省份", "icon": "�️", "category": "address", "description": "中国省份"},
        {"id": "city", "name": "城市", "icon": "🏙️", "category": "address", "description": "中国城市"},
        {"id": "district", "name": "区县", "icon": "🏘️", "category": "address", "description": "区/县"},
        {"id": "street", "name": "街道", "icon": "🛣️", "category": "address", "description": "街道名称"},
        {"id": "zipcode", "name": "邮编", "icon": "📮", "category": "address", "description": "邮政编码"},
        {"id": "latitude", "name": "纬度", "icon": "🌍", "category": "address", "description": "地理纬度"},
        {"id": "longitude", "name": "经度", "icon": "🌍", "category": "address", "description": "地理经度"},
        {"id": "country", "name": "国家", "icon": "🌏", "category": "address", "description": "国家名称"},
        {"id": "countryCode", "name": "国家代码", "icon": "🌏", "category": "address", "description": "ISO国家代码"},
        
        # ==================== 日期时间类 ====================
        {"id": "date", "name": "日期", "icon": "📅", "category": "datetime", "description": "YYYY-MM-DD"},
        {"id": "datetime", "name": "日期时间", "icon": "🕐", "category": "datetime", "description": "完整日期时间"},
        {"id": "timestamp", "name": "时间戳", "icon": "⏱️", "category": "datetime", "description": "Unix时间戳"},
        {"id": "time", "name": "时间", "icon": "🕐", "category": "datetime", "description": "HH:MM:SS"},
        {"id": "year", "name": "年份", "icon": "📅", "category": "datetime", "description": "年份"},
        {"id": "month", "name": "月份", "icon": "📅", "category": "datetime", "description": "月份"},
        {"id": "weekday", "name": "星期", "icon": "📅", "category": "datetime", "description": "星期几"},
        {"id": "isoDate", "name": "ISO日期", "icon": "📅", "category": "datetime", "description": "ISO 8601格式"},
        
        # ==================== 金融财务类 ====================
        {"id": "bankCard", "name": "银行卡号", "icon": "💳", "category": "finance", "description": "16-19位卡号"},
        {"id": "amount", "name": "金额", "icon": "💰", "category": "finance", "description": "随机金额"},
        {"id": "price", "name": "价格", "icon": "💵", "category": "finance", "description": "商品价格"},
        {"id": "currency", "name": "货币代码", "icon": "💱", "category": "finance", "description": "CNY/USD等"},
        {"id": "creditCard", "name": "信用卡号", "icon": "💳", "category": "finance", "description": "信用卡号码"},
        {"id": "cvv", "name": "CVV码", "icon": "🔐", "category": "finance", "description": "3位安全码"},
        {"id": "iban", "name": "IBAN", "icon": "🏦", "category": "finance", "description": "国际银行账号"},
        {"id": "bitcoin", "name": "比特币地址", "icon": "₿", "category": "finance", "description": "BTC地址"},
        {"id": "ethereum", "name": "以太坊地址", "icon": "Ξ", "category": "finance", "description": "ETH地址"},
        
        # ==================== 互联网类 ====================
        {"id": "url", "name": "URL", "icon": "🔗", "category": "internet", "description": "网址链接"},
        {"id": "domain", "name": "域名", "icon": "🌍", "category": "internet", "description": "域名"},
        {"id": "ip", "name": "IPv4", "icon": "🌐", "category": "internet", "description": "IPv4地址"},
        {"id": "ipv6", "name": "IPv6", "icon": "🌐", "category": "internet", "description": "IPv6地址"},
        {"id": "mac", "name": "MAC地址", "icon": "📶", "category": "internet", "description": "物理地址"},
        {"id": "userAgent", "name": "User Agent", "icon": "🖥️", "category": "internet", "description": "浏览器UA"},
        {"id": "port", "name": "端口号", "icon": "🔌", "category": "internet", "description": "网络端口"},
        {"id": "protocol", "name": "协议", "icon": "📡", "category": "internet", "description": "HTTP/HTTPS等"},
        {"id": "slug", "name": "URL Slug", "icon": "🔗", "category": "internet", "description": "URL友好字符串"},
        {"id": "httpMethod", "name": "HTTP方法", "icon": "📡", "category": "internet", "description": "GET/POST等"},
        {"id": "httpStatus", "name": "HTTP状态码", "icon": "📊", "category": "internet", "description": "200/404等"},
        
        # ==================== 企业信息类 ====================
        {"id": "company", "name": "公司名称", "icon": "🏢", "category": "company", "description": "公司全称"},
        {"id": "companyShort", "name": "公司简称", "icon": "🏢", "category": "company", "description": "公司简称"},
        {"id": "department", "name": "部门", "icon": "🏛️", "category": "company", "description": "部门名称"},
        {"id": "jobTitle", "name": "职位", "icon": "💼", "category": "company", "description": "职位名称"},
        {"id": "industry", "name": "行业", "icon": "🏭", "category": "company", "description": "所属行业"},
        {"id": "taxId", "name": "税号", "icon": "📋", "category": "company", "description": "纳税人识别号"},
        {"id": "businessLicense", "name": "营业执照号", "icon": "📜", "category": "company", "description": "统一社会信用代码"},
        
        # ==================== 文本内容类 ====================
        {"id": "paragraph", "name": "段落", "icon": "📄", "category": "text", "description": "多句文本"},
        {"id": "sentence", "name": "句子", "icon": "💬", "category": "text", "description": "一句话"},
        {"id": "word", "name": "词语", "icon": "📝", "category": "text", "description": "单个词"},
        {"id": "title", "name": "标题", "icon": "📰", "category": "text", "description": "文章标题"},
        {"id": "description", "name": "描述", "icon": "📝", "category": "text", "description": "简短描述"},
        {"id": "content", "name": "文章内容", "icon": "📄", "category": "text", "description": "长文本内容"},
        {"id": "hashtag", "name": "话题标签", "icon": "#️⃣", "category": "text", "description": "#话题"},
        {"id": "emoji", "name": "表情符号", "icon": "😀", "category": "text", "description": "随机emoji"},
        
        # ==================== 商品电商类 ====================
        {"id": "productName", "name": "商品名称", "icon": "🛍️", "category": "ecommerce", "description": "商品名"},
        {"id": "productCategory", "name": "商品分类", "icon": "📦", "category": "ecommerce", "description": "商品类别"},
        {"id": "sku", "name": "SKU", "icon": "🏷️", "category": "ecommerce", "description": "库存单位"},
        {"id": "barcode", "name": "条形码", "icon": "📊", "category": "ecommerce", "description": "商品条码"},
        {"id": "brand", "name": "品牌", "icon": "🏷️", "category": "ecommerce", "description": "品牌名称"},
        {"id": "rating", "name": "评分", "icon": "⭐", "category": "ecommerce", "description": "1-5星评分"},
        {"id": "stock", "name": "库存数量", "icon": "📦", "category": "ecommerce", "description": "库存量"},
        {"id": "discount", "name": "折扣", "icon": "🎫", "category": "ecommerce", "description": "折扣百分比"},
        {"id": "orderNumber", "name": "订单号", "icon": "📋", "category": "ecommerce", "description": "订单编号"},
        {"id": "trackingNumber", "name": "物流单号", "icon": "📮", "category": "ecommerce", "description": "快递单号"},
        
        # ==================== 社交媒体类 ====================
        {"id": "wechat", "name": "微信号", "icon": "💬", "category": "social", "description": "微信ID"},
        {"id": "qq", "name": "QQ号", "icon": "🐧", "category": "social", "description": "QQ号码"},
        {"id": "weibo", "name": "微博", "icon": "📱", "category": "social", "description": "微博账号"},
        {"id": "twitter", "name": "Twitter", "icon": "🐦", "category": "social", "description": "Twitter账号"},
        {"id": "facebook", "name": "Facebook", "icon": "📘", "category": "social", "description": "Facebook账号"},
        {"id": "instagram", "name": "Instagram", "icon": "📷", "category": "social", "description": "Instagram账号"},
        {"id": "linkedin", "name": "LinkedIn", "icon": "💼", "category": "social", "description": "LinkedIn账号"},
        {"id": "github", "name": "GitHub", "icon": "🐙", "category": "social", "description": "GitHub用户名"},
        
        # ==================== 文件媒体类 ====================
        {"id": "filename", "name": "文件名", "icon": "📁", "category": "file", "description": "文件名称"},
        {"id": "fileExtension", "name": "文件扩展名", "icon": "📄", "category": "file", "description": ".jpg/.pdf等"},
        {"id": "mimeType", "name": "MIME类型", "icon": "📋", "category": "file", "description": "文件类型"},
        {"id": "fileSize", "name": "文件大小", "icon": "💾", "category": "file", "description": "文件大小"},
        {"id": "imageUrl", "name": "图片URL", "icon": "🖼️", "category": "file", "description": "图片链接"},
        {"id": "videoUrl", "name": "视频URL", "icon": "🎬", "category": "file", "description": "视频链接"},
        {"id": "audioUrl", "name": "音频URL", "icon": "🎵", "category": "file", "description": "音频链接"},
        
        # ==================== 车辆交通类 ====================
        {"id": "licensePlate", "name": "车牌号", "icon": "🚗", "category": "vehicle", "description": "车牌号码"},
        {"id": "vin", "name": "车架号", "icon": "🚙", "category": "vehicle", "description": "VIN码"},
        {"id": "carBrand", "name": "汽车品牌", "icon": "🚗", "category": "vehicle", "description": "汽车品牌"},
        {"id": "carModel", "name": "汽车型号", "icon": "🚙", "category": "vehicle", "description": "车型"},
        {"id": "flightNumber", "name": "航班号", "icon": "✈️", "category": "vehicle", "description": "航班编号"},
        {"id": "trainNumber", "name": "车次", "icon": "🚄", "category": "vehicle", "description": "火车车次"},
        
        # ==================== 医疗健康类 ====================
        {"id": "bloodType", "name": "血型", "icon": "🩸", "category": "medical", "description": "A/B/O/AB型"},
        {"id": "height", "name": "身高", "icon": "📏", "category": "medical", "description": "身高cm"},
        {"id": "weight", "name": "体重", "icon": "⚖️", "category": "medical", "description": "体重kg"},
        {"id": "bmi", "name": "BMI", "icon": "📊", "category": "medical", "description": "体重指数"},
        {"id": "temperature", "name": "体温", "icon": "🌡️", "category": "medical", "description": "体温℃"},
        {"id": "heartRate", "name": "心率", "icon": "❤️", "category": "medical", "description": "心率bpm"},
        
        # ==================== 教育学术类 ====================
        {"id": "university", "name": "大学", "icon": "🎓", "category": "education", "description": "大学名称"},
        {"id": "major", "name": "专业", "icon": "📚", "category": "education", "description": "专业名称"},
        {"id": "degree", "name": "学位", "icon": "🎓", "category": "education", "description": "学士/硕士/博士"},
        {"id": "gpa", "name": "GPA", "icon": "📊", "category": "education", "description": "绩点"},
        {"id": "studentId", "name": "学号", "icon": "🎓", "category": "education", "description": "学生编号"},
        {"id": "course", "name": "课程", "icon": "📖", "category": "education", "description": "课程名称"},
        
        # ==================== 其他类 ====================
        {"id": "status", "name": "状态", "icon": "🔄", "category": "other", "description": "状态值"},
        {"id": "priority", "name": "优先级", "icon": "⚡", "category": "other", "description": "高/中/低"},
        {"id": "tag", "name": "标签", "icon": "🏷️", "category": "other", "description": "标签"},
        {"id": "category", "name": "分类", "icon": "📂", "category": "other", "description": "分类名称"},
        {"id": "version", "name": "版本号", "icon": "🔢", "category": "other", "description": "版本号"},
        {"id": "language", "name": "语言", "icon": "🌐", "category": "other", "description": "语言代码"},
        {"id": "timezone", "name": "时区", "icon": "🌍", "category": "other", "description": "时区"},
        {"id": "locale", "name": "地区", "icon": "🌏", "category": "other", "description": "地区代码"},
    ]

    # 分类名称映射
    CATEGORY_NAMES = {
        "identifier": "标识符",
        "personal": "个人信息",
        "address": "地址位置",
        "datetime": "日期时间",
        "finance": "金融财务",
        "internet": "互联网",
        "company": "企业信息",
        "text": "文本内容",
        "ecommerce": "商品电商",
        "social": "社交媒体",
        "file": "文件媒体",
        "vehicle": "车辆交通",
        "medical": "医疗健康",
        "education": "教育学术",
        "other": "其他",
    }

    def get_all_types(self) -> List[Dict[str, Any]]:
        """获取所有数据类型"""
        return self.DATA_TYPES

    def get_types_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        按分类获取数据类型
        
        Args:
            category: 分类ID
        
        Returns:
            该分类下的所有数据类型
        """
        return [t for t in self.DATA_TYPES if t.get("category") == category]

    def get_type_by_id(self, type_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取数据类型
        
        Args:
            type_id: 数据类型ID
        
        Returns:
            数据类型信息，如果不存在返回None
        """
        return next((t for t in self.DATA_TYPES if t.get("id") == type_id), None)

    def get_categories(self) -> List[Dict[str, str]]:
        """
        获取所有分类及统计信息
        
        Returns:
            分类列表，包含ID、名称和数量
        """
        # 获取所有唯一分类
        categories = {}
        for data_type in self.DATA_TYPES:
            cat = data_type.get("category")
            if cat:
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += 1
        
        # 构建结果列表，保持顺序
        result = []
        for cat_id, cat_name in self.CATEGORY_NAMES.items():
            if cat_id in categories:
                result.append({
                    "id": cat_id,
                    "name": cat_name,
                    "count": categories[cat_id]
                })
        
        return result
    
    def search_types(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索数据类型
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的数据类型列表
        """
        if not keyword:
            return self.DATA_TYPES
        
        keyword_lower = keyword.lower()
        results = []
        
        for data_type in self.DATA_TYPES:
            # 在ID、名称、描述中搜索
            if (keyword_lower in data_type.get("id", "").lower() or
                keyword_lower in data_type.get("name", "").lower() or
                keyword_lower in data_type.get("description", "").lower()):
                results.append(data_type)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取数据类型统计信息
        
        Returns:
            统计信息字典
        """
        categories = self.get_categories()
        
        return {
            "total_types": len(self.DATA_TYPES),
            "total_categories": len(categories),
            "categories": categories,
            "types_by_category": {
                cat["id"]: cat["count"] for cat in categories
            }
        }


# 单例实例
data_type_service = DataTypeService()
