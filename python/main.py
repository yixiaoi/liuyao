from gua_engine.gua_builder import build_hexagram, step8_parse
from gua_engine.yongshen_researcher import ask_deepseek_for_yongshen, parse_yongshen_response,add_yongshen_to_gua
from gua_engine.rule_data import process_all_lines_wangshuai, process_all_lines_xunkong, process_all_changed_lines

def main():
     # 第 1 步：排盘
    raw_input = ["老阴", "少阴", "少阳", "少阳", "少阳", "老阴"]
    question="是否有财运？"
    #raw_input = ["少阳", "少阴", "少阴", "少阳", "少阴", "少阴"] 暗动无变卦
    #raw_input = ["少阳", "老阴", "少阳", "少阳", "少阳", "少阴"]
    #raw_input = ["少阳", "少阴", "老阴", "少阳", "老阳", "老阴"]
    #raw_input = ["少阳", "老阳", "少阴", "少阴", "老阴", "少阳"]
    gua = build_hexagram(raw_input,"戊","子","戊","戌")

    # from pprint import pprint
    # pprint(gua)

    # 第 2 步：向 AI 请求用神
    gua = step8_parse(gua)
    response =ask_deepseek_for_yongshen(gua,question)
    # print("GPT 原始返回：", response)

    yongshen = parse_yongshen_response(response)
    gua = add_yongshen_to_gua(gua, yongshen)
    # print("用神结果：", yongshen)
    # print("最终排盘结果：", gua)

    gua = process_all_lines_wangshuai(gua)
    gua = process_all_lines_xunkong(gua)
    gua = process_all_changed_lines(gua)
    print("最终排盘结果（含旺衰）：", gua)
if __name__ == "__main__":
    main()