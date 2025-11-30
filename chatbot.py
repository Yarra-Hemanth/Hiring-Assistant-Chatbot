from openai import OpenAI
import re
import json

class HiringAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using GPT-4o-mini for cost efficiency
        
        # System prompt for the hiring assistant
        self.system_prompt = """You are a professional hiring assistant for TalentScout, a recruitment agency specializing in technology placements. Your role is to conduct initial candidate screening through a friendly, conversational interview.

CONVERSATION FLOW:
1. Start with a warm greeting and brief introduction
2. Collect candidate information in a natural, conversational manner:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (programming languages, frameworks, databases, tools)

3. After collecting tech stack, ask 3-5 relevant technical questions based on their technologies
4. End gracefully, thanking them and mentioning next steps

RULES:
- Be conversational and friendly, not robotic
- Ask one question at a time to avoid overwhelming the candidate
- If the user provides multiple pieces of information at once, acknowledge all of them
- For tech stack, encourage them to list all relevant technologies
- Generate technical questions appropriate to their experience level
- If user asks unrelated questions, politely redirect to the hiring process
- Detect exit keywords like "bye", "exit", "quit", "goodbye" and end the conversation gracefully
- Don't repeat questions already answered
- Keep responses concise but friendly

TECHNICAL QUESTIONS:
- For junior candidates (0-2 years): Focus on fundamentals and basic concepts
- For mid-level (3-5 years): Include scenario-based and practical questions
- For senior (5+ years): Ask about architecture, best practices, and complex scenarios
- Questions should be specific to technologies they mentioned

When you have collected a piece of information, acknowledge it naturally in conversation."""

        # Fields to collect
        self.required_fields = {
            'name': r'(?:my name is |i am |i\'m |call me )([a-zA-Z\s]+)',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'phone': r'(\+?\d[\d\s\-\(\)]{8,}\d)',
            'experience': r'(\d+)\s*(?:years?|yrs?)',
            'position': r'(?:position|role|job)(?:\s+is|\s+as)?\s+([a-zA-Z\s/]+?)(?:\.|,|$)',
            'location': r'(?:from|in|at|located in)\s+([a-zA-Z\s,]+)',
        }
        
    def extract_candidate_info(self, message, existing_data):
        """Extract candidate information from the message"""
        message_lower = message.lower()
        extracted = {}
        
        # Extract information using regex patterns
        for field, pattern in self.required_fields.items():
            if field not in existing_data:
                match = re.search(pattern, message_lower)
                if match:
                    extracted[field] = match.group(1).strip()
        
        # Special handling for tech stack
        if 'tech_stack' not in existing_data:
            tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 
                           'node', 'django', 'flask', 'spring', 'sql', 'mongodb', 
                           'postgresql', 'mysql', 'aws', 'azure', 'docker', 'kubernetes',
                           'typescript', 'c++', 'c#', 'ruby', 'php', 'golang', 'rust']
            
            found_tech = [tech for tech in tech_keywords if tech in message_lower]
            if found_tech or any(keyword in message_lower for keyword in ['tech stack', 'technologies', 'languages', 'frameworks']):
                extracted['tech_stack'] = message
        
        return extracted

    def check_exit_intent(self, message):
        """Check if user wants to end the conversation"""
        exit_keywords = ['bye', 'goodbye', 'exit', 'quit', 'end', 'stop', 'thanks bye', 'thank you bye']
        message_lower = message.lower().strip()
        return any(keyword in message_lower for keyword in exit_keywords)

    def get_response(self, user_message, conversation_history, candidate_data):
        """Get response from the chatbot"""
        
        # Check for exit intent
        if self.check_exit_intent(user_message):
            return {
                'message': "Thank you for your time! We have recorded your information and will review your profile. Our team will reach out to you within 2-3 business days with the next steps. Have a great day! 👋",
                'conversation_ended': True,
                'candidate_data': candidate_data
            }
        
        # Extract any new candidate information
        new_info = self.extract_candidate_info(user_message, candidate_data)
        candidate_data.update(new_info)
        
        # Build conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation context about collected data
        if candidate_data:
            context = f"\n\nCURRENT CANDIDATE DATA COLLECTED:\n{json.dumps(candidate_data, indent=2)}"
            messages.append({"role": "system", "content": context})
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            bot_message = response.choices[0].message.content
            
            return {
                'message': bot_message,
                'conversation_ended': False,
                'candidate_data': candidate_data
            }
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return {
                'message': "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                'conversation_ended': False,
                'candidate_data': candidate_data
            }