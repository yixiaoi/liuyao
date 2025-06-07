from typing import List, Dict
from gua_engine.gua_data import three_yao_to_gua, sixty_four_gua, na_jia_table,zhi_to_element,eight_gua_to_element


def build_hexagram(raw_input: List[str],day_gan: str = "", day_zhi: str = "", month_gan: str = "",month_zhi: str = "") -> Dict:
    gua = step1_parse_input(raw_input)
    gua = step2_get_gua_name(gua)
    gua = step3_assign_subject_object(gua)
    gua = step4_assign_na_jia(gua)
    gua = step5_assign_wuxing(gua)
    gua = step6_assign_six_relative(gua)
    gua = step7_assign_six_gods(gua, day_gan)
    gua = step8_assign_changed_lines_info(gua)
    gua["month_gan"] =  month_gan
    gua["month_zhi"] =  month_zhi
    gua["day_gan"] = day_gan
    gua["day_zhi"] = day_zhi
    return gua


def step1_parse_input(raw_input: List[str]) -> Dict:

    valid_yao_types = {"少阳", "老阳", "少阴", "老阴"}
    
    if len(raw_input) != 6:
        raise ValueError(f"需要6爻输入，当前输入 {len(raw_input)} 爻")
    
    invalid_yao = set(raw_input) - valid_yao_types
    if invalid_yao:
        raise ValueError(f"发现无效爻类型: {', '.join(invalid_yao)}. 只允许: 少阳, 老阳, 少阴, 老阴")

    yao_map = {
        "少阳": {"is_yang": True, "is_moving": False},
        "老阳": {"is_yang": True, "is_moving": True},
        "少阴": {"is_yang": False, "is_moving": False},
        "老阴": {"is_yang": False, "is_moving": True},
    }

    lines = []
    original = []
    changed = []

    for i, yao in enumerate(raw_input):
        info = yao_map[yao]
        yang = info["is_yang"]
        moving = info["is_moving"]

        # 动变阴阳
        changed_yang = not yang if moving else yang

        line = {
            "index": i + 1,
            "raw": yao,
            "is_yang": yang,
            "is_moving": moving,
            "changed": moving,
            "is_shi": False,
            "is_ying": False
        }
        lines.append(line)
        original.append(1 if yang else 0)
        changed.append(1 if changed_yang else 0)

    gua = {
        "raw_input": raw_input,
        "original_hexagram": original,
        "changed_hexagram": changed,
        "lines": lines,
    }

    return gua

def step2_get_gua_name(gua: dict) -> dict:
    binary = gua["original_hexagram"]  
    lower = tuple(binary[0:3])  
    upper = tuple(binary[3:6])  

    inner_name = three_yao_to_gua.get(lower, "未知") # 内卦
    outer_name = three_yao_to_gua.get(upper, "未知") # 外卦

    gua_name = sixty_four_gua.get((inner_name, outer_name), "未知卦")[0]   # 获取卦名
    gong_name = sixty_four_gua.get((inner_name, outer_name), "未知卦")[1]   # 获取卦名
    gua_type = sixty_four_gua.get((inner_name, outer_name), "未知卦")[2]   # 卦类型，如 "一世"、"归魂"、"六世"

    gua["hexagram_name"] = gua_name
    gua["inner_gua"] = inner_name
    gua["outer_gua"] = outer_name
    gua["gong_name"] = gong_name
    gua["generation_type"] = gua_type 

    return gua

def step3_assign_subject_object(gua: dict) -> dict:

    generation_type = gua.get("generation_type") 
    
    # 映射表：世位 → (世爻索引, 应爻索引)
    subject_object_map = {
        "一世": (1, 4),
        "二世": (2, 5),
        "三世": (3, 6),
        "四世": (4, 1),
        "五世": (5, 2),
        "本宫": (6, 3),
        "游魂": (4, 1),
        "归魂": (3, 6),
    }

    shi_index, ying_index = subject_object_map.get(generation_type, (None, None))
    if shi_index is None:
        raise ValueError(f"未知的世位类型：{generation_type}")
    
    for i, line in enumerate(gua["lines"]):
        line["is_shi"] = (i+1 == shi_index)
        line["is_ying"] = (i+1 == ying_index)
    
    gua["shi_position"] = shi_index
    gua["ying_position"] = ying_index

    return gua


def step4_assign_na_jia(gua: dict) -> dict:
    inner_gua = gua["inner_gua"]
    outer_gua = gua["outer_gua"]
    
    inner_list = na_jia_table[inner_gua]["inner"]
    outer_list = na_jia_table[outer_gua]["outer"]

    # 为六爻分别赋值纳甲：初~三爻（index 0~2）用内卦；四~上爻（index 3~5）用外卦
    for i, line in enumerate(gua["lines"]):
        if i < 3:
            gan, zhi = inner_list[i]
        else:
            gan, zhi = outer_list[i - 3]
        line["na_jia_gan"] = gan
        line["na_jia_zhi"] = zhi

    return gua

def step5_assign_wuxing(gua: dict) -> dict:
    for line in gua["lines"]:
        dizhi = line.get("na_jia_zhi")
        line["element"] = zhi_to_element.get(dizhi, "未知")
    return gua


def step6_assign_six_relative(gua: dict) -> dict:
    # 生克关系
    wuxing_generate_me = {"金": "土", "水": "金", "木": "水", "火": "木", "土": "火"}
    wuxing_i_generate = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    wuxing_i_overcome = {"金": "木", "水": "火", "木": "土", "火": "金", "土": "水"}
    wuxing_overcome_me = {"金": "火", "水": "土", "木": "金", "火": "水", "土": "木"}

    # 当前卦的“我”的五行（即本宫五行）
    gong = gua["gong_name"]
    if not gong:
        raise ValueError("gua 字典中缺少 'gong' 键")

    my_element = eight_gua_to_element.get(gong, None)
    if not my_element:
        raise ValueError("gua 字典中缺少 'element' 键")

    for line in gua["lines"]:
        other = line["element"]
        if other is None:
            line["six_relative"] = "未知"
            continue

        if wuxing_generate_me[my_element] == other:
            line["six_relative"] = "父母"
        elif wuxing_i_generate[my_element] == other:
            line["six_relative"] = "子孙"
        elif wuxing_overcome_me[my_element] == other:
            line["six_relative"] = "官鬼"
        elif wuxing_i_overcome[my_element] == other:
            line["six_relative"] = "妻财"
        elif my_element == other:
            line["six_relative"] = "兄弟"
        else:
            line["six_relative"] = "未知"

    return gua

def step7_assign_six_gods(gua: dict, day_gan: str = "") -> dict:
    six_gods_orders = {
        "甲": ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"],
        "乙": ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"],
        "丙": ["朱雀", "勾陈", "腾蛇", "白虎", "玄武", "青龙"],
        "丁": ["朱雀", "勾陈", "腾蛇", "白虎", "玄武", "青龙"],
        "戊": ["勾陈", "腾蛇", "白虎", "玄武", "青龙", "朱雀"],
        "己": ["腾蛇", "白虎", "玄武", "青龙", "朱雀", "勾陈"],
        "庚": ["白虎", "玄武", "青龙", "朱雀", "勾陈", "腾蛇"],
        "辛": ["白虎", "玄武", "青龙", "朱雀", "勾陈", "腾蛇"],
        "壬": ["玄武", "青龙", "朱雀", "勾陈", "腾蛇", "白虎"],
        "癸": ["玄武", "青龙", "朱雀", "勾陈", "腾蛇", "白虎"],
    }
    if day_gan not in six_gods_orders:
        raise ValueError(f"无效的日干：{day_gan}")

    six_gods = six_gods_orders[day_gan]

    for i, line in enumerate(gua["lines"]):
        line["six_god"] = six_gods[i]

    return gua

def step8_assign_changed_lines_info(gua: dict) -> dict:
    changed_lines = [i for i, line in enumerate(gua["lines"]) if line["is_moving"]]
    if not changed_lines:
        return gua  # 无变爻则不做处理

    # 判断变的是内卦、外卦、或全卦
    is_inner_changed = any(i < 3 for i in changed_lines)
    is_outer_changed = any(i >= 3 for i in changed_lines)

    changed_inner = tuple(gua["changed_hexagram"][0:3])
    changed_outer = tuple(gua["changed_hexagram"][3:6])

    changed_inner_name = three_yao_to_gua.get(changed_inner, "未知")
    changed_outer_name = three_yao_to_gua.get(changed_outer, "未知")

    changed_gua_name = sixty_four_gua.get((changed_inner_name, changed_outer_name), "未知卦")[0]
    gua["changed_hexagram_name"] = changed_gua_name


    # 用变卦的哪个卦装纳甲
    if is_inner_changed and not is_outer_changed:
        used_gua_name = changed_inner_name
        position = "inner"
    elif is_outer_changed and not is_inner_changed:
        used_gua_name = changed_outer_name
        position = "outer"
    else:
        used_gua_name = changed_inner_name  # 或 outer 皆可，全变都变
        position = "all"

    used_gua_list = na_jia_table[used_gua_name][position if position != "all" else "inner"]
    used_outer_list = na_jia_table[changed_outer_name]["outer"]

    # 取本卦的本宫五行，用于六亲判断
    my_element = eight_gua_to_element[gua["gong_name"]]

    # 生克关系
    wuxing_generate_me = {"金": "土", "水": "金", "木": "水", "火": "木", "土": "火"}
    wuxing_i_generate = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    wuxing_i_overcome = {"金": "木", "水": "火", "木": "土", "火": "金", "土": "水"}
    wuxing_overcome_me = {"金": "火", "水": "土", "木": "金", "火": "水", "土": "木"}

    # 只处理变爻
    for i in changed_lines:
        line = gua["lines"][i]
        if i < 3:
            gan, zhi = used_gua_list[i]
        else:
            gan, zhi = used_outer_list[i - 3]

        element = zhi_to_element.get(zhi, "未知")

        # 六亲计算仍用原卦“我”的五行
        if wuxing_generate_me[my_element] == element:
            six_relative = "父母"
        elif wuxing_i_generate[my_element] == element:
            six_relative = "子孙"
        elif wuxing_overcome_me[my_element] == element:
            six_relative = "官鬼"
        elif wuxing_i_overcome[my_element] == element:
            six_relative = "妻财"
        elif my_element == element:
            six_relative = "兄弟"
        else:
            six_relative = "未知"

        # 更新该变爻的值
        line["changed_na_jia_gan"] = gan
        line["changed_na_jia_zhi"] = zhi
        line["changed_element"] = element
        line["changed_six_relative"] = six_relative

    return gua
