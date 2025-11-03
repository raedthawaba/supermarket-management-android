# 🚀 رفع الملفات على أجزاء - دليل مبسط

## 📋 **الطريقة المبسطة - خطوة بخطوة:**

### **الخطوة 1: تهيئة المشروع**
```bash
git init
git config user.name "اسمك الكامل"
git config user.email "بريدك الإلكتروني"
```

### **الخطوة 2: إنشاء .gitignore**
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Android/Buildozer
*.apk
*.aab
bin/
.buildozer/
android/

# Environment
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/

# Database
*.db
*.sqlite
*.sqlite3
EOF
```

### **الخطوة 3: الجزء الأول - الملفات الأساسية**
```bash
git add android_supermarket_app.py main_android_app.py requirements_android.txt
git commit -m "الجزء 1: الملفات الأساسية للتطبيق"
```

### **الخطوة 4: الجزء الثاني - ملفات البناء**
```bash
git add buildozer.spec buildozer_github_actions.spec
git commit -m "الجزء 2: ملفات البناء والتكوين"
```

### **الخطوة 5: الجزء الثالث - GitHub Actions**
```bash
git add .github/workflows/main.yml
git commit -m "الجزء 3: GitHub Actions CI/CD"
```

### **الخطوة 6: الجزء الرابع - التوثيق**
```bash
git add README.md requirements.txt main.py .gitignore
git commit -m "الجزء 4: التوثيق والملفات الإضافية"
```

### **الخطوة 7: ربط ورفع المستودع**
```bash
git remote add origin https://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@github.com/raedthawaba/supermarket-management-android.git
git push -u origin main
```

## ⚡ **الطريقة السريعة (أمر واحد):**
```bash
bash upload_step_by_step.sh
```

## 📱 **بعد الرفع:**
1. اذهب للمستودع: https://github.com/raedthawaba/supermarket-management-android
2. اضغط على "Actions"
3. انتظر 15-20 دقيقة
4. حمّل APK من "Artifacts"

## ✅ **الفوائد:**
- ✅ تجنب timeout
- ✅ مرونة في التحكم
- ✅ commit منظمة وواضحة
- ✅ سهولة تتبع المشاكل