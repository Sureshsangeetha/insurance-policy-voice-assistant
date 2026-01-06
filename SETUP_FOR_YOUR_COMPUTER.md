# 🎯 Setup Instructions for Your Windows Computer

## What You Need to Do Now

You have the **templates** folder with **index.html** already (from the first version). Now you need to:

### Step 1: Replace app.py with the Gemini Version

**Delete your old app.py and use the new one I provided.**

In PowerShell in your project folder:
```powershell
cd D:\studies\design_thinking\sample2
```

Replace the app.py with the new Gemini version (download from the files above).

### Step 2: Update requirements.txt

Replace your requirements.txt with:
```txt
flask==3.0.0
flask-cors==4.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0
```

### Step 3: Install New Dependencies

```powershell
# Make sure you're in your virtual environment
venv\Scripts\activate

# Uninstall old packages
pip uninstall anthropic -y

# Install Gemini packages
pip install google-generativeai==0.3.2
```

Or just reinstall everything:
```powershell
pip install -r requirements.txt
```

### Step 4: Update Your .env File

Change your `.env` file from:
```env
ANTHROPIC_API_KEY=sk-ant-...
```

To:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Where to get your Gemini API key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy it
5. Paste in .env file

### Step 5: Run It!

```powershell
python app.py
```

You should see:
```
Starting Insurance Policy Enquiry AI Agent (Gemini Version)...
API Key configured: True
 * Running on http://127.0.0.1:5000
```

### Step 6: Test

Open: http://localhost:5000

---

## 📁 Your Final Project Structure

```
D:\studies\design_thinking\sample2\
├── app.py                    ← NEW Gemini version
├── .env                      ← Updated with GEMINI_API_KEY
├── requirements.txt          ← Updated for Gemini
├── templates/
│   └── index.html           ← Already there (keep it!)
├── policy_documents/
│   └── sample_health_policy.md
├── venv/                    ← Your virtual environment
└── agent.log                ← Log file
```

---

## ✅ Quick Checklist

- [ ] Download new `app.py` (Gemini version)
- [ ] Update `requirements.txt`
- [ ] Run: `pip install -r requirements.txt`
- [ ] Get Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Update `.env` with `GEMINI_API_KEY=your_key`
- [ ] Run: `python app.py`
- [ ] Open: http://localhost:5000
- [ ] Test with a question!

---

## 🎉 Why This is Better for You

**FREE API** ✅
- No credit card needed
- 60 requests per minute
- Perfect for testing and learning

**Same Features** ✅
- Voice input
- Text input
- Document upload
- Confidence scoring
- Auto escalation

**Easy Setup** ✅
- Just change API key
- No payment setup
- Works immediately

---

## 🐛 If You Get Errors

### Error: "Module 'google.generativeai' not found"
```powershell
pip install google-generativeai
```

### Error: "GEMINI_API_KEY not configured"
Check your .env file:
```env
GEMINI_API_KEY=your_actual_key_here
```
(No quotes, no spaces)

### Error: "templates/index.html not found"
You already have this from before! Just make sure the `templates` folder is in the same directory as `app.py`.

---

## 💡 Pro Tip

Keep your old files as backup:
```powershell
# Backup old version
mkdir backup
copy app.py backup\app_anthropic.py
copy .env backup\.env_anthropic
```

Then use the new Gemini version!

---

**You're all set!** Just follow the steps above and you'll have a working AI agent with your FREE Gemini API key! 🚀
