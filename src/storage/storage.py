logs_storage = []
insights_storage = []
rules_storage = []

def add_log(log: dict):
    logs_storage.append(log)

def get_logs(limit: int, offset: int, level: str = None):
    filtered_logs = logs_storage
    if level:
        filtered_logs = [log for log in logs_storage if log['level'].lower() == level.lower()]
    return filtered_logs[offset:offset + limit], len(filtered_logs)

def add_insight(log_id: int, insight: str):
    insights_storage.append({"log_id": log_id, "insight": insight})

def get_insights(limit: int, offset: int):
    return insights_storage[offset:offset + limit], len(insights_storage)