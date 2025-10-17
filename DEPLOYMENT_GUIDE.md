# 🚀 Deployment Guide - PythonAnywhere

**Complete step-by-step instructions to deploy the SA Health App to PythonAnywhere**

---

## 📋 Prerequisites

- ✅ GitHub account (you have: rapid-flapper)
- ✅ Your code is on GitHub (yes: sa-health-app)
- ✅ PythonAnywhere account (we'll create this)

---

## 🎯 Step 1: Create PythonAnywhere Account

### **1.1 Sign Up**

1. Go to: https://www.pythonanywhere.com
2. Click **"Start running Python online in less than a minute!"**
3. Click **"Create a Beginner account"** (FREE)
4. Fill in:
   - **Username**: Choose something professional (e.g., `sahealthapp` or `arnolddev`)
   - **Email**: Your email
   - **Password**: Create a strong password
5. Click **"Register"**
6. Verify your email

**Your URL will be**: `https://YOUR-USERNAME.pythonanywhere.com`

For example, if you chose `sahealthapp`, your URL will be:
```
https://sahealthapp.pythonanywhere.com
```

---

## 🔧 Step 2: Set Up Your Web App

### **2.1 Open Bash Console**

1. Log in to PythonAnywhere
2. Click **"Dashboard"** (top menu)
3. Click **"Consoles"** tab
4. Click **"Bash"** to open a new console

### **2.2 Clone Your Repository**

In the Bash console, type these commands:

```bash
# Clone your GitHub repository
git clone https://github.com/rapid-flapper/sa-health-app.git

# Navigate into the project
cd sa-health-app

# Verify files are there
ls
```

You should see all your files: `app.py`, `data/`, `app/`, etc.

### **2.3 Create Virtual Environment**

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Wait for installation to complete (~30 seconds).

### **2.4 Test That It Works**

```bash
# Quick test
python3.10 -c "from flask import Flask; print('Flask works!')"
python3.10 -c "from gtts import gTTS; print('gTTS works!')"
```

If both print "works!", you're good! ✅

---

## 🌐 Step 3: Configure Web App

### **3.1 Create Web App**

1. Go back to Dashboard
2. Click **"Web"** tab (top menu)
3. Click **"Add a new web app"**
4. Click **"Next"** (accept default domain)
5. Select **"Manual configuration"**
6. Select **"Python 3.10"**
7. Click **"Next"**

### **3.2 Configure Virtual Environment**

Scroll down to **"Virtualenv"** section:

1. Enter the path to your virtual environment:
   ```
   /home/YOUR-USERNAME/sa-health-app/venv
   ```
   Replace `YOUR-USERNAME` with your PythonAnywhere username
   
2. Click the **blue checkmark** to save

### **3.3 Configure WSGI File**

1. Scroll to **"Code"** section
2. Click on the **WSGI configuration file** link (blue text)
   - It will be something like: `/var/www/yourname_pythonanywhere_com_wsgi.py`

3. **Delete everything** in that file

4. Replace with this code:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR-USERNAME/sa-health-app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment to production (not development)
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application
```

**IMPORTANT**: Replace `YOUR-USERNAME` with your actual PythonAnywhere username!

5. Click **"Save"** (top right)

### **3.4 Configure Static Files**

1. Go back to the **Web** tab
2. Scroll to **"Static files"** section
3. Add a new static file mapping:
   - **URL**: `/static/`
   - **Directory**: `/home/YOUR-USERNAME/sa-health-app/app/static`
   
   (Replace `YOUR-USERNAME` with your username)

4. Click the **green checkmark**

---

## 🎉 Step 4: Launch Your App!

### **4.1 Reload the Web App**

1. Scroll to the top of the **Web** tab
2. Click the big green **"Reload"** button
3. Wait 5-10 seconds

### **4.2 Visit Your App**

Click the link at the top:
```
https://YOUR-USERNAME.pythonanywhere.com
```

**You should see**:
- The home page with "Welcome" and "Launch Interactive App" button
- Click "Launch Interactive App"
- You'll see the full SA Health App! 🎉

### **4.3 Test Everything**

✅ Test on desktop browser  
✅ Test on phone (works from anywhere now!)  
✅ Try all features:
- Language selection
- Category filtering
- Phrase display
- Audio playback

---

## 📱 Share with Others

**Your app is now live!** Share this URL:

```
https://YOUR-USERNAME.pythonanywhere.com/app
```

Anyone in the world can access it now! 🌍

---

## 🐛 Troubleshooting

### **Problem: "Something went wrong" error**

**Solution**: Check error logs
1. Go to **Web** tab
2. Scroll to **"Log files"** section
3. Click on **"Error log"**
4. Look for recent errors

Common issues:
- Wrong virtualenv path
- WSGI file has wrong username
- Missing dependencies

### **Problem: Static files (CSS) don't load**

**Solution**: Check static files path
1. Go to **Web** tab
2. Check **"Static files"** section
3. Make sure path is: `/home/YOUR-USERNAME/sa-health-app/app/static`

### **Problem: Audio doesn't work**

**Solution**: Check if gTTS is installed
1. Open **Bash console**
2. Run:
   ```bash
   cd sa-health-app
   source venv/bin/activate
   pip list | grep gTTS
   ```
3. If not there, install it:
   ```bash
   pip install gtts
   ```

### **Problem: 404 Not Found**

**Solution**: Make sure you're going to `/app` not just `/`
- ❌ `https://yourname.pythonanywhere.com` (home page only)
- ✅ `https://yourname.pythonanywhere.com/app` (full app)

---

## 🔄 Updating Your App Later

When you make changes to your code:

### **On Your Computer:**

```bash
# Commit and push changes
git add .
git commit -m "Description of changes"
git push origin dev
git checkout main
git merge dev
git push origin main
```

### **On PythonAnywhere:**

1. Open **Bash console**
2. Run:
   ```bash
   cd sa-health-app
   git pull origin main
   ```
3. Go to **Web** tab
4. Click **"Reload"** button

Your changes are now live! 🎉

---

## 💰 Free Tier Limitations

PythonAnywhere FREE account includes:
- ✅ One web app
- ✅ Your own subdomain (yourname.pythonanywhere.com)
- ✅ 512MB storage
- ✅ Python 3.10 support
- ⚠️ Goes to sleep after inactivity (wakes up on first request)
- ⚠️ No custom domain (need paid plan)
- ⚠️ Limited CPU time per day

**For your MVP testing, the free tier is perfect!** 👍

---

## 🎯 Testing Checklist

Before sharing with healthcare workers:

✅ Home page loads  
✅ App page loads  
✅ Both language selectors work  
✅ All 8 categories work  
✅ All 10 phrases display correctly  
✅ Audio plays for all languages  
✅ Works on desktop browser  
✅ Works on mobile browser  
✅ Loading states show properly  
✅ No console errors  

---

## 📊 Gathering Feedback

### **Questions to Ask Healthcare Workers:**

**Usability:**
- Is the interface intuitive?
- Are buttons easy to find and tap?
- Is text readable?
- Is audio quality acceptable?

**Content:**
- Which phrases are most useful?
- What phrases are missing?
- Which categories are most needed?
- Any medical terminology issues?

**Features:**
- What would make this more useful?
- Any pain points in the workflow?
- Would offline mode be valuable?

**Audio:**
- Is pronunciation good enough for Zulu/Xhosa/Sepedi?
- Would you pay for professional recordings?
- Any specific phrases need better audio?

---

## 🚀 After Deployment

### **Share Your App:**

**With Friends:**
```
Hey! Check out this medical translation app I built:
https://YOUR-USERNAME.pythonanywhere.com/app

It helps healthcare workers communicate across SA's 11 languages.
Would love your feedback!
```

**With Healthcare Workers:**
```
I've developed a tool to help with multilingual patient communication.
It's a prototype with 10 phrases in 5 languages.

Try it: https://YOUR-USERNAME.pythonanywhere.com/app

Your feedback on:
- Usefulness of current phrases
- Missing phrases you need
- Audio quality
- Overall user experience

Would be invaluable for development!
```

---

## 📈 Next Steps After Feedback

Based on what you learn:

**Phase 2 Planning:**
1. Prioritize most-needed phrases
2. Expand to 50-100 phrases
3. Decide on audio strategy:
   - Record native speakers?
   - Use Azure TTS (better quality)?
   - Keep gTTS (good enough)?
4. Add requested features
5. Consider PWA for offline use

---

## ✅ Quick Reference

**Your URLs:**
- Dashboard: https://www.pythonanywhere.com/user/YOUR-USERNAME/
- Your App: https://YOUR-USERNAME.pythonanywhere.com/app
- Bash Console: Dashboard → Consoles → Bash
- Web Config: Dashboard → Web
- Error Logs: Web → Log files → Error log

**Common Commands:**
```bash
# Connect to PythonAnywhere
ssh YOUR-USERNAME@ssh.pythonanywhere.com

# Update code
cd sa-health-app
git pull origin main

# Reload app
# Go to Web tab → Click Reload button
```

---

## 🎉 You're Ready to Deploy!

Follow the steps above, and within **15-20 minutes** your app will be live and accessible worldwide!

**Good luck!** 🚀

If you run into any issues during deployment, let me know and I'll help troubleshoot!
