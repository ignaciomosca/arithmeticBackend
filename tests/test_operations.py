from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from arithmetic.db.dao.operation_dao import OperationDAO
from arithmetic.db.dao.record_dao import RecordDAO
from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.web.api.operation.schema import OperationBase, OperationEnum


@pytest.mark.anyio
async def test_new_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests performing the perform operation function."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.ADDITION, first_term=1, second_term=2)
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.ADDITION.value, 1)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=1, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=1, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 1)


@pytest.mark.anyio
async def test_random_string(
    with_user_id: int | None,
    fastapi_app: FastAPI,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tests performing the perform random operation function."""

    # Create a mock for the httpx.AsyncClient.post method
    async def mock_post(*args: tuple, **kwargs: dict) -> AsyncMock:
        # Create a mock response object
        mock_response = AsyncMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "result": {"random": {"data": ["mocked_random_string"]}},
        }
        return mock_response

    # Apply the monkeypatch to replace the post method with the mock
    monkeypatch.setattr(AsyncClient, "post", mock_post)

    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.RANDOM)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.RANDOM.value, 10)

    response = await authenticated_client.post(url, json=operation.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
