# rules/engine.py
from rule_data import ALL_RULES

def match_rules(gua):
    gua["matched_rules_global"] = []
    for idx, yao in enumerate(gua["lines"]):
        yao["matched_rules"] = []

    matched_rules = []
    for rule in ALL_RULES:
        gua = rule(gua)

    return gua
