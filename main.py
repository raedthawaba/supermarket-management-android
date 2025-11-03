#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نقطة دخول تطبيق إدارة السوبر ماركت للأندرويد
تطوير: MiniMax Agent
"""

# استيراد الوحدات الأساسية
import sys
import os

# إضافة المجلد الحالي لمسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق الرئيسي
from main_android_app import SupermarketApp

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    try:
        # إنشاء وتشغيل التطبيق
        app = SupermarketApp()
        app.run()
        
    except Exception as e:
        # تسجيل أي أخطاء
        print(f"خطأ في تشغيل التطبيق: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()