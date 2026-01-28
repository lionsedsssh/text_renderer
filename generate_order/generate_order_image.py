#!/usr/bin/env python3
"""
Script to generate order images
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

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
        "SimHei.ttf",  # SimHei
        "SimSun.ttf",  # SimSun
        "Microsoft YaHei.ttf",  # Microsoft YaHei
        "STHeiti.ttc",  # STHeiti
        "STSong.ttc",  # STSong
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

def generate_order_image():
    """
    Generate an order image
    """
    # Set image dimensions
    width, height = 900, 800
    
    # Create white background image
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Use PIL to draw text
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    # Get different sized fonts
    font_title = get_chinese_font(28)
    font_header = get_chinese_font(18)
    font_normal = get_chinese_font(16)
    font_company = get_chinese_font(20)
    font_large = get_chinese_font(24)
    
    # Draw company logo area (top banner)
    draw.rectangle([0, 0, width, 60], fill=(70, 130, 180), outline=(70, 130, 180))
    draw.text((30, 18), "My Store - Order System", font=font_company, fill=(255, 255, 255))
    
    # Draw title
    title = "ORDER DETAILS"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, font=font_title, fill=(0, 0, 0))
    
    # Draw separator line
    draw.line([(50, 130), (width-50, 130)], fill=(100, 100, 100), width=1)
    
    # Draw order information
    order_info = [
        ("Order No.:", "ORD202601260001"),
        ("Customer Name:", "Mr. Zhang"),
        ("Phone Number:", "138-0000-1234"),
        ("Delivery Address:", "123 Somewhere Street, Chaoyang District, Beijing"),
        ("Order Date:", "2026-01-26 10:30:00"),
        ("Shipping Method:", "Standard Shipping"),
        ("Payment Method:", "Alipay"),
        ("Order Status:", "Pending Shipment")
    ]
    
    y_pos = 150
    for i, (label, value) in enumerate(order_info):
        # Alternating background color
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(245, 245, 245))
        
        draw.text((70, y_pos), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((220, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 35
    
    # Draw table header
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
    
    # Draw table content
    products = [
        ("1", "iPhone 15 Pro Max 256GB Deep Purple", "9999.00", "1", "9999.00"),
        ("2", "AirPods Pro 2nd Generation", "1999.00", "1", "1999.00"),
        ("3", "MacBook Pro 14-inch M3 Chip", "15999.00", "1", "15999.00"),
        ("4", "iPad Air 11-inch Wi-Fi 256GB", "4599.00", "2", "9198.00"),
        ("5", "Magic Mouse Wireless", "649.00", "1", "649.00"),
    ]
    
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
    
    # Draw bottom statistics
    total_y = y_pos + len(products) * row_height + 20
    
    # Separator line
    draw.line([(50, total_y-10), (width-50, total_y-10)], fill=(100, 100, 100), width=1)
    
    # Total row
    draw.text((width - 250, total_y), "Items Total:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "38,444.00", font=font_normal, fill=(0, 0, 0))
    
    # Shipping fee
    total_y += 35
    draw.text((width - 250, total_y), "Shipping Fee:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "0.00", font=font_normal, fill=(0, 0, 0))
    
    # Grand total
    total_y += 35
    draw.text((width - 250, total_y), "Order Total:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "38,444.00", font=font_normal, fill=(0, 0, 0))
    
    # Draw total amount (large display)
    total_y += 50
    draw.text((width - 300, total_y), "Amount Due: $38,444.00", font=font_large, fill=(220, 20, 60))
    
    # Add bottom information
    total_y += 60
    draw.text((70, total_y), "Note: Contact customer service at 400-123-4567 if you have any questions", font=font_normal, fill=(100, 100, 100))
    total_y += 25
    draw.text((70, total_y), "Thank you for your purchase, wish you a pleasant life!", font=font_normal, fill=(100, 100, 100))
    
    # Convert back to OpenCV format and save
    img = np.array(img_pil)
    
    # Save image
    output_path = "order_image.png"
    cv2.imwrite(output_path, img)
    
    print(f"Order image generated: {output_path}")
    return output_path
if __name__ == "__main__":
    generate_order_image()