from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from sqlmodel import select, func
from math import ceil
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets
from appconfig import Settings

security_stats = HTTPBasic()
config = Settings()

# Dependency to inject db sessions
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    from main import db
    async for session in db.get_db_session():
        yield session


async def get_paginated_data(query: select, dbsession: AsyncSession, response_schema, current_page: int = 1, records_per_page: int = 10):
    # Prepare the query for execution
    query.execution_options(prepared=True)
    # Calculate the offset based on the current page and records per page
    offset = (current_page - 1) * records_per_page

    # Query total number of records
    count_query = select(func.count()).select_from(query.subquery())
    total_records = await dbsession.scalar(count_query)

    # Calculate the last page number
    last_page = ceil(total_records / records_per_page)

    # Query items using the calculated offset and records per page
    items_query = query.offset(offset).limit(records_per_page)
    result = await dbsession.execute(items_query)            
    items = result.scalars().all()    

    for item in items:
        await dbsession.refresh(item)
          
    return response_schema(
            data=items,
            total_pages=last_page,
            total_items=total_records,
            page_number=current_page,
            page_size=min(len(items), total_records)
        )


async def reset_minute_counters(request_stats:dict):
    while True:
        await asyncio.sleep(60)
        for stats in request_stats.values():
            stats["last_minute_count"] = 0


async def save_stats(request_stats:dict):
    import pickle
    while True:
        await asyncio.sleep(7200)
        with open('monthly_request_stats.pkl', 'wb') as f:
            pickle.dump(request_stats, f, pickle.HIGHEST_PROTOCOL)


def verify_admin(credentials: HTTPBasicCredentials = Depends(security_stats)):
    correct_username = secrets.compare_digest(credentials.username, config.STATS_USER)
    correct_password = secrets.compare_digest(credentials.password, config.STATS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username