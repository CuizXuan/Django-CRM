import pytz
from django.utils.translation import gettext_lazy as _


INDCHOICES = (
    ("ADVERTISING", "广告"),
    ("AGRICULTURE", "农业"),
    ("APPAREL & ACCESSORIES", "服装与配饰"),
    ("AUTOMOTIVE", "汽车"),
    ("BANKING", "银行"),
    ("BIOTECHNOLOGY", "生物技术"),
    ("BUILDING MATERIALS & EQUIPMENT", "建筑材料与设备"),
    ("CHEMICAL", "化工"),
    ("COMPUTER", "计算机"),
    ("EDUCATION", "教育"),
    ("ELECTRONICS", "电子"),
    ("ENERGY", "能源"),
    ("ENTERTAINMENT & LEISURE", "娱乐与休闲"),
    ("FINANCE", "金融"),
    ("FOOD & BEVERAGE", "食品与饮料"),
    ("GROCERY", "杂货"),
    ("HEALTHCARE", "医疗保健"),
    ("INSURANCE", "保险"),
    ("LEGAL", "法律"),
    ("MANUFACTURING", "制造业"),
    ("PUBLISHING", "出版"),
    ("REAL ESTATE", "房地产"),
    ("SERVICE", "服务"),
    ("SOFTWARE", "软件"),
    ("SPORTS", "体育"),
    ("TECHNOLOGY", "技术"),
    ("TELECOMMUNICATIONS", "电信"),
    ("TELEVISION", "电视"),
    ("TRANSPORTATION", "交通"),
    ("VENTURE CAPITAL", "风险投资"),
)

TYPECHOICES = (
    ("CUSTOMER", "客户"),
    ("INVESTOR", "投资者"),
    ("PARTNER", "合作伙伴"),
    ("RESELLER", "经销商"),
)

ROLES = (
    ("ADMIN", "管理员"),
    ("USER", "用户"),
)

LEAD_STATUS = (
    ("assigned", "已分配"),
    ("in process", "处理中"),
    ("converted", "已转换"),
    ("recycled", "已回收"),
    ("closed", "已关闭"),
)


LEAD_SOURCE = (
    ("call", "电话"),
    ("email", "邮件"),
    ("existing customer", "现有客户"),
    ("partner", "合作伙伴"),
    ("public relations", "公共关系"),
    ("compaign", "营销活动"),
    ("other", "其他"),
)

STATUS_CHOICE = (
    ("New", "新建"),
    ("Assigned", "已分配"),
    ("Pending", "待处理"),
    ("Closed", "已关闭"),
    ("Rejected", "已拒绝"),
    ("Duplicate", "重复"),
)

PRIORITY_CHOICE = (
    ("Low", "低"),
    ("Normal", "普通"),
    ("High", "高"),
    ("Urgent", "紧急"),
)

CASE_TYPE = (("Question", "问题"), ("Incident", "事件"), ("Problem", "问题"))

STAGES = (
    ("PROSPECTING", "潜在客户"),
    ("QUALIFICATION", "资格审核"),
    ("PROPOSAL", "提案"),
    ("NEGOTIATION", "谈判"),
    ("CLOSED_WON", "已赢得"),
    ("CLOSED_LOST", "已丢失"),
)

OPPORTUNITY_TYPES = (
    ("NEW_BUSINESS", "新业务"),
    ("EXISTING_BUSINESS", "现有业务"),
    ("RENEWAL", "续约"),
    ("UPSELL", "追加销售"),
    ("CROSS_SELL", "交叉销售"),
)

SOURCES = (
    ("NONE", "无"),
    ("CALL", "电话"),
    ("EMAIL", "邮件"),
    ("EXISTING CUSTOMER", "现有客户"),
    ("PARTNER", "合作伙伴"),
    ("PUBLIC RELATIONS", "公共关系"),
    ("CAMPAIGN", "营销活动"),
    ("WEBSITE", "网站"),
    ("OTHER", "其他"),
)

EVENT_PARENT_TYPE = ((10, "客户"), (13, "线索"), (14, "商机"), (11, "工单"))

EVENT_STATUS = (
    ("Planned", "计划中"),
    ("Held", "已举行"),
    ("Not Held", "未举行"),
    ("Not Started", "未开始"),
    ("Started", "已开始"),
    ("Completed", "已完成"),
    ("Canceled", "已取消"),
    ("Deferred", "已推迟"),
)


COUNTRIES = (
    ("GB", _("英国")),
    ("AF", _("阿富汗")),
    ("AX", _("奥兰群岛")),
    ("AL", _("阿尔巴尼亚")),
    ("DZ", _("阿尔及利亚")),
    ("AS", _("美属萨摩亚")),
    ("AD", _("安道尔")),
    ("AO", _("安哥拉")),
    ("AI", _("安圭拉")),
    ("AQ", _("南极洲")),
    ("AG", _("安提瓜和巴布达")),
    ("AR", _("阿根廷")),
    ("AM", _("亚美尼亚")),
    ("AW", _("阿鲁巴")),
    ("AU", _("澳大利亚")),
    ("AT", _("奥地利")),
    ("AZ", _("阿塞拜疆")),
    ("BS", _("巴哈马")),
    ("BH", _("巴林")),
    ("BD", _("孟加拉国")),
    ("BB", _("巴巴多斯")),
    ("BY", _("白俄罗斯")),
    ("BE", _("比利时")),
    ("BZ", _("伯利兹")),
    ("BJ", _("贝宁")),
    ("BM", _("百慕大")),
    ("BT", _("不丹")),
    ("BO", _("玻利维亚")),
    ("BA", _("波斯尼亚和黑塞哥维那")),
    ("BW", _("博茨瓦纳")),
    ("BV", _("布维岛")),
    ("BR", _("巴西")),
    ("IO", _("英属印度洋领地")),
    ("BN", _("文莱")),
    ("BG", _("保加利亚")),
    ("BF", _("布基纳法索")),
    ("BI", _("布隆迪")),
    ("KH", _("柬埔寨")),
    ("CM", _("喀麦隆")),
    ("CA", _("加拿大")),
    ("CV", _("佛得角")),
    ("KY", _("开曼群岛")),
    ("CF", _("中非共和国")),
    ("TD", _("乍得")),
    ("CL", _("智利")),
    ("CN", _("中国")),
    ("CX", _("圣诞岛")),
    ("CC", _("科科斯（基林）群岛")),
    ("CO", _("哥伦比亚")),
    ("KM", _("科摩罗")),
    ("CG", _("刚果（布）")),
    ("CD", _("刚果（金）")),
    ("CK", _("库克群岛")),
    ("CR", _("哥斯达黎加")),
    ("CI", _("科特迪瓦")),
    ("HR", _("克罗地亚")),
    ("CU", _("古巴")),
    ("CY", _("塞浦路斯")),
    ("CZ", _("捷克共和国")),
    ("DK", _("丹麦")),
    ("DJ", _("吉布提")),
    ("DM", _("多米尼克")),
    ("DO", _("多米尼加共和国")),
    ("EC", _("厄瓜多尔")),
    ("EG", _("埃及")),
    ("SV", _("萨尔瓦多")),
    ("GQ", _("赤道几内亚")),
    ("ER", _("厄立特里亚")),
    ("EE", _("爱沙尼亚")),
    ("ET", _("埃塞俄比亚")),
    ("FK", _("福克兰群岛（马尔维纳斯）")),
    ("FO", _("法罗群岛")),
    ("FJ", _("斐济")),
    ("FI", _("芬兰")),
    ("FR", _("法国")),
    ("GF", _("法属圭亚那")),
    ("PF", _("法属波利尼西亚")),
    ("TF", _("法属南部领地")),
    ("GA", _("加蓬")),
    ("GM", _("冈比亚")),
    ("GE", _("格鲁吉亚")),
    ("DE", _("德国")),
    ("GH", _("加纳")),
    ("GI", _("直布罗陀")),
    ("GR", _("希腊")),
    ("GL", _("格陵兰")),
    ("GD", _("格林纳达")),
    ("GP", _("瓜德罗普")),
    ("GU", _("关岛")),
    ("GT", _("危地马拉")),
    ("GG", _("根西岛")),
    ("GN", _("几内亚")),
    ("GW", _("几内亚比绍")),
    ("GY", _("圭亚那")),
    ("HT", _("海地")),
    ("HM", _("赫德岛和麦克唐纳群岛")),
    ("VA", _("梵蒂冈")),
    ("HN", _("洪都拉斯")),
    ("HK", _("香港")),
    ("HU", _("匈牙利")),
    ("IS", _("冰岛")),
    ("IN", _("印度")),
    ("ID", _("印度尼西亚")),
    ("IR", _("伊朗")),
    ("IQ", _("伊拉克")),
    ("IE", _("爱尔兰")),
    ("IM", _("马恩岛")),
    ("IL", _("以色列")),
    ("IT", _("意大利")),
    ("JM", _("牙买加")),
    ("JP", _("日本")),
    ("JE", _("泽西岛")),
    ("JO", _("约旦")),
    ("KZ", _("哈萨克斯坦")),
    ("KE", _("肯尼亚")),
    ("KI", _("基里巴斯")),
    ("KP", _("朝鲜")),
    ("KR", _("韩国")),
    ("KW", _("科威特")),
    ("KG", _("吉尔吉斯斯坦")),
    ("LA", _("老挝")),
    ("LV", _("拉脱维亚")),
    ("LB", _("黎巴嫩")),
    ("LS", _("莱索托")),
    ("LR", _("利比里亚")),
    ("LY", _("利比亚")),
    ("LI", _("列支敦士登")),
    ("LT", _("立陶宛")),
    ("LU", _("卢森堡")),
    ("MO", _("澳门")),
    ("MK", _("北马其顿")),
    ("MG", _("马达加斯加")),
    ("MW", _("马拉维")),
    ("MY", _("马来西亚")),
    ("MV", _("马尔代夫")),
    ("ML", _("马里")),
    ("MT", _("马耳他")),
    ("MH", _("马绍尔群岛")),
    ("MQ", _("马提尼克")),
    ("MR", _("毛里塔尼亚")),
    ("MU", _("毛里求斯")),
    ("YT", _("马约特")),
    ("MX", _("墨西哥")),
    ("FM", _("密克罗尼西亚")),
    ("MD", _("摩尔多瓦")),
    ("MC", _("摩纳哥")),
    ("MN", _("蒙古")),
    ("ME", _("黑山")),
    ("MS", _("蒙特塞拉特")),
    ("MA", _("摩洛哥")),
    ("MZ", _("莫桑比克")),
    ("MM", _("缅甸")),
    ("NA", _("纳米比亚")),
    ("NR", _("瑙鲁")),
    ("NP", _("尼泊尔")),
    ("NL", _("荷兰")),
    ("AN", _("荷属安的列斯")),
    ("NC", _("新喀里多尼亚")),
    ("NZ", _("新西兰")),
    ("NI", _("尼加拉瓜")),
    ("NE", _("尼日尔")),
    ("NG", _("尼日利亚")),
    ("NU", _("纽埃")),
    ("NF", _("诺福克岛")),
    ("MP", _("北马里亚纳群岛")),
    ("NO", _("挪威")),
    ("OM", _("阿曼")),
    ("PK", _("巴基斯坦")),
    ("PW", _("帕劳")),
    ("PS", _("巴勒斯坦领土")),
    ("PA", _("巴拿马")),
    ("PG", _("巴布亚新几内亚")),
    ("PY", _("巴拉圭")),
    ("PE", _("秘鲁")),
    ("PH", _("菲律宾")),
    ("PN", _("皮特凯恩群岛")),
    ("PL", _("波兰")),
    ("PT", _("葡萄牙")),
    ("PR", _("波多黎各")),
    ("QA", _("卡塔尔")),
    ("RE", _("留尼汪")),
    ("RO", _("罗马尼亚")),
    ("RU", _("俄罗斯")),
    ("RW", _("卢旺达")),
    ("BL", _("圣巴泰勒米")),
    ("SH", _("圣赫勒拿")),
    ("KN", _("圣基茨和尼维斯")),
    ("LC", _("圣卢西亚")),
    ("MF", _("圣马丁")),
    ("PM", _("圣皮埃尔和密克隆")),
    ("VC", _("圣文森特和格林纳丁斯")),
    ("WS", _("萨摩亚")),
    ("SM", _("圣马力诺")),
    ("ST", _("圣多美和普林西比")),
    ("SA", _("沙特阿拉伯")),
    ("SN", _("塞内加尔")),
    ("RS", _("塞尔维亚")),
    ("SC", _("塞舌尔")),
    ("SL", _("塞拉利昂")),
    ("SG", _("新加坡")),
    ("SK", _("斯洛伐克")),
    ("SI", _("斯洛文尼亚")),
    ("SB", _("所罗门群岛")),
    ("SO", _("索马里")),
    ("ZA", _("南非")),
    ("GS", _("南乔治亚和南桑威奇群岛")),
    ("ES", _("西班牙")),
    ("LK", _("斯里兰卡")),
    ("SD", _("苏丹")),
    ("SR", _("苏里南")),
    ("SJ", _("斯瓦尔巴和扬马延")),
    ("SZ", _("斯威士兰")),
    ("SE", _("瑞典")),
    ("CH", _("瑞士")),
    ("SY", _("叙利亚")),
    ("TW", _("台湾（中国省份）")),
    ("TJ", _("塔吉克斯坦")),
    ("TZ", _("坦桑尼亚")),
    ("TH", _("泰国")),
    ("TL", _("东帝汶")),
    ("TG", _("多哥")),
    ("TK", _("托克劳")),
    ("TO", _("汤加")),
    ("TT", _("特立尼达和多巴哥")),
    ("TN", _("突尼斯")),
    ("TR", _("土耳其")),
    ("TM", _("土库曼斯坦")),
    ("TC", _("特克斯和凯科斯群岛")),
    ("TV", _("图瓦卢")),
    ("UG", _("乌干达")),
    ("UA", _("乌克兰")),
    ("AE", _("阿拉伯联合酋长国")),
    ("US", _("美国")),
    ("UM", _("美国本土外小岛屿")),
    ("UY", _("乌拉圭")),
    ("UZ", _("乌兹别克斯坦")),
    ("VU", _("瓦努阿图")),
    ("VE", _("委内瑞拉")),
    ("VN", _("越南")),
    ("VG", _("英属维尔京群岛")),
    ("VI", _("美属维尔京群岛")),
    ("WF", _("瓦利斯和富图纳")),
    ("EH", _("西撒哈拉")),
    ("YE", _("也门")),
    ("ZM", _("赞比亚")),
    ("ZW", _("津巴布韦")),
)

CURRENCY_CODES = (
    ("USD", _("美元")),
    ("EUR", _("欧元")),
    ("GBP", _("英镑")),
    ("INR", _("印度卢比")),
    ("CAD", _("加拿大元")),
    ("AUD", _("澳大利亚元")),
    ("JPY", _("日元")),
    ("CNY", _("人民币")),
    ("CHF", _("瑞士法郎")),
    ("SGD", _("新加坡元")),
    ("AED", _("阿联酋迪拉姆")),
    ("BRL", _("巴西雷亚尔")),
    ("MXN", _("墨西哥比索")),
)

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "INR": "₹",
    "CAD": "CA$",
    "AUD": "A$",
    "JPY": "¥",
    "CNY": "¥",
    "CHF": "CHF",
    "SGD": "S$",
    "AED": "د.إ",
    "BRL": "R$",
    "MXN": "MX$",
}

# 工具函数保持不变...
def convert_to_custom_timezone(custom_date, custom_timezone, to_utc=False):
    user_time_zone = pytz.timezone(custom_timezone)
    if to_utc:
        custom_date = user_time_zone.localize(custom_date.replace(tzinfo=None))
        user_time_zone = pytz.UTC
    return custom_date.astimezone(user_time_zone)


# =============================================================================
# CRM Entity Utilities
# =============================================================================

def get_or_create_tags(tag_data, org):
    """
    Handle tag creation/lookup for any CRM model.

    Args:
        tag_data: List of tag names or JSON string of tag names
        org: Organization instance

    Returns:
        List of Tag objects
    """
    import json
    from common.models import Tags

    tags = []
    if not tag_data:
        return tags

    # Handle JSON string input
    if isinstance(tag_data, str):
        try:
            tag_data = json.loads(tag_data)
        except json.JSONDecodeError:
            tag_data = [tag_data]

    for tag_name in tag_data:
        if not tag_name:
            continue
        tag_obj, _ = Tags.objects.get_or_create(
            slug=tag_name.lower(),
            org=org,
            defaults={'name': tag_name}
        )
        tags.append(tag_obj)
    return tags


def handle_m2m_assignment(instance, field_name, ids, model_class, org, extra_filters=None):
    """
    Handle ManyToMany field assignment with org filtering.

    Args:
        instance: Model instance with the M2M field
        field_name: Name of the M2M field
        ids: List of IDs or JSON string of IDs to assign
        model_class: The related model class
        org: Organization instance
        extra_filters: Optional dict of additional filters (e.g., {'is_active': True})

    Returns:
        QuerySet of objects that were assigned
    """
    import json

    field = getattr(instance, field_name)

    if not ids:
        return model_class.objects.none()

    # Handle JSON string input
    if isinstance(ids, str):
        try:
            ids = json.loads(ids)
        except json.JSONDecodeError:
            ids = [ids]

    filters = {'id__in': ids, 'org': org}
    if extra_filters:
        filters.update(extra_filters)

    objects = model_class.objects.filter(**filters)
    if objects.exists():
        field.add(*objects)
    return objects


def create_attachment(file, content_object, profile):
    """
    Create an attachment for any CRM content object.

    Args:
        file: The uploaded file object
        content_object: The model instance to attach to
        profile: The user's profile

    Returns:
        Attachments instance
    """
    from common.models import Attachments

    attachment = Attachments()
    attachment.created_by = profile.user
    attachment.file_name = file.name
    attachment.content_object = content_object
    attachment.attachment = file
    attachment.org = profile.org
    attachment.save()
    return attachment


# =============================================================================
# Document File Type Utilities
# =============================================================================

def is_document_file_image(ext):
    image_ext_list = [
        "bmp", "dds", "gif", "jpg", "jpeg", "png", "psd",
        "pspimage", "tga", "thm", "tif", "tiff", "yuv",
    ]
    return ext.lower() in image_ext_list


def is_document_file_audio(ext):
    audio_ext_list = ["aif", "iff", "m3u", "m4a", "mid", "mp3", "mpa", "wav", "wma"]
    return ext.lower() in audio_ext_list


def is_document_file_video(ext):
    video_ext_list = [
        "3g2", "3gp", "asf", "avi", "flv", "m4v", "mov",
        "mp4", "mpg", "rm", "srt", "swf", "vob", "wmv",
    ]
    return ext.lower() in video_ext_list


def is_document_file_pdf(ext):
    pdf_ext_list = ["indd", "pct", "pdf"]
    return ext.lower() in pdf_ext_list


def is_document_file_code(ext):
    code_ext_list = [
        "aspx", "json", "jsp", "do", "htm", "html", "ser", "php", "jad", "cfm",
        "xml", "js", "pod", "asp", "atomsvc", "rdf", "pou", "jsf", "abs", "pl",
        "asm", "srz", "luac", "cod", "lib", "arxml", "bas", "ejs", "fs", "hbs",
        "s", "ss", "cms", "pyc", "vcxproj", "jse", "smali", "xla", "lxk", "pdb",
        "src", "cs", "ipb", "ave", "mst", "vls", "rcc", "sax", "scr", "dtd",
        "axd", "mrl", "xsl", "ino", "spr", "xsd", "cgi", "isa", "ws", "rss",
        "dvb", "nupkg", "xlm", "v4e", "prg", "form", "bat", "mrc", "asi", "jdp",
        "fmb", "graphml", "gcode", "aia", "py", "atp", "mzp", "o", "scs", "mm",
        "cpp", "java", "gypi", "idb", "txml", "c", "vip", "tra", "rc", "action",
        "vlx", "asta", "pyo", "lua", "gml", "prl", "rfs", "cpb", "sh", "rbf",
        "gp", "phtml", "bp", "scb", "sln", "vbp", "wbf", "bdt", "mac", "rpy",
        "eaf", "mc", "mwp", "gnt", "h", "swift", "e", "styl", "cxx", "as",
        "liquid", "dep", "fas", "vbs", "aps", "vbe", "lss", "cmake", "resx",
        "csb", "dpk", "pdml", "txx", "dbg", "jsa", "sxs", "sasf", "pm", "csx",
        "r", "wml", "au3", "stm", "cls", "cc", "ins", "jsc", "dwp", "rpg",
        "arb", "bml", "inc", "eld", "sct", "sm", "wbt", "csproj", "tcz", "html5",
        "gbl", "cmd", "dlg", "tpl", "rbt", "xcp", "tpm", "qry", "mfa", "ptx",
        "lsp", "pag", "ebc", "php3", "cob", "csc", "pyt", "dwt", "rb", "wsdl",
        "lap", "textile", "sfx", "x", "a5r", "dbp", "pmp", "ipr", "fwx", "pbl",
        "vbw", "phl", "cbl", "pas", "mom", "dbmdl", "lol", "wdl", "ppam", "plx",
        "vb", "cgx", "lst", "lmp", "vd", "bcp", "thtml", "scpt", "isu", "mrd",
        "perl", "dtx", "f", "wpk", "ipf", "ptl", "luca", "hx", "uvproj", "qvs",
        "vba", "xjb", "appxupload", "ti", "svn-base", "bsc", "mak", "vcproj",
        "dsd", "ksh", "pyw", "bxml", "mo", "irc", "gcl", "dbml", "mlv", "wsf",
        "tcl", "dqy", "ssi", "pbxproj", "bal", "trt", "sal", "hkp", "vbi", "dob",
        "htc", "p", "ats", "seam", "loc", "pli", "rptproj", "pxml", "pkb", "dpr",
        "scss", "dsb", "bb", "vbproj", "ash", "rml", "nbk", "nvi", "lmv", "mw",
        "jl", "dso", "cba", "jks", "ary", "run", "vps", "clm", "brml", "msha",
        "mdp", "tmh", "jsx", "sdl", "ptxml", "fxl", "wmw", "dcr", "bcc", "cbp",
        "bmo", "bsv", "less", "gss", "ctl", "rpyc", "ascx", "odc", "wiki", "obr",
        "l", "axs", "bpr", "ppa", "rpo", "sqlproj", "smm", "dsr", "arq", "din",
        "jml", "jsonp", "ml", "rc2", "myapp", "cla", "xme", "obj", "jsdtscope",
        "gyp", "datasource", "cp", "rh", "lpx", "a2w", "ctp", "ulp", "nt",
        "script", "bxl", "gs", "xslt", "mg", "pch", "mhl", "zpd", "psm1", "asz",
        "m", "jacl", "pym", "rws", "acu", "ssq", "wxs", "coffee", "ncb", "akt",
        "pyx", "zero", "hs", "mkb", "tru", "xul", "mfl", "sca", "sbr", "master",
        "opv", "matlab", "sami", "agc", "slim", "tea", "m51", "mec", "asc",
        "gch", "enml", "kst", "jade", "dfb", "ips", "rgs", "vbx", "cspkg", "ncx",
        "brs", "wfs", "ifp", "nse", "xtx", "j", "cx", "ps1", "nas", "mk", "ccs",
        "vrp", "lnp", "cml", "c#", "idl", "exp", "apb", "nsi", "asmx", "tdo",
        "pjt", "fdt", "s5d", "mvba", "mf", "odl", "bzs", "jardesc", "tgml",
        "moc", "wxi", "cpz", "fsx", "jav", "ocb", "agi", "tec", "txl", "amw",
        "mscr", "dfd", "dpd", "pun", "f95", "vdproj", "xsc", "diff", "wxl",
        "dgml", "airi", "kmt", "ksc", "io", "rbw", "sas", "vcp", "resources",
        "param", "cg", "hlsl", "vssscc", "bgm", "xn", "targets", "sl", "gsc",
        "qs", "owl", "devpak", "phps", "hdf", "pri", "nbin", "xaml", "s4e",
        "scm", "tk", "poc", "uix", "clw", "factorypath", "s43", "awd", "htr",
        "php2", "classpath", "pickle", "rob", "msil", "ebx", "tsq", "lml", "f90",
        "lds", "vup", "pbi", "swt", "vap", "ig", "pdo", "frt", "fcg", "c++",
        "xcl", "dfn", "aar", "for", "re", "twig", "ebm", "dhtml", "hc", "pro",
        "ahk", "rule", "bsh", "jcs", "zrx", "wsdd", "csp", "drc", "appxsym",
    ]
    return ext.lower() in code_ext_list


def is_document_file_text(ext):
    text_ext_list = [
        "doc", "docx", "log", "msg", "odt", "pages", "rtf", "tex", "txt", "wpd", "wps",
    ]
    return ext.lower() in text_ext_list


def is_document_file_sheet(ext):
    sheet_ext_list = ["csv", "xls", "xlsx", "xlsm", "xlsb", "xltx", "xltm", "xlt"]
    return ext.lower() in sheet_ext_list


def is_document_file_zip(ext):
    ext_list = ["zip", "7z", "gz", "rar", "zipx", "ace", "tar"]
    return ext.lower() in ext_list