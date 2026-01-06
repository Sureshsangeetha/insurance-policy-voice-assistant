"""
Insurance Policy Enquiry AI Agent - Backend (Gemini Version)
Flask application with Google Gemini API integration
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize Gemini client
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables!")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")

# In-memory conversation storage (use database in production)
conversations = {}

# Policy documents storage
POLICY_DOCS_PATH = "policy_documents"
os.makedirs(POLICY_DOCS_PATH, exist_ok=True)

# System prompt for the AI agent
SYSTEM_PROMPT = """You are an Insurance Policy Enquiry Assistance AI agent. Your role is to:

1. Answer insurance policy-related questions ONLY using the provided policy documents
2. Classify user intent into categories: COVERAGE, PREMIUM, BENEFITS, EXCLUSIONS, CLAIM_INFO, RENEWAL, GENERAL, UNKNOWN
3. Provide clear, well-formatted responses with policy references
4. Escalate when confidence is low (<0.70) or policy content is ambiguous
5. Never provide advice, only factual policy information

STRICT FORMATTING RULES:
- Use bullet points (•) for lists
- Keep responses clear and organized
- Highlight key information with **bold** text
- Use numbered steps for procedures
- Keep paragraphs short (2-3 sentences max)
- Start with a brief summary, then provide details

RESPONSE FORMAT:
1. Start with a brief answer (1-2 sentences)
2. Provide key points as bullet points
3. Include document reference
4. State confidence level

Example Response Format:
"This policy covers hospitalization expenses including:

• Room rent up to $500/day
• ICU charges up to $1,000/day
• Doctor consultation fees
• Diagnostic tests and procedures

**Document Reference:** Section 1.1 - Medical Expenses Covered
**Confidence:** High (0.85)"

STRICT RULES:
- Only answer from approved policy documents
- Include document name and section in responses
- Do NOT interpret, advise, or infer
- Escalate if uncertain or if user requests advice
- Keep responses concise and scannable"""

def load_policy_documents():
    """Load all policy documents from the policy_documents directory"""
    policies = []
    
    if not os.path.exists(POLICY_DOCS_PATH):
        logger.warning(f"Policy documents directory not found: {POLICY_DOCS_PATH}")
        return policies
    
    for filename in os.listdir(POLICY_DOCS_PATH):
        if filename.endswith(('.txt', '.md', '.json')):
            filepath = os.path.join(POLICY_DOCS_PATH, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    policies.append({
                        'filename': filename,
                        'content': content
                    })
                    logger.info(f"Loaded policy document: {filename}")
            except Exception as e:
                logger.error(f"Error loading {filename}: {str(e)}")
    
    return policies

def classify_intent(user_message):
    """Classify user intent based on keywords"""
    message_lower = user_message.lower()
    
    keywords = {
        'COVERAGE': ['cover', 'covered', 'include', 'included', 'what is covered'],
        'PREMIUM': ['premium', 'cost', 'price', 'payment', 'pay', 'amount'],
        'BENEFITS': ['benefit', 'advantage', 'add-on', 'addon', 'feature'],
        'EXCLUSIONS': ['not covered', 'exclude', 'exclusion', 'exception'],
        'CLAIM_INFO': ['claim', 'file claim', 'claim process', 'submit claim'],
        'RENEWAL': ['renew', 'renewal', 'expire', 'expiry', 'grace period'],
        'GENERAL': ['validity', 'document', 'policy number', 'terms', 'conditions']
    }
    
    for intent, words in keywords.items():
        if any(word in message_lower for word in words):
            return intent
    
    return 'UNKNOWN'

def calculate_confidence(response_text, policy_docs):
    """Calculate confidence score based on policy document match"""
    if not policy_docs:
        return 0.3
    
    # Check if response contains specific policy references
    has_document_ref = any(doc['filename'].lower() in response_text.lower() 
                          for doc in policy_docs)
    has_section_ref = any(word in response_text.lower() 
                         for word in ['section', 'clause', 'article', 'paragraph'])
    
    # Base confidence
    confidence = 0.75 if has_document_ref and has_section_ref else 0.65
    
    # Boost confidence if response has bullet points (structured)
    if '•' in response_text or '*' in response_text or '-' in response_text:
        confidence += 0.05
    
    # Reduce confidence if response contains uncertainty words
    uncertainty_words = ['might', 'could', 'possibly', 'unclear', 'not sure']
    if any(word in response_text.lower() for word in uncertainty_words):
        confidence -= 0.2
    
    return max(0.3, min(0.95, confidence))

def should_escalate(confidence_score, user_message, response_text):
    """Determine if query should be escalated to human agent"""
    # Confidence threshold
    if confidence_score < 0.70:
        return True, "Low confidence in response"
    
    # User explicitly asks for human
    escalation_keywords = ['speak to agent', 'human agent', 'representative', 
                          'talk to person', 'customer service']
    if any(keyword in user_message.lower() for keyword in escalation_keywords):
        return True, "User requested human agent"
    
    # Response contains escalation indicators
    escalation_indicators = ['should escalate', 'recommend escalation', 
                            'consult with', 'unclear', 'ambiguous']
    if any(indicator in response_text.lower() for indicator in escalation_indicators):
        return True, "Response indicates escalation needed"
    
    return False, None

@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_configured': GEMINI_API_KEY is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user query and return AI response"""
    if not GEMINI_API_KEY:
        return jsonify({
            'error': 'Gemini API key not configured',
            'message': 'Please set GEMINI_API_KEY in .env file'
        }), 500
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', str(datetime.now().timestamp()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Processing query - Conversation: {conversation_id}")
        
        # Load policy documents
        policy_docs = load_policy_documents()
        
        # Build context with policy documents
        policy_context = "\n\n".join([
            f"POLICY DOCUMENT: {doc['filename']}\n{doc['content']}"
            for doc in policy_docs
        ]) if policy_docs else "No policy documents available."
        
        # Get conversation history
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversation_history = conversations[conversation_id]
        
        # Build conversation context for Gemini
        conversation_text = ""
        for msg in conversation_history[-6:]:  # Last 6 messages
            role = "User" if msg['role'] == 'user' else "Assistant"
            conversation_text += f"{role}: {msg['content']}\n\n"
        
        # Create the full prompt
        full_prompt = f"""{SYSTEM_PROMPT}

POLICY DOCUMENTS:
{policy_context}

CONVERSATION HISTORY:
{conversation_text}

USER QUERY: {user_message}

IMPORTANT: Format your response with:
1. Brief summary (1-2 sentences)
2. Key points as bullet points (use • symbol)
3. Document reference
4. Confidence assessment

Remember: Use bullet points, keep it organized, and cite the specific policy section."""
        
        # Call Gemini API
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(full_prompt)
        
        ai_response = response.text
        
        # Classify intent
        intent = classify_intent(user_message)
        
        # Calculate confidence
        confidence_score = calculate_confidence(ai_response, policy_docs)
        
        # Check for escalation
        needs_escalation, escalation_reason = should_escalate(
            confidence_score, user_message, ai_response
        )
        
        # Store conversation
        conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        conversation_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        conversations[conversation_id] = conversation_history
        
        # Prepare response
        result = {
            'timestamp': datetime.now().isoformat(),
            'transcribed_input': user_message,
            'intent': intent,
            'confidence_score': round(confidence_score, 2),
            'retrieved_content': {
                'document_name': policy_docs[0]['filename'] if policy_docs else 'None',
                'section': 'Auto-detected from response',
                'content_summary': ai_response[:200] + '...' if len(ai_response) > 200 else ai_response
            },
            'voice_response': ai_response,
            'follow_up_required': confidence_score < 0.80,
            'escalation_flag': needs_escalation,
            'escalation_reason': escalation_reason,
            'callback_requested': False,
            'resolution_status': 'ESCALATED' if needs_escalation else 'RESOLVED',
            'conversation_id': conversation_id
        }
        
        logger.info(f"Query processed - Intent: {intent}, Confidence: {confidence_score:.2f}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id in conversations:
        return jsonify({
            'conversation_id': conversation_id,
            'messages': conversations[conversation_id]
        })
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/api/upload_policy', methods=['POST'])
def upload_policy():
    """Upload a new policy document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith(('.txt', '.md', '.json')):
        filename = os.path.join(POLICY_DOCS_PATH, file.filename)
        file.save(filename)
        logger.info(f"Policy document uploaded: {file.filename}")
        return jsonify({
            'message': 'Policy document uploaded successfully',
            'filename': file.filename
        })
    
    return jsonify({'error': 'Invalid file type. Only .txt, .md, .json allowed'}), 400

@app.route('/api/policies', methods=['GET'])
def list_policies():
    """List all available policy documents"""
    policies = load_policy_documents()
    return jsonify({
        'count': len(policies),
        'policies': [{'filename': p['filename'], 'size': len(p['content'])} 
                    for p in policies]
    })

if __name__ == '__main__':
    logger.info("Starting Insurance Policy Enquiry AI Agent (Gemini Version)...")
    logger.info(f"API Key configured: {GEMINI_API_KEY is not None}")
    
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
