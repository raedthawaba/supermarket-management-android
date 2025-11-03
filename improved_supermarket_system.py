#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة السوبر ماركت المحسن
تطوير: MiniMax Agent
تاريخ: 2025-11-04
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
                        customer_name TEXT NOT NULL,
                        customer_phone TEXT NOT NULL,
                        total_amount REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # جدول تفاصيل الفواتير
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price REAL NOT NULL,
                        total_price REAL NOT NULL,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                        FOREIGN KEY (product_id) REFERENCES products (id)
                    )
                ''')
                
                # إدراج البيانات الافتراضية
                self.insert_default_products(cursor)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def insert_default_products(self, cursor):
        """إدراج المنتجات الافتراضية"""
        default_products = [
            # البقوليات
            ('الرز', 1.5, 'بقوليات', 100),
            ('برغل', 0.5, 'بقوليات', 50),
            ('فاصولياء', 1.0, 'بقوليات', 30),
            ('عدس', 1.5, 'بقوليات', 40),
            ('معكرونة', 2.0, 'بقوليات', 60),
            ('فريكة', 2.0, 'بقوليات', 25),
            ('حمص', 1.0, 'بقوليات', 35),
            ('فول', 1.0, 'بقوليات', 45),
            ('الملح', 1.5, 'بقوليات', 200),
            ('سكر', 1.0, 'بقوليات', 150),
            ('فلفل أسود', 1.5, 'بقوليات', 20),
            ('فلفل أحمر', 1.0, 'بقوليات', 20),
            ('اللوبيا', 1.5, 'بقوليات', 30),
            ('الادمامي', 1.0, 'بقوليات', 25),
            ('القمح', 2.0, 'بقوليات', 40),
            ('الشعير', 1.0, 'بقوليات', 30),
            ('الشوفان', 2.0, 'بقوليات', 25),
            ('الذرة', 1.5, 'بقوليات', 35),
            
            # اللوازم المنزلية
            ('مصفاة', 1.5, 'لوازم منزلية', 50),
            ('صحن', 0.5, 'لوازم منزلية', 100),
            ('كأس', 1.0, 'لوازم منزلية', 80),
            ('ابريق', 1.5, 'لوازم منزلية', 30),
            ('سكين', 2.0, 'لوازم منزلية', 40),
            ('شوك', 2.0, 'لوازم منزلية', 40),
            ('طنجرة', 1.0, 'لوازم منزلية', 25),
            ('سلة', 1.0, 'لوازم منزلية', 45),
            ('ملاعق', 1.5, 'لوازم منزلية', 60),
            ('صينية', 1.0, 'لوازم منزلية', 30),
            ('وعاء الخلط', 1.5, 'لوازم منزلية', 20),
            ('فتاحة علب', 1.0, 'لوازم منزلية', 25),
            ('مقشرة', 1.5, 'لوازم منزلية', 30),
            ('لوح التقطيع', 1.0, 'لوازم منزلية', 20),
            ('حفارة', 2.0, 'لوازم منزلية', 15),
            ('سلة قمامة', 1.0, 'لوازم منزلية', 25),
            ('منفضة', 2.0, 'لوازم منزلية', 20),
            ('اكياس', 1.5, 'لوازم منزلية', 200),
            
            # الأدوات الكهربائية
            ('مكنسة', 30.0, 'أدوات كهربائية', 10),
            ('تلفزيون', 140.0, 'أدوات كهربائية', 5),
            ('غسالة', 300.0, 'أدوات كهربائية', 3),
            ('مكرويف', 40.0, 'أدوات كهربائية', 8),
            ('خلاط', 15.0, 'أدوات كهربائية', 12),
            ('فرن غاز', 110.0, 'أدوات كهربائية', 6),
            ('مقلاة كهرباء', 20.0, 'أدوات كهربائية', 15),
            ('مروحة سقف', 10.0, 'أدوات كهربائية', 20),
            ('مروحة أرضية', 15.0, 'أدوات كهربائية', 18),
            ('تلفزيون 32', 140.0, 'أدوات كهربائية', 8),
            ('تلفزيون 43', 230.0, 'أدوات كهربائية', 5),
            ('فلتر ماء', 130.0, 'أدوات كهربائية', 7),
            ('غسالة أوتو', 430.0, 'أدوات كهربائية', 2),
            ('مكواة', 15.0, 'أدوات كهربائية', 15),
            ('مبردة', 90.0, 'أدوات كهربائية', 4),
        ]
        
        # التحقق من وجود منتجات أولاً
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)",
                default_products
            )
            logger.info(f"Inserted {len(default_products)} default products")
    
    def get_products_by_category(self, category: str) -> List[Tuple]:
        """جلب المنتجات حسب الفئة"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name, price FROM products WHERE category = ? ORDER BY name",
                    (category,)
                )
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching products for category {category}: {e}")
            return []
    
    def save_invoice(self, invoice_data: Dict, items: List[Dict]) -> bool:
        """حفظ الفاتورة في قاعدة البيانات"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # إدراج الفاتورة
                cursor.execute(
                    """INSERT INTO invoices 
                       (invoice_number, customer_name, customer_phone, total_amount) 
                       VALUES (?, ?, ?, ?)""",
                    (invoice_data['number'], invoice_data['customer_name'], 
                     invoice_data['customer_phone'], invoice_data['total'])
                )
                
                invoice_id = cursor.lastrowid
                
                # إدراج تفاصيل الفاتورة
                for item in items:
                    cursor.execute(
                        """INSERT INTO invoice_details 
                           (invoice_id, product_id, quantity, unit_price, total_price) 
                           VALUES (?, ?, ?, ?, ?)""",
                        (invoice_id, item['product_id'], item['quantity'], 
                         item['unit_price'], item['total_price'])
                    )
                
                conn.commit()
                logger.info(f"Invoice {invoice_data['number']} saved successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error saving invoice: {e}")
            return False
    
    def search_invoice(self, invoice_number: str) -> Optional[Dict]:
        """البحث عن فاتورة"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # البحث عن الفاتورة
                cursor.execute(
                    "SELECT * FROM invoices WHERE invoice_number = ?",
                    (invoice_number,)
                )
                invoice = cursor.fetchone()
                
                if not invoice:
                    return None
                
                # جلب تفاصيل الفاتورة
                cursor.execute(
                    """SELECT p.name, id.quantity, id.unit_price, id.total_price 
                       FROM invoice_details id 
                       JOIN products p ON id.product_id = p.id 
                       WHERE id.invoice_id = ?""",
                    (invoice[0],)
                )
                
                items = cursor.fetchall()
                
                return {
                    'invoice': invoice,
                    'items': items
                }
                
        except Exception as e:
            logger.error(f"Error searching invoice: {e}")
            return None

class ProductManager:
    """إدارة المنتجات"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.categories = ['بقوليات', 'لوازم منزلية', 'أدوات كهربائية']
    
    def get_products(self, category: str) -> Dict[int, Dict]:
        """جلب المنتجات لفئة معينة"""
        products = {}
        product_list = self.db_manager.get_products_by_category(category)
        
        for product_id, name, price in product_list:
            products[product_id] = {
                'name': name,
                'price': price,
                'quantity': 0
            }
        
        return products

class InvoiceManager:
    """إدارة الفواتير"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.invoices_dir = Path("invoices")
        self.invoices_dir.mkdir(exist_ok=True)
    
    def generate_invoice_number(self) -> str:
        """إنشاء رقم فاتورة عشوائي"""
        return str(hash(datetime.now().strftime("%Y%m%d%H%M%S")) % 10000 + 1000)
    
    def calculate_total(self, items: Dict[int, int], products: Dict[int, Dict]) -> float:
        """حساب المجموع الكلي"""
        total = 0.0
        for product_id, quantity in items.items():
            if quantity > 0:
                total += quantity * products[product_id]['price']
        return total
    
    def save_invoice_text(self, invoice_data: Dict, items: List[Tuple], total: float) -> bool:
        """حفظ الفاتورة كنص"""
        try:
            # تنظيف اسم الملف
            safe_filename = "".join(
                c for c in invoice_data['number'] if c.isalnum() or c in "-_."
            )
            file_path = self.invoices_dir / f"{safe_filename}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\tسوبر ماركت الخبير يرحب بكم\n")
                f.write("=======================================\n")
                f.write(f"\t رقم الفاتورة: {invoice_data['number']}\n")
                f.write(f"\t الاسم: {invoice_data['customer_name']}\n")
                f.write(f"\t رقم الهاتف: {invoice_data['customer_phone']}\n")
                f.write("=======================================\n")
                f.write(f"\nالسعر\t\tالعدد\t\tالمشتريات\n")
                f.write("=======================================\n")
                
                for item in items:
                    f.write(f"\n{item[1]}\t\t{item[2]}\t\t{item[0]}\n")
                
                f.write("\n......................................\n")
                f.write(f"\n\t{total:.2f} $\t\tالمجموع الكلي\n")
                f.write("\n......................................\n")
            
            logger.info(f"Invoice saved to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving invoice text: {e}")
            return False

class SupermarketGUI:
    """الواجهة الرئيسية للنظام"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # تهيئة المكونات
        self.db_manager = DatabaseManager()
        self.product_manager = ProductManager(self.db_manager)
        self.invoice_manager = InvoiceManager(self.db_manager)
        
        # متغيرات الواجهة
        self.setup_variables()
        
        # بناء الواجهة
        self.create_widgets()
        
        # تحميل البيانات الأولية
        self.load_initial_data()
    
    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.root.title('نظام إدارة السوبر ماركت المحسن')
        self.root.geometry('1400x800')
        self.root.resizable(True, True)
        
        # تحديد الألوان
        self.colors = {
            'primary': '#0B2F3A',
            'secondary': '#0B4C5F',
            'accent': '#DBA901',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
        # إعداد النمط
        style = ttk.Style()
        style.theme_use('clam')
        
        # تخصيص الألوان
        style.configure('Title.TLabel', font=('Tajawal', 16, 'bold'), 
                       foreground='white', background=self.colors['primary'])
        style.configure('Header.TLabel', font=('Tajawal', 12, 'bold'), 
                       foreground='gold', background=self.colors['secondary'])
        style.configure('Product.TLabel', font=('Tajawal', 10), 
                       foreground='white', background=self.colors['secondary'])
    
    def setup_variables(self):
        """إعداد متغيرات الواجهة"""
        # بيانات العميل
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.invoice_number = tk.StringVar()
        
        # الإجماليات
        self.pulses_total = tk.StringVar(value="0.00 $")
        self.household_total = tk.StringVar(value="0.00 $")
        self.electrical_total = tk.StringVar(value="0.00 $")
        self.grand_total = tk.StringVar(value="0.00 $")
        
        # حفظ المنتجات
        self.products_data = {}
        
        # إنشاء متغيرات الكميات لكل فئة
        self.create_quantity_variables()
    
    def create_quantity_variables(self):
        """إنشاء متغيرات الكميات للمنتجات"""
        self.quantity_vars = {}
        
        for category in self.product_manager.categories:
            self.quantity_vars[category] = {}
            products = self.product_manager.get_products(category)
            
            for product_id in products.keys():
                self.quantity_vars[category][product_id] = tk.IntVar(value=0)
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # شريط العنوان
        self.create_title_bar(main_frame)
        
        # إنشاء التبويبات
        self.create_notebook_interface(main_frame)
        
        # لوحة المعلومات والفواتير
        self.create_info_panel(main_frame)
        
        # لوحة التحكم
        self.create_control_panel(main_frame)
    
    def create_title_bar(self, parent):
        """إنشاء شريط العنوان"""
        title_frame = tk.Frame(parent, bg=self.colors['primary'], height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, text='إدارة المشاريع : سوبر ماركت', 
                               style='Title.TLabel')
        title_label.pack(expand=True)
    
    def create_notebook_interface(self, parent):
        """إنشاء واجهة التبويبات"""
        # إطار التبويبات
        notebook_frame = ttk.Frame(parent)
        notebook_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # إنشاء التبويبات
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء تبويب لكل فئة منتجات
        for category in self.product_manager.categories:
            self.create_category_tab(category)
    
    def create_category_tab(self, category: str):
        """إنشاء تبويب فئة المنتجات"""
        # إطار التبويب
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=category)
        
        # عنوان الفئة
        header_label = ttk.Label(tab_frame, text=category, style='Header.TLabel')
        header_label.pack(pady=10)
        
        # إطار المنتجات
        products_frame = ttk.Frame(tab_frame)
        products_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # إنشاء شبكة المنتجات
        self.create_products_grid(products_frame, category)
    
    def create_products_grid(self, parent, category: str):
        """إنشاء شبكة المنتجات"""
        # مسح البيانات القديمة
        for widget in parent.winfo_children():
            widget.destroy()
        
        products = self.product_manager.get_products(category)
        self.products_data[category] = products
        
        # إعداد الشبكة
        row = 0
        col = 0
        max_cols = 2
        
        for product_id, product_info in products.items():
            # إطار المنتج
            product_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
            product_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            # اسم المنتج
            name_label = ttk.Label(product_frame, text=product_info['name'], 
                                  style='Product.TLabel')
            name_label.pack(pady=5)
            
            # السعر
            price_label = ttk.Label(product_frame, text=f"{product_info['price']:.2f} $", 
                                   style='Product.TLabel')
            price_label.pack()
            
            # حقل الكمية
            quantity_frame = ttk.Frame(product_frame)
            quantity_frame.pack(pady=5)
            
            # أزرار التحكم في الكمية
            ttk.Button(quantity_frame, text="-", 
                      command=lambda pid=product_id: self.decrease_quantity(category, pid),
                      width=3).pack(side=tk.LEFT)
            
            quantity_entry = ttk.Entry(quantity_frame, textvariable=self.quantity_vars[category][product_id],
                                      width=5, justify=tk.CENTER)
            quantity_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Button(quantity_frame, text="+", 
                      command=lambda pid=product_id: self.increase_quantity(category, pid),
                      width=3).pack(side=tk.LEFT)
            
            # تحديث الشبكة
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # إعداد أوزان الأعمدة
        for i in range(max_cols):
            parent.grid_columnconfigure(i, weight=1)
    
    def increase_quantity(self, category: str, product_id: int):
        """زيادة الكمية"""
        current_value = self.quantity_vars[category][product_id].get()
        self.quantity_vars[category][product_id].set(current_value + 1)
    
    def decrease_quantity(self, category: str, product_id: int):
        """تقليل الكمية"""
        current_value = self.quantity_vars[category][product_id].get()
        if current_value > 0:
            self.quantity_vars[category][product_id].set(current_value - 1)
    
    def create_info_panel(self, parent):
        """إنشاء لوحة المعلومات"""
        info_frame = ttk.Frame(parent)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # إطار بيانات العميل
        customer_frame = ttk.LabelFrame(info_frame, text="بيانات العميل", padding=10)
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        # حقول بيانات العميل
        ttk.Label(customer_frame, text="اسم العميل:").pack(anchor=tk.W)
        ttk.Entry(customer_frame, textvariable=self.customer_name).pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(customer_frame, text="رقم الهاتف:").pack(anchor=tk.W)
        ttk.Entry(customer_frame, textvariable=self.customer_phone).pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(customer_frame, text="رقم الفاتورة:").pack(anchor=tk.W)
        invoice_frame = ttk.Frame(customer_frame)
        invoice_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Entry(invoice_frame, textvariable=self.invoice_number).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(invoice_frame, text="بحث", command=self.search_invoice).pack(side=tk.RIGHT, padx=(5, 0))
        
        # منطقة عرض الفاتورة
        invoice_frame = ttk.LabelFrame(info_frame, text="فاتورة المبيعات", padding=10)
        invoice_frame.pack(fill=tk.BOTH, expand=True)
        
        # منطقة النص مع شريط التمرير
        self.invoice_text = scrolledtext.ScrolledText(invoice_frame, height=20, width=40,
                                                     font=('Courier', 10))
        self.invoice_text.pack(fill=tk.BOTH, expand=True)
        
        # رسالة ترحيب
        self.show_welcome_message()
    
    def create_control_panel(self, parent):
        """إنشاء لوحة التحكم"""
        control_frame = ttk.LabelFrame(parent, text="لوحة التحكم", padding=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # إطار المجاميع
        totals_frame = ttk.Frame(control_frame)
        totals_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # المجاميع
        totals = [
            ("البقوليات", self.pulses_total),
            ("اللوازم المنزلية", self.household_total),
            ("الأدوات الكهربائية", self.electrical_total),
            ("المجموع الكلي", self.grand_total)
        ]
        
        for i, (label, var) in enumerate(totals):
            row_frame = ttk.Frame(totals_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"{label}:", width=15).pack(side=tk.LEFT)
            ttk.Entry(row_frame, textvariable=var, state="readonly", width=20).pack(side=tk.RIGHT)
        
        # أزرار التحكم
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        ttk.Button(buttons_frame, text="حساب الإجمالي", 
                  command=self.calculate_totals, style='Accent.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="تصدير فاتورة", 
                  command=self.export_invoice).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="مسح الحقول", 
                  command=self.clear_fields).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="إغلاق البرنامج", 
                  command=self.root.quit).pack(fill=tk.X, pady=2)
    
    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        # إنشاء رقم فاتورة عشوائي
        self.invoice_number.set(self.invoice_manager.generate_invoice_number())
    
    def show_welcome_message(self):
        """عرض رسالة الترحيب"""
        self.invoice_text.delete(1.0, tk.END)
        self.invoice_text.insert(tk.END, "\tسوبر ماركت الخبير يرحب بكم\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
        self.invoice_text.insert(tk.END, f"\t رقم الفاتورة: {self.invoice_number.get()}\n")
        self.invoice_text.insert(tk.END, f"\t الاسم: {self.customer_name.get()}\n")
        self.invoice_text.insert(tk.END, f"\t رقم الهاتف: {self.customer_phone.get()}\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
        self.invoice_text.insert(tk.END, "\nالسعر\t\tالعدد\t\tالمشتريات\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
    
    def calculate_totals(self):
        """حساب الإجماليات"""
        try:
            category_totals = {}
            all_items = []
            
            # حساب إجمالي كل فئة
            for category in self.product_manager.categories:
                total = 0.0
                category_items = []
                
                if category in self.products_data:
                    for product_id, product_info in self.products_data[category].items():
                        quantity = self.quantity_vars[category][product_id].get()
                        if quantity > 0:
                            item_total = quantity * product_info['price']
                            total += item_total
                            category_items.append({
                                'product_id': product_id,
                                'name': product_info['name'],
                                'quantity': quantity,
                                'unit_price': product_info['price'],
                                'total_price': item_total
                            })
                            all_items.extend(category_items)
                
                category_totals[category] = total
            
            # تحديث المتغيرات
            self.pulses_total.set(f"{category_totals.get('بقوليات', 0):.2f} $")
            self.household_total.set(f"{category_totals.get('لوازم منزلية', 0):.2f} $")
            self.electrical_total.set(f"{category_totals.get('أدوات كهربائية', 0):.2f} $")
            
            grand_total = sum(category_totals.values())
            self.grand_total.set(f"{grand_total:.2f} $")
            
            logger.info(f"Calculated totals: {category_totals}")
            
        except Exception as e:
            logger.error(f"Error calculating totals: {e}")
            messagebox.showerror("خطأ", "حدث خطأ أثناء حساب الإجماليات")
    
    def export_invoice(self):
        """تصدير الفاتورة"""
        try:
            # التحقق من البيانات المطلوبة
            if not self.customer_name.get().strip():
                messagebox.showerror("خطأ", "يجب إدخال اسم العميل")
                return
            
            if not self.customer_phone.get().strip():
                messagebox.showerror("خطأ", "يجب إدخال رقم هاتف العميل")
                return
            
            # التحقق من وجود منتجات
            has_products = False
            for category in self.product_manager.categories:
                for product_id in self.quantity_vars[category]:
                    if self.quantity_vars[category][product_id].get() > 0:
                        has_products = True
                        break
                if has_products:
                    break
            
            if not has_products:
                messagebox.showerror("خطأ", "يجب اختيار منتج واحد على الأقل")
                return
            
            # إنشاء بيانات الفاتورة
            invoice_data = {
                'number': self.invoice_number.get(),
                'customer_name': self.customer_name.get(),
                'customer_phone': self.customer_phone.get(),
                'total': float(self.grand_total.get().replace(' $', ''))
            }
            
            # جمع المنتجات
            items = []
            for category in self.product_manager.categories:
                if category in self.products_data:
                    for product_id, product_info in self.products_data[category].items():
                        quantity = self.quantity_vars[category][product_id].get()
                        if quantity > 0:
                            items.append({
                                'product_id': product_id,
                                'name': product_info['name'],
                                'quantity': quantity,
                                'unit_price': product_info['price'],
                                'total_price': quantity * product_info['price']
                            })
            
            # حفظ في قاعدة البيانات
            if self.db_manager.save_invoice(invoice_data, items):
                # حفظ كنص
                if self.invoice_manager.save_invoice_text(invoice_data, 
                                                        [(item['name'], item['quantity'], 
                                                          item['unit_price'], item['total_price']) 
                                                         for item in items], 
                                                        invoice_data['total']):
                    
                    # عرض الفاتورة
                    self.display_invoice(invoice_data, items, invoice_data['total'])
                    
                    messagebox.showinfo("نجح", "تم حفظ الفاتورة بنجاح")
                    
                    # إنشاء فاتورة جديدة
                    self.clear_fields()
                    self.invoice_number.set(self.invoice_manager.generate_invoice_number())
                    self.show_welcome_message()
                else:
                    messagebox.showerror("خطأ", "فشل في حفظ الفاتورة كنص")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ الفاتورة في قاعدة البيانات")
                
        except Exception as e:
            logger.error(f"Error exporting invoice: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
    
    def display_invoice(self, invoice_data: Dict, items: List[Dict], total: float):
        """عرض الفاتورة"""
        self.invoice_text.delete(1.0, tk.END)
        
        # رأس الفاتورة
        self.invoice_text.insert(tk.END, "\tسوبر ماركت الخبير يرحب بكم\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
        self.invoice_text.insert(tk.END, f"\t رقم الفاتورة: {invoice_data['number']}\n")
        self.invoice_text.insert(tk.END, f"\t الاسم: {invoice_data['customer_name']}\n")
        self.invoice_text.insert(tk.END, f"\t رقم الهاتف: {invoice_data['customer_phone']}\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
        self.invoice_text.insert(tk.END, "\nالسعر\t\tالعدد\t\tالمشتريات\n")
        self.invoice_text.insert(tk.END, "=======================================\n")
        
        # تفاصيل المنتجات
        for item in items:
            self.invoice_text.insert(tk.END, 
                                   f"\n{item['unit_price']:.2f}\t\t{item['quantity']}\t\t{item['name']}\n")
        
        # إجمالي الفاتورة
        self.invoice_text.insert(tk.END, "\n......................................\n")
        self.invoice_text.insert(tk.END, f"\n\t{total:.2f} $\t\tالمجموع الكلي\n")
        self.invoice_text.insert(tk.END, "\n......................................\n")
    
    def search_invoice(self):
        """البحث عن فاتورة"""
        try:
            invoice_number = self.invoice_number.get().strip()
            if not invoice_number:
                messagebox.showwarning("تحذير", "يجب إدخال رقم الفاتورة")
                return
            
            result = self.db_manager.search_invoice(invoice_number)
            
            if result:
                invoice = result['invoice']
                items = result['items']
                
                # تحديث بيانات العميل
                self.customer_name.set(invoice[2])
                self.customer_phone.set(invoice[3])
                
                # عرض الفاتورة
                self.display_invoice({
                    'number': invoice[1],
                    'customer_name': invoice[2],
                    'customer_phone': invoice[3],
                    'total': invoice[4]
                }, items, invoice[4])
                
                messagebox.showinfo("نجح", "تم العثور على الفاتورة")
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على فاتورة بهذا الرقم")
                
        except Exception as e:
            logger.error(f"Error searching invoice: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ أثناء البحث: {str(e)}")
    
    def clear_fields(self):
        """مسح جميع الحقول"""
        # مسح بيانات العميل
        self.customer_name.set("")
        self.customer_phone.set("")
        
        # مسح الكميات
        for category in self.product_manager.categories:
            for product_id in self.quantity_vars[category]:
                self.quantity_vars[category][product_id].set(0)
        
        # مسح الإجماليات
        self.pulses_total.set("0.00 $")
        self.household_total.set("0.00 $")
        self.electrical_total.set("0.00 $")
        self.grand_total.set("0.00 $")
        
        # عرض رسالة الترحيب
        self.show_welcome_message()
        
        logger.info("All fields cleared")
    
    def run(self):
        """تشغيل التطبيق"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في التطبيق: {str(e)}")

def main():
    """الدالة الرئيسية"""
    try:
        logger.info("Starting Supermarket Management System")
        app = SupermarketGUI()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        messagebox.showerror("خطأ", f"فشل في تشغيل التطبيق: {str(e)}")

if __name__ == "__main__":
    main()