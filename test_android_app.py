#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لوحدة واجهة المستخدم
"""

import os
import sys

# إضافة المجلد الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """اختبار استيراد الوحدات"""
    print("🧪 اختبار استيراد الوحدات...")
    
    try:
        # اختبار Kivy
        import kivy
        print(f"✅ Kivy {kivy.__version__}")
        
        # اختبار KivyMD
        import kivymd
        print(f"✅ KivyMD {kivymd.__version__}")
        
        # اختبار الوحدات المحلية
        from main_android_app import (
            CustomButton, 
            ProductCard, 
            ProductsScreen,
            CartScreen,
            SupermarketApp
        )
        print("✅ تم استيراد جميع مكونات واجهة المستخدم")
        
        # اختبار الوحدات الخلفية
        from android_supermarket_app import (
            DatabaseManager,
            ProductManager,
            InvoiceManager
        )
        print("✅ تم استيراد جميع وحدات النظام الخلفية")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

def test_ui_components():
    """اختبار مكونات واجهة المستخدم"""
    print("\n🧪 اختبار مكونات واجهة المستخدم...")
    
    try:
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        
        # اختبار إنشاء مكونات أساسية
        layout = BoxLayout(orientation='vertical')
        label = Label(text='اختبار', font_size='16sp')
        button = Button(text='زر اختبار', size_hint_y=None, height=50)
        text_input = TextInput(hint_text='نص اختبار', size_hint_y=None, height=40)
        
        print("✅ تم إنشاء مكونات واجهة المستخدم بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار واجهة المستخدم: {e}")
        return False

def test_database_connection():
    """اختبار اتصال قاعدة البيانات"""
    print("\n🧪 اختبار اتصال قاعدة البيانات...")
    
    try:
        from android_supermarket_app import DatabaseManager, ProductManager
        
        # إنشاء قاعدة بيانات اختبار
        db = DatabaseManager(':memory:')  # قاعدة بيانات في الذاكرة للاختبار
        
        # اختبار إدارة المنتجات
        pm = ProductManager(db)
        categories = pm.get_categories()
        
        print(f"✅ اتصال قاعدة البيانات يعمل - {len(categories)} فئة")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار تطبيق إدارة السوبر ماركت للأندرويد")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_ui_components,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ فشل الاختبار: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 النتائج: {passed}/{total} اختبار نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! التطبيق جاهز للبناء")
        print("\n📱 لبناء APK، استخدم الأمر:")
        print("   buildozer android debug")
    else:
        print("⚠️  هناك بعض المشاكل، يرجى المراجعة")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)