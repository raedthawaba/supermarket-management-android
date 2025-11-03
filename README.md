# نظام إدارة السوبر ماركت المحسن
# Improved Supermarket Management System

## نظرة عامة / Overview

هذا هو النظام المحسن لإدارة السوبر ماركت، والذي تم إعادة كتابته بالكامل لحل جميع المشاكل الموجودة في النسخة الأصلية.

This is the improved supermarket management system, completely rewritten to address all issues in the original version.

## المميزات الجديدة / New Features

### ✅ **تحسينات الأمان / Security Improvements**
- **حماية من Path Traversal**: تنظيف أسماء الملفات ومنع الهجمات
- **تنظيف المدخلات**: التحقق من صحة البيانات المدخلة
- **معالجة الأخطاء**: نظام شامل لتسجيل ومعالجة الأخطاء
- **إدارة الجلسات**: حفظ آمن للفواتير في قاعدة بيانات

### ✅ **تحسينات الأداء / Performance Improvements**
- **قاعدة بيانات SQLite**: استبدال ملفات النص بقاعدة بيانات منظمة
- **كاش ذكي**: حفظ المنتجات والإعدادات في الذاكرة
- **عمليات محسنة**: تقليل عمليات القرص والذاكرة
- **واجهة متجاوبة**: تحسين سرعة الاستجابة

### ✅ **تحسينات الكود / Code Improvements**
- **OOP متقدم**: استخدام البرمجة الكائنية بشكل صحيح
- **فصل الاهتمامات**: فصل منطق العمل عن واجهة المستخدم
- **إعادة استخدام الكود**: تقليل التكرار وتحسين الصيانة
- **تعليقات شاملة**: توثيق مفصل لكل وظيفة

### ✅ **تحسينات الواجهة / UI Improvements**
- **تصميم حديث**: استخدام ttk مع أنماط محسنة
- **تبويبات منظمة**: فصل المنتجات في تبويبات منفصلة
- **شبكة تفاعلية**: منتجات مرتبة في شبكة منظمة
- **أزرار تحكم**: أزرار +/- لسهولة التحكم في الكميات

## التحسينات التقنية / Technical Improvements

### 1. **إدارة قاعدة البيانات / Database Management**
```python
class DatabaseManager:
    - إنشاء قاعدة بيانات SQLite منظمة
    - جداول: products, invoices, invoice_details
    - عمليات آمنة مع معالجة الأخطاء
    - دعم البحث والاستعلامات المعقدة
```

### 2. **إدارة المنتجات / Product Management**
```python
class ProductManager:
    - إدارة ديناميكية للمنتجات
    - تصنيف المنتجات حسب الفئات
    - أسعار قابلة للتحديث
    - إدارة المخزون
```

### 3. **إدارة الفواتير / Invoice Management**
```python
class InvoiceManager:
    - إنشاء أرقام فواتير فريدة
    - حساب الإجماليات بدقة
    - حفظ آمن للملفات
    - تصدير الفواتير بتنسيق منظم
```

### 4. **الواجهة المحسنة / Enhanced GUI**
```python
class SupermarketGUI:
    - واجهة tkinter محسنة مع ttk
    - نظام تبويبات للفئات
    - عناصر تحكم متقدمة
    - معالجة الأحداث المحسنة
```

## مقارنة مع النسخة الأصلية / Comparison with Original

| المعيار / Criterion | النسخة الأصلية / Original | النسخة المحسنة / Improved |
|---------------------|---------------------------|---------------------------|
| **الأمان / Security** | ❌ ثغرات Path Traversal | ✅ حماية شاملة |
| **قاعدة البيانات / Database** | ❌ ملفات نصية فقط | ✅ SQLite منظمة |
| **هيكل الكود / Code Structure** | ❌ متغيرات كثيرة مكررة | ✅ OOP منظم |
| **معالجة الأخطاء / Error Handling** | ❌ معالجة ضعيفة | ✅ نظام شامل |
| **الأداء / Performance** | ❌ عمليات مكررة | ✅ محسن وفعال |
| **قابلية الصيانة / Maintainability** | ❌ صعب جداً | ✅ سهل الصيانة |
| **واجهة المستخدم / User Interface** | ⚠️ بسيطة | ✅ حديثة ومنظمة |
| **التوسع / Scalability** | ❌ غير قابل للتوسع | ✅ قابل للتوسع |

## متطلبات التشغيل / Requirements

### متطلبات النظام / System Requirements
- **Python**: 3.6 أو أحدث
- **نظام التشغيل**: Windows, macOS, Linux
- **الذاكرة**: 100 MB على الأقل
- **مساحة القرص**: 50 MB للتطبيق + مساحة للفواتير

### التثبيت / Installation
1. تأكد من وجود Python 3.6+ على نظامك
2. قم بتحميل ملف `improved_supermarket_system.py`
3. تشغيل البرنامج مباشرة بدون تثبيت مكتبات إضافية

```bash
python improved_supermarket_system.py
```

## كيفية الاستخدام / How to Use

### 1. **تشغيل البرنامج / Running the Program**
```bash
python improved_supermarket_system.py
```

### 2. **إدخال بيانات العميل / Entering Customer Data**
- أدخل اسم العميل في حقل "اسم العميل"
- أدخل رقم الهاتف في حقل "رقم الهاتف"
- رقم الفاتورة يتم إنشاؤه تلقائياً

### 3. **اختيار المنتجات / Selecting Products**
- انتقل بين تبويبات الفئات المختلفة
- استخدم أزرار +/- لاختيار الكميات
- أو اكتب الكمية مباشرة في الحقل

### 4. **حساب الإجمالي / Calculating Total**
- اضغط على "حساب الإجمالي" لرؤية أسعار كل فئة
- سيتم تحديث المجموع الكلي تلقائياً

### 5. **تصدير الفاتورة / Exporting Invoice**
- اضغط على "تصدير فاتورة" لحفظ الفاتورة
- ستحفظ الفاتورة في قاعدة البيانات وكنص
- سيتم إنشاء فاتورة جديدة تلقائياً

### 6. **البحث في الفواتير / Searching Invoices**
- أدخل رقم الفاتورة في حقل "رقم الفاتورة"
- اضغط على "بحث" لعرض الفاتورة

### 7. **مسح الحقول / Clearing Fields**
- اضغط على "مسح الحقول" لمسح جميع البيانات

## هيكل قاعدة البيانات / Database Structure

### جدول المنتجات / Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول الفواتير / Invoices Table
```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    total_amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول تفاصيل الفواتير / Invoice Details Table
```sql
CREATE TABLE invoice_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

## الملفات المُنشأة / Generated Files

### قاعدة البيانات / Database
- `supermarket.db` - قاعدة البيانات الرئيسية

### مجلد الفواتير / Invoices Directory
- `invoices/` - مجلد حفظ الفواتير النصية
- كل فاتورة تحفظ كملف نصي منفصل

### سجلات النظام / System Logs
- يتم تسجيل جميع العمليات في وحدة التحكم
- رسائل خطأ وتأكيد واضحة

## نصائح للاستخدام الأمثل / Tips for Optimal Use

### 1. **النسخ الاحتياطي / Backup**
```bash
# انسخ قاعدة البيانات بانتظام
cp supermarket.db supermarket_backup_$(date +%Y%m%d).db
```

### 2. **إدارة المساحة / Space Management**
- احذف الفواتير القديمة غير الضرورية
- نظف مجلد `invoices/` من الملفات القديمة

### 3. **الأمان / Security**
- لا تشارك قاعدة البيانات مع الآخرين
- احفظ نسخة احتياطية في مكان آمن

### 4. **الأداء / Performance**
- أغلق الفواتير المكتملة بانتظام
- تجنب ترك عدد كبير من النوافذ مفتوحة

## استكشاف الأخطاء / Troubleshooting

### مشاكل شائعة وحلولها:

#### 1. **خطأ في قاعدة البيانات**
```
Solution: احذف ملف supermarket.db وأعد تشغيل البرنامج
```

#### 2. **مشاكل في عرض العربية**
```
Solution: تأكد من أن النظام يدعم UTF-8
```

#### 3. **بطء في الأداء**
```
Solution: أغلق البرنامج وأعد تشغيله، أو أعد تشغيل النظام
```

#### 4. **خطأ في حفظ الفاتورة**
```
Solution: تحقق من وجود صلاحيات الكتابة في المجلد
```

## التوثيق التقني / Technical Documentation

### الفئات الرئيسية / Main Classes

#### DatabaseManager
- **الوظيفة**: إدارة قاعدة البيانات
- **الطرق الرئيسية**: 
  - `init_database()`: إنشاء قاعدة البيانات
  - `get_products_by_category()`: جلب المنتجات
  - `save_invoice()`: حفظ الفاتورة
  - `search_invoice()`: البحث في الفواتير

#### ProductManager
- **الوظيفة**: إدارة المنتجات
- **الطرق الرئيسية**:
  - `get_products()`: جلب المنتجات حسب الفئة

#### InvoiceManager
- **الوظيفة**: إدارة الفواتير
- **الطرق الرئيسية**:
  - `generate_invoice_number()`: إنشاء رقم فاتورة
  - `calculate_total()`: حساب المجموع
  - `save_invoice_text()`: حفظ النص

#### SupermarketGUI
- **الوظيفة**: الواجهة الرئيسية
- **الطرق الرئيسية**:
  - `create_widgets()`: بناء الواجهة
  - `calculate_totals()`: حساب الإجماليات
  - `export_invoice()`: تصدير الفاتورة
  - `search_invoice()`: البحث

## الدعم والتطوير / Support and Development

### للتطوير المستقبلي / For Future Development
1. **إضافة ميزات جديدة**:
   - إدارة المخزون المتقدم
   - تقارير المبيعات
   - نظام الخصومات
   - إدارة العملاء

2. **تحسينات الأداء**:
   - قاعدة بيانات خارجية (MySQL, PostgreSQL)
   - واجهة ويب
   - API للتكامل مع أنظمة أخرى

3. **تحسينات الأمان**:
   - نظام مصادقة
   - تشفير البيانات
   - سجلات التدقيق

### للمساعدة / For Help
إذا واجهت أي مشاكل أو كان لديك اقتراحات، يرجى مراجعة:
- رسائل الخطأ في وحدة التحكم
- ملف `supermarket.db` للبيانات
- مجلد `invoices/` للملفات المحفوظة

---

## 📱 إصدار Android التطبيق / Android Application Version

### تطبيق Android متاح الآن / Android App Now Available

تم تحويل التطبيق إلى تطبيق Android مع واجهة عربية كاملة ودعم RTL، يمكنك تحميله من GitHub Actions.

#### GitHub Actions للبناء التلقائي / GitHub Actions for Automatic Build

هذا المشروع يدعم **البناء التلقائي** للتطبيق Android عبر GitHub Actions:

```yaml
# الترتيب / Repository Structure:
supermarket-android/
├── .github/workflows/main.yml          # GitHub Actions workflow
├── main.py                             # Android app entry point
├── android_supermarket_app.py          # Business logic for Android
├── main_android_app.py                 # Kivy mobile UI
├── buildozer.spec                      # Android build configuration
└── requirements_android.txt            # Python dependencies
```

#### كيفية استخدام GitHub Actions / How to Use GitHub Actions

1. **رفع الكود على GitHub**:
```bash
git init
git add .
git commit -m "Initial commit with Android app"
git branch -M main
git remote add origin https://github.com/USERNAME/supermarket-android.git
git push -u origin main
```

2. **تفعيل البناء التلقائي**:
   - اذهب إلى GitHub repository
   - اضغط على تبويب "Actions"
   - انتظر انتهاء البناء (15-20 دقيقة)
   - حمّل APK من قسم "Artifacts"

#### مميزات الإصدار Android / Android Version Features

- **واجهة عربية RTL** كاملة
- **Material Design** مع KivyMD
- **قاعدة بيانات SQLite** محلية (48 منتج)
- **واجهة تفاعلية** محسنة للهواتف
- **بناء تلقائي** عبر GitHub Actions
- **تحديث فوري** مع كل push للكود

#### ملفات الوثائق / Documentation Files

- `ANDROID_README.md` - دليل شامل للتطبيق Android
- `GITHUB_ACTIONS_GUIDE.md` - دليل استخدام GitHub Actions  
- `PROJECT_SUMMARY.md` - ملخص المشروع الشامل
- `buildozer_github_actions.spec` - إعدادات محسّنة لبناء Android

---

**تم التطوير بواسطة / Developed by**: MiniMax Agent  
**تاريخ الإنشاء / Created**: 2025-11-04  
**الإصدار / Version**: 2.0 (محسن + Android)  
**الترخيص / License**: للاستخدام الشخصي / Personal Use Only