from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.models import Url
from app.services.id_generator import id_generator
from app.utils.base62 import encode
from app.core.redis import redis_client

CACHE_TTL = 3600

class UrlService:
    @staticmethod
    async def shorten(db: AsyncSession, long_url: str, custom_alias: str | None = None, expires_at: datetime | None = None) -> str:
        new_id = await id_generator.next_id()
        
        short_code = custom_alias if custom_alias else encode(new_id)
        
        try:
            db_url = Url(
                id=new_id, 
                short_code=short_code, 
                long_url=long_url, 
                expires_at=expires_at
            )
            db.add(db_url)
            await db.commit()
            await db.refresh(db_url)
            
            # Cache it
            await redis_client.set(f"url:{short_code}", long_url, ex=CACHE_TTL)
            
            return short_code
        except IntegrityError:
            await db.rollback()
            if custom_alias:
                raise ValueError("Alias already taken")
            # Collision on generated ID is extremely rare/impossible with unique ID gen
            raise ValueError("Unexpected collision")

    @staticmethod
    async def get_original_url(db: AsyncSession, short_code: str) -> str | None:
        # 1. Check Redis
        cached = await redis_client.get(f"url:{short_code}")
        if cached:
            return cached

        # 2. Check DB
        result = await db.execute(select(Url).where(Url.short_code == short_code))
        url_obj = result.scalars().first()
        
        if not url_obj:
            return None
            
        if url_obj.expires_at and datetime.now(url_obj.expires_at.tzinfo) > url_obj.expires_at:
            return None

        # 3. Set Cache
        await redis_client.set(f"url:{short_code}", url_obj.long_url, ex=CACHE_TTL)
        
        return url_obj.long_url
