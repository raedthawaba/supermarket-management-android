# دليل استخدام GitHub Actions لبناء APK

## نظرة عامة

هذا المشروع يحتوي على **GitHub Actions workflow** تلقائي لبناء تطبيق Android من كود Python باستخدام Kivy و Buildozer.

## كيفية الاستخدام

### 1. رفع المشروع على GitHub

```bash
git init
git add .
git commit -m "Initial commit with Android app"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY_NAME.git
git push -u origin main
```

### 2. تفعيل GitHub Actions

1. اذهب إلى صفحة repository على GitHub
2. اضغط على تبويب "Actions"
3. ستجد أن الـ workflow يبدأ تلقائياً عند رفع الكود
4. اضغط على "main.yml" لعرض تفاصيل الـ build

### 3. مراقبة عملية البناء

- **الـ workflow يعمل تلقائياً** عند كل push إلى main/master branch
- يمكنك مشاهدة التقدم في تبويب "Actions"
- عملية البناء تستغرق حوالي 15-20 دقيقة (أول مرة)
- البناء اللاحق أسرع (5-10 دقائق)

### 4. تحميل APK

عند انتهاء البناء بنجاح:

1. اذهب إلى تبويب "Actions"
2. اضغط على آخر workflow run
3. اضغط على "android-apk" في Artifacts section
4. اضغط على "Download" لتحميل ملف APK

## تفاصيل الـ Workflow

### المراحل (Stages)

1. **Checkout Code**: تحميل الكود من repository
2. **Setup Python**: تنزيل وإعداد Python 3.12
3. **Install Dependencies**: تنزيل المكتبات المطلوبة (Kivy, KivyMD, Buildozer)
4. **Install Java**: تنزيل Java JDK 11 (مطلوب لـ Android build)
5. **Install Android SDK**: تنزيل Android SDK و NDK
6. **System Dependencies**: تنزيل المكتبات الإضافية للنظام
7. **Build APK**: بناء ملف APK باستخدام Buildozer
8. **Upload Artifact**: رفع APK كملف قابل للتحميل

### المتطلبات التقنية

- **GitHub Account**: مطلوب لرفع الكود
- **Git**: لرفع المشروع
- **GitHub Actions**: مفعل تلقائياً في معظم الـ repositories

## الترتيب في المستودع

تأكد من أن هذه الملفات موجودة في جذر المشروع:

```
your-repo/
├── .github/
│   └── workflows/
│       └── main.yml          # ← ملف GitHub Actions
├── main.py                    # Entry point للتطبيق
├── android_supermarket_app.py # منطق العمل
├── main_android_app.py        # واجهة المستخدم
├── buildozer.spec            # إعدادات البناء
├── requirements_android.txt  # متطلبات Python
└── ANDROID_README.md         # دليل التطبيق
```

## إعدادات مخصصة (اختيارية)

### تغيير اسم التطبيق

في ملف `buildozer.spec`, غيّر:

```ini
[app]
title = اسم تطبيقك الجديد
package.name = اسم_حزمة_التطبيق
package.domain = com.yourcompany
```

### إضافة أيقونة للتطبيق

1. أضف ملف صورة `icon.png` في مجلد المشروع
2. أزل التعليق في `buildozer.spec`:

```ini
#icon.filename = %(source.dir)s/data/icon.png
icon.filename = %(source.dir)s/icon.png
```

### تغيير إصدارات Android

في الـ workflow `main.yml`, يمكنك تغيير:
- Android API Level: غيّر `android-33` إلى إصدار أحدث
- NDK Version: غيّر `25.2.9519653` إلى إصدار أحدث

## استكشاف الأخطاء

### مشاكل شائعة

1. **Build fails with Java errors**
   - تأكد من Java JDK 11 مُثبت
   - تحقق من الـ logs في Actions tab

2. **Android SDK download fails**
   - تحقق من اتصال الإنترنت في الـ GitHub Actions
   - قد تحتاج لإضافة retries

3. **Kivy dependencies conflict**
   - تأكد من أن `requirements_android.txt` محدّث
   - استخدم إصدارات متوافق مع Buildozer

4. **APK size too large**
   - حذف الملفات غير المستخدمة
   - استخدام ProGuard (مستقبلياً)

### 查看 Logs

إذا فشل البناء، اذهب إلى:
1. تبويب "Actions" في GitHub
2. اضغط على الـ workflow المُفشل
3. اضغط على اسم الـ step المفقود
4. شاهد الـ logs المفصّلة

## آلية العمل التلقائي

الـ workflow يعمل في هذه الحالات:

✅ **يُفعل تلقائياً عند:**
- Push إلى main/master branch
- Pull request إلى main/master branch

❌ **لا يُفعل عند:**
- Push إلى feature branches
- تعديل ملفات غير مرتبطة (مثل README.md)

يمكنك تفعيله يدوياً أيضاً من تبويب "Actions".

## ملاحظات مهمة

- **الـ build يستهلك GitHub Actions minutes** (محدود في الحسابات المجانية)
- **APK file يتم حفظه لمدة 30 يوماً** في GitHub Actions
- **بناء APK يستغرق وقتاً طويلاً** في أول مرة (بسبب تحميل Android SDK)
- **البناء اللاحق أسرع** لأن Android SDK محفوظ في cache

## الدعم

إذا واجهت مشاكل، راجع:
1. [Buildozer Documentation](https://buildozer.readthedocs.io/)
2. [GitHub Actions Documentation](https://docs.github.com/en/actions)
3. [Kivy for Android](https://kivy.org/doc/stable/guide/android.html)

---

**تم إنشاء هذا الـ workflow بواسطة MiniMax Agent** 🤖