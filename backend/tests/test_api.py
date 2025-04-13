import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import tempfile

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to GreenStamp API"}

def test_upload_report():
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        # Write some dummy content
        temp_file.write(b"%PDF-1.4\n")
        temp_file.seek(0)
        
        # Upload the file
        files = {"file": ("test.pdf", temp_file, "application/pdf")}
        response = client.post("/reports/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert "esg_score" in data
        assert "summary" in data
        assert "greenwashing_risk" in data

def test_get_reports():
    response = client.get("/reports")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_report_by_id():
    # First upload a report
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        temp_file.write(b"%PDF-1.4\n")
        temp_file.seek(0)
        
        files = {"file": ("test.pdf", temp_file, "application/pdf")}
        upload_response = client.post("/reports/upload", files=files)
        report_id = upload_response.json()["id"]
        
        # Then get the report
        response = client.get(f"/reports/{report_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == report_id

def test_get_nonexistent_report():
    response = client.get("/reports/999999")
    assert response.status_code == 404 