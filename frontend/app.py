import streamlit as st
import requests
from PIL import Image
import io
import time

# Page configuration
st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .format-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        cursor: pointer;
    }
    
    .caption-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_captions' not in st.session_state:
    st.session_state.generated_captions = {}
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Social Media Caption Generator</h1>
        <p>Transform your images into engaging social media content with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Upload Image**: Choose an image file (JPG, PNG, GIF)
        2. **Select Format**: Pick your preferred caption style
        3. **Generate**: Click to create your caption
        4. **Copy & Share**: Use the generated caption on social media
        """)
        
        st.header("🎨 Available Formats")
        formats_info = {
            "Casual": "Friendly and relaxed tone",
            "Formal": "Professional and polished",
            "Funny": "Humorous and entertaining",
            "Trendy": "Hip and contemporary",
            "Professional": "Business-focused content",
            "Inspirational": "Motivating and uplifting"
        }
        
        for format_name, description in formats_info.items():
            st.markdown(f"**{format_name}**: {description}")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'gif'],
            help="Upload an image to generate captions for social media"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            st.info(f"📊 **Image Info**: {uploaded_file.name} | Size: {image.size[0]}x{image.size[1]} pixels")
            
            st.session_state.current_image = uploaded_file
    
    with col2:
        st.header("🎯 Generate Caption")
        
        if st.session_state.current_image is not None:
            # Format selection
            format_options = ["casual", "formal", "funny", "trendy", "professional", "inspirational"]
            selected_format = st.selectbox(
                "Choose Caption Style",
                format_options,
                format_func=lambda x: x.title(),
                help="Select the tone and style for your caption"
            )
            
            # Generate button
            if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your image and creating the perfect caption..."):
                    try:
                        # Simulate API call (replace with actual API call)
                        caption = generate_caption_local(st.session_state.current_image, selected_format)
                        
                        # Store in session state
                        st.session_state.generated_captions[selected_format] = caption
                        
                        st.success("✅ Caption generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating caption: {str(e)}")
            
            # Display generated captions
            if st.session_state.generated_captions:
                st.header("📝 Generated Captions")
                
                for format_type, caption in st.session_state.generated_captions.items():
                    with st.expander(f"{format_type.title()} Caption", expanded=True):
                        st.markdown(f"""
                        <div class="caption-box">
                            <p style="font-size: 1.1em; line-height: 1.6;">{caption}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Copy button
                        if st.button(f"📋 Copy {format_type.title()} Caption", key=f"copy_{format_type}"):
                            st.code(caption, language="text")
                            st.success("Caption copied to display! Select and copy the text above.")
                        
                        # Caption stats
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.markdown(f"""
                            <div class="stats-box">
                                <strong>{len(caption)}</strong><br>Characters
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_stats2:
                            word_count = len(caption.split())
                            st.markdown(f"""
                            <div class="stats-box">
                                <strong>{word_count}</strong><br>Words
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_stats3:
                            hashtag_count = caption.count('#')
                            st.markdown(f"""
                            <div class="stats-box">
                                <strong>{hashtag_count}</strong><br>Hashtags
                            </div>
                            """, unsafe_allow_html=True)
        
        else:
            st.info("👆 Please upload an image first to generate captions")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 Powered by AI | Built with Streamlit & Hugging Face Transformers</p>
        <p>Transform your images into engaging social media content</p>
    </div>
    """, unsafe_allow_html=True)

def generate_caption_local(image_file, format_type):
    """Generate caption using local AI models"""
    try:
        # This would normally call your backend API
        # For now, we'll use sample captions
        sample_captions = {
            'casual': "Just captured this amazing moment! ✨ Living life one photo at a time 📸 #life #moments #vibes",
            'formal': "Pleased to share this meaningful experience. Grateful for these opportunities to capture beauty. #professional #quality",
            'funny': "When you accidentally take a good photo and pretend it was totally planned 😂 #accidentalgenius #oops #funny",
            'trendy': "Main character energy only 💅 Serving looks and living dreams ✨ #aesthetic #slay #vibes #unbothered",
            'professional': "Celebrating another milestone in our journey toward excellence. Success is built on moments like these. #business #success #growth",
            'inspirational': "Every great journey begins with a single step. What step will you take today? 🌟 #inspiration #motivation #dreams"
        }
        
        # Simulate processing time
        time.sleep(2)
        
        return sample_captions.get(format_type, sample_captions['casual'])
        
    except Exception as e:
        raise Exception(f"Failed to generate caption: {str(e)}")

if __name__ == "__main__":
    main()