# 🛡️ Insurance Policy Enquiry AI Agent (Gemini Version)

A voice-enabled conversational AI agent built with Python Flask and **Google Gemini API** to answer insurance policy-related customer enquiries accurately using approved policy documents.

## 🎯 Features

- **Voice & Text Input**: Supports both voice commands and text input
- **Multi-turn Conversations**: Maintains conversation context across multiple queries
- **Intent Classification**: Automatically classifies queries into categories
- **Confidence Scoring**: Calculates confidence scores and escalates low-confidence queries
- **Policy Document Management**: Upload and manage multiple policy documents
- **Real-time Processing**: Instant responses using Google Gemini Pro
- **Powered by Google Gemini**: Uses Google's advanced AI model

## 📋 Prerequisites

- Python 3.8 or higher
- **Google Gemini API key** (Free! Get it from Google AI Studio)
- Modern web browser with microphone support (for voice input)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- google-generativeai (Gemini API)
- flask-cors (CORS support)
- python-dotenv (environment management)

### Step 2: Get Your FREE Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key

**Note:** Gemini API is completely FREE for personal use! No credit card required.

### Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
# On Windows
copy .env.example .env

# On Mac/Linux
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=5000
DEBUG=False
```

**Important:** Replace `your_gemini_api_key_here` with your actual API key!

### Step 4: Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Step 5: Open in Browser

```
http://localhost:5000
```

## 📁 Project Structure

```
insurance-ai-agent-gemini/
├── app.py                      # Main Flask application (Gemini version)
├── templates/
│   └── index.html             # Frontend UI
├── policy_documents/          # Policy documents directory
│   └── sample_health_policy.md # Sample policy document
├── requirements.txt           # Python dependencies (Gemini)
├── .env.example              # Environment variables template
├── .env                      # Your actual config (create this)
├── agent.log                 # Application logs (auto-generated)
└── README.md                 # This file
```

## 🎮 How to Use

### Text Input
1. Type your question in the input box
2. Click "Send" or press Enter
3. View the AI's response with confidence score

### Voice Input
1. Click the microphone button (🎤)
2. Speak your question clearly
3. The speech will be transcribed automatically
4. Click Send to get the response

### Upload Policy Documents
1. Scroll to the bottom of the page
2. Drag and drop policy documents (.txt, .md, .json)
3. Or click to browse and select files
4. Documents are immediately available for queries

## 📝 Sample Queries

Try these example questions:

- "What is covered under this health insurance policy?"
- "How much is the annual premium?"
- "What are the exclusions in the policy?"
- "How do I file a claim?"
- "When is my policy renewal date?"
- "What is the waiting period for pre-existing conditions?"
- "Is maternity covered?"
- "What is the room rent limit?"

## 🔧 API Endpoints

### Health Check
```
GET /api/health
```
Returns API connection status

### Process Query
```
POST /api/query
Body: {
  "message": "Your question here",
  "conversation_id": "optional_conversation_id"
}
```
Returns structured response with intent, confidence, and answer

### Upload Policy Document
```
POST /api/upload_policy
Body: FormData with file
```
Uploads a new policy document

### List Policies
```
GET /api/policies
```
Returns list of all uploaded policy documents

## 🆚 Gemini vs Claude Comparison

### Why Gemini?

| Feature | Gemini Pro | Claude Sonnet |
|---------|-----------|---------------|
| **Cost** | ✅ FREE (60 requests/min) | ❌ Paid (~$0.01-0.03/query) |
| **Access** | ✅ No credit card needed | ❌ Requires payment setup |
| **Speed** | ⚡ Very fast | ⚡ Fast |
| **Quality** | ✅ Excellent | ✅ Excellent |
| **Rate Limits** | 60 req/min (free) | Based on tier |

**Bottom line:** Gemini is perfect for testing, learning, and small-scale deployments because it's completely free!

## 🎯 Intent Categories

| Intent | Description | Example Queries |
|--------|-------------|-----------------|
| COVERAGE | What is/isn't covered | "What does this policy cover?" |
| PREMIUM | Cost and payments | "How much is the premium?" |
| BENEFITS | Policy advantages | "What benefits do I get?" |
| EXCLUSIONS | Non-covered items | "What is not covered?" |
| CLAIM_INFO | Claim process info | "How do I file a claim?" |
| RENEWAL | Renewal details | "When does policy expire?" |
| GENERAL | General policy info | "What is my policy number?" |
| UNKNOWN | Unclear intent | Requires clarification |

## 🚨 Escalation Logic

Queries are escalated to human agents when:

1. **Confidence < 0.70**: AI is not confident about the answer
2. **Ambiguous Policy Content**: Information is unclear in documents
3. **User Requests Human**: User explicitly asks for human agent
4. **Advisory Requests**: User asks for advice or interpretation

## ⚙️ Configuration

### Environment Variables

```env
GEMINI_API_KEY=your_api_key_here    # Required
PORT=5000                           # Server port
DEBUG=False                         # Debug mode (True/False)
```

## 📤 Adding Your Own Policy Documents

1. Create your policy document in `.txt`, `.md`, or `.json` format
2. Upload via the web interface or place in `policy_documents/` folder
3. The AI will automatically use it to answer questions

### Policy Document Format Tips

```markdown
# Policy Name

## Section 1: Coverage
Clear description of what's covered...

## Section 2: Premium
Premium amounts and payment details...

## Section 3: Exclusions
What is NOT covered...
```

## 🐛 Troubleshooting

### "Gemini API key not configured"
- Make sure `.env` file exists in the project root
- Verify `GEMINI_API_KEY=your_actual_key` (no quotes, no spaces)
- Check that you copied the complete API key

### "Module not found: google.generativeai"
```bash
pip install google-generativeai==0.3.2
```

### "Port already in use"
Change port in `.env`:
```env
PORT=5001
```

### Voice Input Not Working
- Use Chrome or Edge browser (best compatibility)
- Allow microphone permissions when prompted
- Check microphone is working in system settings

### API Rate Limit Error
Gemini free tier allows 60 requests per minute. If you hit the limit:
- Wait 1 minute
- Reduce query frequency
- Consider upgrading (still very affordable)

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- API keys are stored in environment variables only
- All conversations are in-memory (cleared on restart)
- No sensitive user data is stored

## 🎉 Why This Gemini Version is Better for You

1. **✅ 100% FREE**: No credit card required, ever
2. **✅ Easy Setup**: Just get API key from Google
3. **✅ No Usage Limits**: 60 requests/minute is generous for testing
4. **✅ High Quality**: Gemini Pro is Google's latest AI model
5. **✅ Fast**: Quick response times
6. **✅ Same Features**: All functionality as Claude version

## 📞 Support

### Getting Your Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

### For Issues
1. Check `agent.log` for errors
2. Run health check: http://localhost:5000/api/health
3. Verify `.env` file has correct API key
4. Make sure `templates/index.html` exists

## 🚀 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Get FREE Gemini API key
3. ✅ Create `.env` with your API key
4. ✅ Run: `python app.py`
5. ✅ Open: http://localhost:5000
6. ✅ Upload your policy documents
7. ✅ Start asking questions!

---

**Built with:**
- Python Flask
- Google Gemini Pro API
- HTML/CSS/JavaScript
- Web Speech API

**Version:** 1.0.0 (Gemini Edition)  
**Last Updated:** January 2025  
**Cost:** FREE! 🎉
