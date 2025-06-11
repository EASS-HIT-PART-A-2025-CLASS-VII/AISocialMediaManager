# AI Social Media Caption Generator

A powerful AI-powered application that generates engaging social media captions from images using state-of-the-art machine learning models.

## Features

- 🖼️ **Image Upload**: Support for JPG, PNG, GIF formats
- 🤖 **AI-Powered**: Uses BLIP for image understanding and GPT-2 for text generation
- 🎨 **Multiple Formats**: Casual, Formal, Funny, Trendy, Professional, Inspirational
- 📱 **Responsive UI**: Beautiful Streamlit interface
- 🐳 **Docker Ready**: Easy deployment with Docker
- 📊 **Caption Analytics**: Character count, word count, hashtag analysis

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

## Usage

1. **Upload Image**: Click "Choose an image file" and select your photo
2. **Select Format**: Choose from 6 different caption styles:
   - **Casual**: Friendly and relaxed tone
   - **Formal**: Professional and polished
   - **Funny**: Humorous and entertaining
   - **Trendy**: Hip and contemporary
   - **Professional**: Business-focused content
   - **Inspirational**: Motivating and uplifting

3. **Generate Caption**: Click "Generate Caption" to create AI-powered content
4. **Copy & Share**: Use the generated caption on your social media platforms

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

## Performance

- **GPU Support**: Automatically detects and uses CUDA if available
- **Model Caching**: Models are cached locally to improve startup time
- **Batch Processing**: Optimized for handling multiple requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the GitHub issues page
2. Create a new issue with detailed description
3. Include error logs and system information

## Roadmap

- [ ] Support for more image formats
- [ ] Additional AI models integration
- [ ] Batch processing for multiple images
- [ ] Social media platform-specific optimization
- [ ] Custom format creation
- [ ] Multi-language support