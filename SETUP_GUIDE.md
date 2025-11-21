# STUDYBOARD PWA - Detailed Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Model Configuration](#model-configuration)
4. [Deployment Options](#deployment-options)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 11+
- **RAM**: 6GB (8GB for Llama-2-7B)
- **Storage**: 10GB free space
- **CPU**: 4 cores, 2.5GHz+
- **Python**: 3.10 or higher
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+

### Recommended Requirements
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU with 6GB+ VRAM (RTX 3060 or better)
- **CUDA**: 11.8 or higher
- **Storage**: SSD with 20GB+ free space

---

## Installation Steps

### Step 1: Environment Setup

#### Windows
```powershell
# Install Python from python.org (3.10+)
# Verify installation
python --version

# Install Git
winget install Git.Git

# Clone repository
git clone https://github.com/Rudra2992009/STUDYBOARD-PWA.git
cd STUDYBOARD-PWA

# Create virtual environment
python -m venv venv
venv\Scripts\activate
```

#### Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.10 python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/Rudra2992009/STUDYBOARD-PWA.git
cd STUDYBOARD-PWA

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python@3.10 git

# Clone repository
git clone https://github.com/Rudra2992009/STUDYBOARD-PWA.git
cd STUDYBOARD-PWA

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Python Dependencies

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

**If you have GPU (NVIDIA with CUDA):**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**If CPU only:**
```bash
pip install torch torchvision torchaudio
```

### Step 3: Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
```

---

## Model Configuration

### Option 1: Automatic Download (Recommended)

Models will download automatically on first run:

```bash
cd backend
python server.py
```

This will:
1. Download TinyLlama-1.1B (~1.4GB)
2. Download Stable Diffusion 2.1 Base (~2GB)
3. Cache models in `~/.cache/huggingface/`

**First-time startup may take 10-30 minutes depending on internet speed.**

### Option 2: Manual Model Selection

Edit `backend/model_loader.py`:

```python
# For lightweight/CPU setup
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # ~1.4GB

# For better quality (requires GPU)
model_name = "meta-llama/Llama-2-7b-chat-hf"  # ~13GB (requires Meta approval)

# Alternative: Microsoft Phi-2
model_name = "microsoft/phi-2"  # ~2.7GB
```

### Option 3: Use Quantized Models

For 4-bit quantization (saves memory):

```bash
pip install bitsandbytes
```

In `model_loader.py`, add:
```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto"
)
```

---

## Deployment Options

### Local Development

```bash
# Terminal 1: Backend
cd backend
python server.py

# Terminal 2: Frontend (optional)
cd public
python -m http.server 8080

# Access at http://localhost:5000
```

### Production with Gunicorn

```bash
cd backend
pip install gunicorn
gunicorn --workers 2 --bind 0.0.0.0:5000 --timeout 300 server:app
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### GitHub Pages (Frontend Only)

1. Push code to GitHub
2. Go to Settings → Pages
3. Set source to `gh-pages` branch
4. GitHub Actions will auto-deploy

**Note**: Backend must be hosted separately (not supported by GitHub Pages)

### Cloud Deployment

#### AWS EC2
```bash
# Launch Ubuntu instance (t3.large or larger)
# SSH into instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3.10 python3-pip nginx -y

# Clone and setup
git clone https://github.com/Rudra2992009/STUDYBOARD-PWA.git
cd STUDYBOARD-PWA/backend
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/studyboard.service
```

Add:
```ini
[Unit]
Description=STUDYBOARD Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/STUDYBOARD-PWA/backend
ExecStart=/usr/bin/python3 server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable studyboard
sudo systemctl start studyboard
```

---

## Troubleshooting

### Issue: "CUDA out of memory"

**Solution 1**: Enable CPU offloading
```python
model.enable_model_cpu_offload()
```

**Solution 2**: Use smaller model
```python
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

**Solution 3**: Reduce batch size
```python
max_new_tokens=256  # Instead of 512
```

### Issue: "Module 'torch' has no attribute 'cuda'"

**Solution**: Reinstall PyTorch
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio
```

### Issue: "Port 5000 already in use"

**Solution**: Change port in `server.py`
```python
PORT = 5001  # or any available port
```

### Issue: "Model download very slow"

**Solution**: Use mirror or download manually
```bash
# Set environment variable
export HF_ENDPOINT=https://hf-mirror.com
python server.py
```

### Issue: "Service worker not registering"

**Solution**: Serve over HTTPS or localhost
```bash
# Use mkcert for local HTTPS
mkcert -install
mkcert localhost
```

### Issue: "Image generation fails"

**Solution 1**: Check VRAM
```python
# Reduce image size
width=256, height=256  # Instead of 512x512
```

**Solution 2**: Disable image generation temporarily
```javascript
// In app.js
generate_image: false
```

---

## Performance Tips

1. **Use SSD** for model storage
2. **Close other applications** to free RAM
3. **Update GPU drivers** for CUDA
4. **Use quantized models** for faster inference
5. **Enable attention slicing** in model_loader.py

```python
image_pipeline.enable_attention_slicing()
```

6. **Batch requests** when possible
7. **Cache model outputs** for repeated queries

---

## Next Steps

- Read [API Documentation](API.md)
- Check [Contributing Guidelines](CONTRIBUTING.md)
- Join community discussions
- Report bugs on GitHub Issues

---

**Need help? Email: rudra160113.work@gmail.com**