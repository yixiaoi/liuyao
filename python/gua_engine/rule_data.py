from gua_engine.gua_data import is_conflict, calc_relation, element_generate_me,is_xunkong_func,zhi_chong, element_to_zhi,is_jin_shen,is_tui_shen

def evaluate_wangshuai(yao, date_info, is_changed=False):
    """
    :param yao: dict，一条爻，格式如题目所示
    :param date_info: dict，含有'month_ganzhi', 'day_ganzhi', 'month_element', 'day_element'
    :param is_changed: 是否是变爻，影响暗动处理逻辑
    :return: {'score': float, 'description': str}
    """

    # 准备基本信息
    yao_element = yao['element']
    yao_dizhi = yao['najia_di_zhi']
    month_ganzhi = date_info['month_ganzhi']
    day_ganzhi = date_info['day_ganzhi']
    month_zhi = month_ganzhi[1]  # 地支
    day_zhi = day_ganzhi[1]
    month_element = date_info['month_element']
    day_element = date_info['day_element']

    score = 0
    desc = []

    ### ==== 冲破先判定：月破/日破（最优先）====
    if is_conflict(yao_dizhi, month_zhi):
        desc.append("月破")
        score -= 2
        return {"score": score, "description": "，".join(desc)}
    if is_conflict(yao_dizhi, day_zhi):
        desc.append("日破")
        score -= 2
        return {"score": score, "description": "，".join(desc)}

    ### ==== 月建关系 ====
    score_month, desc_month = calc_relation(yao_element, yao_dizhi, month_zhi, month_element, "月建")
    score += score_month
    desc.extend(desc_month)

    ### ==== 日辰关系 ====
    score_day, desc_day = calc_relation(yao_element, yao_dizhi, day_zhi, day_element, "日辰")
    score += score_day
    desc.extend(desc_day)

    return {"score": score, "description": "，".join(desc)}

def is_wangxiang_func(yao, date_info):
    """判断这个爻在日月中是否算旺相"""
    month_score, _ = calc_relation(yao['element'], yao['najia_di_zhi'],
                                   date_info['month_ganzhi'][1], date_info['month_element'], "月")
    day_score, _ = calc_relation(yao['element'], yao['najia_di_zhi'],
                                 date_info['day_ganzhi'][1], date_info['day_element'], "日")
    return (month_score + day_score) > 0.5


def is_an_dong(yao, all_lines, date_info, is_wangxiang_func, is_xunkong_func):
    """判断是否是暗动"""
    if yao.get("is_changed"):  # 动爻不能暗动
        return False

    yao_dizhi = yao['najia_di_zhi']
    yao_element = yao['element']
    day_zhi = date_info['day_ganzhi'][1]  # 日辰地支
    day_element = date_info['day_element']

    # ① 日辰冲旺相
    if is_conflict(yao_dizhi, day_zhi) and is_wangxiang_func(yao, date_info):
        return True

    # ② 被其他动爻生扶 且日辰冲
    if is_conflict(yao_dizhi, day_zhi):
        for line in all_lines:
            if line.get("is_changed"):
                element = line['element']
                # 其他动爻对本爻生扶
                if element_generate_me[yao_element] == element or yao_element == element:
                    return True

    # ③ 日辰冲旬空
    if is_conflict(yao_dizhi, day_zhi) and is_xunkong_func(yao, date_info['day_ganzhi']):
        return True

    return False

def process_all_lines_wangshuai(guaxiang: dict):
    date_info = guaxiang['divination_context']['date_info']
    all_lines = guaxiang['lines']
    for line in all_lines:
        # 原爻旺衰
        base_eval = evaluate_wangshuai(line, date_info)
        line["wang_shuai"] = base_eval  # 将旺衰结果存回

        # 判断是否是暗动爻
        if not line.get("is_changed") and is_an_dong(line, all_lines, date_info,
                                                     is_wangxiang_func, is_xunkong_func):
            print(f"爻位 {line['index']} 暗动") 
            line["wang_shuai"] = {base_eval['score'],base_eval["description"]+"暗动"}  
            line['is_an_dong'] = True  # 标记为变爻
        else:
            line['is_an_dong'] = False 

        # 若有变爻则处理变爻
        if line.get('is_changed') and 'changed_properties' in line:
            changed_line = line['changed_properties'].copy()
            changed_line['najia_di_zhi'] = changed_line['najia_di_zhi']
            changed_line['element'] = changed_line['element']
            changed_eval = evaluate_wangshuai(changed_line, date_info, is_changed=True)
            line['changed_properties']["wang_shuai"] = changed_eval  # 将变爻旺衰结果存回

    return guaxiang


def process_all_lines_xunkong(gua):
    """
    处理所有爻的旬空状态
    :param gua: dict，包含所有爻信息的卦象
    :return: 更新后的卦象
    """
    date_info = gua['divination_context']['date_info']
    month_jian = date_info['month_ganzhi'][1]  # 月建地支


    for yao in gua['lines']:
        yao_dizhi = yao['najia_di_zhi']
        is_xunkong = is_xunkong_func(yao, date_info['day_ganzhi'])
        yao['is_xunkong'] = is_xunkong

        if is_xunkong:
            desc = []
            is_jiakong = False  #默认真空
            desc.append(f"旬空地支：{yao['najia_di_zhi']}在{date_info['day_ganzhi']}旬空")
            #判断真空假空
            if yao["is_changed"] or (not yao["is_changed"] and yao.get("is_an_dong")):
                is_jiakong = True
                desc.append(f"自身发动")
            # if yao["relation"]["other_yao_generate_me"]:
            #     is_jiakong = True
            #     desc.append(f"他爻相生")
            if yao_dizhi == month_jian:
                is_jiakong = True
                desc.append(f"临当月之月建 {month_jian}，为旺相")

            if not is_jiakong:
                desc.append("{yao_dizhi} 静爻、无生、非旺相，属真空无用")
            #假空判断什么时候填实
            else:
                tianshi_zhi = element_to_zhi.get(yao['element'], "未知")
                chongshi_zhi = zhi_chong.get(yao_dizhi)
            
                desc.append(f"假空，在{tianshi_zhi}日可填实，在{chongshi_zhi}日可冲实")

            
            xunkong_props = {}
            xunkong_props["is_jiakong"] = is_jiakong
            xunkong_props["description"] = "，".join(desc)
            
            yao['xunkong_propertie'] = xunkong_props
    return gua

def process_all_lines_jin_tui_shen (gua):
    """
    处理所有爻的进退神状态
    :param gua: dict，包含所有爻信息的卦象
    :return: 更新后的卦象
    """
    for yao in gua['lines']:
        if yao["is_changed"]:
            yao["changed_properties"]["is_jin_shen"] = is_jin_shen(yao)
            yao["changed_properties"]["is_tui_shen"] = is_tui_shen(yao)

    return gua


def rule_fumu_mov_transform_ke(gua):
    matched = []
    for yao in gua.get("yaos", []):
        if (
            yao.get("type") == "父母"
            and yao.get("is_moving")
            and yao.get("transforms_to") is not None
            and 克(yao["transforms_to"]["element"], yao["element"])
        ):
            matched.append("父母爻发动化回头克")
    return matched

def 克(elem_a, elem_b):
    # 简化的五行相克逻辑示例，可自行扩展为五行表
    克关系 = {
        "木": "土",
        "火": "金",
        "土": "水",
        "金": "木",
        "水": "火"
    }
    return 克关系.get(elem_a) == elem_b


# 注册所有规则
ALL_RULES = [
    rule_fumu_mov_transform_ke,
    # 你可以继续添加规则函数
]