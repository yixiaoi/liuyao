from gua_engine.gua_builder import build_hexagram
if __name__ == "__main__":
    raw_input = ["少阳", "老阳", "少阴", "少阴", "老阳", "少阴"]
    #raw_input = ["少阳", "少阴", "老阴", "少阳", "老阳", "老阴"]
    #raw_input = ["少阳", "老阳", "少阴", "少阴", "老阴", "少阳"]
    gua = build_hexagram(raw_input,"辛","卯","辛","寅")

    from pprint import pprint
    pprint(gua)
