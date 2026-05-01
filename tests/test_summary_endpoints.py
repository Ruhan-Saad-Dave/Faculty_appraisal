import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL = "http://testserver"

@pytest.mark.asyncio
async def test_teaching_process_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        # Mocking faculty ID
        response = await ac.get("/api/v1/part-a/teaching-process/summary/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalMarksOutOf100" in res_data
    assert "scaledMarksOutOf25" in res_data

@pytest.mark.asyncio
async def test_course_file_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/course-files/summary/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_teaching_methods_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/teaching-methods/summary/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_project_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/projects/summary/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_qualification_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/qualification-enhancement/summary/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data
