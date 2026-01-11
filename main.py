import asyncio
import logging
from typing import List, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from models.base import Base
from models.connect import async_engine, async_session
from jsonplaceholder_requests import fetch_all_data
from models.tables import User, Post


NAME = Path(__file__).stem
logger = logging.getLogger(NAME)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def add_users_to_db(
    session: AsyncSession,
    users_data: List[Dict]
) -> List[User]:
    """Добавляем юзеров в бдшку"""
    users = []
    for user_data in users_data:
        user = User(
            name=user_data.get("name", ""),
            username=user_data.get("username", ""),
            email=user_data.get("email", "")
        )
        users.append(user)
        logger.info(f"Создан пользователь: {user.username}")
    
    session.add_all(users)
    await session.commit()
    logger.info(f"Добавлено {len(users)} пользователей в БД")
    return users


async def add_posts_to_db(
    session: AsyncSession,
    posts_data: list[dict]
) -> list[Post]:
    """Создает посты для существующих пользователей"""
    
    user_ids_from_posts = {post.get("userId") for post in posts_data}
    
    existing_users_stmt = select(User.id).where(User.id.in_(user_ids_from_posts))
    existing_user_ids = {user_id for user_id in await session.scalars(existing_users_stmt)}
    
    valid_posts_data = [
        post_data for post_data in posts_data 
        if post_data.get("userId") in existing_user_ids
    ]
    
    posts = [
        Post(
            id=post_data["id"],
            user_id=post_data["userId"],
            title=post_data["title"],
            body=post_data["body"]
        )
        for post_data in valid_posts_data
    ]
    
    session.add_all(posts)
    await session.commit()
    
    logger.info(f"Добавлено {len(posts)} постов в БД")
    return posts



async def async_main() -> None:

    logger.info("Создание таблиц в БД...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы созданы")
    
    logger.info("Загрузка данных из API...")
    users_data, posts_data = await fetch_all_data()
    logger.info(f"Загружено {len(users_data)} пользователей и {len(posts_data)} постов из API")
    
    async with async_session() as session:
        users = await add_users_to_db(session, users_data)
        posts = await add_posts_to_db(session, posts_data)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()