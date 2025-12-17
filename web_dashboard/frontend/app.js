
const API_URL = "http://localhost:8000/api";

// --- Tab Navigation ---
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
    
    document.getElementById('page-title').innerText = 
        tabId.charAt(0).toUpperCase() + tabId.slice(1).replace('-', ' ');
}

// --- Live Inference Call ---
async function fetchFeatures() {
    const userId = document.getElementById('entityIdInput').value;
    const output = document.getElementById('jsonOutput');
    
    output.innerText = "⏳ Connecting to Go Server...";
    
    try {
        const response = await fetch(API_URL + '/inference', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });
        
        const data = await response.json();
        output.innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        output.innerText = "❌ Error: Backend not running on port 8000.\\nRun: python web_dashboard/backend/main.py";
    }
}

// --- AI Chat Logic ---
function handleChat(e) {
    if (e.key === 'Enter') sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value;
    if (!msg) return;

    addMessage(msg, 'user');
    input.value = '';

    const typingId = addMessage('Thinking...', 'ai', true);

    try {
        const response = await fetch(API_URL + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        
        const data = await response.json();
        document.getElementById(typingId).remove();
        addMessage(data.response, 'ai');
        
    } catch (error) {
        document.getElementById(typingId).remove();
        addMessage("⚠️ AI Offline. Is the Python Backend running?", 'ai');
    }
}

function addMessage(text, sender, isTemp = false) {
    const chatWindow = document.getElementById('chatWindow');
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    if (isTemp) div.id = 'typing-' + Date.now();
    
    // Basic Markdown Formatting
    const formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    
    div.innerHTML = '<div class="bubble">' + formatted + '</div>';
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div.id;
}