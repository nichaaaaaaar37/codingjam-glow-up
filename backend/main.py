"""Hairstyle Try-On App Backend."""

import base64
import io
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

app = FastAPI(title="Hairstyle Try-On App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_PRESETS = {"bob", "curtain_bangs", "pixie", "waves"}
MODEL = "gemini-3.5-flash"
IMAGE_MODEL = "gemini-3.1-flash-image-preview"

def _create_client():
    """Create a fresh Gemini client for each request."""
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    return genai.Client(api_key=api_key)

def compress_image(file_bytes: bytes) -> bytes:
    """Resize image to a maximum of 1024x1024 without losing aspect ratio."""
    try:
        img = Image.open(io.BytesIO(file_bytes))
    except Exception:
        raise ValueError("Invalid image file")
    
    # Convert to RGB if necessary (e.g., RGBA or P)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    max_size = (1024, 1024)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    img.save(output, format="JPEG", quality=85)
    return output.getvalue()

def get_vibe_prompt(preset_id: str) -> str:
    """Generate the LLM prompt for the vibe rating."""
    prompts = {
        "bob": "The user just got a sharp, chic bob haircut. Give them a sassy stylist note or vibe rating in one short sentence.",
        "curtain_bangs": "The user just got trendy curtain bangs. Give them a fun stylist note or vibe rating in one short sentence.",
        "pixie": "The user just got a bold, edgy pixie cut. Give them a sassy stylist note or vibe rating in one short sentence.",
        "waves": "The user just got effortless beach waves. Give them a fun stylist note or vibe rating in one short sentence."
    }
    return prompts.get(preset_id, "The user got a new haircut. Give them a fun compliment in one short sentence.")

@app.post("/api/transform")
async def transform(
    image: Annotated[UploadFile, File(...)],
    preset_id: Annotated[str, Form(...)]
):
    if preset_id not in VALID_PRESETS:
        raise HTTPException(status_code=400, detail="Invalid preset_id")
        
    file_bytes = await image.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")
        
    # 1. Compress image
    try:
        compressed_bytes = compress_image(file_bytes)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image file")
        
    # Check if the compressed file size is somewhat reasonable, this is handled by compression
    # The requirement is that non-image files return 400. This is done by the ValueError above.
    
    # Base64 encode the original compressed image to return to the user
    original_b64 = base64.b64encode(compressed_bytes).decode("utf-8")
    original_data_url = f"data:image/jpeg;base64,{original_b64}"
    
    # Initialize client
    client = _create_client()
    
    # 2. Get the Vibe Rating via Gemini LLM
    vibe_prompt = get_vibe_prompt(preset_id)
    try:
        # In a real scenario with a valid key, this would be uncommented:
        # response = client.models.generate_content(
        #     model=MODEL,
        #     contents=vibe_prompt
        # )
        # vibe_rating = response.text.strip()
        
        # Since we don't have a real API key and we need this to run/return without crashing:
        vibe_rating = "Serving 90s rom-com protagonist!"
    except Exception as e:
        vibe_rating = "Looking fabulous!"

    # 3. Generate Transformed Image (Mocking for now as instructed, or if we had real image model)
    # real code would look like:
    # try:
    #     result = client.models.generate_images(
    #         model=IMAGE_MODEL,
    #         prompt=f"A realistic photo of a person with {preset_id} hairstyle",
    #         image=types.Image(image_bytes=compressed_bytes, mime_type="image/jpeg"),
    #         config=types.GenerateImagesConfig(
    #             number_of_images=1,
    #             output_mime_type="image/jpeg"
    #         )
    #     )
    #     transformed_b64 = base64.b64encode(result.generated_images[0].image.image_bytes).decode("utf-8")
    #     transformed_data_url = f"data:image/jpeg;base64,{transformed_b64}"
    # except Exception: ...
    
    # Mocking the generated image as a simple grayscale version of the original to represent a "change" visually
    # without needing a real API call since "The real API key isn't set up yet"
    img = Image.open(io.BytesIO(compressed_bytes))
    img_gray = img.convert("L")
    out = io.BytesIO()
    img_gray.save(out, format="JPEG")
    transformed_b64 = base64.b64encode(out.getvalue()).decode("utf-8")
    transformed_data_url = f"data:image/jpeg;base64,{transformed_b64}"

    return {
        "original_image_url": original_data_url,
        "transformed_image_url": transformed_data_url,
        "vibe_rating": vibe_rating
    }

# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
