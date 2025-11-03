#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق إدارة السوبر ماركت للأندرويد
تطوير: MiniMax Agent
تاريخ: 2025-11-04
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# إعداد نظام التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager:
    """إدارة قاعدة البيانات"""
    
    def __init__(self, db_path: str = "supermarket.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # جدول المنتجات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        category TEXT NOT NULL,
                        stock INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # جدول الفواتير
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_number TEXT UNIQUE NOT NULL,
                        customer_name TEXT,
                        total_amount REAL DEFAULT 0,
                        payment_method TEXT DEFAULT 'cash',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # جدول تفاصيل الفواتير
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER,
                        product_id INTEGER,
                        product_name TEXT,
                        quantity INTEGER,
                        unit_price REAL,
                        total_price REAL,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                        FOREIGN KEY (product_id) REFERENCES products (id)
                    )
                ''')
                
                # إدخال المنتجات الأساسية إذا لم تكن موجودة
                cursor.execute("SELECT COUNT(*) FROM products")
                if cursor.fetchone()[0] == 0:
                    self._insert_default_products(cursor)
                
                conn.commit()
                logger.info("تم إنشاء قاعدة البيانات بنجاح")
                
        except Exception as e:
            logger.error(f"خطأ في إنشاء قاعدة البيانات: {e}")
            raise
    
    def _insert_default_products(self, cursor):
        """إدخال المنتجات الافتراضية"""
        default_products = [
            # مشروبات
            ('ماء معدني 500ml', 1.0, 'مشروبات', 50),
            ('عصير برتقال 1L', 4.5, 'مشروبات', 30),
            ('كولا 330ml', 2.0, 'مشروبات', 40),
            ('شاي سادة', 8.0, 'مشروبات', 25),
            ('قهوة عربية', 12.0, 'مشروبات', 20),
            ('حليب كامل الدسم 1L', 3.5, 'مشروبات', 35),
            
            # أطعمة
            ('خبز أبيض', 1.5, 'أطعمة', 100),
            ('أرز بسمتي 1kg', 8.0, 'أطعمة', 25),
            ('سكر أبيض 1kg', 6.0, 'أطعمة', 30),
            ('ملح طعام', 2.0, 'أطعمة', 40),
            ('زيت زيتون 500ml', 15.0, 'أطعمة', 15),
            ('دجاج مجمد 1kg', 18.0, 'أطعمة', 20),
            ('لحم بقري 1kg', 35.0, 'أطعمة', 10),
            ('بيض 30 حبة', 12.0, 'أطعمة', 25),
            ('جبنة بيضاء 500g', 8.0, 'أطعمة', 15),
            
            # أغذية الأطفال
            ('حليب بودرة للأطفال 400g', 25.0, 'أطفال', 20),
            ('حفاضات للأطفال M', 15.0, 'أطفال', 30),
            ('مسحوق الغسيل 500g', 6.0, 'أطفال', 25),
            ('شامبو الأطفال 200ml', 8.0, 'أطفال', 15),
            
            # خضار وفواكه
            ('تفاح أحمر 1kg', 5.0, 'خضروات وفواكه', 40),
            ('موز 1kg', 4.0, 'خضروات وفواكه', 35),
            ('برتقال 1kg', 3.5, 'خضروات وفواكه', 30),
            ('طماطم 1kg', 3.0, 'خضروات وفواكه', 25),
            ('خيار 1kg', 2.5, 'خضروات وفواكه', 20),
            ('بطاطس 1kg', 2.0, 'خضروات وفواكه', 30),
            ('بصل 1kg', 2.5, 'خضروات وفواكه', 25),
            ('جزر 1kg', 3.0, 'خضروات وفواكه', 20),
            
            # ألبان
            ('زبدة طبيعية 250g', 12.0, 'ألبان', 15),
            ('زيتون محشي', 8.0, 'ألبان', 20),
            ('مربى الفراولة 250g', 6.0, 'ألبان', 18),
            ('عسل طبيعي 500g', 25.0, 'ألبان', 10),
            
            # حلويات
            ('شكولاتة 100g', 8.0, 'حلويات', 25),
            ('بسكويت بالفانيليا', 5.0, 'حلويات', 30),
            ('كيك جاهز', 15.0, 'حلويات', 10),
            
            # جلي وشامبو
            ('صابون غسيل 150g', 3.0, 'تنظيف', 40),
            ('مسحوق غسيل 2kg', 12.0, 'تنظيف', 20),
            ('معقم شاور gel', 5.0, 'تنظيف', 25),
            
            # مسحوق الشاي والقهوة
            ('شاي أحمر 100g', 7.0, 'مشروبات', 25),
            ('قهوة فورية 100g', 15.0, 'مشروبات', 15),
            ('ماء غاز', 1.5, 'مشروبات', 50),
            
            # خضار مجمدة
            ('لحمة مجمدة 500g', 18.0, 'لحوم مجمدة', 15),
            ('دجاج مجزأ', 16.0, 'لحوم مجمدة', 20),
            
            # سناكس ووجبات خفيفة
            ('رقائق البطاطس', 2.5, 'سناكس', 40),
            ('بسكويت مالح', 3.0, 'سناكس', 35),
            ('لوز محمص', 12.0, 'سناكس', 20),
            
            # مشروبات ساخنة
            ('كافيه موكا', 10.0, 'مشروبات ساخنة', 15),
            ('شاي بالنعناع', 4.0, 'مشروبات ساخنة', 30),
            ('عرقسوس', 8.0, 'مشروبات ساخنة', 10),
        ]
        
        cursor.executemany(
            'INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)',
            default_products
        )
        logger.info(f"تم إدخال {len(default_products)} منتج افتراضي")

class ProductManager:
    """إدارة المنتجات"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_all_products(self) -> List[Dict]:
        """جلب جميع المنتجات"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, price, category, stock
                    FROM products
                    ORDER BY category, name
                ''')
                return [
                    {
                        'id': row[0],
                        'name': row[1],
                        'price': row[2],
                        'category': row[3],
                        'stock': row[4]
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            logger.error(f"خطأ في جلب المنتجات: {e}")
            return []
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """جلب المنتجات حسب الفئة"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, price, category, stock
                    FROM products
                    WHERE category = ?
                    ORDER BY name
                ''', (category,))
                return [
                    {
                        'id': row[0],
                        'name': row[1],
                        'price': row[2],
                        'category': row[3],
                        'stock': row[4]
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            logger.error(f"خطأ في جلب منتجات الفئة {category}: {e}")
            return []
    
    def get_categories(self) -> List[str]:
        """جلب جميع الفئات"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"خطأ في جلب الفئات: {e}")
            return []
    
    def search_products(self, search_term: str) -> List[Dict]:
        """البحث في المنتجات"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, price, category, stock
                    FROM products
                    WHERE name LIKE ?
                    ORDER BY name
                ''', (f'%{search_term}%',))
                return [
                    {
                        'id': row[0],
                        'name': row[1],
                        'price': row[2],
                        'category': row[3],
                        'stock': row[4]
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            logger.error(f"خطأ في البحث: {e}")
            return []

class InvoiceManager:
    """إدارة الفواتير"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_invoice(self, customer_name: str = "", payment_method: str = "cash") -> str:
        """إنشاء فاتورة جديدة"""
        try:
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO invoices (invoice_number, customer_name, payment_method)
                    VALUES (?, ?, ?)
                ''', (invoice_number, customer_name, payment_method))
                conn.commit()
            
            logger.info(f"تم إنشاء فاتورة جديدة: {invoice_number}")
            return invoice_number
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء الفاتورة: {e}")
            raise
    
    def add_item_to_invoice(self, invoice_number: str, product_id: int, quantity: int) -> bool:
        """إضافة منتج للفاتورة"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # جلب معلومات المنتج
                cursor.execute('SELECT id, name, price FROM products WHERE id = ?', (product_id,))
                product = cursor.fetchone()
                if not product:
                    raise ValueError(f"المنتج برقم {product_id} غير موجود")
                
                product_name = product[1]
                unit_price = product[2]
                total_price = unit_price * quantity
                
                # جلب ID الفاتورة
                cursor.execute('SELECT id FROM invoices WHERE invoice_number = ?', (invoice_number,))
                invoice = cursor.fetchone()
                if not invoice:
                    raise ValueError(f"الفاتورة {invoice_number} غير موجودة")
                
                invoice_id = invoice[0]
                
                # إضافة المنتج للفاتورة
                cursor.execute('''
                    INSERT INTO invoice_details (invoice_id, product_id, product_name, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (invoice_id, product_id, product_name, quantity, unit_price, total_price))
                
                # تحديث إجمالي الفاتورة
                cursor.execute('''
                    UPDATE invoices 
                    SET total_amount = (
                        SELECT COALESCE(SUM(total_price), 0) 
                        FROM invoice_details 
                        WHERE invoice_id = ?
                    )
                    WHERE id = ?
                ''', (invoice_id, invoice_id))
                
                conn.commit()
                logger.info(f"تم إضافة {quantity} من {product_name} للفاتورة {invoice_number}")
                return True
                
        except Exception as e:
            logger.error(f"خطأ في إضافة المنتج للفاتورة: {e}")
            return False
    
    def get_invoice_total(self, invoice_number: str) -> float:
        """جلب إجمالي الفاتورة"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT total_amount FROM invoices WHERE invoice_number = ?', (invoice_number,))
                result = cursor.fetchone()
                return result[0] if result else 0.0
        except Exception as e:
            logger.error(f"خطأ في جلب إجمالي الفاتورة: {e}")
            return 0.0
    
    def get_invoice_details(self, invoice_number: str) -> Dict:
        """جلب تفاصيل الفاتورة"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # معلومات الفاتورة
                cursor.execute('''
                    SELECT invoice_number, customer_name, total_amount, payment_method, created_at
                    FROM invoices WHERE invoice_number = ?
                ''', (invoice_number,))
                invoice_info = cursor.fetchone()
                
                if not invoice_info:
                    return {}
                
                # تفاصيل المنتجات
                cursor.execute('''
                    SELECT product_name, quantity, unit_price, total_price
                    FROM invoice_details
                    WHERE invoice_id = (SELECT id FROM invoices WHERE invoice_number = ?)
                ''', (invoice_number,))
                items = cursor.fetchall()
                
                return {
                    'invoice_number': invoice_info[0],
                    'customer_name': invoice_info[1],
                    'total_amount': invoice_info[2],
                    'payment_method': invoice_info[3],
                    'created_at': invoice_info[4],
                    'items': [
                        {
                            'name': item[0],
                            'quantity': item[1],
                            'unit_price': item[2],
                            'total_price': item[3]
                        }
                        for item in items
                    ]
                }
                
        except Exception as e:
            logger.error(f"خطأ في جلب تفاصيل الفاتورة: {e}")
            return {}

# معلومات التطبيق
APP_INFO = {
    'name': 'Supermarket Manager',
    'version': '1.0.0',
    'package': 'com.minimax.supermarket',
    'author': 'MiniMax Agent'
}

# إعدادات التطبيق
APP_CONFIG = {
    'theme': 'Dark',
    'language': 'ar',
    'currency': 'ريال',
    'db_name': 'supermarket.db'
}