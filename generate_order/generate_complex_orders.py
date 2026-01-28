#!/usr/bin/env python3
"""
生成复杂订单图片的脚本
包含多种复杂订单类型，如电商订单、B2B订单、国际订单、混合订单等
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
        "/System/Library/ Fonts/PingFang.ttc",
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

def generate_ecommerce_order(order_id, output_path):
    """
    生成电商订单（复杂格式）
    包含优惠券、积分抵扣、促销活动等信息
    """
    width, height = 1000, 900
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(28)
    font_header = get_chinese_font(20)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_tiny = get_chinese_font(12)
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    customer_name = f"用户{random.choice(['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'])}"
    phone = f"138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    shipping_address = f"{random.randint(100, 9999)} {random.choice(['主街', '橡树街', '松树街', '榆树街', '枫树街'])}，{random.choice(['北京', '上海', '广州', '深圳', '杭州'])}，{random.choice(['北京', '上海', '广东', '深圳', '浙江'])}"
    shipping_method = random.choice(["标准配送", "快递", "隔夜达", "免运费"])
    payment_method = random.choice(["信用卡", "支付宝", "微信支付", "银行转账", "花呗"])
    status = random.choice(["待付款", "待发货", "已发货", "已签收", "已完成", "已取消"])
    
    # 收集订单数据以生成JSON
    order_data = {
        "order_id": order_id,
        "order_date": order_date,
        "customer_name": customer_name,
        "phone": phone,
        "shipping_address": shipping_address,
        "shipping_method": shipping_method,
        "payment_method": payment_method,
        "status": status,
        "promotions": [],
        "items": [],
        "original_total": 0,
        "discount_total": 0,
        "final_total": 0,
        "points_used": 0,
        "points_deduction": 0
    }
    
    # 头部横幅
    draw.rectangle([0, 0, width, 80], fill=(231, 76, 60), outline=(231, 76, 60))
    draw.text((50, 25), "电商平台 - 订单中心", font=font_header, fill=(255, 255, 255))
    draw.text((width - 250, 30), f"电商订单 #{order_id}", font=font_normal, fill=(255, 255, 255))
    
    # 订单基础信息
    y_pos = 100
    basic_info = [
        ("订单编号:", order_id),
        ("下单时间:", order_date),
        ("客户姓名:", customer_name),
        ("联系电话:", phone),
        ("收货地址:", shipping_address),
        ("配送方式:", shipping_method),
        ("支付方式:", payment_method),
        ("订单状态:", status)
    ]
    
    for i, (label, value) in enumerate(basic_info):
        # 交替背景色
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(248, 249, 250))
        else:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(253, 253, 254))
        
        draw.text((70, y_pos), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((250, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 30
    
    # 促销活动信息
    y_pos += 10
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(255, 248, 220), outline=(253, 234, 190), width=1)
    draw.text((70, y_pos + 12), "🎉 活动优惠: 满300减50 + 会员折扣10%", font=font_normal, fill=(243, 156, 18))
    y_pos += 50
    
    # 商品表格标题
    draw.text((70, y_pos), "商品清单", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 表头
    col_headers = ["商品", "规格", "单价", "数量", "小计", "优惠"]
    col_widths = [300, 150, 100, 80, 100, 120]
    
    # 表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(52, 73, 94), outline=(52, 73, 94))
    
    x_pos = 70
    for i, header in enumerate(col_headers):
        draw.text((x_pos, y_pos + 12), header, font=font_normal, fill=(255, 255, 255))
        x_pos += col_widths[i]
    
    y_pos += 40
    
    # 商品列表
    product_names = [
        "iPhone 15 Pro Max 256GB", "MacBook Air M2 13英寸", "iPad Air 5 256GB", 
        "AirPods Pro 2代", "Apple Watch Series 9", "Beats Studio Buds",
        "华为Mate 60 Pro", "小米14 Ultra", "OPPO Find X7", "vivo X100 Pro",
        "联想ThinkPad X1", "戴尔XPS 13", "华硕ROG魔霸", "微星GS66 Stealth"
    ]
    
    products = []
    num_products = random.randint(2, 5)
    for i in range(num_products):
        name = random.choice(product_names)
        spec = random.choice(["64GB", "128GB", "256GB", "512GB", "1TB", "标准版", "高配版"])
        price = round(random.uniform(100, 10000), 2)
        qty = random.randint(1, 3)
        subtotal = qty * price
        
        # 随机添加优惠
        discount = 0
        if random.random() > 0.5:
            discount = round(subtotal * random.uniform(0.05, 0.3), 2)
        
        final_subtotal = subtotal - discount
        products.append((name, spec, f"{price:.2f}", str(qty), f"{final_subtotal:.2f}", f"-{discount:.2f}" if discount > 0 else "无"))
        
        order_data["items"].append({
            "name": name,
            "specification": spec,
            "unit_price": price,
            "quantity": qty,
            "original_subtotal": subtotal,
            "discount": discount,
            "final_subtotal": final_subtotal
        })
    
    # 绘制商品行
    for i, product in enumerate(products):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([50, y_pos, width-50, y_pos + 50], fill=bg_color, outline=(230, 230, 230), width=1)
        
        x_pos = 70
        for j, cell in enumerate(product):
            draw.text((x_pos, y_pos + 15), cell, font=font_normal, fill=(52, 58, 64))
            x_pos += col_widths[j]
        
        y_pos += 50
    
    # 计算总计
    original_total = sum(float(item["original_subtotal"]) for item in order_data["items"])
    total_discount = sum(float(item["discount"]) for item in order_data["items"])
    shipping_cost = round(random.uniform(0, 30), 2) if original_total < 300 else 0  # 满300免邮
    tax_rate = 0.1
    tax = round((original_total - total_discount) * tax_rate, 2)
    final_total = original_total - total_discount + shipping_cost + tax
    
    # 积分抵扣
    points_available = random.randint(0, 5000)
    points_used = min(points_available, int(final_total * 10))  # 最多抵扣订单金额的10%
    points_deduction = round(points_used / 100, 2)  # 100积分=1元
    final_total -= points_deduction
    
    # 更新订单数据
    order_data["original_total"] = original_total
    order_data["discount_total"] = total_discount
    order_data["shipping_cost"] = shipping_cost
    order_data["tax"] = tax
    order_data["points_used"] = points_used
    order_data["points_deduction"] = points_deduction
    order_data["final_total"] = final_total
    
    # 订单总计区域
    y_pos += 20
    draw.rectangle([width - 350, y_pos, width - 50, y_pos + 220], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    
    summary_items = [
        ("商品原价:", f"¥{original_total:.2f}"),
        ("优惠金额:", f"-¥{total_discount:.2f}"),
        ("运费:", f"¥{shipping_cost:.2f}" if shipping_cost > 0 else "免运费"),
        ("税费(10%):", f"¥{tax:.2f}"),
        ("积分抵扣:", f"-¥{points_deduction:.2f}"),
        ("订单总额:", f"¥{final_total:.2f}")
    ]
    
    summary_y = y_pos + 20
    for label, value in summary_items:
        draw.text((width - 330, summary_y), label, font=font_normal, fill=(52, 58, 64))
        draw.text((width - 120, summary_y), value, font=font_normal, fill=(52, 58, 64))
        summary_y += 30
    
    # 订单备注
    y_pos += 240
    draw.text((70, y_pos), "订单备注:", font=font_header, fill=(70, 70, 70))
    y_pos += 30
    remarks = [
        "• 请小心包装，易碎品",
        "• 工作日送货，节假日不配送",
        "• 如需发票请联系客服"
    ]
    for remark in remarks:
        draw.text((90, y_pos), remark, font=font_small, fill=(100, 100, 100))
        y_pos += 25
    
    # 页脚
    y_pos += 40
    draw.rectangle([70, y_pos, width-70, y_pos + 60], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 15), "感谢您在电商平台购物！订单 #" + order_id, font=font_normal, fill=(52, 58, 64))
    draw.text((100, y_pos + 35), "客服热线: 400-123-4567 | 客服邮箱: service@ecommerce.com", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"电商订单已生成: {output_path} 和 {json_path}")
    return order_data

def generate_b2b_order(order_id, output_path):
    """
    生成B2B企业订单（复杂格式）
    包含合同编号、账期、信用额度等企业级信息
    """
    width, height = 1000, 950
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(30)
    font_header = get_chinese_font(22)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_tiny = get_chinese_font(12)
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    contract_number = f"CT-{random.randint(10000, 99999)}-{order_date[:4]}"
    po_number = f"PO-{random.randint(10000, 99999)}"
    credit_limit = random.uniform(10000, 100000)
    credit_used = random.uniform(1000, credit_limit * 0.8)
    payment_terms = random.choice(["30天账期", "60天账期", "90天账期", "预付款", "货到付款"])
    delivery_date = (datetime.now() + timedelta(days=random.randint(5, 15))).strftime("%Y-%m-%d")
    
    company_name = f"{random.choice(['科技', '贸易', '制造', '电子', '机械', '化工'])}{random.randint(100, 999)}有限公司"
    contact_person = f"{random.choice(['张', '李', '王', '刘', '陈'])}{random.choice(['经理', '主管', '总监', '主任'])}"
    company_address = f"{random.randint(100, 9999)} {random.choice(['商务园', '科技园', '工业区'])} {random.randint(1, 20)}号楼"
    city = random.choice(['北京', '上海', '广州', '深圳', '杭州', '苏州', '武汉', '成都'])
    tax_id = f"91{random.randint(10000000000000000, 99999999999999999)}"
    
    # 收集订单数据以生成JSON
    order_data = {
        "order_id": order_id,
        "contract_number": contract_number,
        "po_number": po_number,
        "order_date": order_date,
        "delivery_date": delivery_date,
        "payment_terms": payment_terms,
        "credit_limit": credit_limit,
        "credit_used": credit_used,
        "company_info": {
            "name": company_name,
            "contact_person": contact_person,
            "address": company_address,
            "city": city,
            "tax_id": tax_id
        },
        "items": [],
        "subtotal": 0,
        "discount": 0,
        "shipping": 0,
        "tax": 0,
        "total": 0
    }
    
    # 头部公司标识
    draw.rectangle([0, 0, width, 100], fill=(44, 62, 80), outline=(44, 62, 80))
    draw.text((50, 25), "ABC科技集团有限公司", font=font_header, fill=(255, 255, 255))
    draw.text((50, 60), "企业采购管理系统", font=font_normal, fill=(200, 200, 200))
    draw.text((width - 250, 35), f"B2B订单 #{order_id}", font=font_normal, fill=(255, 255, 255))
    draw.text((width - 250, 65), f"合同编号: {contract_number}", font=font_small, fill=(200, 200, 200))
    
    # 企业客户信息
    y_pos = 120
    customer_info = [
        f"客户公司: {company_name}",
        f"联系人: {contact_person}",
        f"地址: {company_address}, {city}",
        f"纳税人识别号: {tax_id}",
        f"采购订单号: {po_number}",
        f"交货日期: {delivery_date}",
        f"付款条件: {payment_terms}",
        f"信用额度: ¥{credit_limit:,.2f} | 已用: ¥{credit_used:,.2f}"
    ]
    
    for i, info in enumerate(customer_info):
        # 交替背景色
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(248, 249, 250))
        else:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(253, 253, 254))
        
        draw.text((70, y_pos), info, font=font_normal, fill=(50, 50, 50))
        y_pos += 30
    
    # 产品表格标题
    y_pos += 20
    draw.text((70, y_pos), "采购商品清单", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 表头
    col_headers = ["序号", "商品名称", "型号", "单位", "单价", "数量", "金额", "税率", "税额"]
    col_widths = [60, 200, 120, 80, 100, 80, 100, 80, 100]
    
    # 表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(52, 73, 94), outline=(52, 73, 94))
    
    x_pos = 60
    for i, header in enumerate(col_headers):
        draw.text((x_pos, y_pos + 12), header, font=font_normal, fill=(255, 255, 255))
        x_pos += col_widths[i]
    
    y_pos += 40
    
    # 产品列表
    product_names = [
        "服务器CPU Intel Xeon", "企业级固态硬盘", "网络交换机", "路由器", 
        "UPS不间断电源", "机柜", "网线", "光纤跳线", "防火墙设备", 
        "负载均衡器", "VPN网关", "无线AP", "监控摄像头", "门禁系统"
    ]
    
    products = []
    num_products = random.randint(3, 8)
    for i in range(num_products):
        idx = str(i+1)
        name = random.choice(product_names)
        model = f"M{random.randint(1000, 9999)}"
        unit = random.choice(["台", "个", "套", "件", "批"])
        price = round(random.uniform(100, 10000), 2)
        qty = random.randint(1, 20)
        amount = qty * price
        tax_rate = random.choice([0.13, 0.09, 0.06, 0.03, 0])  # 不同税率
        tax_amount = round(amount * tax_rate, 2)
        
        products.append((
            idx, name, model, unit, f"{price:.2f}", str(qty), 
            f"{amount:.2f}", f"{tax_rate*100}%", f"{tax_amount:.2f}"
        ))
        
        order_data["items"].append({
            "index": idx,
            "name": name,
            "model": model,
            "unit": unit,
            "unit_price": price,
            "quantity": qty,
            "amount": amount,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount
        })
    
    # 绘制产品行
    for i, product in enumerate(products):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([50, y_pos, width-50, y_pos + 45], fill=bg_color, outline=(230, 230, 230), width=1)
        
        x_pos = 60
        for j, cell in enumerate(product):
            draw.text((x_pos, y_pos + 12), cell, font=font_normal if j != 7 else font_small, fill=(52, 58, 64))
            x_pos += col_widths[j]
        
        y_pos += 45
    
    # 计算总计
    subtotal = sum(float(item["amount"]) for item in order_data["items"])
    total_tax = sum(float(item["tax_amount"]) for item in order_data["items"])
    discount_rate = random.uniform(0.02, 0.1)  # 2%-10% 折扣
    discount = round(subtotal * discount_rate, 2)
    shipping = round(random.uniform(0, 500), 2)
    total = subtotal - discount + total_tax + shipping
    
    # 更新订单数据
    order_data["subtotal"] = subtotal
    order_data["discount"] = discount
    order_data["shipping"] = shipping
    order_data["tax"] = total_tax
    order_data["total"] = total
    
    # 总计区域
    y_pos += 20
    draw.rectangle([width - 350, y_pos, width - 50, y_pos + 200], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    
    summary_items = [
        ("商品合计:", f"¥{subtotal:,.2f}"),
        ("折扣(-{:.1f}%):".format(discount_rate*100), f"-¥{discount:,.2f}"),
        ("运费:", f"¥{shipping:,.2f}"),
        ("税额合计:", f"¥{total_tax:,.2f}"),
        ("订单总额:", f"¥{total:,.2f}")
    ]
    
    summary_y = y_pos + 20
    for label, value in summary_items:
        draw.text((width - 330, summary_y), label, font=font_normal, fill=(52, 58, 64))
        draw.text((width - 120, summary_y), value, font=font_normal, fill=(52, 58, 64))
        summary_y += 35
    
    # 付款信息
    y_pos += 220
    draw.text((70, y_pos), "付款信息:", font=font_header, fill=(70, 70, 70))
    y_pos += 35
    
    payment_info = [
        f"付款条件: {payment_terms}",
        f"发票类型: 增值税专用发票",
        f"开票信息: {company_name} ({tax_id})",
        f"收货地址: {company_address}, {city}",
        f"期望交期: {delivery_date}"
    ]
    
    for info in payment_info:
        draw.text((90, y_pos), info, font=font_normal, fill=(52, 58, 64))
        y_pos += 28
    
    # 合同条款
    y_pos += 40
    draw.text((70, y_pos), "合同条款:", font=font_header, fill=(70, 70, 70))
    y_pos += 30
    
    terms = [
        "• 质量保证期：验收合格后12个月",
        "• 售后服务：7×24小时技术支持",
        "• 违约责任：按合同法相关规定执行",
        "• 争议解决：提交甲方所在地法院管辖"
    ]
    
    for term in terms:
        draw.text((90, y_pos), term, font=font_small, fill=(100, 100, 100))
        y_pos += 25
    
    # 页脚
    y_pos += 40
    draw.rectangle([70, y_pos, width-70, y_pos + 80], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "ABC科技集团有限公司", font=font_normal, fill=(52, 58, 64))
    draw.text((100, y_pos + 45), f"地址: 北京市海淀区中关村大街1号 | 电话: 010-12345678 | 订单 #{order_id}", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"B2B企业订单已生成: {output_path} 和 {json_path}")
    return order_data

def generate_international_order(order_id, output_path):
    """
    生成国际订单（复杂格式）
    包含多币种、关税、物流跟踪等国际交易信息
    """
    width, height = 1000, 1000
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(28)
    font_header = get_chinese_font(20)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_tiny = get_chinese_font(12)
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    tracking_number = f"TRK{random.randint(100000000, 999999999)}"
    shipping_carrier = random.choice(["DHL", "FedEx", "UPS", "TNT", "中国邮政"])
    origin_country = random.choice(["中国", "美国", "德国", "日本", "韩国"])
    destination_country = random.choice(["美国", "加拿大", "英国", "德国", "法国", "澳大利亚", "日本"])
    currency = random.choice(["USD", "EUR", "GBP", "JPY", "CNY"])
    exchange_rate = round(random.uniform(6, 8), 2) if currency == "USD" else 1  # 相对于人民币的汇率
    
    # 客户信息
    customer_name = f"{random.choice(['Johnson', 'Smith', 'Williams', 'Brown', 'Jones'])}, {random.choice(['International Corp', 'Global Trading', 'Worldwide Ltd', 'Enterprise Inc'])}"
    address = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm Blvd'])}, {random.choice(['New York', 'London', 'Tokyo', 'Sydney', 'Toronto'])}"
    vat_number = f"GB{random.randint(100000000, 999999999)}" if destination_country == "英国" else f"DE{random.randint(100000000, 999999999)}" if destination_country == "德国" else ""
    
    # 收集订单数据以生成JSON
    order_data = {
        "order_id": order_id,
        "tracking_number": tracking_number,
        "shipping_carrier": shipping_carrier,
        "order_date": order_date,
        "origin_country": origin_country,
        "destination_country": destination_country,
        "currency": currency,
        "exchange_rate": exchange_rate,
        "customer_info": {
            "name": customer_name,
            "address": address,
            "vat_number": vat_number
        },
        "items": [],
        "subtotal_usd": 0,
        "tax_usd": 0,
        "shipping_usd": 0,
        "duty_usd": 0,
        "total_usd": 0
    }
    
    # 头部国际化标识
    draw.rectangle([0, 0, width, 100], fill=(52, 152, 219), outline=(52, 152, 219))
    draw.text((50, 25), "全球贸易平台 - 国际订单系统", font=font_header, fill=(255, 255, 255))
    draw.text((50, 60), f"订单编号: {order_id} | 跟踪号: {tracking_number}", font=font_normal, fill=(200, 200, 200))
    
    # 国际运输信息
    y_pos = 120
    transport_info = [
        f"发货国家: {origin_country}",
        f"目的国家: {destination_country}",
        f"承运商: {shipping_carrier}",
        f"货币单位: {currency}",
        f"汇率: 1{currency} = {exchange_rate}CNY",
        f"客户名称: {customer_name}",
        f"客户地址: {address}",
        f"增值税号: {vat_number if vat_number else 'N/A'}"
    ]
    
    for i, info in enumerate(transport_info):
        # 交替背景色
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(236, 240, 241))
        else:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(248, 249, 250))
        
        draw.text((70, y_pos), info, font=font_normal, fill=(50, 50, 50))
        y_pos += 30
    
    # 商品表格标题
    y_pos += 20
    draw.text((70, y_pos), "国际商品清单", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 表头
    col_headers = ["序号", "商品名称", "HS编码", "原产国", "单价", "数量", "总价", "关税码", "税率"]
    col_widths = [60, 180, 100, 80, 100, 80, 100, 100, 80]
    
    # 表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(41, 128, 185), outline=(41, 128, 185))
    
    x_pos = 60
    for i, header in enumerate(col_headers):
        draw.text((x_pos, y_pos + 12), header, font=font_small, fill=(255, 255, 255))
        x_pos += col_widths[i]
    
    y_pos += 40
    
    # 国际商品列表
    product_names = [
        "智能手机", "笔记本电脑", "平板电脑", "智能手表", 
        "蓝牙耳机", "移动电源", "数码相机", "无人机", 
        "智能音箱", "VR眼镜", "游戏手柄", "机械键盘"
    ]
    
    products = []
    num_products = random.randint(3, 6)
    for i in range(num_products):
        idx = str(i+1)
        name = random.choice(product_names)
        hs_code = f"{random.randint(8517, 8548)}{random.randint(10, 99)}00"  # 海关编码
        origin_country = random.choice(["中国", "马来西亚", "泰国", "越南"])
        unit_price = round(random.uniform(10, 500), 2)
        qty = random.randint(1, 100)
        total_price = qty * unit_price
        tariff_code = f"TC{random.randint(1000, 9999)}"
        tariff_rate = round(random.uniform(0.05, 0.25), 2)  # 关税率5%-25%
        
        products.append((
            idx, name, hs_code, origin_country, 
            f"{unit_price:.2f}{currency}", str(qty), 
            f"{total_price:.2f}{currency}", tariff_code, f"{tariff_rate*100}%"
        ))
        
        order_data["items"].append({
            "index": idx,
            "name": name,
            "hs_code": hs_code,
            "origin_country": origin_country,
            "unit_price_usd": unit_price,
            "quantity": qty,
            "total_price_usd": total_price,
            "tariff_code": tariff_code,
            "tariff_rate": tariff_rate
        })
    
    # 绘制商品行
    for i, product in enumerate(products):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([50, y_pos, width-50, y_pos + 45], fill=bg_color, outline=(230, 230, 230), width=1)
        
        x_pos = 60
        for j, cell in enumerate(product):
            draw.text((x_pos, y_pos + 12), cell, font=font_small if j != 0 else font_normal, fill=(52, 58, 64))
            x_pos += col_widths[j]
        
        y_pos += 45
    
    # 计算国际费用
    subtotal = sum(float(item["total_price_usd"]) for item in order_data["items"])
    duty_rate = random.uniform(0.05, 0.30)  # 关税率
    duty = round(subtotal * duty_rate, 2)
    tax_rate = random.uniform(0.05, 0.25)  # 当地税
    tax = round((subtotal + duty) * tax_rate, 2)
    shipping = round(random.uniform(50, 500), 2)
    total = subtotal + duty + tax + shipping
    
    # 更新订单数据
    order_data["subtotal_usd"] = subtotal
    order_data["duty_usd"] = duty
    order_data["tax_usd"] = tax
    order_data["shipping_usd"] = shipping
    order_data["total_usd"] = total
    
    # 费用明细
    y_pos += 20
    draw.text((70, y_pos), "费用明细:", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    fee_items = [
        ("商品小计:", f"{subtotal:.2f}{currency}"),
        ("国际运费:", f"{shipping:.2f}{currency}"),
        (f"进口关税({duty_rate*100}%):", f"{duty:.2f}{currency}"),
        (f"当地税费({tax_rate*100}%):", f"{tax:.2f}{currency}"),
        ("订单总额:", f"{total:.2f}{currency}")
    ]
    
    for label, value in fee_items:
        draw.text((90, y_pos), f"{label}", font=font_normal, fill=(52, 58, 64))
        draw.text((width - 200, y_pos), f"{value}", font=font_normal, fill=(52, 58, 64))
        y_pos += 30
    
    # 物流信息
    y_pos += 20
    draw.text((70, y_pos), "物流追踪信息:", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    logistics_steps = [
        f"✓ {order_date} - 订单已接收",
        f"✓ {order_date} - 货物打包完成", 
        f"~ {datetime.now().strftime('%Y-%m-%d')} - 货物已发出 ({shipping_carrier})",
        f"~ {datetime.now() + timedelta(days=3)}. - 清关中",
        f"~ {datetime.now() + timedelta(days=7)} - 预计到达"
    ]
    
    for step in logistics_steps:
        draw.text((90, y_pos), step, font=font_normal, fill=(52, 58, 64))
        y_pos += 28
    
    # 国际贸易条款
    y_pos += 30
    draw.text((70, y_pos), "国际贸易条款:", font=font_header, fill=(70, 70, 70))
    y_pos += 30
    
    trade_terms = [
        "• 贸易条款: FOB (离岸价)",
        "• 付款方式: 信用证(L/C) 或 电汇(T/T)",
        "• 包装要求: 出口标准包装",
        "• 保险: 由买方自行购买",
        "• 质检: 符合目的地国家标准"
    ]
    
    for term in trade_terms:
        draw.text((90, y_pos), term, font=font_small, fill=(100, 100, 100))
        y_pos += 25
    
    # 汇率说明
    y_pos += 30
    draw.rectangle([70, y_pos, width-70, y_pos + 50], fill=(235, 245, 251), outline=(173, 216, 230), width=1)
    draw.text((90, y_pos + 15), f"汇率参考: 1{currency} = {exchange_rate}CNY | 总计: {total:.2f}{currency} ≈ {total*exchange_rate:.2f}CNY", 
              font=font_normal, fill=(52, 58, 64))
    
    # 页脚
    y_pos += 70
    draw.rectangle([70, y_pos, width-70, y_pos + 80], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "全球贸易平台", font=font_normal, fill=(52, 58, 64))
    draw.text((100, y_pos + 45), f"客服: international@globaltrade.com | 订单 #{order_id} | 跟踪号: {tracking_number}", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"国际订单已生成: {output_path} 和 {json_path}")
    return order_data

def generate_mixed_order(order_id, output_path):
    """
    生成混合订单（复杂格式）
    结合电商、B2B、国际等多种订单特点
    """
    width, height = 1050, 1100
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(32)
    font_header = get_chinese_font(22)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_tiny = get_chinese_font(12)
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    order_type = random.choice(["标准订单", "VIP订单", "企业订单", "批发订单", "定制订单"])
    priority = random.choice(["普通", "加急", "特急"])
    payment_status = random.choice(["未支付", "部分支付", "已支付", "已退款"])
    fulfillment_status = random.choice(["待处理", "拣货中", "打包中", "已发货", "已签收", "已完成"])
    
    customer_name = f"客户{random.choice(['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'])}"
    company_name = f"{random.choice(['科技', '贸易', '制造', '电子', '机械'])}{random.randint(1, 999)}有限公司" if random.random() > 0.5 else ""
    phone = f"138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    email = f"customer{random.randint(1000, 9999)}@example.com"
    
    # 地址信息（可能包含国际地址）
    is_international = random.random() > 0.7
    if is_international:
        address = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd'])}, {random.choice(['New York', 'London', 'Tokyo'])}, {random.choice(['USA', 'UK', 'Japan'])}"
    else:
        address = f"{random.randint(100, 9999)} {random.choice(['主街', '橡树街', '松树街'])}，{random.choice(['北京', '上海', '广州', '深圳', '杭州'])}，{random.choice(['北京', '上海', '广东', '深圳', '浙江'])}"
    
    # 收集订单数据以生成JSON
    order_data = {
        "order_id": order_id,
        "order_type": order_type,
        "priority": priority,
        "order_date": order_date,
        "payment_status": payment_status,
        "fulfillment_status": fulfillment_status,
        "customer_info": {
            "name": customer_name,
            "company": company_name,
            "phone": phone,
            "email": email,
            "address": address,
            "is_international": is_international
        },
        "promotions": [],
        "items": [],
        "original_total": 0,
        "discount_total": 0,
        "tax_total": 0,
        "shipping_total": 0,
        "other_fees": 0,
        "final_total": 0
    }
    
    # 头部复杂标识
    draw.rectangle([0, 0, width, 120], fill=(155, 89, 182), outline=(155, 89, 182))
    draw.text((50, 25), "全能商业平台", font=font_title, fill=(255, 255, 255))
    draw.text((50, 70), "电商 · B2B · 国际贸易 · 批发 · 定制", font=font_normal, fill=(236, 240, 241))
    
    # 订单基本信息
    order_info_text = f"混合订单 #{order_id} | 类型: {order_type} | 优先级: {priority} | 状态: {payment_status}/{fulfillment_status}"
    draw.text((width - len(order_info_text) * 8, 40), order_info_text, font=font_small, fill=(255, 255, 255))
    
    # 客户信息区域
    y_pos = 140
    draw.rectangle([50, y_pos, width-50, y_pos + 140], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((70, y_pos + 15), "客户信息", font=font_header, fill=(70, 70, 70))
    
    customer_fields = [
        ("客户姓名:", customer_name),
        ("公司名称:" if company_name else "", company_name if company_name else ""),
        ("联系电话:", phone),
        ("电子邮箱:", email),
        ("收货地址:", address),
        ("国际订单:" if is_international else "", "是" if is_international else "否")
    ]
    
    customer_y = y_pos + 50
    for label, value in customer_fields:
        if label:  # 只绘制非空标签
            draw.text((90, customer_y), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((250, customer_y), f"{value}", font=font_normal, fill=(0, 0, 0))
        customer_y += 25
    
    y_pos += 160
    
    # 订单状态信息
    draw.rectangle([50, y_pos, width-50, y_pos + 80], fill=(236, 250, 255), outline=(200, 220, 255), width=1)
    draw.text((70, y_pos + 15), "订单状态", font=font_header, fill=(70, 70, 70))
    
    status_info = [
        f"订单日期: {order_date}",
        f"支付状态: {payment_status}",
        f"履约状态: {fulfillment_status}",
        f"订单类型: {order_type}",
        f"优先级别: {priority}"
    ]
    
    status_y = y_pos + 45
    for info in status_info:
        draw.text((90, status_y), info, font=font_normal, fill=(50, 50, 50))
        status_y += 20
    
    y_pos += 100
    
    # 促销活动区域
    promotions = []
    promo_types = ["满减", "折扣", "买赠", "积分", "优惠券", "会员价"]
    num_promos = random.randint(0, 3)
    for i in range(num_promos):
        promo_type = random.choice(promo_types)
        if promo_type == "满减":
            promotions.append(f"满{random.randint(100, 1000)}减{random.randint(10, 100)}")
        elif promo_type == "折扣":
            promotions.append(f"{random.randint(80, 95)}折优惠")
        elif promo_type == "买赠":
            promotions.append(f"买{random.randint(2, 5)}送{random.randint(1, 2)}")
        elif promo_type == "积分":
            promotions.append(f"积分抵扣{random.randint(50, 500)}分")
        elif promo_type == "优惠券":
            promotions.append(f"优惠券减免{random.randint(5, 50)}元")
        else:  # 会员价
            promotions.append(f"会员专享{random.randint(90, 98)}折")
    
    if promotions:
        draw.rectangle([50, y_pos, width-50, y_pos + 40 + len(promotions)*25], fill=(255, 248, 220), outline=(253, 234, 190), width=1)
        draw.text((70, y_pos + 15), "促销活动", font=font_header, fill=(70, 70, 70))
        
        promo_y = y_pos + 45
        for promo in promotions:
            draw.text((90, promo_y), f"🎉 {promo}", font=font_normal, fill=(243, 156, 18))
            promo_y += 25
        
        y_pos = promo_y + 20
    else:
        y_pos += 80
    
    # 商品表格标题
    draw.text((70, y_pos), "商品清单", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 表头
    col_headers = ["序号", "商品名称", "规格/型号", "品牌", "单价", "数量", "小计", "优惠", "税率", "最终价"]
    col_widths = [50, 180, 100, 80, 80, 60, 80, 80, 70, 80]
    
    # 表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(52, 73, 94), outline=(52, 73, 94))
    
    x_pos = 60
    for i, header in enumerate(col_headers):
        draw.text((x_pos, y_pos + 12), header, font=font_small, fill=(255, 255, 255))
        x_pos += col_widths[i]
    
    y_pos += 40
    
    # 商品列表
    product_categories = [
        ("电子产品", ["iPhone", "iPad", "MacBook", "AirPods", "Apple Watch"]),
        ("家电", ["电视", "冰箱", "洗衣机", "空调", "微波炉"]),
        ("服装", ["T恤", "牛仔裤", "外套", "运动鞋", "帽子"]),
        ("图书", ["小说", "技术书籍", "儿童读物", "杂志", "工具书"]),
        ("食品", ["零食", "饮料", "调料", "干货", "进口食品"])
    ]
    
    products = []
    num_products = random.randint(4, 8)
    for i in range(num_products):
        idx = str(i+1)
        category, items = random.choice(product_categories)
        name = random.choice(items)
        spec = random.choice(["标准版", "高配版", "专业版", "豪华版", "限量版"])
        brand = random.choice(["苹果", "华为", "小米", "三星", "索尼", "戴尔", "联想", "美的", "格力"])
        unit_price = round(random.uniform(10, 5000), 2)
        qty = random.randint(1, 5)
        subtotal = qty * unit_price
        
        # 计算各种优惠
        discount = 0
        if random.random() > 0.5:
            discount_type = random.choice(["百分比", "固定金额"])
            if discount_type == "百分比":
                discount_rate = random.uniform(0.05, 0.3)
                discount = round(subtotal * discount_rate, 2)
            else:
                discount = min(round(random.uniform(10, 200), 2), subtotal * 0.5)  # 最大折扣不超过原价一半
        
        final_subtotal = subtotal - discount
        tax_rate = random.choice([0.13, 0.09, 0.06, 0.03, 0])
        tax_amount = round(final_subtotal * tax_rate, 2)
        final_price = final_subtotal + tax_amount
        
        products.append((
            idx, f"{category}-{name}", spec, brand, 
            f"{unit_price:.2f}", str(qty), 
            f"{subtotal:.2f}", f"-{discount:.2f}", 
            f"{tax_rate*100}%", f"{final_price:.2f}"
        ))
        
        order_data["items"].append({
            "index": idx,
            "name": f"{category}-{name}",
            "specification": spec,
            "brand": brand,
            "unit_price": unit_price,
            "quantity": qty,
            "original_subtotal": subtotal,
            "discount": discount,
            "after_discount_subtotal": final_subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "final_price": final_price
        })
    
    # 绘制商品行
    for i, product in enumerate(products):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([50, y_pos, width-50, y_pos + 45], fill=bg_color, outline=(230, 230, 230), width=1)
        
        x_pos = 60
        for j, cell in enumerate(product):
            draw.text((x_pos, y_pos + 12), cell, font=font_small if j not in [0, 1] else font_normal, fill=(52, 58, 64))
            x_pos += col_widths[j]
        
        y_pos += 45
    
    # 计算总计
    original_total = sum(float(item["original_subtotal"]) for item in order_data["items"])
    total_discount = sum(float(item["discount"]) for item in order_data["items"])
    subtotal_after_discount = original_total - total_discount
    total_tax = sum(float(item["tax_amount"]) for item in order_data["items"])
    
    # 其他费用
    shipping_cost = round(random.uniform(0, 100), 2) if original_total < 200 else 0  # 满200包邮
    handling_fee = round(random.uniform(0, 30), 2) if random.random() > 0.7 else 0  # 手续费
    insurance = round(random.uniform(0, 50), 2) if is_international else 0  # 国际订单保险
    
    other_fees = shipping_cost + handling_fee + insurance
    final_total = subtotal_after_discount + total_tax + other_fees
    
    # 更新订单数据
    order_data["original_total"] = original_total
    order_data["discount_total"] = total_discount
    order_data["tax_total"] = total_tax
    order_data["shipping_total"] = shipping_cost
    order_data["handling_fee"] = handling_fee
    order_data["insurance"] = insurance
    order_data["other_fees"] = other_fees
    order_data["final_total"] = final_total
    
    # 费用汇总区域
    y_pos += 20
    draw.rectangle([width - 380, y_pos, width - 50, y_pos + 280], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((width - 360, y_pos + 15), "费用汇总", font=font_header, fill=(70, 70, 70))
    
    summary_items = [
        ("商品原价:", f"¥{original_total:.2f}"),
        ("优惠金额:", f"-¥{total_discount:.2f}"),
        ("优惠后小计:", f"¥{subtotal_after_discount:.2f}"),
        ("税费合计:", f"¥{total_tax:.2f}"),
        ("运费:", f"¥{shipping_cost:.2f}" if shipping_cost > 0 else "免运费"),
        ("手续费:", f"¥{handling_fee:.2f}" if handling_fee > 0 else "无"),
        ("保险费:" if is_international else "", f"¥{insurance:.2f}" if insurance > 0 else ""),
        ("其他费用:", f"¥{other_fees:.2f}"),
        ("订单总额:", f"¥{final_total:.2f}")
    ]
    
    summary_y = y_pos + 50
    for label, value in summary_items:
        if label:  # 只绘制非空标签
            draw.text((width - 360, summary_y), label, font=font_normal, fill=(52, 58, 64))
            draw.text((width - 120, summary_y), value, font=font_normal, fill=(52, 58, 64))
        summary_y += 28
    
    # 促销活动详情
    y_pos += 300
    if promotions:
        draw.text((70, y_pos), "促销活动详情:", font=font_header, fill=(70, 70, 70))
        y_pos += 35
        
        for promo in promotions:
            draw.text((90, y_pos), f"• {promo}", font=font_normal, fill=(243, 156, 18))
            y_pos += 28
    
    # 特殊说明
    y_pos += 20
    draw.text((70, y_pos), "特殊说明:", font=font_header, fill=(70, 70, 70))
    y_pos += 35
    
    special_notes = [
        "• 此为混合订单，包含多种业务模式",
        "• 国际订单部分需注意关税政策",
        "• 企业客户享受批量采购优惠",
        "• VIP客户享有专属客服支持",
        "• 所有商品享受7天无理由退换"
    ]
    
    for note in special_notes:
        draw.text((90, y_pos), note, font=font_small, fill=(100, 100, 100))
        y_pos += 25
    
    # 页脚
    y_pos += 40
    draw.rectangle([70, y_pos, width-70, y_pos + 100], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "全能商业平台 - 您的一站式商业解决方案", font=font_normal, fill=(52, 58, 64))
    draw.text((100, y_pos + 45), f"客服热线: 400-8888-9999 | 客服邮箱: service@allbusiness.com", font=font_small, fill=(100, 100, 100))
    draw.text((100, y_pos + 70), f"订单 #{order_id} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"混合订单已生成: {output_path} 和 {json_path}")
    return order_data

def generate_customized_order(order_id, output_path):
    """
    生成定制化订单（最复杂格式）
    包含个性化配置、生产进度、质量检测等信息
    """
    width, height = 1050, 1200
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font_title = get_chinese_font(32)
    font_header = get_chinese_font(24)
    font_normal = get_chinese_font(16)
    font_small = get_chinese_font(14)
    font_tiny = get_chinese_font(12)
    
    # 生成模拟数据
    order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
    order_type = "定制订单"
    customization_level = random.choice(["基础定制", "深度定制", "完全定制"])
    production_status = random.choice(["设计中", "打样中", "生产中", "质检中", "包装中", "待发货"])
    delivery_method = random.choice(["标准配送", "加急配送", "专人配送", "自提"])
    
    customer_name = f"客户{random.choice(['张三', '李四', '王五', '赵六', '钱七', '孙八'])}"
    company_name = f"{random.choice(['创新', '卓越', '精品', '匠心'])}定制有限公司"
    contact_person = f"{random.choice(['张', '李', '王', '刘'])}{random.choice(['设计师', '项目经理', '采购经理'])}"
    phone = f"139-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    email = f"custom{random.randint(1000, 9999)}@custom.com"
    
    # 收集订单数据以生成JSON
    order_data = {
        "order_id": order_id,
        "order_type": order_type,
        "customization_level": customization_level,
        "order_date": order_date,
        "production_status": production_status,
        "delivery_method": delivery_method,
        "customer_info": {
            "name": customer_name,
            "company": company_name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email
        },
        "customization_details": {},
        "production_schedule": [],
        "quality_checks": [],
        "items": [],
        "design_cost": 0,
        "material_cost": 0,
        "production_cost": 0,
        "total_cost": 0
    }
    
    # 头部定制化标识
    draw.rectangle([0, 0, width, 140], fill=(46, 204, 113), outline=(46, 204, 113))
    draw.text((50, 25), "匠心定制 - 个性化解决方案", font=font_title, fill=(255, 255, 255))
    draw.text((50, 75), "专业设计 · 精工制造 · 个性体验", font=font_normal, fill=(236, 240, 241))
    draw.text((width - 300, 35), f"定制订单 #{order_id}", font=font_normal, fill=(255, 255, 255))
    draw.text((width - 300, 65), f"定制等级: {customization_level}", font=font_small, fill=(200, 200, 200))
    draw.text((width - 300, 85), f"生产状态: {production_status}", font=font_small, fill=(200, 200, 200))
    
    # 客户及联系方式
    y_pos = 160
    draw.rectangle([50, y_pos, width-50, y_pos + 120], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((70, y_pos + 15), "客户及项目信息", font=font_header, fill=(70, 70, 70))
    
    customer_fields = [
        ("客户名称:", customer_name),
        ("公司名称:", company_name),
        ("项目联系人:", contact_person),
        ("联系电话:", phone),
        ("电子邮箱:", email),
        ("交付方式:", delivery_method)
    ]
    
    customer_y = y_pos + 50
    for label, value in customer_fields:
        draw.text((90, customer_y), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((250, customer_y), f"{value}", font=font_normal, fill=(0, 0, 0))
        customer_y += 25
    
    y_pos += 140
    
    # 定制需求详情
    draw.text((70, y_pos), "定制需求详情", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 产品定制选项
    customization_options = {
        "产品类型": random.choice(["高端手表", "定制珠宝", "手工皮具", "艺术陶瓷", "木制工艺品", "金属制品"]),
        "主要材质": random.choice(["不锈钢", "纯银", "真皮", "陶瓷", "钛合金", "贵金属"]),
        "颜色方案": random.choice(["经典黑金", "玫瑰金", "铂金银", "双色搭配", "彩色镶嵌", "透明质感"]),
        "尺寸规格": f"{random.randint(20, 100)}mm × {random.randint(20, 100)}mm × {random.randint(5, 30)}mm",
        "工艺要求": random.choice(["抛光", "拉丝", "雕刻", "镶嵌", "镀层", "复合工艺"]),
        "功能特性": random.choice(["防水", "防磁", "计时", "存储", "装饰", "实用"]),
        "包装要求": random.choice(["精美礼盒", "定制包装", "环保材料", "奢华包装", "简约包装"]),
        "附加服务": random.choice(["刻字", "证书", "保养", "延保", "礼品卡", "个性化卡片"])
    }
    
    # 存储定制详情
    order_data["customization_details"] = customization_options.copy()
    
    # 显示定制选项
    for key, value in customization_options.items():
        draw.text((90, y_pos), f"{key}:", font=font_normal, fill=(50, 50, 50))
        draw.text((250, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 30
    
    y_pos += 20
    
    # 设计稿预览区域（模拟）
    draw.rectangle([70, y_pos, width-70, y_pos + 150], fill=(250, 250, 250), outline=(200, 200, 200), width=1)
    draw.text((90, y_pos + 15), "设计稿预览", font=font_header, fill=(70, 70, 70))
    draw.text((90, y_pos + 50), "┌─────────────────────────────────────────────────────┐", font=font_tiny, fill=(100, 100, 100))
    draw.text((90, y_pos + 65), "│                    [设计图占位符]                     │", font=font_tiny, fill=(100, 100, 100))
    draw.text((90, y_pos + 80), "│                                                     │", font=font_tiny, fill=(100, 100, 100))
    draw.text((90, y_pos + 95), "│           客户确认签字: _________________            │", font=font_tiny, fill=(100, 100, 100))
    draw.text((90, y_pos + 110), "└─────────────────────────────────────────────────────┘", font=font_tiny, fill=(100, 100, 100))
    draw.text((90, y_pos + 125), "* 设计稿已通过客户确认", font=font_small, fill=(243, 156, 18))
    
    y_pos += 170
    
    # 生产进度计划
    draw.text((70, y_pos), "生产进度计划", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 进度阶段
    stages = [
        ("设计确认", "已确认", order_date),
        ("物料采购", "进行中", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")),
        ("样品制作", "待开始", (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")),
        ("批量生产", "待开始", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")),
        ("质量检验", "待开始", (datetime.now() + timedelta(days=12)).strftime("%Y-%m-%d")),
        ("包装发货", "待开始", (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
    ]
    
    # 存储生产进度
    for stage_name, status, date in stages:
        order_data["production_schedule"].append({
            "stage": stage_name,
            "status": status,
            "expected_date": date
        })
    
    # 绘制进度表格
    stage_headers = ["阶段", "状态", "预计完成日期"]
    stage_col_widths = [200, 150, 200]
    
    # 表头
    draw.rectangle([70, y_pos, width-70, y_pos + 35], fill=(52, 73, 94), outline=(52, 73, 94))
    x_pos = 90
    for i, header in enumerate(stage_headers):
        draw.text((x_pos, y_pos + 10), header, font=font_normal, fill=(255, 255, 255))
        x_pos += stage_col_widths[i]
    
    y_pos += 35
    
    # 表格内容
    for i, (stage_name, status, date) in enumerate(stages):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([70, y_pos, width-70, y_pos + 35], fill=bg_color, outline=(230, 230, 230), width=1)
        
        x_pos = 90
        draw.text((x_pos, y_pos + 10), stage_name, font=font_normal, fill=(52, 58, 64))
        x_pos += stage_col_widths[0]
        draw.text((x_pos, y_pos + 10), status, font=font_normal, fill=(52, 58, 64))
        x_pos += stage_col_widths[1]
        draw.text((x_pos, y_pos + 10), date, font=font_normal, fill=(52, 58, 64))
        
        y_pos += 35
    
    y_pos += 20
    
    # 质量检测标准
    draw.text((70, y_pos), "质量检测标准", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    quality_standards = [
        ("外观检查", "表面光滑无瑕疵，颜色均匀一致"),
        ("尺寸精度", "误差范围±0.1mm"),
        ("材质检测", "符合环保标准，无有害物质"),
        ("耐用性测试", "通过10万次耐磨测试"),
        ("安全检测", "通过国际安全认证"),
        ("包装检查", "防震防潮包装完整")
    ]
    
    # 存储质量检测标准
    for standard, description in quality_standards:
        order_data["quality_checks"].append({
            "standard": standard,
            "description": description,
            "passed": random.choice([True, False]) if production_status in ["质检中", "包装中", "待发货"] else None
        })
    
    for standard, description in quality_standards:
        draw.text((90, y_pos), f"• {standard}: {description}", font=font_small, fill=(52, 58, 64))
        y_pos += 28
    
    y_pos += 20
    
    # 成本明细
    draw.text((70, y_pos), "成本明细", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    # 计算成本
    design_cost = round(random.uniform(500, 3000), 2)
    material_cost = round(random.uniform(1000, 8000), 2)
    production_cost = round(random.uniform(800, 5000), 2)
    packaging_cost = round(random.uniform(100, 500), 2)
    shipping_cost = round(random.uniform(50, 300), 2)
    tax_rate = 0.13
    tax = round((design_cost + material_cost + production_cost + packaging_cost) * tax_rate, 2)
    total_cost = design_cost + material_cost + production_cost + packaging_cost + shipping_cost + tax
    
    # 更新订单数据
    order_data["design_cost"] = design_cost
    order_data["material_cost"] = material_cost
    order_data["production_cost"] = production_cost
    order_data["packaging_cost"] = packaging_cost
    order_data["shipping_cost"] = shipping_cost
    order_data["tax"] = tax
    order_data["total_cost"] = total_cost
    
    cost_items = [
        ("设计费用:", f"¥{design_cost:.2f}"),
        ("材料费用:", f"¥{material_cost:.2f}"),
        ("生产费用:", f"¥{production_cost:.2f}"),
        ("包装费用:", f"¥{packaging_cost:.2f}"),
        ("税费(13%):", f"¥{tax:.2f}"),
        ("运费:", f"¥{shipping_cost:.2f}"),
        ("总计:", f"¥{total_cost:.2f}")
    ]
    
    # 成本汇总表格
    cost_headers = ["费用项目", "金额"]
    cost_col_widths = [300, 200]
    
    # 表头
    draw.rectangle([70, y_pos, width//2, y_pos + 35], fill=(52, 73, 94), outline=(52, 73, 94))
    x_pos = 90
    for i, header in enumerate(cost_headers):
        draw.text((x_pos, y_pos + 10), header, font=font_normal, fill=(255, 255, 255))
        x_pos += cost_col_widths[i]
    
    y_pos += 35
    
    # 表格内容
    for i, (label, value) in enumerate(cost_items):
        # 行背景
        bg_color = (248, 249, 250) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([70, y_pos, width//2, y_pos + 35], fill=bg_color, outline=(230, 230, 230), width=1)
        
        draw.text((90, y_pos + 10), label, font=font_normal, fill=(52, 58, 64))
        draw.text((350, y_pos + 10), value, font=font_normal, fill=(52, 58, 64))
        
        y_pos += 35
    
    # 特殊条款
    y_pos += 30
    draw.text((70, y_pos), "定制服务条款", font=font_header, fill=(70, 70, 70))
    y_pos += 40
    
    terms = [
        "• 定制产品一经确认，不可随意更改设计",
        "• 客户需对提供的设计素材版权负责",
        "• 质量问题在收货后7天内可申请售后",
        "• 定制产品不适用7天无理由退货政策",
        "• 版权归客户所有，制造商保留展示权",
        "• 交付时间根据定制复杂程度可能调整"
    ]
    
    for term in terms:
        draw.text((90, y_pos), term, font=font_small, fill=(100, 100, 100))
        y_pos += 25
    
    # 页脚
    y_pos += 40
    draw.rectangle([70, y_pos, width-70, y_pos + 100], fill=(248, 249, 250), outline=(230, 230, 230), width=1)
    draw.text((100, y_pos + 20), "匠心定制 - 为您打造独一无二的产品", font=font_normal, fill=(52, 58, 64))
    draw.text((100, y_pos + 45), f"客服: custom@craftsmanship.com | 订单 #{order_id} | 定制等级: {customization_level}", font=font_small, fill=(100, 100, 100))
    draw.text((100, y_pos + 70), f"地址: 北京市朝阳区创意园区A座 | 电话: 400-123-定制", font=font_small, fill=(100, 100, 100))
    
    img = np.array(img_pil)
    cv2.imwrite(output_path, img)
    
    # 写入JSON数据
    json_path = output_path.replace('.png', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)
    
    print(f"定制订单已生成: {output_path} 和 {json_path}")
    return order_data

def main():
    """
    生成复杂订单的主函数
    生成约20个不同类型的复杂订单
    """
    import os  # 确保导入os模块
    
    # 创建输出目录
    output_dir = "generated_complex_orders"
    os.makedirs(output_dir, exist_ok=True)
    
    # 定义订单类型和对应的生成函数
    order_types = [
        ("ecommerce", generate_ecommerce_order),
        ("b2b", generate_b2b_order),
        ("international", generate_international_order),
        ("mixed", generate_mixed_order),
        ("customized", generate_customized_order)
    ]
    
    num_orders = 20  # 生成20个复杂订单
    
    print(f"开始生成 {num_orders} 个复杂订单...")
    
    for i in range(num_orders):
        order_id = f"CXORD{i+1:04d}"
        order_type_idx = i % len(order_types)
        order_type, generator_func = order_types[order_type_idx]
        
        # 生成图片和JSON文件
        output_path = os.path.join(output_dir, f"complex_order_{order_type}_{order_id}.png")
        generator_func(order_id, output_path)
    
    print(f"完成生成 {num_orders} 个复杂订单！")

if __name__ == "__main__":
    main()