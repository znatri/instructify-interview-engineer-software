from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.item import Item
from app.models.user import User
from tests.utils import get_jwt_header

# TODO: Implement Integration Test for FASTapi endpoint at "/users/valid"
class TestAPIEndpoint:
    async def test_get_unauthorized_request(self, client:AsyncClient, create_user):
        user: User = await create_user()
        jwt_header = get_jwt_header(user)

        resp = await client.get(settings.API_PATH + "/users/valid", headers = jwt_header)
        assert resp.status_code == 403, resp.text
    
    async def test_get_valid_users(self, client:AsyncClient, create_user, db: AsyncSession):
        user: User = await create_user()
        db.add(user)
        await db.commit()
        assert user.id
        
        jwt_header = get_jwt_header(user)

        resp = await client.get(settings.API_PATH + "/users/valid", headers = jwt_header)
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list), resp.text

