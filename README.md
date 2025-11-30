# TalentScout - AI Hiring Assistant Chatbot

An intelligent hiring assistant chatbot built with Flask and OpenAI GPT that conducts initial candidate screening by gathering essential information and asking relevant technical questions based on the candidate's tech stack.

## 🎯 Features

- **Interactive Conversational Interface**: Natural, friendly chat experience for candidates
- **Intelligent Information Gathering**: Collects candidate details including name, email, phone, experience, position, location, and tech stack
- **Dynamic Technical Questions**: Generates 3-5 relevant technical questions based on declared tech stack
- **Context-Aware Conversations**: Maintains conversation flow and remembers previous responses
- **Exit Detection**: Gracefully handles conversation endings with keywords like "bye", "exit", "quit"
- **Data Persistence**: Saves candidate information to JSON file for later review
- **Clean UI**: Modern, responsive design with gradient theme
- **Session Management**: Proper handling of multiple conversations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd hiring-assistant-chatbot
```

2. **Create a virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-actual-api-key-here
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
```
Navigate to: http://localhost:5000
```

## 📁 Project Structure

```
hiring-assistant-chatbot/
├── app.py                  # Flask application and routes
├── chatbot.py              # Chatbot logic and OpenAI integration
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── chat.js        # Frontend JavaScript
├── templates/
│   └── index.html         # Main chat interface
└── data/
    ├── candidates.json    # Stored candidate data
    └── .gitkeep          # Keep directory in git
```

## 🛠️ Technical Details

### Technologies Used

- **Backend**: Flask 3.0.0
- **LLM**: OpenAI GPT-4o-mini (via openai 1.54.3)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: JSON files
- **Environment Management**: python-dotenv 1.0.0

### Key Components

#### 1. **app.py**
- Flask application setup
- Route handlers for chat and reset endpoints
- Session management for conversation history
- Candidate data persistence

#### 2. **chatbot.py**
- `HiringAssistant` class with OpenAI integration
- System prompt engineering for hiring context
- Information extraction using regex patterns
- Exit intent detection
- Technical question generation based on tech stack

#### 3. **Frontend (HTML/CSS/JS)**
- Responsive chat interface
- Real-time message display
- Loading indicators
- Smooth animations and transitions

## 💡 Prompt Engineering

### System Prompt Design

The chatbot uses a carefully crafted system prompt that:

1. **Establishes Role**: Defines the assistant as a professional recruiter
2. **Guides Conversation Flow**: Specifies the exact sequence of information gathering
3. **Sets Tone**: Ensures friendly, conversational interactions
4. **Defines Rules**: Prevents off-topic conversations and ensures one question at a time
5. **Adapts Questions**: Generates questions appropriate to experience level

### Information Extraction

The chatbot uses multiple strategies:
- **Regex patterns** for structured data (email, phone, experience)
- **Keyword detection** for tech stack identification
- **Context awareness** to avoid repetitive questions

### Technical Question Generation

Questions are tailored based on:
- **Experience Level**: Junior (0-2 yrs), Mid (3-5 yrs), Senior (5+ yrs)
- **Tech Stack**: Specific to mentioned technologies
- **Question Types**: Fundamentals, scenarios, architecture, best practices

## 🔒 Data Privacy & Security

- Candidate data stored locally in JSON format
- API keys managed through environment variables
- Session-based conversation management
- No data shared with third parties
- Complies with data privacy best practices

## 🎨 UI/UX Features

- **Modern Design**: Gradient theme with purple accents
- **Responsive**: Works on desktop and mobile devices
- **Smooth Animations**: Message fade-in effects
- **Loading Indicators**: Visual feedback during API calls
- **Scroll Management**: Auto-scrolls to latest messages
- **Reset Function**: Easy conversation restart

## 🧪 Usage Example

1. User opens the chat
2. Bot greets and introduces itself
3. Bot asks for name → User responds
4. Bot asks for email → User responds
5. Bot collects phone, experience, position, location
6. Bot asks about tech stack → User lists technologies
7. Bot generates 3-5 technical questions based on tech stack
8. User can answer or type "bye" to exit
9. Bot thanks user and mentions next steps
10. Data saved to `data/candidates.json`

## 🐛 Challenges & Solutions

### Challenge 1: Context Management
**Problem**: Maintaining conversation context across multiple exchanges
**Solution**: Using session storage and passing conversation history to GPT with recent message limiting (last 10 messages)

### Challenge 2: Information Extraction
**Problem**: Extracting structured data from natural language
**Solution**: Combination of regex patterns for structured fields and keyword detection for tech stack

### Challenge 3: API Rate Limiting
**Problem**: Potential for API limits with multiple users
**Solution**: Using GPT-4o-mini for cost efficiency and implementing proper error handling

### Challenge 4: Preventing Off-Topic Conversations
**Problem**: Users asking unrelated questions
**Solution**: System prompt explicitly instructs to redirect to hiring context

## 🚀 Deployment Options

### Local Deployment
Already configured! Just run `python app.py`

### Cloud Deployment (Bonus)

#### Option 1: Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Option 2: AWS EC2
1. Launch EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Set up environment variables
4. Run with Gunicorn: `gunicorn -b 0.0.0.0:5000 app:app`

#### Option 3: Google Cloud Run
1. Create `Dockerfile`
2. Build and push to Container Registry
3. Deploy to Cloud Run

## 📝 Future Enhancements

- [ ] Sentiment analysis during conversation
- [ ] Multilingual support
- [ ] Audio/video interview capabilities
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Admin dashboard for reviewing candidates
- [ ] Email notifications to recruiters
- [ ] Resume parsing and analysis
- [ ] Calendar integration for scheduling

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Developed as part of AI/ML Intern Assignment for TalentScout

## 🙏 Acknowledgments

- OpenAI for GPT API
- Flask community for excellent documentation
- TalentScout for the opportunity

---

**Note**: Remember to never commit your `.env` file with actual API keys to version control!