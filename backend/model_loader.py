import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from PIL import Image
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages loading and inference for Llama (text) and Stable Diffusion (image) models
    """
    
    def __init__(self):
        self.text_model = None
        self.text_tokenizer = None
        self.image_pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.ready = False
        
        logger.info(f"Using device: {self.device}")
    
    def initialize(self):
        """Initialize text model (image model optional)"""
        try:
            logger.info("Initializing models...")
            self._load_text_model()
            
            # Try to load image model, but don't fail if it doesn't work
            try:
                self._load_image_model()
            except Exception as e:
                logger.warning(f"Image generation disabled: {str(e)}")
                logger.info("Continuing with text-only mode...")
            
            self.ready = True
            logger.info("Models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise
    
    def _load_text_model(self):
        """Load text generation model"""
        try:
            model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            logger.info(f"Loading text model: {model_name}")
            
            self.text_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            
            self.text_model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.text_model = self.text_model.to(self.device)
            
            logger.info("Text model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading text model: {str(e)}")
            raise
    
    def _load_image_model(self):
        """Load Stable Diffusion model (optional)"""
        try:
            # Use a model that doesn't require authentication
            from diffusers import StableDiffusionPipeline
            model_name = "runwayml/stable-diffusion-v1-5"
            
            logger.info(f"Loading image model: {model_name}")
            
            self.image_pipeline = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None
            )
            
            self.image_pipeline = self.image_pipeline.to(self.device)
            
            if self.device == "cuda":
                self.image_pipeline.enable_attention_slicing()
            
            logger.info("Image model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading image model: {str(e)}")
            raise
    
    def generate_text(self, user_message, exam_class="10", max_length=512):
        """Generate educational response"""
        try:
            prompt = self._create_educational_prompt(user_message, exam_class)
            inputs = self.text_tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.text_model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.text_tokenizer.eos_token_id
                )
            
            response = self.text_tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = response[len(prompt):].strip()
            
            return answer if answer else "I'm here to help with your studies. Could you please rephrase your question?"
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return "I apologize, but I encountered an error. Please try asking your question again."
    
    def _create_educational_prompt(self, question, exam_class):
        """Create structured prompt"""
        return f"""You are an AI tutor helping a Class {exam_class} student prepare for board exams.
Student Question: {question}

Provide a clear, accurate, and educational response suitable for Class {exam_class} level:
"""
    
    def generate_image(self, user_message, text_response, width=512, height=512):
        """Generate educational visualization (optional)"""
        if not self.image_pipeline:
            logger.warning("Image generation not available")
            return None
        
        try:
            image_prompt = f"Educational illustration, clear diagram, {user_message[:100]}, textbook style, simple and clear"
            logger.info(f"Generating image with prompt: {image_prompt[:100]}...")
            
            with torch.no_grad():
                result = self.image_pipeline(
                    prompt=image_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=20,  # Reduced for speed
                    guidance_scale=7.5
                )
            
            image = result.images[0]
            filename = self._generate_image_filename(user_message)
            filepath = os.path.join('generated_images', filename)
            image.save(filepath)
            
            logger.info(f"Image saved: {filename}")
            return f"/api/images/{filename}"
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None
    
    def _generate_image_filename(self, message):
        """Generate unique filename"""
        hash_str = hashlib.md5(f"{message}{datetime.now()}".encode()).hexdigest()[:12]
        return f"study_img_{hash_str}.png"
    
    def is_ready(self):
        """Check if models are ready"""
        return self.ready
    
    def get_status(self):
        """Get current status"""
        return {
            'ready': self.ready,
            'device': self.device,
            'text_model_loaded': self.text_model is not None,
            'image_model_loaded': self.image_pipeline is not None
        }
