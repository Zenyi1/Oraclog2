import asyncio
from ..storage.storage import add_log, rules_storage
from .rule_engine import rule_match

log_queue = asyncio.Queue()
#analysis_queue = asyncio.Queue() 

async def consume_logs():
    while True:
        log = await log_queue.get()
        try:
            # Only persist logs that match configured rules.
            # Non-matching logs are discarded (removed from the queue).
            if rule_match(log, rules_storage):
                add_log(log)
        except Exception as e:
            # keep consumer running on errors
            print(f"Error processing log: {e}")
        finally:
            log_queue.task_done()