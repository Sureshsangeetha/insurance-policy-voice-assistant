# ⚡ Quick Setup Guide (Gemini Version)

## 🎯 Get Running in 3 Minutes!

### Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

### Step 2: Get FREE Gemini API Key (1 minute)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key

**✅ No credit card needed! Completely FREE!**

### Step 3: Add API Key (30 seconds)

Create `.env` file:

**On Windows:**
```powershell
copy .env.example .env
notepad .env
```

**On Mac/Linux:**
```bash
cp .env.example .env
nano .env
```

Add your key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

⚠️ **Important:** 
- No quotes around the key
- No spaces around the `=`
- Replace `your_actual_api_key_here` with your real key

### Step 4: Run! (10 seconds)

```bash
python app.py
```

Open browser: **http://localhost:5000**

---

## ✅ Verify It's Working

You should see:
```
Starting Insurance Policy Enquiry AI Agent (Gemini Version)...
API Key configured: True
 * Running on http://127.0.0.1:5000
```

---

## 🎤 Test It!

### Try These Questions:

1. **Text:** "What is covered under this policy?"
2. **Voice:** Click 🎤 and say "How much is the premium?"
3. **Upload:** Drag a policy document to test

---

## 🐛 Quick Fixes

### ❌ "Module 'google.generativeai' not found"
```bash
pip install google-generativeai
```

### ❌ "API key not configured"
Make sure:
1. `.env` file exists
2. Contains: `GEMINI_API_KEY=your_key`
3. No typos in "GEMINI_API_KEY"

### ❌ "templates/index.html not found"
Make sure you have the `templates` folder with `index.html` inside it in the same directory as `app.py`.

### ❌ Port already in use
Edit `.env`:
```env
PORT=5001
```

---

## 📁 Your Files Should Look Like:

```
your-project-folder/
├── app.py                  ← Main file
├── .env                    ← YOUR API KEY (create this!)
├── .env.example           ← Template
├── requirements.txt       ← Dependencies
├── templates/
│   └── index.html        ← UI
└── policy_documents/     ← Your policies
    └── sample_health_policy.md
```

---

## 💰 Cost

**FREE!** Gemini Pro is free for personal use:
- 60 requests per minute
- No credit card required
- No hidden fees
- Perfect for testing and small projects

---

## 🎉 You're Done!

Your AI agent is now running with Google Gemini!

**What's Different from Claude Version?**
- ✅ Uses Google Gemini (FREE) instead of Anthropic Claude (Paid)
- ✅ Same features, same UI, same functionality
- ✅ Just a different AI provider

**Need Help?**
- Check `agent.log` for errors
- Visit: https://ai.google.dev/tutorials/python_quickstart
- Make sure API key is correct

---

**Ready to go!** 🚀
