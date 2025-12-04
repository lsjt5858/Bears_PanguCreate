import type { DataField } from "@/components/data-generator-platform"

export const dataTypes = [
  // 标识符
  { id: "uuid", name: "UUID", icon: "🔑", category: "identifier" },
  { id: "number", name: "数字", icon: "🔢", category: "identifier" },
  { id: "string", name: "随机字符串", icon: "📝", category: "identifier" },
  { id: "boolean", name: "布尔值", icon: "✓", category: "identifier" },

  // 个人信息
  { id: "chineseName", name: "中文姓名", icon: "👤", category: "personal" },
  { id: "englishName", name: "英文姓名", icon: "👤", category: "personal" },
  { id: "email", name: "邮箱", icon: "📧", category: "personal" },
  { id: "chinesePhone", name: "中国手机号", icon: "📱", category: "personal" },
  { id: "phone", name: "国际手机号", icon: "📞", category: "personal" },
  { id: "chineseIdCard", name: "身份证号", icon: "🪪", category: "personal" },
  { id: "age", name: "年龄", icon: "🎂", category: "personal" },
  { id: "gender", name: "性别", icon: "⚧", category: "personal" },

  // 地址
  { id: "chineseAddress", name: "中国地址", icon: "📍", category: "address" },
  { id: "province", name: "省份", icon: "🗺️", category: "address" },
  { id: "city", name: "城市", icon: "🏙️", category: "address" },
  { id: "zipcode", name: "邮编", icon: "📮", category: "address" },

  // 日期时间
  { id: "date", name: "日期", icon: "📅", category: "datetime" },
  { id: "datetime", name: "日期时间", icon: "🕐", category: "datetime" },
  { id: "timestamp", name: "时间戳", icon: "⏱️", category: "datetime" },

  // 金融
  { id: "bankCard", name: "银行卡号", icon: "💳", category: "finance" },
  { id: "amount", name: "金额", icon: "💰", category: "finance" },

  // 互联网
  { id: "url", name: "URL", icon: "🔗", category: "internet" },
  { id: "ip", name: "IPv4", icon: "🌐", category: "internet" },
  { id: "ipv6", name: "IPv6", icon: "🌐", category: "internet" },
  { id: "mac", name: "MAC地址", icon: "📶", category: "internet" },
  { id: "domain", name: "域名", icon: "🌍", category: "internet" },

  // 企业
  { id: "company", name: "公司名称", icon: "🏢", category: "company" },
  { id: "jobTitle", name: "职位", icon: "💼", category: "company" },

  // 文本
  { id: "paragraph", name: "段落", icon: "📄", category: "text" },
  { id: "sentence", name: "句子", icon: "💬", category: "text" },
  { id: "word", name: "词语", icon: "📝", category: "text" },
]

export function getDataTypesByCategory(category: string) {
  return dataTypes.filter((dt) => dt.category === category)
}

// 中文姓氏
const surnames = [
  "王",
  "李",
  "张",
  "刘",
  "陈",
  "杨",
  "黄",
  "赵",
  "周",
  "吴",
  "徐",
  "孙",
  "马",
  "胡",
  "朱",
  "郭",
  "何",
  "罗",
  "高",
  "林",
]

// 中文名字
const givenNames = [
  "伟",
  "芳",
  "娜",
  "敏",
  "静",
  "丽",
  "强",
  "磊",
  "军",
  "洋",
  "勇",
  "艳",
  "杰",
  "娟",
  "涛",
  "明",
  "超",
  "秀英",
  "华",
  "慧",
]

// 英文名
const englishFirstNames = [
  "James",
  "John",
  "Robert",
  "Michael",
  "David",
  "Mary",
  "Patricia",
  "Jennifer",
  "Linda",
  "Elizabeth",
]
const englishLastNames = [
  "Smith",
  "Johnson",
  "Williams",
  "Brown",
  "Jones",
  "Garcia",
  "Miller",
  "Davis",
  "Rodriguez",
  "Martinez",
]

// 省份
const provinces = [
  "北京市",
  "上海市",
  "广东省",
  "江苏省",
  "浙江省",
  "山东省",
  "河南省",
  "四川省",
  "湖北省",
  "湖南省",
  "福建省",
  "安徽省",
  "河北省",
  "陕西省",
  "辽宁省",
]

// 城市
const cities = [
  "北京",
  "上海",
  "广州",
  "深圳",
  "杭州",
  "南京",
  "成都",
  "武汉",
  "西安",
  "重庆",
  "苏州",
  "天津",
  "青岛",
  "长沙",
  "郑州",
]

// 区域
const districts = ["朝阳区", "海淀区", "浦东新区", "天河区", "南山区", "江干区", "鼓楼区", "武侯区", "江汉区", "雁塔区"]

// 街道
const streets = ["中山路", "人民路", "解放路", "建设路", "和平路", "文化路", "科技路", "创新大道", "学院路", "商业街"]

// 公司后缀
const companySuffixes = [
  "科技有限公司",
  "网络科技有限公司",
  "信息技术有限公司",
  "电子商务有限公司",
  "软件开发有限公司",
  "数据服务有限公司",
  "智能科技有限公司",
  "云计算有限公司",
]

// 公司前缀
const companyPrefixes = [
  "华",
  "中",
  "东",
  "南",
  "北",
  "新",
  "创",
  "智",
  "云",
  "数",
  "信",
  "科",
  "盛",
  "通",
  "达",
  "恒",
  "博",
]

// 职位
const jobTitles = [
  "高级工程师",
  "产品经理",
  "项目经理",
  "技术总监",
  "运营经理",
  "市场经理",
  "人力资源经理",
  "财务经理",
  "销售经理",
  "测试工程师",
  "前端工程师",
  "后端工程师",
  "全栈工程师",
  "数据分析师",
  "UI设计师",
]

// 性别
const genders = ["男", "女"]

// 随机词语
const words = ["测试", "数据", "系统", "平台", "服务", "管理", "开发", "技术", "产品", "项目"]

// 句子模板
const sentenceTemplates = [
  "这是一个用于测试的示例数据。",
  "系统正在处理相关请求。",
  "数据已成功生成并保存。",
  "用户信息已更新完成。",
  "订单处理中，请稍候。",
]

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function randomElement<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]
}

function generateUUID(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === "x" ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

function generateChineseName(): string {
  return randomElement(surnames) + randomElement(givenNames)
}

function generateEnglishName(): string {
  return `${randomElement(englishFirstNames)} ${randomElement(englishLastNames)}`
}

function generateEmail(): string {
  const domains = ["gmail.com", "163.com", "qq.com", "outlook.com", "company.com"]
  const name = Math.random().toString(36).substring(2, 10)
  return `${name}@${randomElement(domains)}`
}

function generateChinesePhone(): string {
  const prefixes = ["138", "139", "150", "151", "152", "158", "159", "186", "187", "188"]
  return randomElement(prefixes) + randomInt(10000000, 99999999).toString()
}

function generatePhone(): string {
  return `+1 ${randomInt(200, 999)}-${randomInt(100, 999)}-${randomInt(1000, 9999)}`
}

function generateChineseIdCard(): string {
  const areaCodes = ["110101", "310101", "440106", "330102", "320102"]
  const year = randomInt(1970, 2005)
  const month = randomInt(1, 12).toString().padStart(2, "0")
  const day = randomInt(1, 28).toString().padStart(2, "0")
  const seq = randomInt(100, 999).toString()
  const checkDigit = randomInt(0, 9).toString()
  return `${randomElement(areaCodes)}${year}${month}${day}${seq}${checkDigit}`
}

function generateDate(): string {
  const year = randomInt(2020, 2024)
  const month = randomInt(1, 12).toString().padStart(2, "0")
  const day = randomInt(1, 28).toString().padStart(2, "0")
  return `${year}-${month}-${day}`
}

function generateDatetime(): string {
  const date = generateDate()
  const hour = randomInt(0, 23).toString().padStart(2, "0")
  const minute = randomInt(0, 59).toString().padStart(2, "0")
  const second = randomInt(0, 59).toString().padStart(2, "0")
  return `${date} ${hour}:${minute}:${second}`
}

function generateTimestamp(): string {
  return (Date.now() - randomInt(0, 365 * 24 * 60 * 60 * 1000)).toString()
}

function generateChineseAddress(): string {
  return `${randomElement(provinces)}${randomElement(cities)}${randomElement(districts)}${randomElement(streets)}${randomInt(1, 999)}号`
}

function generateUrl(): string {
  const protocols = ["https://"]
  const domains = ["example.com", "test.com", "demo.org", "sample.net"]
  const paths = ["/api/v1", "/user", "/data", "/product", "/service"]
  return `${randomElement(protocols)}${randomElement(domains)}${randomElement(paths)}`
}

function generateIP(): string {
  return `${randomInt(1, 255)}.${randomInt(0, 255)}.${randomInt(0, 255)}.${randomInt(1, 254)}`
}

function generateIPv6(): string {
  const segments = Array(8)
    .fill(0)
    .map(() => randomInt(0, 65535).toString(16).padStart(4, "0"))
  return segments.join(":")
}

function generateMAC(): string {
  const segments = Array(6)
    .fill(0)
    .map(() => randomInt(0, 255).toString(16).padStart(2, "0").toUpperCase())
  return segments.join(":")
}

function generateDomain(): string {
  const names = ["example", "test", "demo", "sample", "mysite"]
  const tlds = [".com", ".net", ".org", ".io", ".cn"]
  return randomElement(names) + randomElement(tlds)
}

function generateBankCard(): string {
  const prefixes = ["6222", "6227", "6228", "9558", "6216"]
  return (
    randomElement(prefixes) +
    Array(12)
      .fill(0)
      .map(() => randomInt(0, 9))
      .join("")
  )
}

function generateAmount(): string {
  const amount = (randomInt(100, 99999) + Math.random()).toFixed(2)
  return `¥${Number.parseFloat(amount).toLocaleString()}`
}

function generateCompany(): string {
  return randomElement(companyPrefixes) + randomElement(companyPrefixes) + randomElement(companySuffixes)
}

function generateJobTitle(): string {
  return randomElement(jobTitles)
}

function generateParagraph(): string {
  return Array(randomInt(3, 5))
    .fill(0)
    .map(() => randomElement(sentenceTemplates))
    .join("")
}

function generateSentence(): string {
  return randomElement(sentenceTemplates)
}

function generateWord(): string {
  return randomElement(words)
}

export function generateValue(type: string): unknown {
  switch (type) {
    case "uuid":
      return generateUUID()
    case "chineseName":
      return generateChineseName()
    case "englishName":
      return generateEnglishName()
    case "email":
      return generateEmail()
    case "chinesePhone":
      return generateChinesePhone()
    case "phone":
      return generatePhone()
    case "chineseIdCard":
      return generateChineseIdCard()
    case "age":
      return randomInt(18, 65)
    case "gender":
      return randomElement(genders)
    case "number":
      return randomInt(1, 100000)
    case "string":
      return Math.random().toString(36).substring(2, 12)
    case "boolean":
      return Math.random() > 0.5
    case "date":
      return generateDate()
    case "datetime":
      return generateDatetime()
    case "timestamp":
      return generateTimestamp()
    case "chineseAddress":
      return generateChineseAddress()
    case "province":
      return randomElement(provinces)
    case "city":
      return randomElement(cities)
    case "zipcode":
      return randomInt(100000, 999999).toString()
    case "url":
      return generateUrl()
    case "ip":
      return generateIP()
    case "ipv6":
      return generateIPv6()
    case "mac":
      return generateMAC()
    case "domain":
      return generateDomain()
    case "bankCard":
      return generateBankCard()
    case "amount":
      return generateAmount()
    case "company":
      return generateCompany()
    case "jobTitle":
      return generateJobTitle()
    case "paragraph":
      return generateParagraph()
    case "sentence":
      return generateSentence()
    case "word":
      return generateWord()
    default:
      return ""
  }
}

export function generateMockData(fields: DataField[], count: number): Record<string, unknown>[] {
  return Array(count)
    .fill(0)
    .map(() => {
      const record: Record<string, unknown> = {}
      fields.forEach((field) => {
        record[field.name] = generateValue(field.type)
      })
      return record
    })
}
