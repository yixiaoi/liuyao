from gua_engine.gua_builder import build_hexagram, step8_parse
from gua_engine.yongshen_engine import ask_deepseek_for_yongshen, parse_yongshen_response,add_yongshen_to_gua

def main():
     # 第 1 步：排盘
    raw_input = ["少阳", "老阴", "少阳", "少阳", "少阳", "少阴"]
    question="我父亲身体健康怎么样？"
    #raw_input = ["少阳", "少阴", "老阴", "少阳", "老阳", "老阴"]
    #raw_input = ["少阳", "老阳", "少阴", "少阴", "老阴", "少阳"]
    gua = build_hexagram(raw_input,"辛","巳","庚","寅")

    from pprint import pprint
    pprint(gua)

    # 第 2 步：向 AI 请求用神
    gua = step8_parse(gua)
    response =ask_deepseek_for_yongshen(gua,question)
    print("GPT 原始返回：", response)

    yongshen = parse_yongshen_response(response)
    gua = add_yongshen_to_gua(gua, yongshen)
    print("用神结果：", yongshen)
    print("最终排盘结果：", gua)

if __name__ == "__main__":
    main()