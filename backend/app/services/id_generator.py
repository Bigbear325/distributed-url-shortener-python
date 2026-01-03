import asyncio
from app.core.redis import redis_client

BLOCK_SIZE = 1000
BLOCK_COUNTER_KEY = "global:block_counter"

class IdGenerator:
    def __init__(self):
        self.current_ptr = 0
        self.current_end = -1
        self._lock = asyncio.Lock()

    async def _fetch_new_block(self):
        try:
            # INCR returns the new value
            block_num = await redis_client.incr(BLOCK_COUNTER_KEY)
            
            start = (block_num - 1) * BLOCK_SIZE
            end = block_num * BLOCK_SIZE - 1
            
            self.current_ptr = start
            self.current_end = end
            print(f"[IdGenerator] Fetched new block: {start} - {end}")
        except Exception as e:
            print(f"[IdGenerator] Failed to fetch block: {e}")
            raise e

    async def next_id(self) -> int:
        async with self._lock:
            if self.current_ptr > self.current_end:
                await self._fetch_new_block()
                if self.current_ptr > self.current_end:
                    raise Exception("Failed to obtain new ID block")
            
            res_id = self.current_ptr
            self.current_ptr += 1
            return res_id

id_generator = IdGenerator()
