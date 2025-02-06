from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from sqlmodel import select, func
from math import ceil

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