const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const loading = document.getElementById('loading');

// Handle Enter key press
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Show loading indicator
    loading.classList.add('active');
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Hide loading indicator
        loading.classList.remove('active');
        
        // Add bot response to chat
        addMessage(data.message, 'bot');
        
        // Check if conversation ended
        if (data.conversation_ended) {
            userInput.disabled = true;
            sendButton.disabled = true;
            
            // Show reset option after a delay
            setTimeout(() => {
                addMessage('Click the reset button to start a new conversation.', 'bot');
            }, 1000);
        }
        
    } catch (error) {
        console.error('Error:', error);
        loading.classList.remove('active');
        addMessage('Sorry, there was an error processing your message. Please try again.', 'bot');
    } finally {
        // Re-enable input
        if (!userInput.disabled) {
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function resetChat() {
    if (!confirm('Are you sure you want to start a new conversation? All current data will be lost.')) {
        return;
    }
    
    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Clear chat container
            chatContainer.innerHTML = `
                <div class="welcome-message">
                    <div class="message bot-message">
                        <div class="message-content">
                            Welcome to TalentScout! 👋 I'm your AI hiring assistant. I'll help guide you through our initial screening process. Let's get started!
                        </div>
                    </div>
                </div>
            `;
            
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.value = '';
            userInput.focus();
        }
    } catch (error) {
        console.error('Error resetting chat:', error);
        alert('Failed to reset chat. Please refresh the page.');
    }
}