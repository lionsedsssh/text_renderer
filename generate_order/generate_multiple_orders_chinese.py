#!/usr/bin/env python3
"""
生成多种类型订单图片的脚本（中文版）
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
    获取支持中文字符的字体，尝试多种可能的字体路径
    """
    font_paths = [
        # macOS 上常见的中文字体
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Menlo.ttc",
        # 通用中文字体名称
        "/System/Library/Fonts/Arial Unicode.ttf",
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
    
    # 如果找不到特定字体，则返回默认字体
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
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    customer_name = f"客户{random.randint(1000, 9999)}"
    email = f"kehu{random.randint(1000, 9999)}@email.com"
    phone = f"138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    address = f"{random.randint(100, 9999)} 号大街，{random.randint(1, 100)}号城市，省份"
    
    # 收集订单数据以生成JSON
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
    
    # 标题
    title = f"订单 #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, font=font_title, fill=(0, 0, 0))
    
    # 订单信息
    order_info = [
        ("订单编号:", order_id),
        ("日期:", order_date),
        ("客户:", customer_name),
        ("邮箱:", email),
        ("电话:", phone),
        ("地址:", address),
    ]
    
    y_pos = 80
    for label, value in order_info:
        draw.text((50, y_pos), f"{label}", font=font_normal, fill=(0, 0, 0))
        draw.text((200, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 30
    
    # 简单产品表格
    y_pos += 20
    draw.text((50, y_pos), "商品:", font=font_header, fill=(0, 0, 0))
    y_pos += 30
    
    products = [
        (f"商品{random.randint(100, 999)}", random.randint(1, 5), round(random.uniform(10, 500), 2)),
        (f"物品{random.randint(100, 999)}", random.randint(1, 3), round(random.uniform(5, 200), 2)),
        (f"货物{random.randint(100, 999)}", random.randint(2, 10), round(random.uniform(15, 300), 2)),
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
        draw.text((300, y_pos), f"数量: {qty}", font=font_normal, fill=(0, 0, 0))
        draw.text((400, y_pos), f"¥{price:.2f}", font=font_normal, fill=(0, 0, 0))
        draw.text((500, y_pos), f"¥{subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # 总计
    order_data["total"] = total
    y_pos += 20
    draw.text((400, y_pos), "总计:", font=font_header, fill=(0, 0, 0))
    draw.text((500, y_pos), f"¥{total:.2f}", font=font_header, fill=(0, 0, 0))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"简单订单已生成: {output_path} 和 {json_path}")
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
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    customer_name = f"客户{random.choice(['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'])}"
    phone = f"138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    shipping_address = f"{random.randint(100, 9999)} {random.choice(['主街', '橡树街', '松树街', '榆树街', '枫树街'])}，{random.choice(['北京', '上海', '广州', '深圳', '杭州'])}，{random.choice(['北京', '上海', '广东', '深圳', '浙江'])}"
    shipping_method = random.choice(["标准配送", "快递", "隔夜达", "免运费"])
    payment_method = random.choice(["信用卡", "支付宝", "银行转账", "货到付款"])
    status = random.choice(["处理中", "已发货", "已签收", "已取消"])
    
    # 收集订单数据以生成JSON
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
    
    # 头部横幅
    draw.rectangle([0, 0, width, 60], fill=(70, 130, 180), outline=(70, 130, 180))
    draw.text((30, 18), "商店名称 - 订单系统", font=font_company, fill=(255, 255, 255))
    
    # 标题
    title = f"详细订单 #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, font=font_title, fill=(0, 0, 0))
    
    # 分割线
    draw.line([(50, 130), (width-50, 130)], fill=(100, 100, 100), width=1)
    
    # 订单信息
    order_info = [
        ("订单编号:", order_id),
        ("客户姓名:", customer_name),
        ("电话:", phone),
        ("收货地址:", shipping_address),
        ("订单日期:", order_date),
        ("配送方式:", shipping_method),
        ("支付方式:", payment_method),
        ("状态:", status)
    ]
    
    y_pos = 150
    for i, (label, value) in enumerate(order_info):
        # 交替背景色
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(245, 245, 245))
        
        draw.text((70, y_pos), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((250, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 35
    
    # 表头
    y_pos += 30
    header_y = y_pos
    
    # 表格列宽
    col1_width = 60   # 商品编号
    col2_width = 320  # 商品名称
    col3_width = 120  # 单价
    col4_width = 100  # 数量
    col5_width = 150  # 小计
    
    # 绘制表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(230, 240, 250), outline=(100, 100, 100), width=1)
    
    # 绘制表头
    draw.text((50 + 20, y_pos + 10), "编号", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + 20, y_pos + 10), "商品名称", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + 30, y_pos + 10), "单价(元)", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + 35, y_pos + 10), "数量", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + col4_width + 40, y_pos + 10), "小计(元)", font=font_header, fill=(30, 30, 30))
    
    y_pos += 40
    
    # 表格内容
    product_names = [
        "无线耳机",
        "智能手表5代",
        "蓝牙音箱",
        "笔记本支架",
        "USB-C数据线2米",
        "手机壳",
        "充电宝20000毫安",
        "无线充电器",
        "降噪耳塞",
        "RGB游戏鼠标"
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
        # 计算当前行Y坐标
        current_y = y_pos + i * row_height
        
        # 交替行背景色
        if i % 2 == 0:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(250, 250, 250))
        else:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(255, 255, 255))
        
        # 绘制边框
        draw.rectangle([50, current_y, width-50, current_y + row_height], outline=(200, 200, 200), width=1)
        
        # 商品编号列
        draw.text((50 + 20, current_y + 12), product[0], font=font_normal, fill=(0, 0, 0))
        
        # 商品名称列
        draw.text((50 + col1_width + 20, current_y + 12), product[1], font=font_normal, fill=(50, 50, 50))
        
        # 单价列
        draw.text((50 + col1_width + col2_width + 40, current_y + 12), product[2], font=font_normal, fill=(0, 0, 0))
        
        # 数量列
        draw.text((50 + col1_width + col2_width + col3_width + 40, current_y + 12), product[3], font=font_normal, fill=(0, 0, 0))
        
        # 小计列
        draw.text((50 + col1_width + col2_width + col3_width + col4_width + 50, current_y + 12), product[4], font=font_normal, fill=(0, 0, 0))
    
    # 底部统计
    total_y = y_pos + len(products) * row_height + 20
    
    # 分割线
    draw.line([(50, total_y-10), (width-50, total_y-10)], fill=(100, 100, 100), width=1)
    
    # 计算总计
    subtotal = sum(float(p[4]) for p in products)
    shipping = round(random.uniform(0, 50), 2) if subtotal < 200 else 0  # 满200元包邮
    tax_rate = 0.08  # 8%税
    tax = round(subtotal * tax_rate, 2)
    grand_total = subtotal + shipping + tax
    
    # 更新订单数据总计
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["grand_total"] = grand_total
    
    # 小计
    draw.text((width - 250, total_y), "小计:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"¥{subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 运费
    total_y += 35
    draw.text((width - 250, total_y), "运费:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"¥{shipping:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 税费
    total_y += 35
    draw.text((width - 250, total_y), "税费(8%):", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"¥{tax:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 总计
    total_y += 35
    draw.text((width - 250, total_y), "总计:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), f"¥{grand_total:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 总金额（大字显示）
    total_y += 50
    draw.text((width - 250, total_y), f"应付金额: ¥{grand_total:.2f}", font=font_large, fill=(220, 20, 60))
    
    # 页脚
    total_y += 60
    draw.text((70, total_y), f"感谢您的光临！订单 #{order_id}", font=font_normal, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"详细订单已生成: {output_path} 和 {json_path}")
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
    
    # 发票头部
    draw.rectangle([0, 0, width, 80], fill=(50, 50, 150), outline=(50, 50, 150))
    draw.text((50, 20), "发 票", font=font_title, fill=(255, 255, 255))
    draw.text((width - 200, 25), f"发票号码: {order_id}", font=font_normal, fill=(255, 255, 255))
    
    # 公司信息
    company_info = [
        "ACME有限公司",
        "北京市朝阳区商务大道123号",
        "10001室",
        "北京，北京 10001",
        "电话: (010) 123-4567",
        "邮箱: billing@acme.com"
    ]
    
    y_pos = 100
    for info in company_info:
        draw.text((50, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # 开票给部分
    y_pos += 20
    draw.text((500, y_pos), "开票给:", font=font_header, fill=(0, 0, 0))
    y_pos += 25
    
    # 生成模拟数据
    invoice_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    po_number = f"采购单-{random.randint(10000, 99999)}"
    client_name = f"客户{random.randint(1000, 9999)}"
    client_address_line1 = f"{random.randint(100, 9999)} 客户路"
    client_address_city_state_zip = f"{random.choice(['上海', '深圳', '广州', '杭州', '成都'])}，{random.choice(['上海', '广东', '浙江', '四川'])} {random.randint(10001, 99999)}"
    contact_person = f"{random.choice(['张', '李', '王', '刘', '陈'])}{random.choice(['先生', '女士', '经理'])}"
    client_email = f"kehu{random.randint(1000, 9999)}@kehu.com"
    
    # 收集订单数据以生成JSON
    order_data = {
        "invoice_id": order_id,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "terms": "30天内付款",
        "po_number": po_number,
        "company_info": {
            "name": "ACME有限公司",
            "address": "北京市朝阳区商务大道123号10001室，北京，北京 10001",
            "phone": "(010) 123-4567",
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
        f"联系人: {contact_person}",
        f"邮箱: {client_email}"
    ]
    
    for info in bill_to:
        draw.text((500, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 20
    
    # 发票详情
    y_pos += 30
    invoice_details = [
        ("发票日期:", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")),
        ("到期日期:", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")),
        ("付款条件:", "30天内付款"),
        ("采购单号:", f"采购单-{random.randint(10000, 99999)}")
    ]
    
    for label, value in invoice_details:
        draw.text((500, y_pos), f"{label}", font=font_normal, fill=(0, 0, 0))
        draw.text((650, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # 表头
    y_pos += 30
    header_y = y_pos
    
    # 表格列宽
    col1_width = 50   # 编号
    col2_width = 300  # 描述
    col3_width = 120  # 单价
    col4_width = 100  # 数量
    col5_width = 130  # 金额
    
    # 绘制表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 35], fill=(240, 240, 240), outline=(100, 100, 100), width=1)
    
    # 绘制表头
    draw.text((50 + 15, y_pos + 10), "编号", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + 15, y_pos + 10), "描述", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + 25, y_pos + 10), "单价(元)", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + 30, y_pos + 10), "数量", font=font_header, fill=(30, 30, 30))
    draw.text((50 + col1_width + col2_width + col3_width + col4_width + 30, y_pos + 10), "金额(元)", font=font_header, fill=(30, 30, 30))
    
    y_pos += 35
    
    # 发票项目
    descriptions = [
        "网站开发服务",
        "软件年度许可",
        "云托管月费",
        "技术支持小时费",
        "咨询服务",
        "数据迁移服务",
        "培训课程",
        "维护合同"
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
        # 计算当前行Y坐标
        current_y = y_pos + i * row_height
        
        # 交替行背景色
        if i % 2 == 0:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(250, 250, 250))
        else:
            draw.rectangle([50, current_y, width-50, current_y + row_height], fill=(255, 255, 255))
        
        # 绘制边框
        draw.rectangle([50, current_y, width-50, current_y + row_height], outline=(200, 200, 200), width=1)
        
        # 编号列
        draw.text((50 + 15, current_y + 10), item[0], font=font_normal, fill=(0, 0, 0))
        
        # 描述列
        draw.text((50 + col1_width + 15, current_y + 10), item[1], font=font_small, fill=(50, 50, 50))
        
        # 单价列
        draw.text((50 + col1_width + col2_width + 30, current_y + 10), item[2], font=font_normal, fill=(0, 0, 0))
        
        # 数量列
        draw.text((50 + col1_width + col2_width + col3_width + 35, current_y + 10), item[3], font=font_normal, fill=(0, 0, 0))
        
        # 金额列
        draw.text((50 + col1_width + col2_width + col3_width + col4_width + 40, current_y + 10), item[4], font=font_normal, fill=(0, 0, 0))
    
    # 总计部分
    total_y = y_pos + len(items) * row_height + 30
    
    # 小计
    subtotal = sum(float(item[4]) for item in items)
    draw.text((width - 200, total_y), "小计:", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 税费
    total_y += 30
    tax_rate = 0.1  # 10% 税
    tax_amount = round(subtotal * tax_rate, 2)
    draw.text((width - 200, total_y), f"税费({int(tax_rate*100)}%):", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{tax_amount:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 总计
    total_y += 40
    grand_total = subtotal + tax_amount
    draw.text((width - 200, total_y), "合 计:", font=font_large, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{grand_total:.2f}", font=font_large, fill=(0, 0, 0))
    
    # 付款条款
    total_y += 60
    draw.text((50, total_y), "付款条款: 30天内付款。逾期付款每月收取1.5%的服务费。", font=font_small, fill=(100, 100, 100))
    total_y += 25
    draw.text((50, total_y), "支票请付给ACME有限公司。如有疑问？致电(010) 123-4567。", font=font_small, fill=(100, 100, 100))
    
    # 计算总计并更新订单数据
    subtotal = sum(float(item[4]) for item in items)
    tax_rate = 0.1  # 10% 税
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = subtotal + tax_amount
    
    # 更新订单数据总计
    order_data["subtotal"] = subtotal
    order_data["tax_rate"] = tax_rate
    order_data["tax_amount"] = tax_amount
    order_data["grand_total"] = grand_total
    
    # 继续绘制总计在图像上
    total_y = y_pos + len(items) * row_height + 30
    
    # 小计
    draw.text((width - 200, total_y), "小计:", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 税费
    total_y += 30
    draw.text((width - 200, total_y), f"税费({int(tax_rate*100)}%):", font=font_normal, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{tax_amount:.2f}", font=font_normal, fill=(0, 0, 0))
    
    # 总计
    total_y += 40
    draw.text((width - 200, total_y), "合 计:", font=font_large, fill=(0, 0, 0))
    draw.text((width - 100, total_y), f"¥{grand_total:.2f}", font=font_large, fill=(0, 0, 0))
    
    # 付款条款
    total_y += 60
    draw.text((50, total_y), "付款条款: 30天内付款。逾期付款每月收取1.5%的服务费。", font=font_small, fill=(100, 100, 100))
    total_y += 25
    draw.text((50, total_y), "支票请付给ACME有限公司。如有疑问？致电(010) 123-4567。", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"发票订单已生成: {output_path} 和 {json_path}")
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
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    customer_id = f"客户-{random.randint(10000, 99999)}"
    status = random.choice(['已完成', '处理中', '已发货', '已签收'])
    
    # 收集订单数据以生成JSON
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
    
    # 标题
    title = f"订单摘要 #{order_id}"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, font=font_title, fill=(0, 0, 0))
    
    # 基本信息
    y_pos = 60
    basic_info = [
        f"日期: {order_date}",
        f"客户ID: {customer_id}",
        f"状态: {status}"
    ]
    
    for info in basic_info:
        draw.text((50, y_pos), info, font=font_normal, fill=(0, 0, 0))
        y_pos += 25
    
    # 商品列表
    y_pos += 15
    draw.text((50, y_pos), "商品:", font=font_header, fill=(0, 0, 0))
    y_pos += 25
    
    products = [
        (f"商品{random.randint(100, 999)}", random.randint(1, 3), round(random.uniform(10, 100), 2)),
        (f"产品{random.randint(100, 999)}", random.randint(1, 2), round(random.uniform(20, 200), 2)),
        (f"配件{random.randint(100, 999)}", random.randint(2, 5), round(random.uniform(5, 50), 2)),
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
        draw.text((width - 150, y_pos), f"¥{subtotal:.2f}", font=font_normal, fill=(0, 0, 0))
        y_pos += 22
    
    # 计算总计
    subtotal = total
    shipping = round(random.uniform(0, 15), 2)
    tax = round(subtotal * 0.08, 2)
    grand_total = round(subtotal + shipping + tax, 2)
    
    # 更新订单数据总计
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["total"] = grand_total
    
    # 摘要
    y_pos += 25
    draw.rectangle([50, y_pos, width-50, y_pos + 100], outline=(150, 150, 150), width=1)
    
    summary_items = [
        ("小计:", f"¥{subtotal:.2f}"),
        ("运费:", f"¥{shipping:.2f}"),
        ("税费:", f"¥{tax:.2f}"),
        ("总计:", f"¥{grand_total:.2f}")
    ]
    
    for label, value in summary_items:
        draw.text((70, y_pos + 10), label, font=font_header, fill=(0, 0, 0))
        draw.text((width - 100, y_pos + 10), value, font=font_header, fill=(0, 0, 0))
        y_pos += 25
    
    # 页脚
    y_pos += 20
    draw.text((50, y_pos), "感谢您的订购！", font=font_normal, fill=(100, 100, 100))
    draw.text((50, y_pos + 20), "问题？联系 support@example.com", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"紧凑型订单已生成: {output_path} 和 {json_path}")
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
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('2026年%m月%d日')
    status = random.choice(['已确认', '处理中', '已发货', '配送中', '已签收'])
    estimated_delivery = (datetime.now() + timedelta(days=random.randint(2, 7))).strftime('2026年%m月%d日')
    customer_name = f"{random.choice(['张', '李', '王', '刘', '陈', '杨'])}{random.choice(['先生', '女士', '经理'])}"
    address = f"{random.randint(100, 9999)}号 {random.choice(['橡树', '松树', '枫树', '雪松', '榆树'])} {random.choice(['街', '大道', '路', '林荫道'])}"
    city = random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都'])
    state_zip = f"{random.choice(['北京', '上海', '广东', '深圳', '浙江', '四川'])} {random.randint(10001, 99999)}"
    
    # 收集订单数据以生成JSON
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
    
    # 现代风格头部带渐变效果模拟
    draw.rectangle([0, 0, width, 100], fill=(41, 128, 185), outline=(41, 128, 185))
    draw.text((50, 30), "现代商店", font=font_large, fill=(255, 255, 255))
    draw.text((width - 300, 40), f"订单确认 #{order_id}", font=font_normal, fill=(255, 255, 255))
    
    # 订单摘要框
    draw.rectangle([50, 130, width-50, 200], fill=(248, 249, 250), outline=(200, 200, 200), width=1)
    
    order_summary = [
        f"订单日期: {order_date}",
        f"订单ID: {order_id}",
        f"状态: {status}",
        f"预计送达: {estimated_delivery}"
    ]
    
    y_pos = 150
    for i, summary in enumerate(order_summary):
        color = (52, 58, 64) if i == 0 else (108, 117, 125)
        draw.text((70, y_pos), summary, font=font_normal if i == 0 else font_small, fill=color)
        if i == 0:
            y_pos += 25
        else:
            y_pos += 20
    
    # 客户信息
    y_pos += 30
    draw.text((70, y_pos), "收货信息", font=font_header, fill=(70, 70, 70))
    y_pos += 30
    
    customer_info = [
        f"姓名: {customer_name}",
        f"地址: {address}",
        f"城市: {city}",
        f"地区: {state_zip}"
    ]
    
    for info in customer_info:
        draw.text((90, y_pos), info, font=font_normal, fill=(100, 100, 100))
        y_pos += 25
    
    # 商品表格
    y_pos += 30
    draw.text((70, y_pos), "订单商品", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 表头带现代样式
    draw.rectangle([70, y_pos, width-70, y_pos + 40], fill=(52, 58, 64), outline=(52, 58, 64))
    draw.text((90, y_pos + 12), "商品", font=font_normal, fill=(255, 255, 255))
    draw.text((400, y_pos + 12), "价格", font=font_normal, fill=(255, 255, 255))
    draw.text((550, y_pos + 12), "数量", font=font_normal, fill=(255, 255, 255))
    draw.text((650, y_pos + 12), "总计", font=font_normal, fill=(255, 255, 255))
    
    y_pos += 40
    
    # 商品行
    products = [
        ("高端无线耳机", "249.99", "1", "249.99"),
        ("超薄笔记本电脑套", "39.99", "2", "79.98"),
        ("蓝牙便携音箱", "89.99", "1", "89.99"),
        ("人体工学办公椅", "199.99", "1", "199.99"),
    ]
    
    for i, product in enumerate(products):
        name, price, qty, total = product
        order_data["items"].append({
            "name": name,
            "price": float(price),
            "quantity": int(qty),
            "total": float(total)
        })
        
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([70, y_pos, width-70, y_pos + 50], fill=bg_color, outline=(230, 230, 230), width=1)
        
        # 商品信息
        draw.text((90, y_pos + 15), name, font=font_normal, fill=(52, 58, 64))
        draw.text((400, y_pos + 15), f"¥{price}", font=font_normal, fill=(52, 58, 64))
        draw.text((550, y_pos + 15), qty, font=font_normal, fill=(52, 58, 64))
        draw.text((650, y_pos + 15), f"¥{total}", font=font_normal, fill=(52, 58, 64))
        
        y_pos += 50
    
    # 计算总计
    subtotal = sum(float(item["total"]) for item in order_data["items"])
    shipping = 15.99
    tax = 42.88
    grand_total = 578.83
    
    # 更新订单数据总计
    order_data["subtotal"] = subtotal
    order_data["shipping"] = shipping
    order_data["tax"] = tax
    order_data["total"] = grand_total
    
    # 摘要部分
    y_pos += 20
    draw.rectangle([width - 300, y_pos, width - 70, y_pos + 160], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    
    summary_items = [
        ("小计:", f"{subtotal:.2f}"),
        ("运费:", f"{shipping:.2f}"),
        ("税费:", f"{tax:.2f}"),
        ("总计:", f"{grand_total:.2f}")
    ]
    
    summary_y = y_pos + 20
    for label, value in summary_items:
        draw.text((width - 280, summary_y), label, font=font_normal, fill=(52, 58, 64))
        draw.text((width - 120, summary_y), f"¥{value}", font=font_normal, fill=(52, 58, 64))
        summary_y += 30
    
    # 页脚带感谢语
    y_pos += 180
    draw.rectangle([70, y_pos, width-70, y_pos + 80], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "感谢您的订购！", font=font_large, fill=(41, 128, 185))
    draw.text((100, y_pos + 50), "问题？联系我们 support@modernshop.com", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"现代风格订单已生成: {output_path} 和 {json_path}")
    return order_data

def main():
    """
    生成不同类型多个订单
    """
    import os  # 确保导入os模块
    
    # 创建统一的子目录
    output_dir = "generated_orders_zh"
    os.makedirs(output_dir, exist_ok=True)
    
    order_types = [
        ("simple", generate_simple_order),
        ("detailed", generate_detailed_order),
        ("invoice", generate_invoice_order),
        ("condensed", generate_condensed_order),
        ("modern", generate_modern_order)
    ]
    
    num_orders = 10  # 生成10个示例订单
    
    for i in range(num_orders):
        order_id = f"ORD{i+1:04d}"
        order_type_idx = i % len(order_types)
        order_type, generator_func = order_types[order_type_idx]
        
        # 在统一子目录中生成图片和JSON文件
        output_path = os.path.join(output_dir, f"order_{order_type}_zh_{order_id}.png")
        generator_func(order_id, output_path)

if __name__ == "__main__":
    main()