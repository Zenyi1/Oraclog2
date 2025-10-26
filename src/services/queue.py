import asyncio
from ..storage.storage import add_log
import time

log_queue = asyncio.Queue()

async def consume_logs():
    while True:
        #time.sleep(30)
        log = await log_queue.get()
        add_log(log)
        log_queue.task_done()