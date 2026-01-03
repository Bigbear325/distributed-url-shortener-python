from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import ShortenRequest, ShortenResponse
from app.services.url_service import UrlService
import os

router = APIRouter()

@router.post("/api/v1/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(req: ShortenRequest, db: AsyncSession = Depends(get_db)):
    try:
        short_code = await UrlService.shorten(
            db, 
            str(req.long_url), 
            req.custom_alias, 
            req.expiration_date
        )
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        return ShortenResponse(
            short_url=f"{base_url}/{short_code}",
            short_code=short_code
        )
    except ValueError as e:
        if str(e) == "Alias already taken":
            raise HTTPException(status_code=409, detail="Alias already taken")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_db)):
    long_url = await UrlService.get_original_url(db, short_code)
    if long_url:
        return RedirectResponse(long_url, status_code=302)
    raise HTTPException(status_code=404, detail="URL not found")
