from flask import Flask, render_template, request, jsonify, session
from chatbot import HiringAssistant
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize chatbot
chatbot = HiringAssistant(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    """Render the main chat interface"""
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Initialize conversation history in session if not exists
        if 'conversation_history' not in session:
            session['conversation_history'] = []
            session['candidate_data'] = {}
        
        # Get bot response
        response = chatbot.get_response(
            user_message, 
            session['conversation_history'],
            session['candidate_data']
        )
        
        # Update conversation history
        session['conversation_history'].append({
            'role': 'user',
            'content': user_message
        })
        session['conversation_history'].append({
            'role': 'assistant',
            'content': response['message']
        })
        
        # Update candidate data if collected
        if response.get('candidate_data'):
            session['candidate_data'].update(response['candidate_data'])
        
        # Save candidate data if conversation ended
        if response.get('conversation_ended'):
            save_candidate_data(session['candidate_data'])
        
        session.modified = True
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation"""
    session.clear()
    return jsonify({'status': 'success'})

def save_candidate_data(candidate_data):
    """Save candidate data to JSON file"""
    if not candidate_data:
        return
    
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, 'candidates.json')
    
    # Add timestamp
    candidate_data['timestamp'] = datetime.now().isoformat()
    
    # Load existing data
    candidates = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                candidates = json.load(f)
        except:
            candidates = []
    
    # Append new candidate
    candidates.append(candidate_data)
    
    # Save back to file
    with open(file_path, 'w') as f:
        json.dump(candidates, f, indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)