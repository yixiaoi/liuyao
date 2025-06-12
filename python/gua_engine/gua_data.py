# 这是一个示例的 Gua 数据结构，实际使用时会根据具体的输入和计算结果进行填充
Gua = {
    "raw_input": ["少阳", "老阳", "少阴", "少阴", "老阴", "少阳"],
    "original_hexagram": [1, 1, 0, 0, 0, 1],  # 1 为阳爻，0 为阴爻
    "changed_hexagram": [1, 0, 0, 0, 1, 1],   # 动爻变爻后的结果
    "lines": [
        {
            "index": 1,     # 初爻为1，往上是2、3、4、5、6
            "raw": "少阳",
            "is_yang": True,
            "is_moving": False,
            "changed": True,   # 动爻才有变
            "line_symbol": "---",   # 阴或阳
            "after_change": "---",  # 阴变阳 or 阳变阴
            "na_jia_gan": "",  # 纳甲天干
            "na_jia_zhi": "",  # 纳甲地支
            "six_god": "",       # 六神（后续）
            "six_relative": "",  # 六亲（后续）
            "element": "",       # 五行（后续）
            "is_subject": False, # 是否为世爻
            "is_object": False   # 是否为应爻
        },
        ...
    ],
    "hexagram_name": "泽山咸",    # 六十四卦卦名
    "hexagram_number": 0,   # 卦序号（1~64）
    "month_branch": "",     # 月支
    "day_branch": ""        # 日支
}



# 八卦名 → 3位阴阳值（0阴1阳）从下往上
eight_gua = {
    "乾": (1, 1, 1),
    "兑": (1, 1, 0),
    "离": (1, 0, 1),
    "震": (1, 0, 0),
    "巽": (0, 1, 1),
    "坎": (0, 1, 0),
    "艮": (0, 0, 1),
    "坤": (0, 0, 0),
}

# 倒过来的映射：3位 → 八卦名
three_yao_to_gua = {v: k for k, v in eight_gua.items()}

# 下卦名 + 上卦名 → 卦名，宫位, 类型
# 八宫卦序映射表 (京房易)
sixty_four_gua = {
    # 乾宫 (乾为天)
    ("乾", "乾"): ("乾为天", "乾", "本宫"),
    ("巽", "乾"): ("天风姤", "乾", "一世"),
    ("艮", "乾"): ("天山遁", "乾", "二世"),
    ("坤", "乾"): ("天地否", "乾", "三世"),
    ("坤", "巽"): ("风地观", "乾", "四世"),
    ("坤", "艮"): ("山地剥", "乾", "五世"),
    ("坤", "离"): ("火地晋", "乾", "游魂"),
    ("乾", "离"): ("火天大有", "乾", "归魂"),
    
    # 兑宫 (兑为泽)
    ("兑", "兑"): ("兑为泽", "兑", "本宫"),
    ("坎", "兑"): ("泽水困", "兑", "一世"),
    ("坤", "兑"): ("泽地萃", "兑", "二世"),
    ("艮", "兑"): ("泽山咸", "兑", "三世"),
    ("艮", "坎"): ("水山蹇", "兑", "四世"),
    ("艮", "坤"): ("地山谦", "兑", "五世"),
    ("艮", "震"): ("雷山小过", "兑", "游魂"),
    ("兑", "震"): ("雷泽归妹", "兑", "归魂"),
    
    # 离宫 (离为火)
    ("离", "离"): ("离为火", "离", "本宫"),
    ("艮", "离"): ("火山旅", "离", "一世"),
    ("巽", "离"): ("火风鼎", "离", "二世"),
    ("坎", "离"): ("火水未济", "离", "三世"),
    ("坎", "艮"): ("山水蒙", "离", "四世"),
    ("坎", "巽"): ("风水涣", "离", "五世"),
    ("坎", "乾"): ("天水讼", "离", "游魂"),
    ("离", "乾"): ("天火同人", "离", "归魂"),
    
    # 震宫 (震为雷)
    ("震", "震"): ("震为雷", "震", "本宫"),
    ("坤", "震"): ("雷地豫", "震", "一世"),
    ("坎", "震"): ("雷水解", "震", "二世"),
    ("巽", "震"): ("雷风恒", "震", "三世"),
    ("巽", "坤"): ("地风升", "震", "四世"),
    ("巽", "坎"): ("水风井", "震", "五世"),
    ("巽", "兑"): ("泽风大过", "震", "游魂"),
    ("震", "兑"): ("泽雷随", "震", "归魂"),
    
    # 巽宫 (巽为风)
    ("巽", "巽"): ("巽为风", "巽", "本宫"),
    ("乾", "巽"): ("风天小畜", "巽", "一世"),
    ("离", "巽"): ("风火家人", "巽", "二世"),
    ("震", "巽"): ("风雷益", "巽", "三世"),
    ("震", "乾"): ("天雷无妄", "巽", "四世"),
    ("震", "离"): ("火雷噬嗑", "巽", "五世"),
    ("震", "艮"): ("山雷颐", "巽", "游魂"),
    ("巽", "艮"): ("山风蛊", "巽", "归魂"),
    
    # 坎宫 (坎为水)
    ("坎", "坎"): ("坎为水", "坎", "本宫"),
    ("兑", "坎"): ("水泽节", "坎", "一世"),
    ("震", "坎"): ("水雷屯", "坎", "二世"),
    ("离", "坎"): ("水火既济", "坎", "三世"),
    ("离", "兑"): ("泽火革", "坎", "四世"),
    ("离", "震"): ("雷火丰", "坎", "五世"),
    ("离", "坤"): ("地火明夷", "坎", "游魂"),
    ("坎", "坤"): ("地水师", "坎", "归魂"),
    
    # 艮宫 (艮为山)
    ("艮", "艮"): ("艮为山", "艮", "本宫"),
    ("离", "艮"): ("山火贲", "艮", "一世"),
    ("乾", "艮"): ("山天大畜", "艮", "二世"),
    ("兑", "艮"): ("山泽损", "艮", "三世"),
    ("兑", "离"): ("火泽睽", "艮", "四世"),
    ("兑", "乾"): ("天泽履", "艮", "五世"),
    ("兑", "巽"): ("风泽中孚", "艮", "游魂"),
    ("艮", "巽"): ("风山渐", "艮", "归魂"),
    
    # 坤宫 (坤为地)
    ("坤", "坤"): ("坤为地", "坤", "本宫"),
    ("震", "坤"): ("地雷复", "坤", "一世"),
    ("兑", "坤"): ("地泽临", "坤", "二世"),
    ("乾", "坤"): ("地天泰", "坤", "三世"),
    ("乾", "震"): ("雷天大壮", "坤", "四世"),
    ("乾", "兑"): ("泽天夬", "坤", "五世"),
    ("乾", "坎"): ("水天需", "坤", "游魂"),
    ("坤", "坎"): ("水地比", "坤", "归魂")
}

na_jia_table = {
    "乾": {
        "inner": [("甲", "子"), ("甲", "寅"), ("甲", "辰")],
        "outer": [("壬", "午"), ("壬", "申"), ("壬", "戌")],
    },
    "坤": {
        "inner": [("乙", "未"), ("乙", "巳"), ("乙", "卯")],
        "outer": [("癸", "丑"), ("癸", "亥"), ("癸", "酉")],
    },
    "坎": {
        "inner": [("戊", "寅"), ("戊", "辰"), ("戊", "午")],
        "outer": [("戊", "申"), ("戊", "戌"), ("戊", "子")],
    },
    "艮": {
        "inner": [("丙", "辰"), ("丙", "午"), ("丙", "申")],
        "outer": [("丙", "戌"), ("丙", "子"), ("丙", "寅")],
    },
    "震": {
        "inner": [("庚", "子"), ("庚", "寅"), ("庚", "辰")],
        "outer": [("庚", "午"), ("庚", "申"), ("庚", "戌")],
    },
    "巽": {
        "inner": [("辛", "丑"), ("辛", "亥"), ("辛", "酉")],
        "outer": [("辛", "未"), ("辛", "巳"), ("辛", "卯")],
    },
    "离": {
        "inner": [("己", "卯"), ("己", "丑"), ("己", "亥")],
        "outer": [("己", "酉"), ("己", "未"), ("己", "巳")],
    },
    "兑": {
        "inner": [("丁", "巳"), ("丁", "卯"), ("丁", "丑")],
        "outer": [("丁", "亥"), ("丁", "酉"), ("丁", "未")],
    },
}

zhi_to_element = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}
element_to_zhi = {v: k for k, v in zhi_to_element.items()}

eight_gua_to_element = {
    "乾": "金", "兑": "金", "离": "火", "震": "木",
    "巽": "木", "坎": "水", "艮": "土", "坤": "土"
}

element_generate_me = {"金": "土", "水": "金", "木": "水", "火": "木", "土": "火"}
element_i_generate = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
element_i_overcome = {"金": "木", "水": "火", "木": "土", "火": "金", "土": "水"}
element_overcome_me = {"金": "火", "水": "土", "木": "金", "火": "水", "土": "木"}


# 地支合关系
zhi_he = {'子': '丑', '寅': '亥', '卯': '戌', '辰': '酉',
          '巳': '申', '午': '未', '丑': '子', '亥': '寅',
          '戌': '卯', '酉': '辰', '申': '巳', '未': '午'}

# 地支冲关系
zhi_chong = {'子': '午', '丑': '未', '寅': '申', '卯': '酉',
             '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
             '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'}

# 有余气（简化，可进一步扩展）
month_qi = {
    '辰': ['寅', '卯'],
    '未': ['巳', '午'],
    '戌': ['申', '酉'],
    '丑': ['亥', '子']
}

def is_conflict(yao_zhi, zhi):
    return zhi_chong.get(yao_zhi) == zhi

def is_he(yao_zhi, zhi):
    return zhi_he.get(yao_zhi) == zhi

def calc_relation(yao_element, yao_zhi, zhi, zhi_element, label):
    score = 0
    desc = []

    if yao_zhi == zhi:
        desc.append(f"临{label}")
        score += 2
    elif element_generate_me.get(yao_element) == zhi_element and is_he(yao_zhi, zhi):
        desc.append(f"{label}生合")
        score += 2
    elif yao_element == zhi_element and yao_zhi != zhi:
        desc.append(f"{label}相扶")
        score += 1
    elif element_generate_me.get(yao_element) == zhi_element:
        desc.append(f"{label}相生")
        score += 1
    elif is_he(yao_zhi, zhi):
        desc.append(f"{label}平合")
        score += 0.5
    elif zhi in month_qi.get(yao_zhi, []) and label == "月建":
        desc.append(f"有{label}气")
        score += 0.5
    elif element_overcome_me.get(yao_element) == zhi_element and is_he(yao_zhi, zhi):
        desc.append(f"{label}克合")
        score -= 0.5
    elif element_overcome_me.get(yao_element) == zhi_element:
        desc.append(f"{label}相克")
        score -= 1
    else:
        desc.append(f"{label}休囚")
        score -= 0.1

    return score, desc


# 写死的旬空表，每组旬含10个日干支，对应一个旬空地支对
xunkong_table = {
    "甲子": ("戌", "亥"),
    "甲戌": ("申", "酉"),
    "甲申": ("午", "未"),
    "甲午": ("辰", "巳"),
    "甲辰": ("寅", "卯"),
    "甲寅": ("子", "丑"),
}

# 六十甲子顺序
liushijiazi = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
]


def is_xunkong_func(yao, day_ganzhi):
    yao_dizhi = yao['najia_di_zhi']
    # 遍历查找 day_ganzhi 属于哪个旬
    for xun_start, xunkong_pair in xunkong_table.items():
        start_index = liushijiazi.index(xun_start)
        xun_group = liushijiazi[start_index:start_index + 10]
        if day_ganzhi in xun_group:
            return yao_dizhi in xunkong_pair

    # 不在表中则默认不空
    return False

# 地支冲关系
jin_shen = {'寅': '卯', '申': '酉', '丑': '辰', '未': '戌'}

tui_shen = {'卯': '寅', '酉': '申', '辰': '丑', '戌': '未'}

def is_jin_shen(yao):
    """判断变爻是否为进神"""
    if not yao["is_changed"]:
        return False
    yao_dizhi = yao['najia_di_zhi']
    changed_dizhi = yao["changed_properties"].get("najia_di_zhi", "")

    if not yao_dizhi in jin_shen:
        return False
    
    if jin_shen.get(yao_dizhi) == changed_dizhi:
        #print(f"进神{yao_dizhi}变为{changed_dizhi}")
        yao["changed_properties"]["description"] += f"进神：{yao_dizhi}变为{changed_dizhi}。" 
        return True
    else:
        return False


def is_tui_shen(yao):
    """判断变爻是否为退神"""
    if not yao["is_changed"]:
        return False
    yao_dizhi = yao['najia_di_zhi']
    changed_dizhi = yao["changed_properties"].get("najia_di_zhi", "")

    if not yao_dizhi in tui_shen:
        return False
    
    if jin_shen.get(yao_dizhi) == changed_dizhi:
        yao["changed_properties"]["description"] += f"退神{yao_dizhi}变为{changed_dizhi}。" 
        #print(f"退神{yao_dizhi}变为{changed_dizhi}")
        return True
    else:
        return False
    
def is_fan_ying(yao):
    """
    判断变爻是否为反吟
    指变爻的地支与原爻的地支相冲
    """
    if not yao["is_changed"]:
        return False
    yao_dizhi = yao['najia_di_zhi']
    changed_dizhi = yao["changed_properties"].get("najia_di_zhi", "")
    
    if is_conflict(yao_dizhi,changed_dizhi):
        yao["changed_properties"]["description"] += f"反吟：{yao_dizhi}与{changed_dizhi}相冲。"
        # print(f"反吟：{yao_dizhi}与{changed_dizhi}相冲")
        return True  
    else:
        return False
    
def is_fu_ying(yao):
    """
    判断变爻是否为伏吟
    指变爻的地支与原爻的地支完全相同
    """
    if not yao["is_changed"]:
        return False
    yao_dizhi = yao['najia_di_zhi']
    changed_dizhi = yao["changed_properties"].get("najia_di_zhi", "")
    
    if yao_dizhi == changed_dizhi:
        yao["changed_properties"]["description"] += f"伏吟：{yao_dizhi}与{changed_dizhi}相同。"
        return True  
    else:
        return False
    
def is_hui_tou_sheng(yao):
    """
    判断变爻是否为回头生
    指变爻的地支与原爻的地支相合
    """
    if not yao["is_changed"]:
        return False
    yao_element = yao['element']
    changed_element = yao["changed_properties"].get("element", "")
    
    if element_generate_me.get(yao_element) == changed_element:
        yao["changed_properties"]["description"] += f"回头生：{yao_element}被{changed_element}生。"
        return True  
    else:
        return False
def is_hui_tou_ke(yao):
    """
    判断变爻是否为回头克
    指变爻的地支与原爻的地支相克
    """
    if not yao["is_changed"]:
        return False
    yao_element = yao['element']
    changed_element = yao["changed_properties"].get("element", "")
    
    if element_overcome_me.get(yao_element) == changed_element:
        yao["changed_properties"]["description"] += f"回头克：{yao_element}被{changed_element}克。"
        return True  
    else:
        return False
    
def check_changed_yao(yao):
    """
    检查变爻的各种状态
    """
    yao["changed_properties"]["description"] = ""
    yao["is_jin_shen"] = is_jin_shen(yao)
    yao["is_tui_shen"] = is_tui_shen(yao)
    yao["is_fan_ying"] = is_fan_ying(yao)
    yao["is_fu_ying"] = is_fu_ying(yao)
    yao["is_hui_tou_sheng"] = is_hui_tou_sheng(yao)
    yao["is_hui_tou_ke"] = is_hui_tou_ke(yao)


    
def change_yao_to_others_relation(yao, gua):
    source_index = yao["index"]
    source_element = yao["element"]
    source_zhi = yao["najia_di_zhi"]

    # 遍历所有其他爻
    for target in gua["lines"]:
        target_index = target["index"]
        if target_index == source_index:
            continue  # 跳过自身

        target_element = target["element"]
        target_zhi = target["najia_di_zhi"]

        # 判断生克关系
        if element_generate_me.get(target_element) == source_element:
            target.setdefault("relations", [])
            target["relations"].append({
                "from": source_index,
                "type": "generate",
                "description": f"动爻{source_index}生爻{target_index}"
            })
        elif element_overcome_me.get(target_element) == source_element:
            target.setdefault("relations", [])
            target["relations"].append({
                "from": source_index,
                "type": "overcome",
                "description": f"动爻{source_index}生爻{target_index}"
            })
        
        # if is_conflict(source_zhi, target_zhi):
        #     target.setdefault("relations", [])
        #     target["relations"].append({
        #         "from": source_index,
        #         "type": "conflict",
        #         "description": f"动爻{source_index}冲爻{target_index}"
        #     })
        # if is_he(source_zhi, target_zhi):
        #     target.setdefault("relations", [])
        #     target["relations"].append({
        #         "from": source_index,
        #         "type": "he",
        #         "description": f"动爻{source_index}合爻{target_index}"
        #     })

    return gua

def yong_shen_relation(yao,yongshen_element,yongshen_index):
    """
    判断用神与动爻的关系
    :param yao: dict，动爻信息
    :param yongshen_element: str，用神的五行元素
    :return: str，描述关系
    :return: bool，是否为元神
    """
    yao_element = yao['element']
    
    
    if yao_element == yongshen_element:
        if yao["index"] == yongshen_index:
            return ("",False)
        else:
            return (f"此爻为用神两现。", False)
    elif element_generate_me.get(yongshen_element) == yao_element:
        return (f"此爻为元神，生用神，是用神力量的源泉，有利的因素，也代表人的思想、想法、思维、意识等",True)
    elif element_overcome_me.get(yongshen_element) == yao_element:
        return (f"此爻为忌神，克用神，是不利用神的因素，表现为阻碍，灾煞、死对头等",False)
    elif element_i_overcome.get(yongshen_element) == yao_element:
        return (f"此爻为仇神,此爻为间接对用神产生不好的影响，表现为仇人、小人、背后说坏话之人",True)
    
    return ("", False)
    

