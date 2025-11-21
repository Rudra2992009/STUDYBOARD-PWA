// PWA Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('ServiceWorker registered:', registration);
      })
      .catch(err => {
        console.error('ServiceWorker registration failed:', err);
      });
  });
}

// PWA Install Prompt
let deferredPrompt;
const installPrompt = document.getElementById('install-prompt');
const installButton = document.getElementById('install-button');
const dismissInstall = document.getElementById('dismiss-install');

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installPrompt.classList.remove('hidden');
});

installButton.addEventListener('click', async () => {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response: ${outcome}`);
    deferredPrompt = null;
    installPrompt.classList.add('hidden');
  }
});

dismissInstall.addEventListener('click', () => {
  installPrompt.classList.add('hidden');
});

// App Variables
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const generateImageCheckbox = document.getElementById('generate-image');
const examClassSelect = document.getElementById('exam-class');
const loadingIndicator = document.getElementById('loading');
const charCount = document.getElementById('char-count');
const statusDot = document.getElementById('connection-status');
const statusText = document.getElementById('status-text');

// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000'
  : '/api';

// Connection Status
function updateConnectionStatus(online) {
  if (online) {
    statusDot.classList.add('online');
    statusText.textContent = 'Online';
  } else {
    statusDot.classList.remove('online');
    statusText.textContent = 'Offline';
  }
}

window.addEventListener('online', () => updateConnectionStatus(true));
window.addEventListener('offline', () => updateConnectionStatus(false));

// Character Counter
userInput.addEventListener('input', () => {
  const length = userInput.value.length;
  charCount.textContent = length;
  
  // Auto-resize textarea
  userInput.style.height = 'auto';
  userInput.style.height = userInput.scrollHeight + 'px';
});

// Send Message
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  const examClass = examClassSelect.value;
  const includeImage = generateImageCheckbox.checked;

  // Display user message
  addMessage(message, 'user');
  userInput.value = '';
  charCount.textContent = '0';
  userInput.style.height = 'auto';

  // Show loading
  loadingIndicator.classList.remove('hidden');
  sendButton.disabled = true;

  try {
    // Call backend API
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        exam_class: examClass,
        generate_image: includeImage
      })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    
    // Display AI response
    addMessage(data.text_response, 'ai', data.image_url);

  } catch (error) {
    console.error('Error:', error);
    addMessage(
      'Sorry, I encountered an error processing your request. Please try again or check your connection.',
      'ai'
    );
  } finally {
    loadingIndicator.classList.add('hidden');
    sendButton.disabled = false;
  }
}

// Add Message to Chat
function addMessage(text, sender, imageUrl = null) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';

  const textDiv = document.createElement('div');
  textDiv.className = 'message-text';
  textDiv.textContent = text;
  contentDiv.appendChild(textDiv);

  // Add image if provided
  if (imageUrl && sender === 'ai') {
    const imageDiv = document.createElement('div');
    imageDiv.className = 'message-image';
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Generated visualization';
    img.loading = 'lazy';
    imageDiv.appendChild(img);
    contentDiv.appendChild(imageDiv);
  }

  // Add timestamp
  const timeDiv = document.createElement('div');
  timeDiv.className = 'message-time';
  timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  contentDiv.appendChild(timeDiv);

  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);

  // Remove welcome message if present
  const welcomeMessage = document.querySelector('.welcome-message');
  if (welcomeMessage && chatMessages.children.length > 1) {
    welcomeMessage.remove();
  }

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Initialize
updateConnectionStatus(navigator.onLine);