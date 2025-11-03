# 🎯 دليل الرفع على أجزاء - اختر ما يناسبك

## 📋 **الخيارات المتاحة:**

### 🚀 **الخيار الأول: سكريبت واحد (الأسرع)**
```bash
bash simple_upload.sh
```
**مميزات:** سريع، بسيط، يعمل دفعة واحدة  
**وقت:** 2-3 دقائق

### ⚡ **الخيار الثاني: أوامر فردية (الأكثر أماناً)**
```bash
# انسخ كل أمر وشغله منفرداً:
git init
git config user.name "اسمك"
git config user.email "بريدك"
git add android_supermarket_app.py main_android_app.py requirements_android.txt
# ... باقي الأوامر
```
**مميزات:** تحكم كامل، لا يوجد timeout  
**وقت:** 5-10 دقائق

### 🎯 **الخيار الثالث: مبسط جداً (للمبتدئين)**
```bash
# أولاً - أول 3 ملفات:
git init && git config user.name "Raed" && git config user.email "email@domain" && git add android_supermarket_app.py main_android_app.py requirements_android.txt && git commit -m "Initial commit" && git remote add origin https://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@github.com/raedthawaba/supermarket-management-android.git && git push -u origin main

# ثانياً - باقي الملفات:
git add buildozer.spec buildozer_github_actions.spec .github/workflows/main.yml && git commit -m "Add build files" && git push
```
**مميزات:** سهل جداً، خطوة بخطوة واضحة  
**وقت:** 3-5 دقائق

## 📁 **الملفات المرفوعة:**

### 📱 **الجزء الأساسي:**
- `android_supermarket_app.py` - التطبيق الأساسي
- `main_android_app.py` - نقطة البداية
- `requirements_android.txt` - المتطلبات

### 🔧 **الجزء الإضافي:**
- `buildozer.spec` - إعدادات البناء الأساسية
- `buildozer_github_actions.spec` - إعدادات البناء للـ CI/CD
- `.github/workflows/main.yml` - GitHub Actions

### 📚 **التوثيق:**
- `README.md` - وصف المشروع

## ✅ **ما سيحدث بعد الرفع:**

1. **فوري:** سترى جميع الملفات في المستودع
2. **في دقيقة:** ستجد تبويب "Actions" في GitHub
3. **بعد 2 دقيقة:** سيبدأ البناء (إنشاء APK)
4. **بعد 15-20 دقيقة:** سيكون APK جاهز للتحميل
5. **في قسم "Artifacts"** ستجد ملف APK

## 🔗 **الروابط المهمة:**
- **المستودع:** https://github.com/raedthawaba/supermarket-management-android
- **Actions:** https://github.com/raedthawaba/supermarket-management-android/actions

## 💡 **اختر الطريقة التي تفضلها وابدأ! 🚀**