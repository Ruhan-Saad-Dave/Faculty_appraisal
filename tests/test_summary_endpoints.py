import pytest
from httpx import AsyncClient
from main import app
import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL = "http://testserver"

@pytest.mark.asyncio
async def test_teaching_process_summary():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Mocking faculty ID 1
        response = await ac.get("/api/v1/part-a/teaching-process/summary/1")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalMarksOutOf100" in res_data
    assert "scaledMarksOutOf25" in res_data

@pytest.mark.asyncio
async def test_course_file_summary():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/course-files/summary/1")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_teaching_methods_summary():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/teaching-methods/summary/1")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_project_summary():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/projects/summary/1")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data

@pytest.mark.asyncio
async def test_qualification_summary():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/part-a/qualification-enhancement/summary/1")
    assert response.status_code == 200
    res_data = response.json()
    assert "totalScore" in res_data
