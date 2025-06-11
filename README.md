# AI Social Media Caption Generator

A powerful AI-powered application that generates engaging social media captions from images using state-of-the-art machine learning models.

## Features

### **AI Caption Generation**
- 🖼️ **Smart Image Analysis**: Upload JPG, PNG, GIF formats
- 🤖 **AI-Powered Captions**: Uses advanced AI models for content understanding
- 🎨 **6 Caption Styles**: Casual, Formal, Funny, Trendy, Professional, Inspirational
- 📋 **Auto-Copy**: Optional automatic clipboard copying
- 🔄 **Regenerate**: Get multiple caption variations

### **Instagram Preview & Management**
- 📱 **Instagram-Like Interface**: Authentic social media preview
- 🎯 **Dual View Modes**: Grid view and Feed view
- 🔄 **Drag & Drop**: Reorder posts to plan your content sequence
- 💾 **Save Posts**: Store generated content for later use

## Tech Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **Transformers**: Hugging Face transformers library
- **BLIP**: Salesforce BLIP model for image captioning
- **GPT-2**: Text generation and enhancement
- **PyTorch**: Deep learning framework

### Frontend
- **Streamlit**: Interactive web application framework
- **PIL**: Python Imaging Library for image processing

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-caption-generator
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application at `http://localhost:8501`

### Manual Installation

1. Install Python 3.9+
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run frontend/app.py
```

## 🎯 How to Use

### **1. Generate Captions**
- Upload an image using drag-and-drop or file picker
- Choose your preferred caption style
- Enable auto-copy if desired
- Click "Generate Caption" to create AI-powered content

### **2. Save & Organize**
- Save generated posts to your preview collection
- Switch to "Preview" tab to see your Instagram-like feed
- Drag and drop posts to reorder them
- Switch between Grid and Feed views

### **3. Plan Your Content**
- Use Grid view to see your overall feed aesthetic
- Use Feed view to see individual post details
- Copy captions directly from the preview
- Delete posts you don't want to keep

## API Endpoints

The FastAPI backend provides the following endpoints:

- `POST /generate-caption`: Generate caption from uploaded image
- `GET /formats`: Get available caption formats
- `GET /health`: Health check endpoint

## Models Used

- **BLIP (Salesforce/blip-image-captioning-base)**: For understanding image content
- **GPT-2**: For enhancing and formatting captions based on style requirements

## Configuration

Create a `.env` file based on `.env.example`:

```env
HUGGINGFACE_API_TOKEN=your_token_here
MODEL_CACHE_DIR=./cache
UPLOAD_DIR=./uploads
```

## Docker Configuration

The application includes:
- **Dockerfile**: Multi-stage build for optimized image size
- **docker-compose.yml**: Easy orchestration with volume mounts
- **Requirements**: All dependencies specified in requirements.txt
