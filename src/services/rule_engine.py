def rule_match(log, rules):
    for rule in rules:
        if rule.level and rule.level.lower() != log["level"].lower():
            continue
        if rule.keyword.lower() in log["message"].lower():
            return True
    return False
