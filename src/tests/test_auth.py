import pytest

auth_prefix = f"/api/v1/auth"


@pytest.mark.asyncio
async def test_user_creation(client):
    response = await client.get(url="/api/v1/auth")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_abc(client):
    assert 1 == 1
