import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image
import requests
from typing import Dict, List
import re

class CaptionGenerator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load BLIP model for image captioning
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model.to(self.device)
        
        # Load GPT-2 for text enhancement
        self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.gpt2_tokenizer.pad_token = self.gpt2_tokenizer.eos_token
        
        # Format templates
        self.format_templates = {
            'casual': {
                'prefix': "Here's a casual social media caption: ",
                'style': "friendly, relaxed, conversational",
                'emojis': True,
                'hashtags': ['#life', '#moments', '#vibes', '#mood']
            },
            'formal': {
                'prefix': "Here's a professional caption: ",
                'style': "professional, polished, respectful",
                'emojis': False,
                'hashtags': ['#professional', '#quality', '#excellence']
            },
            'funny': {
                'prefix': "Here's a humorous caption: ",
                'style': "funny, witty, entertaining, playful",
                'emojis': True,
                'hashtags': ['#funny', '#lol', '#humor', '#comedy']
            },
            'trendy': {
                'prefix': "Here's a trendy caption: ",
                'style': "hip, contemporary, Gen-Z style, trendy slang",
                'emojis': True,
                'hashtags': ['#aesthetic', '#vibes', '#slay', '#mood', '#main']
            },
            'professional': {
                'prefix': "Here's a business-focused caption: ",
                'style': "business-focused, corporate, achievement-oriented",
                'emojis': False,
                'hashtags': ['#business', '#success', '#growth', '#leadership']
            },
            'inspirational': {
                'prefix': "Here's an inspirational caption: ",
                'style': "motivating, uplifting, encouraging, positive",
                'emojis': True,
                'hashtags': ['#inspiration', '#motivation', '#believe', '#dreams']
            }
        }

    def generate_base_caption(self, image: Image.Image) -> str:
        """Generate base caption from image using BLIP model"""
        try:
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                out = self.blip_model.generate(**inputs, max_length=50, num_beams=5)
            
            caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            print(f"Error generating base caption: {e}")
            return "A beautiful moment captured in this image"

    def enhance_caption(self, base_caption: str, format_type: str) -> str:
        """Enhance caption based on format type"""
        try:
            template = self.format_templates.get(format_type, self.format_templates['casual'])
            
            # Create prompt for GPT-2
            prompt = f"Transform this image description into a {template['style']} social media caption: {base_caption}\n\nCaption:"
            
            # Tokenize and generate
            inputs = self.gpt2_tokenizer.encode(prompt, return_tensors="pt", max_length=100, truncation=True)
            
            with torch.no_grad():
                outputs = self.gpt2_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 50,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.gpt2_tokenizer.eos_token_id
                )
            
            generated_text = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract caption part
            caption_start = generated_text.find("Caption:") + len("Caption:")
            enhanced_caption = generated_text[caption_start:].strip()
            
            # Clean up the caption
            enhanced_caption = self.clean_caption(enhanced_caption)
            
            # Add format-specific elements
            enhanced_caption = self.add_format_elements(enhanced_caption, template)
            
            return enhanced_caption
            
        except Exception as e:
            print(f"Error enhancing caption: {e}")
            return self.get_fallback_caption(base_caption, format_type)

    def clean_caption(self, caption: str) -> str:
        """Clean and format the generated caption"""
        # Remove incomplete sentences
        sentences = caption.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            caption = '.'.join(sentences[:-1]) + '.'
        
        # Remove extra whitespace
        caption = ' '.join(caption.split())
        
        # Ensure proper capitalization
        if caption and not caption[0].isupper():
            caption = caption[0].upper() + caption[1:]
        
        return caption

    def add_format_elements(self, caption: str, template: Dict) -> str:
        """Add emojis and hashtags based on format"""
        result = caption
        
        if template['emojis']:
            result = self.add_emojis(result, template.get('style', ''))
        
        # Add hashtags
        hashtags = ' '.join(template['hashtags'][:3])  # Limit to 3 hashtags
        result = f"{result} {hashtags}"
        
        return result

    def add_emojis(self, caption: str, style: str) -> str:
        """Add appropriate emojis based on style"""
        emoji_map = {
            'casual': ['✨', '💙', '😊', '🌟', '💫'],
            'funny': ['😂', '🤣', '😅', '🙃', '😆'],
            'trendy': ['🔥', '💅', '✨', '💯', '🌟'],
            'inspirational': ['🌟', '💪', '✨', '🙏', '💫']
        }
        
        # Simple emoji addition logic
        if 'funny' in style:
            return f"{caption} {emoji_map['funny'][0]}"
        elif 'trendy' in style:
            return f"{caption} {emoji_map['trendy'][0]}"
        elif 'inspirational' in style:
            return f"{caption} {emoji_map['inspirational'][0]}"
        else:
            return f"{caption} {emoji_map['casual'][0]}"

    def get_fallback_caption(self, base_caption: str, format_type: str) -> str:
        """Provide fallback captions when AI generation fails"""
        fallbacks = {
            'casual': f"Just captured this amazing moment! {base_caption} ✨ #life #moments",
            'formal': f"Pleased to share this experience. {base_caption} #professional",
            'funny': f"When life gives you moments like this... {base_caption} 😂 #funny",
            'trendy': f"Main character energy only! {base_caption} 🔥 #aesthetic #vibes",
            'professional': f"Celebrating another milestone. {base_caption} #success #growth",
            'inspirational': f"Every moment is a new beginning. {base_caption} ✨ #inspiration"
        }
        
        return fallbacks.get(format_type, fallbacks['casual'])

    def generate_caption(self, image: Image.Image, format_type: str = 'casual') -> str:
        """Main method to generate caption"""
        try:
            # Generate base caption from image
            base_caption = self.generate_base_caption(image)
            
            # Enhance caption based on format
            enhanced_caption = self.enhance_caption(base_caption, format_type)
            
            return enhanced_caption
            
        except Exception as e:
            print(f"Error in caption generation: {e}")
            return self.get_fallback_caption("A beautiful image", format_type)