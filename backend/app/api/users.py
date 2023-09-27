from typing import Any, List

from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Response

from app.core.logger import logger
from app.deps.db import get_async_session
from app.deps.users import current_superuser
from app.models.user import User
from app.schemas.user import UserRead

import requests

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
async def get_users(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    logger.info("Fetching users")
    total = await session.scalar(select(func.count(User.id)))
    users = (
        (await session.execute(select(User).offset(skip).limit(limit))).scalars().all()
    )
    response.headers["Content-Range"] = f"{skip}-{skip + len(users)}/{total}"
    return users

@router.get("/users/valid")
async def validate_users(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
    skip: int = 0,
    limit: int = 100
) -> Any :
    logger.info("Fetching users")
    total = await session.scalar(select(func.count(User.id)))
    users = ((await session.execute(select(User).offset(skip).limit(limit))).scalars().all())
    logger.info("Validating domain urls")
    # create a container to store valid users
    valid_users = []
    # iterate over users list in O(n)
    for user in users:
        try:
            # implemntation note: find a better method to get domain name, currently it doesn't account for multiple "@" and can be thrown off
            domain = "https://" + user.email.split("@")[-1] 
            r = requests.get(domain)
            if r.status_code == 200:
                valid_users.append(user)
        # the following exception was unaccounted for and resulted in the errorr during the live interview
        except requests.exceptions.RequestException as e:
            logger.error(f"Error validating user: {e}")
            pass
    response.headers["Content-Range"] = f"{skip} - {skip + len(valid_users)}/{total}"
    return valid_users
    