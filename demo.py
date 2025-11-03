#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تجريبي لاختبار نظام إدارة السوبر ماركت المحسن
Demo script for testing the Improved Supermarket Management System

يمكن استخدام هذا الملف لاختبار النظام بسرعة
This file can be used to quickly test the system
"""

import os
import sys
from pathlib import Path

# إضافة المجلد الحالي للمسار
sys.path.insert(0, str(Path(__file__).parent))

def test_system():
    """اختبار النظام"""
    print("=" * 60)
    print("🛒 نظام إدارة السوبر ماركت المحسن - اختبار النظام")
    print("🛒 Improved Supermarket Management System - System Test")
    print("=" * 60)
    
    # التحقق من وجود Python
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # التحقق من وجود الملفات المطلوبة
    print("\n📋 Checking required files...")
    
    files_to_check = [
        "improved_supermarket_system.py",
        "requirements.txt",
        "README.md"
    ]
    
    all_files_exist = True
    for file_name in files_to_check:
        if Path(file_name).exists():
            print(f"✅ {file_name} - Found")
        else:
            print(f"❌ {file_name} - Missing")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Some required files are missing!")
        return False
    
    print("\n🧪 Testing system components...")
    
    try:
        # اختبار استيراد الوحدات
        print("📦 Testing imports...")
        import tkinter as tk
        import sqlite3
        import json
        import logging
        print("✅ All required modules available")
        
        # اختبار استيراد نظامنا
        print("🏗️  Testing system import...")
        
        # نقوم بتشغيل اختبار سريع دون الواجهة
        print("⚡ Running quick functionality test...")
        
        # اختبار إنشاء قاعدة البيانات
        from improved_supermarket_system import DatabaseManager, ProductManager
        
        # إنشاء قاعدة بيانات مؤقتة للاختبار
        test_db = "test_supermarket.db"
        
        # حذف الملف إذا كان موجوداً
        if Path(test_db).exists():
            Path(test_db).unlink()
        
        db_manager = DatabaseManager(test_db)
        print("✅ Database creation successful")
        
        # اختبار جلب المنتجات
        product_manager = ProductManager(db_manager)
        categories = product_manager.categories
        print(f"✅ Product categories loaded: {len(categories)} categories")
        
        # اختبار جلب منتجات لكل فئة
        total_products = 0
        for category in categories:
            products = product_manager.get_products(category)
            total_products += len(products)
            print(f"📦 {category}: {len(products)} products")
        
        print(f"✅ Total products loaded: {total_products}")
        
        # حذف قاعدة البيانات المؤقتة
        Path(test_db).unlink()
        print("🧹 Test database cleaned up")
        
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام")
        print("🎉 All tests passed! System is ready to use")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def show_usage_instructions():
    """عرض تعليمات الاستخدام"""
    print("\n" + "=" * 60)
    print("📖 تعليمات الاستخدام / Usage Instructions")
    print("=" * 60)
    
    print("""
🚀 لتشغيل النظام / To run the system:
   python improved_supermarket_system.py

📋 الميزات الرئيسية / Main Features:
   ✅ إدارة المنتجات (3 فئات)
   ✅ حساب الإجماليات التلقائي
   ✅ قاعدة بيانات SQLite
   ✅ حفظ واسترجاع الفواتير
   ✅ واجهة عربية محسنة
   ✅ معالجة أخطاء شاملة

🔧 للاختبار / For testing:
   python demo.py

📚 للمزيد من التفاصيل / For more details:
   اقرأ ملف README.md / Read README.md file

⚠️ ملاحظات مهمة / Important Notes:
   - تأكد من وجود Python 3.6+
   - لا حاجة لتثبيت مكتبات إضافية
   - ستحتاج صلاحيات الكتابة في المجلد
""")

def main():
    """الدالة الرئيسية للملف التجريبي"""
    print("مرحباً بك في نظام إدارة السوبر ماركت المحسن!")
    print("Welcome to the Improved Supermarket Management System!")
    
    # تشغيل الاختبار
    if test_system():
        show_usage_instructions()
        
        # سؤال المستخدم عما إذا كان يريد تشغيل النظام
        print("\n" + "=" * 60)
        response = input("هل تريد تشغيل النظام الآن؟ (y/n): ").strip().lower()
        
        if response in ['y', 'yes', 'نعم', 'ن']:
            print("\n🚀 Starting the system...")
            print("Press Ctrl+C to exit")
            print("-" * 40)
            
            try:
                from improved_supermarket_system import main as run_system
                run_system()
            except KeyboardInterrupt:
                print("\n👋 تم إيقاف النظام بواسطة المستخدم")
                print("👋 System stopped by user")
            except Exception as e:
                print(f"\n❌ خطأ في تشغيل النظام: {str(e)}")
                print(f"❌ System error: {str(e)}")
        else:
            print("\n✅ تم حفظ البرنامج للتشغيل لاحقاً")
            print("✅ Program saved for later use")
            print("💡 استخدم الأمر: python improved_supermarket_system.py")
    else:
        print("\n❌ فشل في اختبار النظام")
        print("❌ System test failed")
        print("🔧 تحقق من الملفات والمتطلبات")
        print("🔧 Check files and requirements")

if __name__ == "__main__":
    main()