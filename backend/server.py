from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime
from model_loader import ModelManager

# Initialize Flask App
app = Flask(__name__, static_folder='../public', static_url_path='')
CORS(app)

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Model Manager
model_manager = ModelManager()

# Configuration
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': model_manager.is_ready()
    })

# Main Chat Endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        exam_class = data.get('exam_class', '10')
        generate_image = data.get('generate_image', True)
        
        logger.info(f"Processing message for class {exam_class}: {user_message[:50]}...")
        
        # Generate text response using Llama
        text_response = model_manager.generate_text(
            user_message,
            exam_class=exam_class
        )
        
        # Generate image if requested
        image_url = None
        if generate_image:
            image_url = model_manager.generate_image(
                user_message,
                text_response
            )
        
        return jsonify({
            'text_response': text_response,
            'image_url': image_url,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

# Model Status Endpoint
@app.route('/api/models/status', methods=['GET'])
def model_status():
    return jsonify(model_manager.get_status())

# Serve Generated Images
@app.route('/api/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('generated_images', filename)

# Serve Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('generated_images', exist_ok=True)
    
    logger.info(f"Starting STUDYBOARD server on {HOST}:{PORT}")
    logger.info("Loading AI models... This may take a few minutes on first run.")
    
    # Initialize models
    model_manager.initialize()
    
    # Run server
    app.run(
        host=HOST,
        port=PORT,
        debug=os.getenv('FLASK_ENV') == 'development'
    )