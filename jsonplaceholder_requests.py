import aiohttp
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"

NAME = Path(__file__).stem
logger = logging.getLogger(NAME)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

async def fetch_api(url: str, params: Optional[Dict] = None) -> List[Dict]:
    """
    GET запрос с созданием сессии
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        logger.warning(f"API недоступно: {url}, ошибка: {type(e).__name__}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при обращении к апи {url}: {e}")
        raise

async def fetch_all_data() -> Tuple[List[Dict], List[Dict]]:

    async with asyncio.TaskGroup() as tg:
        users_task = tg.create_task(fetch_api(USERS_DATA_URL), name="fetch_users")
        logger.info("Created task fetch_users")
        posts_task = tg.create_task(fetch_api(POSTS_DATA_URL), name="fetch_posts")
        logger.info("Created task fetch_posts")
    
    users_data = users_task.result()
    posts_data = posts_task.result()
    
    logger.info("Got results fetch_users")
    logger.info("Got results fetch_posts")
    
    return users_data, posts_data
        

async def main() -> None:
    
    users_data, posts_data = await fetch_all_data()
        
    logger.info(f"Всего пользователей: {len(users_data)}")
    logger.info(f"Всего постов: {len(posts_data)}")


if __name__ == "__main__":
    asyncio.run(main())