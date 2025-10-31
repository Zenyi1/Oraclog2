def rule_match(log: dict, rules: list):
    
    msg = (log.get("message") or "").lower()
    print(msg)
    log_level = (log.get("level") or "").lower()
    print(log_level)

    for rule in rules:
        # support both dict and object-like access
        if isinstance(rule, dict):
            r_keyword = rule.get("keyword")
            r_level = rule.get("level")
        else:
            r_keyword = getattr(rule, "keyword", None)
            r_level = getattr(rule, "level", None)

        # check level if provided on the rule
        if r_level and r_level.lower() != log_level.lower():
            continue

        if r_keyword.lower() in msg.lower():
            #print("added")
            return True

    return False
