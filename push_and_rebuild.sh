#!/bin/bash
# سكريبت دفع التغييرات وإعادة تشغيل بناء APK
# Git Push and APK Rebuild Script

echo "🚀 بدء عملية دفع التغييرات وإعادة بناء APK..."

# التحقق من وجود git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. يرجى تثبيت Git أولاً."
    exit 1
fi

echo "📁 فحص الملفات المحدثة..."
echo "=== requirements.txt ==="
head -10 requirements.txt

echo ""
echo "=== buildozer.spec (أول 20 سطر) ==="
head -20 buildozer.spec

echo ""
echo "=== pyproject.toml (أول 15 سطر) ==="
head -15 pyproject.toml

echo ""
echo "🔍 التحقق من حالة Git..."
git status

echo ""
echo "📝 إضافة جميع التغييرات..."
git add .

echo ""
echo "💬 إنشاء commit بالرسالة المحدثة..."
git commit -m "إصلاح: إضافة متطلبات Python الصحيحة لبناء Android APK

- تحديث requirements.txt بالمكتبات المطلوبة (kivy, kivymd, buildozer)
- تحديث buildozer.spec بإصدارات محددة
- تحسين pyproject.toml لمشروع Android
- إضافة setuptools و cython لبناء أفضل

يحل مشكلة 'No file matched to requirements.txt'
الخطوات التالية: GitHub Actions ستبدأ البناء تلقائياً"

echo ""
echo "📤 دفع التغييرات إلى GitHub..."
echo "⚠️  قد تحتاج إلى إدخال بيانات الاعتماد الخاصة بك"

# محاولة الدفع مع إرشادات واضحة
echo ""
echo "✨ تأكيد الدفع:"
echo "git push origin main"

# تحقق إضافي
echo ""
echo "🔍 الملفات المهمة للتأكد:"
ls -la requirements.txt buildozer.spec pyproject.toml main.py android_supermarket_app.py main_android_app.py

echo ""
echo "🎯 التوقعات بعد Push:"
echo "1. GitHub Actions ستبدأ تلقائياً"
echo "2. خطوة 'Set up Python 3.12' ستمر بنجاح"
echo "3. سيتم تثبيت جميع التبعيات"
echo "4. ستبدأ عملية تحميل Android SDK"
echo "5. بناء APK النهائي"

echo ""
echo "✅ تم تحضير السكريبت. يرجى تنفيذ الأمر التالي يدوياً:"
echo "git push origin main"