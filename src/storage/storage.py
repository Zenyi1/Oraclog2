from datetime import datetime
from typing import List, Tuple, Optional


all_logs_storage = []      
problematic_logs_storage = [] 
insights_storage = []       
rules_storage = []         
def add_log(log: dict) -> None:
    # Add timestamp if not present
    if 'timestamp' not in log:
        log['timestamp'] = datetime.now().isoformat()
    
    # Store in all logs
    all_logs_storage.append(log)

def add_problematic_log(log: dict) -> None:
    problematic_logs_storage.append(log)

def get_logs(limit: int, offset: int, level: str = None) -> Tuple[List[dict], int]:
    filtered_logs = all_logs_storage
    if level:
        filtered_logs = [log for log in all_logs_storage if log['level'].lower() == level.lower()]
    return filtered_logs[offset:offset + limit], len(filtered_logs)

def get_logs_by_timestamp(timestamp: str) -> List[dict]:
    return [log for log in all_logs_storage if log['timestamp'] == timestamp]

def get_problematic_logs(limit: int, offset: int) -> Tuple[List[dict], int]:
    return (problematic_logs_storage[offset:offset + limit], 
            len(problematic_logs_storage))

def add_insight(log_id: int, insight: str) -> None:
    insights_storage.append({"log_id": log_id, "insight": insight})

def get_insights(limit: int, offset: int) -> Tuple[List[dict], int]:
    return insights_storage[offset:offset + limit], len(insights_storage)