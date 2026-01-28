#!/usr/bin/env python3
"""
中文版订单图片生成脚本
用于生成带有中文内容的订单图片
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import platform

def get_chinese_font(size):
    """
    获取支持中文字符的字体，尝试多种可能的字体路径
    针对不同操作系统进行优化
    """
    system = platform.system()
    font_paths = []
    
    if system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # 苹方
            "/System/Library/Fonts/Hiragino Sans GB.ttc",  # 冬青黑体简体中文
            "/System/Library/Fonts/STHeiti Light.ttc",  # 华文细黑
            "/System/Library/Fonts/STHeiti Medium.ttc",  # 华文黑体
            "/System/Library/Fonts/SimHei.ttf",  # 如果存在的话
            "/System/Library/Fonts/Microsoft YaHei.ttf",  # 微软雅黑
            "/System/Library/Fonts/Arial Unicode.ttf",  # Arial Unicode
        ]
    elif system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
        ]
    elif system == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # DejaVu 字体
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # 文泉驿微米黑
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # 文泉驿正黑
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",  # Noto 字体
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Noto 字体
        ]
    else:
        # 通用字体路径
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Arial Unicode.ttf",
            "simhei.ttf",
            "simsun.ttc",
            "microsoft-yahei.ttf",
        ]
    
    # 尝试项目数据目录中的字体
    project_fonts = [
        "./data/fonts/chn/simhei.ttf",
        "./data/fonts/chn/simsun.ttf", 
        "./data/fonts/chn/microsoft-yahei.ttf",
        "../data/fonts/chn/simhei.ttf",
        "../data/fonts/chn/simsun.ttf",
        "../data/fonts/chn/microsoft-yahei.ttf",
    ]
    
    all_font_paths = project_fonts + font_paths
    
    for font_path in all_font_paths:
        try:
            if os.path.exists(font_path):
                print(f"找到字体文件: {font_path}")
                return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"无法加载字体 {font_path}: {str(e)}")
            continue
    
    # 如果特定字体未找到，尝试系统默认中文字体
    try:
        # 尝试通过字体名称获取（适用于某些系统）
        import matplotlib.font_manager as fm
        # 查找包含中文字符的字体
        chinese_fonts = [f.name for f in fm.fontManager.ttflist if 'chinese' in f.name.lower() or 'sans' in f.name.lower()]
        if chinese_fonts:
            return ImageFont.truetype(chinese_fonts[0], size)
    except:
        pass
    
    # 最后的备选方案：返回默认字体
    print("警告: 未能找到合适的中文字体，将使用默认字体")
    try:
        return ImageFont.truetype("Arial.ttf", size)
    except:
        return ImageFont.load_default()

def generate_order_image_chinese():
    """
    生成中文版订单图片
    """
    # 设置图片尺寸
    width, height = 900, 800
    
    # 创建白色背景图片
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # 使用PIL绘制文本
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    # 获取不同大小的字体
    font_title = get_chinese_font(28)
    font_header = get_chinese_font(18)
    font_normal = get_chinese_font(16)
    font_company = get_chinese_font(20)
    font_large = get_chinese_font(24)
    
    # 绘制公司Logo区域（顶部横幅）
    draw.rectangle([0, 0, width, 60], fill=(70, 130, 180), outline=(70, 130, 180))
    draw.text((30, 18), "我的店铺 - 订单系统", font=font_company, fill=(255, 255, 255))
    
    # 绘制标题
    title = "订单详情"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, font=font_title, fill=(0, 0, 0))
    
    # 绘制分隔线
    draw.line([(50, 130), (width-50, 130)], fill=(100, 100, 100), width=1)
    
    # 绘制订单信息
    order_info = [
        ("订单号:", "ORD202601260001"),
        ("客户姓名:", "张先生"),
        ("联系电话:", "138-0000-1234"),
        ("收货地址:", "北京市朝阳区某街某号"),
        ("下单时间:", "2026-01-26 10:30:00"),
        ("配送方式:", "标准配送"),
        ("支付方式:", "支付宝"),
        ("订单状态:", "待发货")
    ]
    
    y_pos = 150
    for i, (label, value) in enumerate(order_info):
        # 交替背景色
        if i % 2 == 0:
            draw.rectangle([50, y_pos-5, width-50, y_pos+25], fill=(245, 245, 245))
        
        draw.text((70, y_pos), f"{label}", font=font_normal, fill=(50, 50, 50))
        draw.text((220, y_pos), f"{value}", font=font_normal, fill=(0, 0, 0))
        y_pos += 35
    
    # 绘制表格头部
    y_pos += 30
    header_y = y_pos
    
    # 表格列宽
    col1_width = 60   # 序号
    col2_width = 320  # 商品名称
    col3_width = 120  # 单价
    col4_width = 100  # 数量
    col5_width = 150  # 小计
    
    # 绘制表头背景
    draw.rectangle([50, y_pos, width-50, y_pos + 40], fill=(230, 240, 250), outline=(100, 100, 100), width=1)
    
    # 绘制表头
    draw.text((50 + 20, y_pos + 10), "序号", font=font_header, fill=(30, 30, 30))
    
    draw.text((50 + col1_width + 20, y_pos + 10), "商品名称", font=font_header, fill=(30, 30, 30))
    
    draw.text((50 + col1_width + col2_width + 30, y_pos + 10), "单价(元)", font=font_header, fill=(30, 30, 30))
    
    draw.text((50 + col1_width + col2_width + col3_width + 35, y_pos + 10), "数量", font=font_header, fill=(30, 30, 30))
    
    draw.text((50 + col1_width + col2_width + col3_width + col4_width + 40, y_pos + 10), "小计(元)", font=font_header, fill=(30, 30, 30))
    
    y_pos += 40
    
    # 绘制表格内容
    products = [
        ("1", "iPhone 15 Pro Max 256GB 深紫色", "9999.00", "1", "9999.00"),
        ("2", "AirPods Pro 第二代", "1999.00", "1", "1999.00"),
        ("3", "MacBook Pro 14英寸 M3芯片", "15999.00", "1", "15999.00"),
        ("4", "iPad Air 11英寸 Wi-Fi 256GB", "4599.00", "2", "9198.00"),
        ("5", "Magic Mouse 无线鼠标", "649.00", "1", "649.00"),
    ]
    
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
        
        # 序号列
        draw.text((50 + 20, current_y + 12), product[0], font=font_normal, fill=(0, 0, 0))
        
        # 商品名称列
        draw.text((50 + col1_width + 20, current_y + 12), product[1], font=font_normal, fill=(50, 50, 50))
        
        # 单价列
        draw.text((50 + col1_width + col2_width + 40, current_y + 12), product[2], font=font_normal, fill=(0, 0, 0))
        
        # 数量列
        draw.text((50 + col1_width + col2_width + col3_width + 40, current_y + 12), product[3], font=font_normal, fill=(0, 0, 0))
        
        # 小计列
        draw.text((50 + col1_width + col2_width + col3_width + col4_width + 50, current_y + 12), product[4], font=font_normal, fill=(0, 0, 0))
    
    # 绘制底部统计
    total_y = y_pos + len(products) * row_height + 20
    
    # 分隔线
    draw.line([(50, total_y-10), (width-50, total_y-10)], fill=(100, 100, 100), width=1)
    
    # 合计行
    draw.text((width - 250, total_y), "商品合计:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "38,444.00", font=font_normal, fill=(0, 0, 0))
    
    # 运费
    total_y += 35
    draw.text((width - 250, total_y), "运费:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "0.00", font=font_normal, fill=(0, 0, 0))
    
    # 订单总计
    total_y += 35
    draw.text((width - 250, total_y), "订单总计:", font=font_normal, fill=(50, 50, 50))
    draw.text((width - 120, total_y), "38,444.00", font=font_normal, fill=(0, 0, 0))
    
    # 绘制总金额（大字显示）
    total_y += 50
    draw.text((width - 300, total_y), "应付金额: ¥38,444.00", font=font_large, fill=(220, 20, 60))
    
    # 添加底部信息
    total_y += 60
    draw.text((70, total_y), "备注: 如有问题请联系客服 400-123-4567", font=font_normal, fill=(100, 100, 100))
    total_y += 25
    draw.text((70, total_y), "感谢您的购买，祝您生活愉快！", font=font_normal, fill=(100, 100, 100))
    
    # 转换回OpenCV格式并保存
    img = np.array(img_pil)
    
    # 保存图片
    output_path = "order_image_chinese.png"
    cv2.imwrite(output_path, img)
    
    print(f"中文订单图片已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_order_image_chinese()