from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.task import BookingTask, TaskStatus, TaskCategory
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.cache_service import cache_service


async def create_task(db: AsyncSession, user_id: int, data: TaskCreate) -> BookingTask:
    task = BookingTask(
        user_id=user_id,
        title=data.title,
        description=data.description,
        category=data.category,
        due_date=data.due_date,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)
    await cache_service.delete_pattern(f"user:{user_id}:tasks:*")
    return task


async def get_tasks(
    db: AsyncSession,
    user_id: int,
    task_status: Optional[TaskStatus] = None,
    category: Optional[TaskCategory] = None,
    skip: int = 0,
    limit: int = 20,
) -> dict:
    suffix    = f"{task_status}:{category}:{skip}:{limit}"
    cache_key = cache_service.user_tasks_key(user_id, suffix)
    cached    = await cache_service.get(cache_key)
    if cached:
        return cached

    query = select(BookingTask).where(BookingTask.user_id == user_id)
    if task_status:
        query = query.where(BookingTask.status == task_status)
    if category:
        query = query.where(BookingTask.category == category)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    rows  = (await db.execute(query.offset(skip).limit(limit).order_by(BookingTask.created_at.desc()))).scalars().all()

    data = {
        "total": total,
        "tasks": [
            {k: str(v) if not isinstance(v, (int, float, bool, type(None), str)) else v
             for k, v in t.__dict__.items() if not k.startswith("_")}
            for t in rows
        ],
    }
    await cache_service.set(cache_key, data)
    return data


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int) -> BookingTask:
    result = await db.execute(
        select(BookingTask).where(BookingTask.id == task_id, BookingTask.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


async def update_task(
    db: AsyncSession, task_id: int, user_id: int, data: TaskUpdate
) -> BookingTask:
    task = await get_task_by_id(db, task_id, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    await db.flush()
    await db.refresh(task)
    await cache_service.delete(cache_service.task_key(task_id))
    await cache_service.delete_pattern(f"user:{user_id}:tasks:*")
    return task


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> dict:
    task = await get_task_by_id(db, task_id, user_id)
    await db.delete(task)
    await cache_service.delete(cache_service.task_key(task_id))
    await cache_service.delete_pattern(f"user:{user_id}:tasks:*")
    return {"message": f"Task {task_id} deleted successfully"}