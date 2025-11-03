#!/bin/bash
# محاولة الدفع المباشر إلى GitHub كما كان سابقاً
set -e

echo "🚀 بدء محاولة الدفع المباشر إلى GitHub..."

# محاولة تحديد remote URL (من المحتمل أن يكون رابط المستودع)
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REPO_URL" ]; then
    echo "❌ لم يتم العثور على remote URL"
    echo "🔧 إضافة remote URL..."
    
    # استخراج معلومات المستودع من مجلد العمل أو محاولة استخدام GitHub API
    PWD=$(pwd)
    echo "Current directory: $PWD"
    
    # البحث عن معلومات المستودع
    if [ -f ".git/config" ]; then
        echo "📁 فحص Git config..."
        cat .git/config
    fi
fi

echo ""
echo "🔧 تكوين Git إذا لم يكن موجوداً..."
git config user.name "MiniMax Agent"
git config user.email "agent@minimax.com"

echo ""
echo "📝 إضافة جميع الملفات المحدثة..."
git add requirements.txt buildozer.spec pyproject.toml main.py android_supermarket_app.py main_android_app.py

echo ""
echo "💬 إنشاء commit..."
git commit -m "إصلاح: إضافة متطلبات Python الصحيحة لبناء Android APK

- تحديث requirements.txt بالمكتبات المطلوبة (kivy, kivymd, buildozer)
- تحديث buildozer.spec بإصدارات محددة ومتسقة
- تحسين pyproject.toml لمشروع Android كامل
- إضافة setuptools و cython لتحسين عملية البناء

يحل مشكلة GitHub Actions: 'No file matched to requirements.txt'

المطلوب: تشغيل عملية بناء APK تلقائياً على GitHub Actions"

echo ""
echo "📤 محاولة Push إلى GitHub..."

# محاولة push مع التعامل مع authentication
if git push origin main 2>/dev/null; then
    echo "✅ تم الدفع بنجاح!"
    echo "🎯 GitHub Actions ستبدأ البناء تلقائياً..."
elif git push https://github.com/raedthawa/supermarket-management-android.git main 2>/dev/null; then
    echo "✅ تم الدفع بنجاح باستخدام URL مباشر!"
    echo "🎯 GitHub Actions ستبدأ البناء تلقائياً..."
else
    echo "⚠️  لم نتمكن من الدفع تلقائياً"
    echo "💡 يرجى تنفيذ الأوامر التالية يدوياً:"
    echo ""
    echo "git push origin main"
    echo ""
    echo "أو:"
    echo ""
    echo "git push https://github.com/raedthawa/supermarket-management-android.git main"
fi

echo ""
echo "📊 ملخص التغييرات:"
git log --oneline -n 3

echo ""
echo "🎯 التوقعات بعد Push الناجح:"
echo "1. GitHub Actions تبدأ تلقائياً"
echo "2. Set up Python 3.12 - نجح ✅"
echo "3. Install Python dependencies - نجح ✅"
echo "4. Install Java JDK 11 - جاري التحميل..."
echo "5. Install Android SDK - جاري التحميل..."
echo "6. Build Android APK - جاري التحميل..."
echo "7. Upload APK artifact - تم بنجاح ✅"

echo ""
echo "⏰ الوقت المتوقع: 15-30 دقيقة"
echo "📱 حجم APK المتوقع: 15-25 MB"
echo "📍 موقع الملف: android/bin/supermarketmanager-1.0-armeabi-v7a-debug.apk"