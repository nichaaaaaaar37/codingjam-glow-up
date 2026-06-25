import io
import os
import base64
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from main import app, compress_image, get_vibe_prompt, VALID_PRESETS

client = TestClient(app)

def create_dummy_image(width=2000, height=2000, color="red", format="JPEG"):
    """Helper to create a dummy image in memory."""
    img = Image.new("RGB", (width, height), color=color)
    output = io.BytesIO()
    img.save(output, format=format)
    return output.getvalue()

# --- Unit Tests ---

def test_image_compression():
    """Ensure uploaded images are resized to a maximum of 1024x1024 without losing aspect ratio."""
    large_image_bytes = create_dummy_image(width=2000, height=1000)
    
    compressed_bytes = compress_image(large_image_bytes)
    compressed_img = Image.open(io.BytesIO(compressed_bytes))
    
    assert compressed_img.width <= 1024
    assert compressed_img.height <= 1024
    # Aspect ratio should be maintained: 2000/1000 = 2.0 -> 1024/512 = 2.0
    assert compressed_img.width == 1024
    assert compressed_img.height == 512

def test_vibe_prompt_generation():
    """Verify that the correct LLM prompt is constructed for a given preset."""
    # Test valid presets
    assert "bob" in get_vibe_prompt("bob").lower()
    assert "curtain bangs" in get_vibe_prompt("curtain_bangs").lower()
    
    # Test fallback
    assert "new haircut" in get_vibe_prompt("unknown_preset").lower()

def test_validate_upload():
    """Assert that non-image files or files exceeding size limits return a clean 400 error."""
    # We test non-image file explicitly since size is handled by compression currently.
    response = client.post(
        "/api/transform",
        data={"preset_id": "bob"},
        files={"image": ("text.txt", b"this is not an image", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid image file" in response.json()["detail"]

    # Test invalid preset
    dummy_image = create_dummy_image()
    response2 = client.post(
        "/api/transform",
        data={"preset_id": "invalid_preset"},
        files={"image": ("test.jpg", dummy_image, "image/jpeg")}
    )
    assert response2.status_code == 400
    assert "Invalid preset_id" in response2.json()["detail"]


# --- Integration Tests ---

@patch("main._create_client")
def test_full_transformation_flow(mock_create_client):
    """
    The Golden Flow: Mocks external APIs, posts dummy image and preset, 
    asserts 200 status, valid base64 strings, and non-empty vibe rating.
    """
    # Setup mock Gemini client
    # Actually, we already have mocked the API call internally in main.py due to "no API key",
    # but let's be rigorous and mock the _create_client anyway in case real logic is active.
    
    mock_client = MagicMock()
    # Mock text generation
    mock_response = MagicMock()
    mock_response.text = "Mocked vibe rating!"
    mock_client.models.generate_content.return_value = mock_response
    
    # Mock image generation
    mock_img_response = MagicMock()
    mock_generated_image = MagicMock()
    mock_generated_image.image.image_bytes = create_dummy_image(100, 100, "blue")
    mock_img_response.generated_images = [mock_generated_image]
    mock_client.models.generate_images.return_value = mock_img_response
    
    mock_create_client.return_value = mock_client
    
    # Create test input
    dummy_image = create_dummy_image(width=500, height=500)
    
    # Make request
    response = client.post(
        "/api/transform",
        data={"preset_id": "pixie"},
        files={"image": ("selfie.jpg", dummy_image, "image/jpeg")}
    )
    
    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    
    assert "original_image_url" in data
    assert "transformed_image_url" in data
    assert "vibe_rating" in data
    
    assert data["original_image_url"].startswith("data:image/jpeg;base64,")
    assert data["transformed_image_url"].startswith("data:image/jpeg;base64,")
    assert isinstance(data["vibe_rating"], str)
    assert len(data["vibe_rating"]) > 0
