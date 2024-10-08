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
async def test_addition_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing an addition."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.ADDITION, first_term=1, second_term=2)
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.ADDITION.value, 1)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())

    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    assert response.text == '"3"'

    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 1)


@pytest.mark.anyio
async def test_substraction_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing a substraction."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(
        type=OperationEnum.SUBTRACTION,
        first_term=3,
        second_term=2,
    )
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.SUBTRACTION.value, 1)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    assert response.text == '"1"'
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 1)


@pytest.mark.anyio
async def test_multiplication_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing a multiplication."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(
        type=OperationEnum.MULTIPLICATION,
        first_term=3,
        second_term=2,
    )
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.MULTIPLICATION.value, 1)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    assert response.text == '"6"'
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 1)


@pytest.mark.anyio
async def test_division_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests performing a division."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.DIVISION, first_term=4, second_term=2)
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.DIVISION.value, 1)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    assert response.text == '"2.0"'
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 1)


@pytest.mark.anyio
async def test_division_by_zero_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing a division by zero and checking for an error."""
    url = fastapi_app.url_path_for("new_operation")

    operation_data = {"type": "DIVISION", "first_term": 4, "second_term": 0}

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.DIVISION.value, 1)

    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation_data)
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_square_root_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing a square root."""
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.SQUARE, first_term=4)
    dao = RecordDAO(dbsession)

    user_dao = UserDAO(dbsession)

    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.SQUARE.value, 5)

    await operation_dao.get_all_operations()
    initial_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_201_CREATED
    assert response.text == '"2.0"'
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(user_id=with_user_id, limit=1, offset=0)
    user = await user_dao.get_user_by_id(with_user_id)
    # Assert that the count increased by 1 after creation
    assert final_count.total_count == initial_count.total_count + 1
    assert user.balance == (100 - 5)


@pytest.mark.anyio
async def test_square_root_of_negative_number_operation(
    fastapi_app: FastAPI,
    with_user_id: int | None,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Test performing the square root of a negative number and checking an error."""
    url = fastapi_app.url_path_for("new_operation")
    operation_dao = OperationDAO(dbsession)
    await operation_dao.add_new_operation(OperationEnum.SQUARE.value, 5)

    operation_data = {"type": "SQUARE", "first_term": -5}

    await operation_dao.get_all_operations()
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation_data)
    # Assert the response status code is 201 OK
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_random_string(
    with_user_id: int | None,
    fastapi_app: FastAPI,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test performing the random operation function."""

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
