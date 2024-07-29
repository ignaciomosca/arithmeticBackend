
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from arithmetic.db.dao.record_dao import RecordDAO
from arithmetic.web.api.operation.schema import OperationBase, OperationEnum


@pytest.mark.anyio
async def test_new_operation(
    fastapi_app: FastAPI,
    authenticated_client: AsyncClient,
    dbsession: AsyncSession,
):
    url = fastapi_app.url_path_for("new_operation")
    operation = OperationBase(type=OperationEnum.ADDITION, first_term=1, second_term=2)
    dao = RecordDAO(dbsession)
    initial_count = await dao.get_all_records(limit=1, offset=0)
    # Send a POST request to create the operations
    response = await authenticated_client.post(url, json=operation.model_dump())
    # Assert the response status code is 200 OK
    assert response.status_code == status.HTTP_201_CREATED
    # Use the DAO again to count operations instances after creation
    final_count = await dao.get_all_records(limit=1, offset=0)
    print(final_count)
    # Assert that the count increased by 1 after creation
    assert final_count == initial_count + 1
