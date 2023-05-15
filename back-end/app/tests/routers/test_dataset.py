import os

import pytest
from httpx import AsyncClient

from app.database.init_mongo_db import drop_database


@pytest.mark.asyncio
async def test_empty_get_datasets(client: AsyncClient):
    """
    Test get all datasets when there are no datasets.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """
    await drop_database()
    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert(len(response.json()) == 0)


@pytest.mark.asyncio
async def test_create_dataset_url(client: AsyncClient):
    """
    Test create dataset.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """
    dataset = {
        "dataset_name": "Test dataset",
        "dataset_description": "Test dataset description",
        "dataset_type": "Test dataset type",
        "version": "0.0.0",
        "path_to_dataset": "https://www.kaggle.com/c/titanic/download/train.csv"
    }

    response = await client.post("/datasets/", json=dataset)
    assert response.status_code == 201
    assert response.json()["dataset_name"] == dataset["dataset_name"]
    assert response.json()["dataset_description"] == dataset["dataset_description"]


@pytest.mark.asyncio
async def test_get_dataset_by_id(client: AsyncClient):
    """
    Test get dataset by id.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """
    dataset = {
        "dataset_name": "Test dataset 2",
        "dataset_description": "Test dataset description 2",
        "dataset_type": "Test dataset type",
        "version": "0.0.0",
        "path_to_dataset": "https://www.kaggle.com/c/titanic/download/train.csv"
    }

    response = await client.post("/datasets/", json=dataset)
    dataset_id = response.json()["_id"]

    response = await client.get(f"/datasets/{dataset_id}")
    assert response.status_code == 200
    assert response.json()["dataset_name"] == dataset["dataset_name"]
    assert response.json()["dataset_description"] == dataset["dataset_description"]


@pytest.mark.asyncio
async def test_create_dataset_filepath(client: AsyncClient):
    """
    Test create dataset.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """
    test_file_path = os.path.join(os.path.dirname(__file__), "test_files", "test_dataset.csv")

    dataset = {
        "dataset_name": "Test dataset 3",
        "dataset_description": "Test dataset description 3",
        "dataset_type": "Test dataset type",
        "version": "0.0.0",
        "path_to_dataset": test_file_path
    }

    response = await client.post("/datasets/", json=dataset)
    assert response.status_code == 201
    assert response.json()["dataset_name"] == dataset["dataset_name"]
    assert response.json()["dataset_description"] == dataset["dataset_description"]


@pytest.mark.asyncio
async def test_get_datasets(client: AsyncClient):
    """
    Test get all datasets.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """

    response = await client.get("/datasets/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_dataset_by_name(client: AsyncClient):
    """
    Test get dataset by name.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """
    dataset = {
        "dataset_name": "Test dataset 4",
        "dataset_description": "Test dataset description 4",
        "dataset_type": "Test dataset type",
        "version": "0.0.0",
        "path_to_dataset": "https://www.kaggle.com/c/titanic/data",
    }

    response = await client.post("/datasets/", json=dataset)

    dataset_name = dataset["dataset_name"]
    response = await client.get(f"/datasets/name/{dataset_name}")
    assert response.status_code == 200
    assert response.json()["dataset_name"] == dataset["dataset_name"]
    assert response.json()["dataset_description"] == dataset["dataset_description"]


@pytest.mark.asyncio
async def test_update_dataset(client: AsyncClient):
    """
    Test update dataset.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """

    dataset_name = "Test dataset 4"

    updated_dataset = { "dataset_name": "Test dataset 4 updated",
                        "dataset_description": "Test dataset description 4 updated",
                        "dataset_type": "Test dataset type updated",
                        "version": "0.0.2"}

    response = await client.get(f"/datasets/name/{dataset_name}")
    dataset_id = response.json()["_id"]

    response = await client.put(f"/datasets/{dataset_id}", json=updated_dataset)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_dataset(client: AsyncClient):
    """
    Test delete dataset.

    Args:
        client (AsyncClient): Async client fixture

    Returns:
        None
    """

    dataset_name = "Test dataset 4 updated"

    response = await client.get(f"/datasets/name/{dataset_name}")
    dataset_id = response.json()["_id"]

    response = await client.delete(f"/datasets/{dataset_id}")

    assert response.status_code == 204
