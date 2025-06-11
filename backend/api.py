from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from .caption_generator import CaptionGenerator
import uvicorn

app = FastAPI(title="AI Caption Generator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize caption generator
caption_generator = CaptionGenerator()

@app.post("/generate-caption")
async def generate_caption(
    image: UploadFile = File(...),
    format_type: str = Form(default="casual")
):
    """Generate caption for uploaded image"""
    try:
        # Read and process image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Generate caption
        caption = caption_generator.generate_caption(pil_image, format_type)
        
        return {
            "success": True,
            "caption": caption,
            "format": format_type,
            "image_name": image.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "caption": None
        }

@app.get("/formats")
async def get_formats():
    """Get available caption formats"""
    return {
        "formats": list(caption_generator.format_templates.keys()),
        "descriptions": {
            format_name: template['style'] 
            for format_name, template in caption_generator.format_templates.items()
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Caption Generator API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)