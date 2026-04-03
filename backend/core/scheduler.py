"""Global APScheduler instance shared across the application."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
