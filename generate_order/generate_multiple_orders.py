#!/usr/bin/env python3
"""
生成多种类型订单图片的脚本
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime, timedelta
import json

def get_chinese_font(size):
    """
    Get a font that supports Chinese characters, trying multiple possible font paths
    """
    font_paths = [
        # Common Chinese fonts on macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Menlo.ttc",
        # Generic Chinese font names
        "Arial Unicode.ttf",
        "SimHei.ttf",
        "SimSun.ttf",
        "Microsoft YaHei.ttf",
        "STHeiti.ttc",
        "STSong.ttc",
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            continue
    
    # If specific fonts are not found, return default font
    try:
        return ImageFont.truetype("Arial.ttf", size)
    except:
        return ImageFont.load_default()

def generate_simple_order(order_id, output_path):
    """
    生成简单格式的订单
    """
    width, height = 800, 600
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(24)
    font_header = get_chinese_font(18)
    font_normal = get_chinese_font(16)
    
    # Generate mock data
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    customer_name = f"Customer {random.randint(1000, 9999)}"
    email = f"customer{random.randint(1000, 9999)}@email.com"
    phone = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    address = f"{random.randint(100, 9999)} Main St, City {random.randint(1, 100)}, State"
    
    # Collect order data for JSON
    order_data = {
        "order_id": order_id,
        "date": order_date,
        "customer": customer_name,
        "email": email,
        "phone": phone,
        "address": address,
        "products": [],
        "total": 0
    }
    
    # Title
    title = f"ORDER #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, font=font_title, fill=(0, 0, 0))
    
    # Order info
    order_info = [
        ("Order ID:", order_id),
        ("Date:", order_date),
        ("Customer:", customer_name),
        ("Email:", email),
        ("Phone:", phone),
        ("Address:", address),
    ]
    
    y_pos = 80
    for label, value in order_info:
        draw.text((50, y_pos), f"{label}", font=font_normal, fill=(0, 0, 0))
        draw.text((200, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 30
    
    # Simple product table
    y_pos += 20
    draw.text((50, y_pos), "PRODUCTS:", font=font_header, fill=(0, 0, 0))
    y_pos += 30
    
    products = [
        (f"Product {random.randint(100, 999)}", random.randint(1, 5), round(random.uniform(10, 500), 2)),
        (f"Item {random.randint(100, 999)}", random.randint(1, 3), round(random.uniform(5, 200), 2)),
        (f"Good {random.randint(100, 999)}", random.randint(2, 10), round(random.uniform(15, 300), 2)),
    ]
    
    total = 0
    for product in products:
        name, qty, price = product
        subtotal = qty * price
        total += subtotal
        order_data["products"].append({
            "name": name,
            "quantity": qty,
            "unit_price": price,
            "subtotal": subtotal
        })
        draw.text((50, y_pos), f"- {name}", font=font_normal, fill=(0, 0, 0))
        draw.text((300, y_pos), f"Qty: {qty}", font=font_normal, fill=(0, 0, 0))
        draw.text((400, y_pos), f"${price:.2f}", font=font_normal, fill=(0, 0, 0))
        draw.text((500, y_pos), f"${subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # Total
    order_data["total"] = total
    y_pos += 20
    draw.text((400, y_pos), "TOTAL:", font=font_header, fill=(0, 0, 0))
    draw.text((500, y_pos), f"${total:.2f}", font=font_header, fill=(0, 0, 0))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # Write JSON data
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"Simple order generated: {output_path} and {json_path}")
    return order_data

def generate_detailed_order(order_id, output_path):
    """
    生成详细表格格式的订单
    """
    width, height = 900, 800
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(28)
    font_header = get_chinese_font(18)
    font_normal = get_chinese_font(16)
    font_company = get_chinese_font(20)
    font_large = get_chinese_font(24)
    
    # Generate mock data
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    customer_name = f"Customer {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"
    phone = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    shipping_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Maple'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}, {random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])}"
    shipping_method = random.choice(["Standard", "Express", "Overnight", "Free Shipping"])
    payment_method = random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"])
    status = random.choice(["Processing", "Shipped", "Delivered", "Cancelled"])
    
    # Collect order data for JSON
    order_data = {
        "order_id": order_id,
        "customer_name": customer_name,
        "phone": phone,
        "shipping_address": shipping_address,
        "order_date": order_date,
        "shipping_method": shipping_method,
        "payment_method": payment_method,
        "status": status,
        "products": [],
        "subtotal": 0,
        "shipping": 0,
        "tax": 0,
        "grand_total": 0
    }
    
    # Header banner
    draw.rectangle([0, 0, width, 60], fill=(70, 130, 180), outline=(70, 130, 180))
    draw.text((30, 18), "SHOP NAME - ORDER SYSTEM", font=font_company, fill=(255, 255, 255))
    
    # Title
    title = f"DETAILED ORDER #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, font=font_title, fill=(0, 0, 0))
    
    # Separator line
    draw.line([(50, 130), (width-50, 130)], fill=(100, 100, 100), width=1)
    
    # Order information
    order_info = [
        ("Order ID:", order_id),
        ("Customer Name:", customer_name),
        ("Phone:", phone),
        ("Shipping Address:", shipping_address),
        ("Order Date:", order_date),
        ("Shipping Method:", shipping_method),
        ("Payment Method:", payment_method),
        ("Status:", status)
    ]
    
    y_pos = 150
    for i, (label, value) in enumerate(order_info):
        # Alternating background color
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(245, 245, 245))
        
        draw.text((70, y_pos), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((250, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 35
    
    # Table header
    y_pos += 30
    header_y = y_pos
    
    # Table column widths
    col1_width = 60   # Item No.
    col2_width = 320  # Product Name
    col3_width = 120  # Unit Price
    col4_width = 100  # Quantity
    col5_width = 150  # Subtotal
    
    # Draw header background
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(230, 240, 250), outline=(100, 100, 100), width=1)
    
    # Draw headers
    draw.text((50 + 20, y_pos + 10), "No.", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + 20, y_pos + 10), "Product Name", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + 30, y_pos + 10), "Unit Price($)", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + 35, y_pos + 10), "Qty", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + col4_width + 40, y_pos + 10), "Subtotal($)", font=font_header, fill=(30, 30, 30))
    
    y_pos += 40
    
    # Table content
    product_names = [
        "Wireless Headphones",
        "Smart Watch Series 5",
        "Bluetooth Speaker",
        "Laptop Stand",
        "USB-C Cable 2m",
        "Phone Case",
        "Power Bank 20000mAh",
        "Wireless Charger",
        "Noise Cancelling Earbuds",
        "Gaming Mouse RGB"
    ]
    
    products = []
    num_products = random.randint(3, 7)
    for i in range(num_products):
        name = random.choice(product_names)
        qty = random.randint(1, 5)
        price = round(random.uniform(10, 500), 2)
        subtotal = qty * price
        products.append((str(i+1), name, f"{price:.2f}", str(qty), f"{subtotal:.2f}"))
        order_data["products"].append({
            "item_no": str(i+1),
            "product_name": name,
            "unit_price": price,
            "quantity": qty,
            "subtotal": subtotal
        })
    
    row_height = 40
    for i, product in enumerate(products):
        # Calculate current row Y coordinate
        current_y = y_pos + i * row_height
        
        # Alternating row background color
        if i % 2 == 0:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(250, 250, 250))
        else:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(255, 255, 255))
        
        # Draw border
        draw.rectangle([50, current_y, width-50, current_y + row_height], outline=(200, 200, 200), width=1)
        
        # Item number column
        draw.text((50 + 20, current_y + 12), product[0], font=font_normal, fill=(0, 0, 0))
        
        # Product name column
        draw.text((50 + col1_width + 20, current_y + 12), product[1], font=font_normal, fill=(50, 50, 50))
        
        # Unit price column
        draw.text((50 + col1_width + col2_width + 40, current_y + 12), product[2], font=font_normal, fill=(0, 0, 0))
        
        # Quantity column
        draw.text((50 + col1_width + col2_width + col3_width + 40, current_y + 12), product[3], font=font_normal, fill=(0, 0, 0))
        
        # Subtotal column
        draw.text((50 + col1_width + col2_width + col3_width + col4_width + 50, current_y + 12), product[4], font=font_normal, fill=(0, 0, 0))
    
    # Bottom statistics
    total_y = y_pos + len(products) * row_height + 20
    
    # Separator line
    draw.line([(50, total_y-10), (width-50, total_y-10)], fill=(100, 100, 100), width=1)
    
    # Calculate totals
    subtotal = sum(float(p[4]) for p in products)
    shipping = round(random.uniform(0, 50), 2) if subtotal < 200 else 0  # Free shipping for orders over $200
    tax_rate = 0.08  # 8% tax
    tax = round(subtotal * tax_rate, 2)
    grand_total = subtotal + shipping + tax
    
    # Update order data with totals
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["grand_total"] = grand_total
    
    # Subtotal
    draw.text((width - 250, total_y), "Subtotal:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"${subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Shipping
    total_y += 35
    draw.text((width - 250, total_y), "Shipping:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"${shipping:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Tax
    total_y += 35
    draw.text((width - 250, total_y), "Tax (8%):", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"${tax:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Grand total
    total_y += 35
    draw.text((width - 250, total_y), "Grand Total:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"${grand_total:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Total amount (large display)
    total_y += 50
    draw.text((width - 250, total_y), f"AMOUNT DUE: ${grand_total:.2f}", font=font_large, fill=(220, 20, 60))
    
    # Footer
    total_y += 60
    draw.text((70, total_y), f"Thank you for your business! Order #{order_id}", font=font_normal, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # Write JSON data
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"Detailed order generated: {output_path} and {json_path}")
    return order_data

def generate_invoice_order(order_id, output_path):
    """
    生成发票格式的订单
    """
    width, height = 850, 700
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(30)
    font_header = get_chinese_font(18)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_large = get_chinese_font(24)
    
    # Invoice header
    draw.rectangle([0, 0, width, 80], fill=(50, 50, 150), outline=(50, 50, 150))
    draw.text((50, 20), "INVOICE", font=font_title, fill=(255, 255, 255))
    draw.text((width - 200, 25), f"Invoice #: {order_id}", font=font_normal, fill=(255, 255, 255))
    
    # Company info
    company_info = [
        "ACME Corporation",
        "123 Business Ave",
        "Suite 100",
        "New York, NY 10001",
        "Phone: (555) 123-4567",
        "Email: billing@acme.com"
    ]
    
    y_pos = 100
    for info in company_info:
        draw.text((50, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # Bill to section
    y_pos += 20
    draw.text((500, y_pos), "BILL TO:", font=font_header, fill=(0, 0, 0))
    y_pos += 25
    
    # Generate mock data
    invoice_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    po_number = f"PO-{random.randint(10000, 99999)}"
    client_name = f"Client {random.randint(1000, 9999)}"
    client_address_line1 = f"{random.randint(100, 9999)} Client Rd"
    client_address_city_state_zip = f"{random.choice(['San Francisco', 'Seattle', 'Boston', 'Miami', 'Denver'])}, {random.choice(['CA', 'WA', 'MA', 'FL', 'CO'])} {random.randint(10001, 99999)}"
    contact_person = f"{random.choice(['John', 'Jane', 'Robert', 'Emily', 'Michael'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis'])}"
    client_email = f"client{random.randint(1000, 9999)}@client.com"
    
    # Collect order data for JSON
    order_data = {
        "invoice_id": order_id,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "terms": "Net 30 Days",
        "po_number": po_number,
        "company_info": {
            "name": "ACME Corporation",
            "address": "123 Business Ave, Suite 100, New York, NY 10001",
            "phone": "(555) 123-4567",
            "email": "billing@acme.com"
        },
        "bill_to": {
            "name": client_name,
            "address": f"{client_address_line1}, {client_address_city_state_zip}",
            "contact_person": contact_person,
            "email": client_email
        },
        "items": [],
        "subtotal": 0,
        "tax_rate": 0.1,
        "tax_amount": 0,
        "grand_total": 0
    }
    
    bill_to = [
        client_name,
        client_address_line1,
        client_address_city_state_zip,
        f"Contact: {contact_person}",
        f"Email: {client_email}"
    ]
    
    for info in bill_to:
        draw.text((500, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 20
    
    # Invoice details
    y_pos += 30
    invoice_details = [
        ("Invoice Date:", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")),
        ("Due Date:", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")),
        ("Terms:", "Net 30 Days"),
        ("PO Number:", f"PO-{random.randint(10000, 99999)}")
    ]
    
    for label, value in invoice_details:
        draw.text((500, y_pos), f"{label}", font=font_normal, fill=(0, 0, 0))
        draw.text((650, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # Table header
    y_pos += 30
    header_y = y_pos
    
    # Table column widths
    col1_width = 50   # #
    col2_width = 300  # Description
    col3_width = 120  # Rate
    col4_width = 100  # Qty
    col5_width = 130  # Amount
    
    # Draw header background
    draw.rectangle([50, y_pos, width-50, y_pos + 35], fill=(240, 240, 240), outline=(100, 100, 100), width=1)
    
    # Draw headers
    draw.text((50 + 15, y_pos + 10), "#", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + 15, y_pos + 10), "Description", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + 25, y_pos + 10), "Rate ($)", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + 30, y_pos + 10), "Qty", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + col4_width + 30, y_pos + 10), "Amount ($)", font=font_header, fill=(30, 30, 30))
    
    y_pos += 35
    
    # Invoice items
    descriptions = [
        "Web Development Services",
        "Software License Annual",
        "Cloud Hosting Monthly",
        "Technical Support Hourly",
        "Consulting Services",
        "Data Migration Service",
        "Training Session",
        "Maintenance Contract"
    ]
    
    items = []
    num_items = random.randint(3, 6)
    for i in range(num_items):
        desc = random.choice(descriptions)
        rate = round(random.uniform(50, 500), 2)
        qty = random.randint(1, 10)
        amount = rate * qty
        items.append((str(i+1), desc, f"{rate:.2f}", str(qty), f"{amount:.2f}"))
        order_data["items"].append({
            "number": str(i+1),
            "description": desc,
            "rate": rate,
            "quantity": qty,
            "amount": amount
        })
    
    row_height = 35
    for i, item in enumerate(items):
        # Calculate current row Y coordinate
        current_y = y_pos + i * row_height
        
        # Alternating row background color
        if i % 2 == 0:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(250, 250, 250))
        else:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(255, 255, 255))
        
        # Draw border
        draw.rectangle([50, current_y, width-50, current_y + row_height], outline=(200, 200, 200), width=1)
        
        # Number column
        draw.text((50 + 15, current_y + 10), item[0], font=font_normal, fill=(0, 0, 0))
        
        # Description column
        draw.text((50 + col1_width + 15, current_y + 10), item[1], font=font_small, fill=(50, 50, 50))
        
        # Rate column
        draw.text((50 + col1_width + col2_width + 30, current_y + 10), item[2], font=font_normal, fill=(0, 0, 0))
        
        # Quantity column
        draw.text((50 + col1_width + col2_width + col3_width + 35, current_y + 10), item[3], font=font_normal, fill=(0, 0, 0))
        
        # Amount column
        draw.text((50 + col1_width + col2_width + col3_width + col4_width + 40, current_y + 10), item[4], font=font_normal, fill=(0, 0, 0))
    
    # Totals section
    total_y = y_pos + len(items) * row_height + 30
    
    # Subtotal
    subtotal = sum(float(item[4]) for item in items)
    draw.text((width - 200, total_y), "Subtotal:", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Tax
    total_y += 30
    tax_rate = 0.1  # 10% tax
    tax_amount = round(subtotal * tax_rate, 2)
    draw.text((width - 200, total_y), f"Tax ({int(tax_rate*100)}%):", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${tax_amount:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Total
    total_y += 40
    grand_total = subtotal + tax_amount
    draw.text((width - 200, total_y), "TOTAL:", font=font_large, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${grand_total:.2f}", font=font_large, fill=(0, 0, 0))
    
    # Payment terms
    total_y += 60
    draw.text((50, total_y), "Payment Terms: Net 30 days. Late payments subject to 1.5% monthly service charge.", font=font_small, fill=(100, 100, 100))
    total_y += 25
    draw.text((50, total_y), "Make checks payable to ACME Corporation. Questions? Call (555) 123-4567.", font=font_small, fill=(100, 100, 100))
    
    # Calculate totals and update order data
    subtotal = sum(float(item[4]) for item in items)
    tax_rate = 0.1  # 10% tax
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = subtotal + tax_amount
    
    # Update order data with totals
    order_data["subtotal"] = subtotal
    order_data["tax_rate"] = tax_rate
    order_data["tax_amount"] = tax_amount
    order_data["grand_total"] = grand_total
    
    # Continue drawing totals on image
    total_y = y_pos + len(items) * row_height + 30
    
    # Subtotal
    draw.text((width - 200, total_y), "Subtotal:", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Tax
    total_y += 30
    draw.text((width - 200, total_y), f"Tax ({int(tax_rate*100)}%):", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${tax_amount:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # Total
    total_y += 40
    draw.text((width - 200, total_y), "TOTAL:", font=font_large, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"${grand_total:.2f}", font=font_large, fill=(0, 0, 0))
    
    # Payment terms
    total_y += 60
    draw.text((50, total_y), "Payment Terms: Net 30 days. Late payments subject to 1.5% monthly service charge.", font=font_small, fill=(100, 100, 100))
    total_y += 25
    draw.text((50, total_y), "Make checks payable to ACME Corporation. Questions? Call (555) 123-4567.", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # Write JSON data
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"Invoice order generated: {output_path} and {json_path}")
    return order_data

def generate_condensed_order(order_id, output_path):
    """
    生成紧凑型订单
    """
    width, height = 700, 500
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(22)
    font_header = get_chinese_font(16)
    font_normal = get_chinese_font(14)
    font_small = get_chinese_font(12)
    
    # Generate mock data
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    customer_id = f"CUST-{random.randint(10000, 99999)}"
    status = random.choice(['Completed', 'Processing', 'Shipped', 'Delivered'])
    
    # Collect order data for JSON
    order_data = {
        "order_id": order_id,
        "date": order_date,
        "customer_id": customer_id,
        "status": status,
        "items": [],
        "subtotal": 0,
        "shipping": 0,
        "tax": 0,
        "total": 0
    }
    
    # Title
    title = f"ORDER SUMMARY #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, font=font_title, fill=(0, 0, 0))
    
    # Basic info
    y_pos = 60
    basic_info = [
        f"Date: {order_date}",
        f"Customer ID: {customer_id}",
        f"Status: {status}"
    ]
    
    for info in basic_info:
        draw.text((50, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # Product list
    y_pos += 15
    draw.text((50, y_pos), "ITEMS:", font=font_header, fill=(0, 0, 0))
    y_pos += 25
    
    products = [
        (f"Item {random.randint(100, 999)}", random.randint(1, 3), round(random.uniform(10, 100), 2)),
        (f"Product {random.randint(100, 999)}", random.randint(1, 2), round(random.uniform(20, 200), 2)),
        (f"Accessory {random.randint(100, 999)}", random.randint(2, 5), round(random.uniform(5, 50), 2)),
    ]
    
    total = 0
    for product in products:
        name, qty, price = product
        subtotal = qty * price
        total += subtotal
        order_data["items"].append({
            "name": name,
            "quantity": qty,
            "unit_price": price,
            "subtotal": subtotal
        })
        draw.text((50, y_pos), f"• {name} x{qty}", font=font_normal, fill=(0, 0, 0))
        draw.text((width - 150, y_pos), f"${subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
        y_pos += 22
    
    # Calculate totals
    subtotal = total
    shipping = round(random.uniform(0, 15), 2)
    tax = round(subtotal * 0.08, 2)
    grand_total = round(subtotal + shipping + tax, 2)
    
    # Update order data with totals
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["total"] = grand_total
    
    # Summary
    y_pos += 25
    draw.rectangle([50, y_pos, width-50, y_pos + 100], outline=(150, 150, 150), width=1)
    
    summary_items = [
        ("Subtotal:", f"${subtotal:.2f}"),
        ("Shipping:", f"${shipping:.2f}"),
        ("Tax:", f"${tax:.2f}"),
        ("TOTAL:", f"${grand_total:.2f}")
    ]
    
    for label, value in summary_items:
        draw.text((70, y_pos + 10), label, font=font_header, fill=(0, 0, 0))
        draw.text((width - 100, y_pos + 10), value, font=font_header, fill=(0, 0, 0))
        y_pos += 25
    
    # Footer
    y_pos += 20
    draw.text((50, y_pos), "Thank you for your order!", font=font_normal, fill=(100, 100, 100))
    draw.text((50, y_pos + 20), "Questions? Contact support@example.com", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # Write JSON data
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"Condensed order generated: {output_path} and {json_path}")
    return order_data

def generate_modern_order(order_id, output_path):
    """
    生成现代风格订单
    """
    width, height = 950, 750
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(32)
    font_header = get_chinese_font(20)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_large = get_chinese_font(26)
    
    # Generate mock data
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%B %d, %Y')
    status = random.choice(['Confirmed', 'Processing', 'Shipped', 'Out for Delivery', 'Delivered'])
    estimated_delivery = (datetime.now() + timedelta(days=random.randint(2, 7))).strftime('%B %d, %Y')
    customer_name = f"{random.choice(['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'])}"
    address = f"{random.randint(100, 9999)} {random.choice(['Oak', 'Pine', 'Maple', 'Cedar', 'Elm'])} {random.choice(['St', 'Ave', 'Rd', 'Blvd'])}"
    city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia'])
    state_zip = f"{random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA'])} {random.randint(10001, 99999)}"
    
    # Collect order data for JSON
    order_data = {
        "order_id": order_id,
        "order_date": order_date,
        "status": status,
        "estimated_delivery": estimated_delivery,
        "customer_info": {
            "name": customer_name,
            "address": address,
            "city": city,
            "state_zip": state_zip
        },
        "items": [],
        "subtotal": 0,
        "shipping": 0,
        "tax": 0,
        "total": 0
    }
    
    # Modern header with gradient effect simulation
    draw.rectangle([0, 0, width, 100], fill=(41, 128, 185), outline=(41, 128, 185))
    draw.text((50, 30), "MODERN SHOP", font=font_large, fill=(255, 255, 255))
    draw.text((width - 300, 40), f"Order Confirmation #{order_id}", font=font_normal, fill=(255, 255, 255))
    
    # Order summary box
    draw.rectangle([50, 130, width-50, 200], fill=(248, 249, 250), outline=(200, 200, 200), width=1)
    
    order_summary = [
        f"Order Date: {order_date}",
        f"Order ID: {order_id}",
        f"Status: {status}",
        f"Estimated Delivery: {estimated_delivery}"
    ]
    
    y_pos = 150
    for i, summary in enumerate(order_summary):
        color = (52, 58, 64) if i == 0 else (108, 117, 125)
        draw.text((70, y_pos), summary, font=font_normal if i == 0 else font_small, fill=color)
        if i == 0:
            y_pos += 25
        else:
            y_pos += 20
    
    # Customer info
    y_pos += 30
    draw.text((70, y_pos), "SHIPPING INFORMATION", font=font_header, fill=(70, 70, 70))
    y_pos += 30
    
    customer_info = [
        f"Name: {customer_name}",
        f"Address: {address}",
        f"City: {city}",
        f"State: {state_zip}"
    ]
    
    for info in customer_info:
        draw.text((90, y_pos), info, font=font_normal, fill=(100, 100, 100))
        y_pos += 25
    
    # Product table
    y_pos += 30
    draw.text((70, y_pos), "ORDER ITEMS", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # Table header with modern styling
    draw.rectangle([70, y_pos, width-70, y_pos + 40], fill=(52, 58, 64), outline=(52, 58, 64))
    draw.text((90, y_pos + 12), "PRODUCT", font=font_normal, fill=(255, 255, 255))
    draw.text((400, y_pos + 12), "PRICE", font=font_normal, fill=(255, 255, 255))
    draw.text((550, y_pos + 12), "QTY", font=font_normal, fill=(255, 255, 255))
    draw.text((650, y_pos + 12), "TOTAL", font=font_normal, fill=(255, 255, 255))
    
    y_pos += 40
    
    # Product rows
    products = [
        ("Premium Wireless Headphones", "249.99", "1", "249.99"),
        ("Ultra Slim Laptop Sleeve", "39.99", "2", "79.98"),
        ("Bluetooth Portable Speaker", "89.99", "1", "89.99"),
        ("Ergonomic Office Chair", "199.99", "1", "199.99"),
    ]
    
    for i, product in enumerate(products):
        name, price, qty, total = product
        order_data["items"].append({
            "name": name,
            "price": float(price),
            "quantity": int(qty),
            "total": float(total)
        })
        
        # Row background
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([70, y_pos, width-70, y_pos + 50], fill=bg_color, outline=(230, 230, 230), width=1)
        
        # Product info
        draw.text((90, y_pos + 15), name, font=font_normal, fill=(52, 58, 64))
        draw.text((400, y_pos + 15), f"${price}", font=font_normal, fill=(52, 58, 64))
        draw.text((550, y_pos + 15), qty, font=font_normal, fill=(52, 58, 64))
        draw.text((650, y_pos + 15), f"${total}", font=font_normal, fill=(52, 58, 64))
        
        y_pos += 50
    
    # Calculate totals
    subtotal = sum(float(item["total"]) for item in order_data["items"])
    shipping = 15.99
    tax = 42.88
    grand_total = 578.83
    
    # Update order data with totals
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["total"] = grand_total
    
    # Summary section
    y_pos += 20
    draw.rectangle([width - 300, y_pos, width - 70, y_pos + 160], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    
    summary_items = [
        ("Subtotal:", f"{subtotal:.2f}"),
        ("Shipping:", f"{shipping:.2f}"),
        ("Tax:", f"{tax:.2f}"),
        ("TOTAL:", f"{grand_total:.2f}")
    ]
    
    summary_y = y_pos + 20
    for label, value in summary_items:
        draw.text((width - 280, summary_y), label, font=font_normal, fill=(52, 58, 64))
        draw.text((width - 120, summary_y), f"${value}", font=font_normal, fill=(52, 58, 64))
        summary_y += 30
    
    # Footer with thank you message
    y_pos += 180
    draw.rectangle([70, y_pos, width-70, y_pos + 80], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "Thank you for your order!", font=font_large, fill=(41, 128, 185))
    draw.text((100, y_pos + 50), "Questions? Contact us at support@modernshop.com", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # Write JSON data
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"Modern order generated: {output_path} and {json_path}")
    return order_data

def main():
    """
    Generate multiple orders of different types
    """
    import os  # Ensure os module is imported
    
    # Create unified subdirectory
    output_dir = "generated_orders"
    os.makedirs(output_dir, exist_ok=True)
    
    order_types = [
        ("simple", generate_simple_order),
        ("detailed", generate_detailed_order),
        ("invoice", generate_invoice_order),
        ("condensed", generate_condensed_order),
        ("modern", generate_modern_order)
    ]
    
    num_orders = 10  # Generate 10 sample orders
    
    for i in range(num_orders):
        order_id = f"ORD{i+1:04d}"
        order_type_idx = i % len(order_types)
        order_type, generator_func = order_types[order_type_idx]
        
        # Generate images and JSON files in unified subdirectory
        output_path = os.path.join(output_dir, f"order_{order_type}_{order_id}.png")
        generator_func(order_id, output_path)

if __name__ == "__main__":
    main()