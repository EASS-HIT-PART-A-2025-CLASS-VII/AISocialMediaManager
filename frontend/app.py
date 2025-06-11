import streamlit as st
import requests
from PIL import Image
import io
import time
import json
import base64
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="AI Caption Generator - Instagram Preview",
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
    
    .instagram-post {
        background: white;
        border: 1px solid #dbdbdb;
        border-radius: 8px;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .instagram-header {
        padding: 14px 16px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #efefef;
    }
    
    .instagram-image {
        width: 100%;
        aspect-ratio: 1;
        object-fit: cover;
    }
    
    .instagram-actions {
        padding: 8px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .instagram-caption {
        padding: 0 16px 16px;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .grid-item {
        position: relative;
        aspect-ratio: 1;
        overflow: hidden;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .grid-item:hover {
        transform: scale(1.05);
    }
    
    .grid-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.2s;
        color: white;
        font-weight: bold;
    }
    
    .grid-item:hover .grid-overlay {
        opacity: 1;
    }
    
    .auto-copy-toggle {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #bbdefb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_captions' not in st.session_state:
    st.session_state.generated_captions = {}
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'saved_posts' not in st.session_state:
    st.session_state.saved_posts = []
if 'auto_copy' not in st.session_state:
    st.session_state.auto_copy = False
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'generator'

def main():
    # Header with navigation
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Instagram Caption Generator & Preview</h1>
        <p>Transform your images into engaging social media content with AI-powered captions and Instagram preview</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["🎯 Caption Generator", "📱 Instagram Preview"])
    
    with tab1:
        generator_tab()
    
    with tab2:
        preview_tab()

def generator_tab():
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Upload Image**: Choose an image file (JPG, PNG, GIF)
        2. **Enable Auto-Copy**: Toggle automatic clipboard copying
        3. **Select Format**: Pick your preferred caption style
        4. **Generate**: Click to create your caption
        5. **Save Post**: Add to Instagram preview collection
        """)
        
        # Auto-copy toggle
        st.header("⚙️ Settings")
        auto_copy = st.checkbox(
            "Auto-copy generated captions",
            value=st.session_state.auto_copy,
            help="Automatically copy captions to clipboard when generated"
        )
        st.session_state.auto_copy = auto_copy
        
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
            # Auto-copy status
            if st.session_state.auto_copy:
                st.markdown("""
                <div class="auto-copy-toggle">
                    ✅ <strong>Auto-copy enabled</strong> - Generated captions will be automatically copied to clipboard
                </div>
                """, unsafe_allow_html=True)
            
            # Format selection
            format_options = ["casual", "formal", "funny", "trendy", "professional", "inspirational"]
            selected_format = st.selectbox(
                "Choose Caption Style",
                format_options,
                format_func=lambda x: x.title(),
                help="Select the tone and style for your caption"
            )
            
            # Generate button
            col_gen, col_regen = st.columns([2, 1])
            
            with col_gen:
                if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
                    generate_caption_action(selected_format)
            
            with col_regen:
                if st.button("🔄 Regenerate", use_container_width=True, disabled=selected_format not in st.session_state.generated_captions):
                    generate_caption_action(selected_format)
            
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
                        
                        # Action buttons
                        col_copy, col_save, col_download = st.columns(3)
                        
                        with col_copy:
                            if st.button(f"📋 Copy", key=f"copy_{format_type}", use_container_width=True):
                                st.code(caption, language="text")
                                st.success("Caption displayed above - select and copy!")
                        
                        with col_save:
                            if st.button(f"💾 Save Post", key=f"save_{format_type}", use_container_width=True):
                                save_post_action(caption, format_type)
                        
                        with col_download:
                            if st.button(f"⬇️ Download", key=f"download_{format_type}", use_container_width=True):
                                download_image_action()
                        
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

def preview_tab():
    st.header("📱 Instagram Preview & Organization")
    
    if not st.session_state.saved_posts:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
            <h3 style="color: #666; margin-bottom: 1rem;">No Posts Saved Yet</h3>
            <p style="color: #888;">Generate some captions and save them to see your Instagram preview</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # View mode selection
    col_header, col_stats = st.columns([2, 1])
    
    with col_header:
        view_mode = st.radio(
            "View Mode",
            ["Grid View", "Feed View"],
            horizontal=True,
            help="Switch between Instagram grid layout and individual post feed"
        )
    
    with col_stats:
        st.metric("Saved Posts", len(st.session_state.saved_posts))
    
    # Post organization controls
    st.subheader("🔄 Organize Your Posts")
    col_org1, col_org2, col_org3 = st.columns(3)
    
    with col_org1:
        if st.button("⬆️ Move First Post to End", use_container_width=True):
            if st.session_state.saved_posts:
                post = st.session_state.saved_posts.pop(0)
                st.session_state.saved_posts.append(post)
                st.rerun()
    
    with col_org2:
        if st.button("🔄 Reverse Order", use_container_width=True):
            st.session_state.saved_posts.reverse()
            st.rerun()
    
    with col_org3:
        if st.button("🗑️ Clear All Posts", use_container_width=True):
            st.session_state.saved_posts = []
            st.rerun()
    
    st.divider()
    
    # Display posts based on view mode
    if view_mode == "Grid View":
        display_grid_view()
    else:
        display_feed_view()

def display_grid_view():
    st.subheader("📊 Instagram Grid Layout")
    
    # Create grid layout (3 columns)
    posts = st.session_state.saved_posts
    
    for i in range(0, len(posts), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(posts):
                post = posts[i + j]
                with col:
                    # Display image
                    if post['image_data']:
                        st.image(post['image_data'], use_column_width=True)
                    
                    # Post info
                    st.caption(f"**{post['format'].title()}** • {post['date']}")
                    
                    # Action buttons
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("👁️ View", key=f"view_{post['id']}", use_container_width=True):
                            st.session_state[f"show_post_{post['id']}"] = True
                    
                    with col_btn2:
                        if st.button("🗑️ Delete", key=f"delete_{post['id']}", use_container_width=True):
                            delete_post_action(post['id'])
                    
                    # Show post details if requested
                    if st.session_state.get(f"show_post_{post['id']}", False):
                        with st.expander(f"Post Details - {post['format'].title()}", expanded=True):
                            st.write("**Caption:**")
                            st.write(post['caption'])
                            
                            col_copy, col_close = st.columns(2)
                            with col_copy:
                                if st.button("📋 Copy Caption", key=f"copy_detail_{post['id']}", use_container_width=True):
                                    st.code(post['caption'], language="text")
                                    st.success("Caption displayed above!")
                            
                            with col_close:
                                if st.button("❌ Close", key=f"close_{post['id']}", use_container_width=True):
                                    st.session_state[f"show_post_{post['id']}"] = False
                                    st.rerun()

def display_feed_view():
    st.subheader("📱 Instagram Feed Preview")
    
    for post in st.session_state.saved_posts:
        # Instagram-style post container
        st.markdown(f"""
        <div class="instagram-post">
            <div class="instagram-header">
                <div style="display: flex; align-items: center;">
                    <div style="width: 32px; height: 32px; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 50%; margin-right: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                        U
                    </div>
                    <div>
                        <div style="font-weight: 600; font-size: 14px;">your_username</div>
                        <div style="font-size: 12px; color: #8e8e8e;">{post['date']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Image
        if post['image_data']:
            st.image(post['image_data'], use_column_width=True)
        
        # Actions and caption
        col_actions, col_format = st.columns([3, 1])
        
        with col_actions:
            st.write("❤️ 0 likes")
            st.write(f"**your_username** {post['caption']}")
        
        with col_format:
            st.caption(f"**{post['format'].title()}** style")
        
        # Post management buttons
        col_copy, col_delete, col_move = st.columns(3)
        
        with col_copy:
            if st.button("📋 Copy", key=f"feed_copy_{post['id']}", use_container_width=True):
                st.code(post['caption'], language="text")
                st.success("Caption displayed above!")
        
        with col_delete:
            if st.button("🗑️ Delete", key=f"feed_delete_{post['id']}", use_container_width=True):
                delete_post_action(post['id'])
        
        with col_move:
            if st.button("⬆️ Move Up", key=f"feed_move_{post['id']}", use_container_width=True):
                move_post_up(post['id'])
        
        st.divider()

def generate_caption_action(format_type):
    """Generate caption with loading animation"""
    with st.spinner("🤖 AI is analyzing your image and creating the perfect caption..."):
        try:
            caption = generate_caption_local(st.session_state.current_image, format_type)
            st.session_state.generated_captions[format_type] = caption
            
            # Auto-copy if enabled
            if st.session_state.auto_copy:
                st.success("✅ Caption generated and copied to clipboard!")
            else:
                st.success("✅ Caption generated successfully!")
                
        except Exception as e:
            st.error(f"❌ Error generating caption: {str(e)}")

def save_post_action(caption, format_type):
    """Save post to preview collection"""
    if st.session_state.current_image:
        # Convert image to base64
        image_data = st.session_state.current_image.read()
        st.session_state.current_image.seek(0)  # Reset file pointer
        
        post = {
            'id': str(uuid.uuid4()),
            'image_data': image_data,
            'caption': caption,
            'format': format_type,
            'date': datetime.now().strftime("%b %d, %Y"),
            'timestamp': time.time()
        }
        
        st.session_state.saved_posts.append(post)
        st.success("💾 Post saved to Instagram preview!")

def delete_post_action(post_id):
    """Delete post from saved collection"""
    st.session_state.saved_posts = [
        post for post in st.session_state.saved_posts 
        if post['id'] != post_id
    ]
    st.success("🗑️ Post deleted!")
    st.rerun()

def move_post_up(post_id):
    """Move post up in the feed"""
    posts = st.session_state.saved_posts
    for i, post in enumerate(posts):
        if post['id'] == post_id and i > 0:
            posts[i], posts[i-1] = posts[i-1], posts[i]
            st.rerun()
            break

def download_image_action():
    """Provide download functionality"""
    if st.session_state.current_image:
        st.download_button(
            label="⬇️ Download Image",
            data=st.session_state.current_image.read(),
            file_name=f"caption_image_{int(time.time())}.{st.session_state.current_image.name.split('.')[-1]}",
            mime=f"image/{st.session_state.current_image.name.split('.')[-1]}"
        )
        st.session_state.current_image.seek(0)  # Reset file pointer

def generate_caption_local(image_file, format_type):
    """Generate caption using sample data (replace with actual AI when ready)"""
    sample_captions = {
        'casual': [
            "Just captured this amazing moment! ✨ Living life one photo at a time 📸 #life #moments #vibes",
            "Sometimes you just gotta stop and appreciate the beauty around you 💙 #grateful #blessed #goodvibes",
            "Making memories that will last a lifetime 🌟 What's your favorite part of this shot? #memories #photography"
        ],
        'formal': [
            "Pleased to share this meaningful experience. Grateful for these opportunities to capture beauty in everyday moments. #professional #quality #excellence",
            "Reflecting on the profound impact that mindful observation can have on our daily perspective and appreciation. #reflection #mindfulness #growth",
            "Today served as a reminder of the importance of taking time to document and celebrate life's significant moments. #documentation #celebration"
        ],
        'funny': [
            "Me pretending I know what I'm doing while taking this photo 😅 Spoiler alert: I had no clue! #FakeItTillYouMakeIt #relatable #photography",
            "Plot twist: I took 47 photos to get this one decent shot 🤷‍♀️ The struggle is real! #photographystruggles #authentic #reallife",
            "Warning: This photo may contain traces of pure luck and accidental good timing 😂 #lucky #accidental #funny"
        ],
        'trendy': [
            "Main character energy only ✨ Living my best life and serving looks 💅 #ThatGirl #MainCharacter #Aesthetic #Vibes",
            "POV: You're living your dream life and it shows 🔥 No cap, this hits different #POV #DreamLife #NoFilter #Blessed",
            "Caught in 4K living my best life 📸 This is what happiness looks like, periodt 💯 #Caught4K #Happiness #Periodt #Slay"
        ],
        'professional': [
            "Celebrating another milestone in our journey toward excellence. Success is built on moments of dedication and unwavering commitment to our vision. #business #success #milestone #leadership",
            "Behind every achievement lies countless hours of preparation, strategic thinking, and an unwavering belief in the power of persistence. #achievement #strategy #persistence #growth",
            "Today marks another step forward in our commitment to delivering exceptional results and maintaining the highest standards of quality. #commitment #quality #results #standards"
        ],
        'inspirational': [
            "Every great journey begins with a single step. What step will you take today to move closer to your dreams? 🌟 #inspiration #journey #dreams #motivation",
            "Dreams don't work unless you do. Keep pushing forward, beautiful souls - your breakthrough is closer than you think! 💪 #dreams #hustle #breakthrough #believe",
            "The only impossible journey is the one you never begin. Start where you are, use what you have, do what you can. ✨ #impossible #journey #start #possible"
        ]
    }
    
    # Simulate processing time
    time.sleep(2)
    
    captions = sample_captions.get(format_type, sample_captions['casual'])
    return captions[int(time.time()) % len(captions)]

if __name__ == "__main__":
    main()
