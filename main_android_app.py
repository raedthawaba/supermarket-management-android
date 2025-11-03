#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
واجهة تطبيق السوبر ماركت للأندرويد
تطوير: MiniMax Agent
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.resources import resource_find

# استيراد قواعد البيانات والمنطق
import android_supermarket_app as backend


class CustomButton(Button):
    """زر مخصص للتطبيق"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.2, 0.6, 0.8, 1)  # أزرق
        self.color = (1, 1, 1, 1)  # أبيض
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = dp(50)


class ProductCard(BoxLayout):
    """بطاقة المنتج"""
    product_data = ObjectProperty(None)
    
    def __init__(self, product=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.spacing = dp(10)
        
        if product:
            self.product_data = product
            self.build_ui()
    
    def build_ui(self):
        """بناء واجهة بطاقة المنتج"""
        # معلومات المنتج
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # اسم المنتج
        name_label = Label(
            text=self.product_data['name'],
            font_size='16sp',
            size_hint_y=0.4,
            text_size=(None, None),
            halign='right',
            valign='middle'
        )
        info_layout.add_widget(name_label)
        
        # السعر والكمية
        details_label = Label(
            text=f"السعر: {self.product_data['price']:.2f} ريال | المخزون: {self.product_data['stock']}",
            font_size='12sp',
            size_hint_y=0.3,
            color=(0.7, 0.7, 0.7, 1)
        )
        info_layout.add_widget(details_label)
        
        # الفئة
        category_label = Label(
            text=f"الفئة: {self.product_data['category']}",
            font_size='10sp',
            size_hint_y=0.3,
            color=(0.5, 0.5, 0.5, 1)
        )
        info_layout.add_widget(category_label)
        
        self.add_widget(info_layout)
        
        # أزرار التحكم
        buttons_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(5))
        
        # زر الإضافة للسلة
        add_button = Button(
            text='إضافة للسلة',
            size_hint_y=0.5,
            background_color=(0.2, 0.8, 0.2, 1)  # أخضر
        )
        add_button.bind(on_press=lambda x: self.add_to_cart())
        buttons_layout.add_widget(add_button)
        
        # زر التفاصيل
        details_button = Button(
            text='التفاصيل',
            size_hint_y=0.5,
            background_color=(0.8, 0.6, 0.2, 1)  # برتقالي
        )
        details_button.bind(on_press=lambda x: self.show_details())
        buttons_layout.add_widget(details_button)
        
        self.add_widget(buttons_layout)
    
    def add_to_cart(self):
        """إضافة للمنتج للسلة"""
        # سيتم تنفيذها في الشاشة الرئيسية
        pass
    
    def show_details(self):
        """عرض تفاصيل المنتج"""
        content = BoxLayout(orientation='vertical', padding=dp(20))
        
        # معلومات المنتج
        details_text = f"""
اسم المنتج: {self.product_data['name']}
السعر: {self.product_data['price']:.2f} ريال
الفئة: {self.product_data['category']}
المخزون المتاح: {self.product_data['stock']} قطعة
        """
        
        details_label = Label(
            text=details_text,
            font_size='14sp',
            text_size=(Window.width * 0.8, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(details_label)
        
        # زر إغلاق
        close_button = CustomButton(text='إغلاق')
        content.add_widget(close_button)
        
        popup = Popup(
            title='تفاصيل المنتج',
            content=content,
            size_hint=(0.8, 0.6)
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()


class ProductsScreen(GridLayout):
    """شاشة المنتجات"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = 1
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # تهيئة إدارة المنتجات
        self.db_manager = backend.DatabaseManager()
        self.product_manager = backend.ProductManager(self.db_manager)
        
        self.build_ui()
    
    def build_ui(self):
        """بناء واجهة شاشة المنتجات"""
        # شريط البحث والفلترة
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        # حقل البحث
        self.search_input = TextInput(
            hint_text='البحث في المنتجات...',
            size_hint_x=0.7,
            multiline=False
        )
        self.search_input.bind(text=self.on_search_text)
        search_layout.add_widget(self.search_input)
        
        # زر البحث
        search_button = CustomButton(
            text='بحث',
            size_hint_x=0.3
        )
        search_button.bind(on_press=lambda x: self.perform_search())
        search_layout.add_widget(search_button)
        
        self.add_widget(search_layout)
        
        # قائمة الفئات
        categories_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(50),
            spacing=dp(5)
        )
        
        self.categories_buttons = []
        categories = self.product_manager.get_categories()
        
        # زر "الكل"
        all_button = CustomButton(
            text='الكل',
            size_hint_x=None,
            width=dp(80)
        )
        all_button.bind(on_press=lambda x: self.filter_by_category('all'))
        categories_layout.add_widget(all_button)
        self.categories_buttons.append(('all', all_button))
        
        # أزرار الفئات
        for category in categories:
            cat_button = CustomButton(
                text=category[:10],  # اختصار النص
                size_hint_x=None,
                width=dp(100)
            )
            cat_button.bind(on_press=lambda x, c=category: self.filter_by_category(c))
            categories_layout.add_widget(cat_button)
            self.categories_buttons.append((category, cat_button))
        
        self.add_widget(categories_layout)
        
        # قائمة المنتجات
        self.products_list = RecycleView(
            size_hint=(1, 1),
            viewclass='ProductCard'
        )
        self.products_list.layout_manager = RecycleBoxLayout(
            default_size=(None, dp(80)),
            default_size_hint=(1, None),
            size_hint_y=None,
            adaptive_height=True,
            padding=dp(5),
            spacing=dp(5)
        )
        self.add_widget(self.products_list)
        
        # تحميل المنتجات الافتراضية
        self.load_products()
    
    def load_products(self, category='all', search_text=''):
        """تحميل المنتجات"""
        try:
            if search_text:
                products = self.product_manager.search_products(search_text)
            elif category != 'all':
                products = self.product_manager.get_products_by_category(category)
            else:
                products = self.product_manager.get_all_products()
            
            # تحويل المنتجات إلى Cards
            product_cards = []
            for product in products:
                product_cards.append({'product_data': product})
            
            self.products_list.data = product_cards
            logger = backend.logger
            logger.info(f"تم تحميل {len(products)} منتج")
            
        except Exception as e:
            backend.logger.error(f"خطأ في تحميل المنتجات: {e}")
    
    def on_search_text(self, instance, value):
        """معالج تغيير نص البحث"""
        if len(value) >= 3 or len(value) == 0:
            Clock.schedule_once(lambda dt: self.perform_search(), 0.5)
    
    def perform_search(self):
        """تنفيذ البحث"""
        search_text = self.search_input.text
        self.load_products(search_text=search_text)
    
    def filter_by_category(self, category):
        """فلترة حسب الفئة"""
        # إعادة تعيين ألوان الأزرار
        for cat_name, button in self.categories_buttons:
            button.background_color = (0.2, 0.6, 0.8, 1)
        
        # تلوين الزر المحدد
        for cat_name, button in self.categories_buttons:
            if cat_name == category:
                button.background_color = (0.8, 0.2, 0.2, 1)  # أحمر للتحديد
                break
        
        self.load_products(category=category)


class CartItem(BoxLayout):
    """عنصر في السلة"""
    product_data = ObjectProperty(None)
    quantity = ObjectProperty(1)
    
    def __init__(self, product=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(10)
        
        if product:
            self.product_data = product
            self.build_ui()
    
    def build_ui(self):
        """بناء واجهة عنصر السلة"""
        # معلومات المنتج
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        name_label = Label(
            text=self.product_data['name'],
            font_size='14sp',
            size_hint_y=0.6
        )
        info_layout.add_widget(name_label)
        
        price_label = Label(
            text=f"{self.product_data['price']:.2f} ريال",
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.4
        )
        info_layout.add_widget(price_label)
        
        self.add_widget(info_layout)
        
        # تحكم الكمية
        quantity_layout = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=dp(5))
        
        # زر تقليل
        decrease_button = Button(
            text='-',
            size_hint_x=0.3,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        decrease_button.bind(on_press=lambda x: self.change_quantity(-1))
        quantity_layout.add_widget(decrease_button)
        
        # عرض الكمية
        self.quantity_label = Label(
            text=str(self.quantity),
            font_size='16sp',
            size_hint_x=0.4
        )
        quantity_layout.add_widget(self.quantity_label)
        
        # زر زيادة
        increase_button = Button(
            text='+',
            size_hint_x=0.3,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        increase_button.bind(on_press=lambda x: self.change_quantity(1))
        quantity_layout.add_widget(increase_button)
        
        self.add_widget(quantity_layout)
    
    def change_quantity(self, delta):
        """تغيير الكمية"""
        new_quantity = max(0, self.quantity + delta)
        self.quantity = new_quantity
        self.quantity_label.text = str(new_quantity)
        
        # إرسال إشارة للتحديث الإجمالي
        self.dispatch('on_quantity_changed', self.product_data['id'], new_quantity)


class CartScreen(BoxLayout):
    """شاشة السلة"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # قائمة المنتجات في السلة
        self.cart_items = []
        self.total_amount = 0.0
        
        self.build_ui()
    
    def build_ui(self):
        """بناء واجهة السلة"""
        # عنوان السلة
        title_label = Label(
            text='سلة التسوق',
            font_size='24sp',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 0.8, 1)
        )
        self.add_widget(title_label)
        
        # قائمة العناصر
        self.cart_list = RecycleView(
            size_hint=(1, 1),
            viewclass='CartItem'
        )
        self.cart_list.layout_manager = RecycleBoxLayout(
            default_size=(None, dp(60)),
            default_size_hint=(1, None),
            size_hint_y=None,
            adaptive_height=True,
            padding=dp(5),
            spacing=dp(5)
        )
        self.add_widget(self.cart_list)
        
        # إجمالي المبلغ
        self.total_label = Label(
            text='المجموع: 0.00 ريال',
            font_size='18sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.8, 0.2, 1)
        )
        self.add_widget(self.total_label)
        
        # أزرار الإجراءات
        actions_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        # زر إفراغ السلة
        clear_button = CustomButton(
            text='إفراغ السلة',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        clear_button.bind(on_press=lambda x: self.clear_cart())
        actions_layout.add_widget(clear_button)
        
        # زر إتمام الشراء
        checkout_button = CustomButton(
            text='إتمام الشراء',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        checkout_button.bind(on_press=lambda x: self.checkout())
        actions_layout.add_widget(checkout_button)
        
        self.add_widget(actions_layout)
    
    def add_to_cart(self, product):
        """إضافة منتج للسلة"""
        # البحث عن المنتج في السلة
        for item in self.cart_items:
            if item['product']['id'] == product['id']:
                item['quantity'] += 1
                break
        else:
            # منتج جديد
            self.cart_items.append({
                'product': product,
                'quantity': 1
            })
        
        self.update_cart_display()
    
    def remove_from_cart(self, product_id):
        """إزالة منتج من السلة"""
        self.cart_items = [item for item in self.cart_items if item['product']['id'] != product_id]
        self.update_cart_display()
    
    def update_quantity(self, product_id, new_quantity):
        """تحديث كمية منتج"""
        for item in self.cart_items:
            if item['product']['id'] == product_id:
                item['quantity'] = new_quantity
                if new_quantity == 0:
                    self.remove_from_cart(product_id)
                    return
                break
        
        self.update_cart_display()
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        # حساب الإجمالي
        self.total_amount = sum(
            item['product']['price'] * item['quantity']
            for item in self.cart_items
        )
        
        self.total_label.text = f'المجموع: {self.total_amount:.2f} ريال'
        
        # تحديث قائمة العناصر
        cart_data = []
        for item in self.cart_items:
            cart_data.append({
                'product_data': item['product'],
                'quantity': item['quantity']
            })
        
        self.cart_list.data = cart_data
    
    def clear_cart(self):
        """إفراغ السلة"""
        self.cart_items = []
        self.update_cart_display()
    
    def checkout(self):
        """إتمام الشراء"""
        if not self.cart_items:
            self.show_message('السلة فارغة', 'لا توجد منتجات في السلة')
            return
        
        # فتح شاشة إتمام الشراء
        checkout_screen = CheckoutScreen(
            cart_items=self.cart_items,
            total_amount=self.total_amount,
            on_complete=self.on_checkout_complete
        )
        
        # إضافة الشاشة كنافذة منبثقة
        checkout_popup = Popup(
            title='إتمام الشراء',
            content=checkout_screen,
            size_hint=(0.9, 0.8)
        )
        checkout_screen.popup = checkout_popup
        checkout_popup.open()
    
    def on_checkout_complete(self):
        """تم إتمام الشراء"""
        self.clear_cart()
        self.show_message('تم بنجاح!', 'تم إنشاء الفاتورة بنجاح')
    
    def show_message(self, title, message):
        """عرض رسالة"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        message_label = Label(
            text=message,
            font_size='14sp',
            text_size=(Window.width * 0.8, None),
            halign='center'
        )
        content.add_widget(message_label)
        
        ok_button = CustomButton(text='حسناً')
        content.add_widget(ok_button)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()


class CheckoutScreen(BoxLayout):
    """شاشة إتمام الشراء"""
    
    def __init__(self, cart_items=None, total_amount=0, on_complete=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        
        self.cart_items = cart_items or []
        self.total_amount = total_amount
        self.on_complete = on_complete
        self.popup = None
        
        # تهيئة إدارة الفواتير
        self.db_manager = backend.DatabaseManager()
        self.invoice_manager = backend.InvoiceManager(self.db_manager)
        
        self.build_ui()
    
    def build_ui(self):
        """بناء واجهة إتمام الشراء"""
        # عنوان المبلغ
        total_label = Label(
            text=f'إجمالي المبلغ: {self.total_amount:.2f} ريال',
            font_size='20sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.8, 0.2, 1)
        )
        self.add_widget(total_label)
        
        # اسم العميل
        name_label = Label(
            text='اسم العميل (اختياري):',
            font_size='14sp',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(name_label)
        
        self.customer_input = TextInput(
            hint_text='أدخل اسم العميل',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        self.add_widget(self.customer_input)
        
        # طريقة الدفع
        payment_label = Label(
            text='طريقة الدفع:',
            font_size='14sp',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(payment_label)
        
        # أزرار طرق الدفع
        payment_buttons = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10)
        )
        
        self.payment_method = 'cash'
        
        cash_button = CustomButton(
            text='نقدي',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cash_button.bind(on_press=lambda x: self.select_payment('cash', cash_button))
        payment_buttons.add_widget(cash_button)
        
        card_button = CustomButton(text='بطاقة')
        card_button.bind(on_press=lambda x: self.select_payment('card', card_button))
        payment_buttons.add_widget(card_button)
        
        self.add_widget(payment_buttons)
        
        # زر إتمام الشراء
        complete_button = CustomButton(
            text='إتمام الشراء',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        complete_button.bind(on_press=lambda x: self.complete_purchase())
        self.add_widget(complete_button)
    
    def select_payment(self, method, button):
        """تحديد طريقة الدفع"""
        self.payment_method = method
        
        # إعادة تعيين ألوان الأزرار
        for child in button.parent.children:
            if isinstance(child, CustomButton):
                child.background_color = (0.2, 0.6, 0.8, 1)
        
        # تلوين الزر المحدد
        button.background_color = (0.8, 0.2, 0.2, 1)
    
    def complete_purchase(self):
        """إتمام عملية الشراء"""
        try:
            # إنشاء الفاتورة
            invoice_number = self.invoice_manager.create_invoice(
                customer_name=self.customer_input.text.strip(),
                payment_method=self.payment_method
            )
            
            # إضافة المنتجات للفاتورة
            for item in self.cart_items:
                self.invoice_manager.add_item_to_invoice(
                    invoice_number=invoice_number,
                    product_id=item['product']['id'],
                    quantity=item['quantity']
                )
            
            # عرض تأكيد
            self.show_success_message(invoice_number)
            
            if self.on_complete:
                self.on_complete()
            
            if self.popup:
                self.popup.dismiss()
            
        except Exception as e:
            backend.logger.error(f"خطأ في إتمام الشراء: {e}")
            self.show_error_message("حدث خطأ أثناء إتمام الشراء")
    
    def show_success_message(self, invoice_number):
        """عرض رسالة نجاح"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        message_text = f"""تم إتمام الشراء بنجاح!

رقم الفاتورة: {invoice_number}
إجمالي المبلغ: {self.total_amount:.2f} ريال
طريقة الدفع: {self.payment_method}

شكراً لتسوقكم معنا!"""
        
        message_label = Label(
            text=message_text,
            font_size='14sp',
            text_size=(Window.width * 0.8, None),
            halign='center'
        )
        content.add_widget(message_label)
        
        ok_button = CustomButton(text='حسناً')
        content.add_widget(ok_button)
        
        popup = Popup(
            title='تم بنجاح!',
            content=content,
            size_hint=(0.8, 0.6)
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_error_message(self, message):
        """عرض رسالة خطأ"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        error_label = Label(
            text=message,
            font_size='14sp',
            text_size=(Window.width * 0.8, None),
            halign='center',
            color=(0.8, 0.2, 0.2, 1)
        )
        content.add_widget(error_label)
        
        ok_button = CustomButton(text='حسناً')
        content.add_widget(ok_button)
        
        popup = Popup(
            title='خطأ',
            content=content,
            size_hint=(0.8, 0.4)
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()


class MainScreen(BoxLayout):
    """الشاشة الرئيسية للتطبيق"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        self.current_screen = 'products'
        self.cart_screen = None
        
        self.build_ui()
    
    def build_ui(self):
        """بناء الواجهة الرئيسية"""
        # شريط التنقل العلوي
        self.build_navigation_bar()
        
        # المحتوى الرئيسي
        self.main_content = BoxLayout(orientation='vertical')
        self.add_widget(self.main_content)
        
        # شريط التنقل السفلي
        self.build_bottom_navigation()
        
        # عرض شاشة المنتجات افتراضياً
        self.show_screen('products')
    
    def build_navigation_bar(self):
        """بناء شريط التنقل العلوي"""
        nav_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )
        
        # زر القائمة
        menu_button = CustomButton(
            text='☰',
            size_hint_x=None,
            width=dp(60),
            font_size='20sp'
        )
        menu_button.bind(on_press=self.show_menu)
        nav_layout.add_widget(menu_button)
        
        # عنوان التطبيق
        title_label = Label(
            text='نظام إدارة السوبر ماركت',
            font_size='18sp',
            size_hint_x=1,
            color=(0.2, 0.6, 0.8, 1)
        )
        nav_layout.add_widget(title_label)
        
        # زر السلة
        cart_button = CustomButton(
            text='🛒',
            size_hint_x=None,
            width=dp(60),
            font_size='20sp'
        )
        cart_button.bind(on_press=lambda x: self.show_screen('cart'))
        nav_layout.add_widget(cart_button)
        
        self.add_widget(nav_layout)
    
    def build_bottom_navigation(self):
        """بناء شريط التنقل السفلي"""
        bottom_nav = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(5)
        )
        
        # زر المنتجات
        products_button = CustomButton(
            text='المنتجات',
            size_hint_x=1
        )
        products_button.bind(on_press=lambda x: self.show_screen('products'))
        bottom_nav.add_widget(products_button)
        
        # زر السلة
        cart_nav_button = CustomButton(
            text='السلة',
            size_hint_x=1
        )
        cart_nav_button.bind(on_press=lambda x: self.show_screen('cart'))
        bottom_nav.add_widget(cart_nav_button)
        
        # زر الفواتير
        invoices_button = CustomButton(
            text='الفواتير',
            size_hint_x=1
        )
        invoices_button.bind(on_press=lambda x: self.show_screen('invoices'))
        bottom_nav.add_widget(invoices_button)
        
        self.add_widget(bottom_nav)
    
    def show_screen(self, screen_name):
        """عرض شاشة محددة"""
        self.main_content.clear_widgets()
        
        if screen_name == 'products':
            products_screen = ProductsScreen()
            self.main_content.add_widget(products_screen)
            
        elif screen_name == 'cart':
            if not self.cart_screen:
                self.cart_screen = CartScreen()
            self.main_content.add_widget(self.cart_screen)
            
        elif screen_name == 'invoices':
            invoices_screen = InvoicesScreen()
            self.main_content.add_widget(invoices_screen)
        
        self.current_screen = screen_name
    
    def show_menu(self, button):
        """عرض قائمة التنقل"""
        # سيتم تنفيذها لاحقاً
        pass


class InvoicesScreen(BoxLayout):
    """شاشة الفواتير"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # تهيئة إدارة الفواتير
        self.db_manager = backend.DatabaseManager()
        self.invoice_manager = backend.InvoiceManager(self.db_manager)
        
        self.build_ui()
    
    def build_ui(self):
        """بناء واجهة شاشة الفواتير"""
        # عنوان الشاشة
        title_label = Label(
            text='الفواتير',
            font_size='24sp',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 0.8, 1)
        )
        self.add_widget(title_label)
        
        # رسالة عدم توفر الميزة
        content_label = Label(
            text='هذه الميزة قيد التطوير\nستكون متاحة قريباً',
            font_size='16sp',
            text_size=(Window.width * 0.8, None),
            halign='center',
            valign='middle'
        )
        self.add_widget(content_label)


class SupermarketApp(App):
    """تطبيق السوبر ماركت الرئيسي"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "نظام إدارة السوبر ماركت"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
    def build(self):
        # تعيين اتجاه التطبيق من اليمين لليسار للعربية
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # خلفية داكنة
        
        # إنشاء الشاشة الرئيسية
        return MainScreen()


if __name__ == '__main__':
    # تشغيل التطبيق
    SupermarketApp().run()