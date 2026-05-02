import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from unittest.mock import patch

BASE_URL = "http://testserver"

@pytest.fixture(autouse=True)
def mock_storage_upload():
    with patch("src.api.Part_B.v1.popular_writings.upload_file_to_supabase") as mock_pw:
        mock_pw.return_value = "mock/path/to/writing.pdf"
        yield

@pytest.mark.asyncio
async def test_create_popular_writing():
    """Tests Part B - Popular Writing with File Upload"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        file_content = b"%PDF-1.4 popular writing"
        files = {"file": ("test_writing.pdf", file_content, "application/pdf")}
        data = {
            "title": "Innovative Tech Documentary",
            "writing_type": "Documentary",
            "date": "2026-05-01",
            "publisher_agency": "TechTV",
            "sr_no": 1,
            "department": "Media & Communication"
        }
        
        response = await ac.post("/api/v1/part-b/popular-writings", data=data, files=files)
        
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["title"] == "Innovative Tech Documentary"
    assert res_data["writing_type"] == "Documentary"
    assert res_data["document"] == "mock/path/to/writing.pdf"

@pytest.mark.asyncio
async def test_get_popular_writings_by_faculty():
    """Tests retrieving popular writings for a faculty member"""
    faculty_id = "00000000-0000-0000-0000-000000000001"
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/v1/part-b/popular-writings/faculty/{faculty_id}")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_popular_writings_summary():
    """Tests the summary score for popular writings"""
    faculty_id = "00000000-0000-0000-0000-000000000001"
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/v1/part-b/popular-writings/summary/{faculty_id}")
    
    assert response.status_code == 200
    res_data = response.json()
    assert "total_score" in res_data
