import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages loading and inference for Llama (text) and Stable Diffusion (image) models
    from Hugging Face without requiring API keys.
    """
    
    def __init__(self):
        self.text_model = None
        self.text_tokenizer = None
        self.image_pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.ready = False
        
        logger.info(f"Using device: {self.device}")
    
    def initialize(self):
        """
        Initialize both text and image generation models.
        Uses smaller/optimized models for faster inference.
        """
        try:
            logger.info("Initializing models...")
            
            # Load Text Model (Llama-based or similar)
            # Using a smaller model for educational purposes
            # For production, replace with Llama-2-7b or larger
            self._load_text_model()
            
            # Load Image Generation Model
            self._load_image_model()
            
            self.ready = True
            logger.info("All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise
    
    def _load_text_model(self):
        """
        Load text generation model from Hugging Face.
        
        Options for model selection:
        1. meta-llama/Llama-2-7b-chat-hf (requires access request)
        2. TinyLlama/TinyLlama-1.1B-Chat-v1.0 (lightweight, no restrictions)
        3. microsoft/phi-2 (good performance, 2.7B params)
        """
        try:
            # Using TinyLlama for demonstration (lightweight and fast)
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
        """
        Load Stable Diffusion model for image generation.
        
        Options:
        1. stabilityai/stable-diffusion-2-1 (full model)
        2. stabilityai/stable-diffusion-2-1-base (lighter)
        3. runwayml/stable-diffusion-v1-5 (alternative)
        """
        try:
            model_name = "stabilityai/stable-diffusion-2-1-base"
            
            logger.info(f"Loading image model: {model_name}")
            
            self.image_pipeline = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None  # Disable for educational content
            )
            
            self.image_pipeline = self.image_pipeline.to(self.device)
            
            # Enable memory optimizations
            if self.device == "cuda":
                self.image_pipeline.enable_attention_slicing()
                # self.image_pipeline.enable_xformers_memory_efficient_attention()
            
            logger.info("Image model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading image model: {str(e)}")
            raise
    
    def generate_text(self, user_message, exam_class="10", max_length=512):
        """
        Generate educational response using the text model.
        
        Args:
            user_message: Student's question
            exam_class: Class level (10 or 12)
            max_length: Maximum response length
        
        Returns:
            Generated text response
        """
        try:
            # Create educational prompt
            prompt = self._create_educational_prompt(user_message, exam_class)
            
            # Tokenize input
            inputs = self.text_tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.text_model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.text_tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.text_tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            # Extract answer (remove prompt)
            answer = response[len(prompt):].strip()
            
            return answer if answer else "I'm here to help with your studies. Could you please rephrase your question?"
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return "I apologize, but I encountered an error. Please try asking your question again."
    
    def _create_educational_prompt(self, question, exam_class):
        """
        Create a structured prompt for educational responses.
        """
        return f"""You are an AI tutor helping a Class {exam_class} student prepare for board exams.
Student Question: {question}

Provide a clear, accurate, and educational response suitable for Class {exam_class} level:
"""
    
    def generate_image(self, user_message, text_response, width=512, height=512):
        """
        Generate educational visualization using Stable Diffusion.
        
        Args:
            user_message: Original question
            text_response: AI's text response
            width: Image width
            height: Image height
        
        Returns:
            Path to generated image
        """
        try:
            # Create image prompt from context
            image_prompt = self._create_image_prompt(user_message, text_response)
            
            logger.info(f"Generating image with prompt: {image_prompt[:100]}...")
            
            # Generate image
            with torch.no_grad():
                result = self.image_pipeline(
                    prompt=image_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=30,
                    guidance_scale=7.5
                )
            
            image = result.images[0]
            
            # Save image
            filename = self._generate_image_filename(user_message)
            filepath = os.path.join('generated_images', filename)
            image.save(filepath)
            
            logger.info(f"Image saved: {filename}")
            
            return f"/api/images/{filename}"
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None
    
    def _create_image_prompt(self, question, response):
        """
        Create an appropriate image generation prompt for educational content.
        """
        # Extract key concepts for visualization
        prompt = f"Educational illustration, clear diagram, {question[:100]}, textbook style, simple and clear"
        return prompt
    
    def _generate_image_filename(self, message):
        """
        Generate unique filename for image.
        """
        hash_str = hashlib.md5(f"{message}{datetime.now()}".encode()).hexdigest()[:12]
        return f"study_img_{hash_str}.png"
    
    def is_ready(self):
        """Check if models are loaded and ready."""
        return self.ready
    
    def get_status(self):
        """Get current status of models."""
        return {
            'ready': self.ready,
            'device': self.device,
            'text_model_loaded': self.text_model is not None,
            'image_model_loaded': self.image_pipeline is not None
        }