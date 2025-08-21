# 📦 仓库物品登记与查询系统

一个基于 **Python Flask + MySQL** 的仓库物品管理系统，支持：
- **物品登记**（物品名称、数量、维修人、图片）
- **物品查询**（支持关键字搜索，显示登记时间和图片）
- **跨平台使用**（Windows、Mac、Linux、手机浏览器均可访问）
- **上传图片** 并存储到 `static/uploads` 目录

---

## ✨ 功能概述
1. **登记页面 `/`**
   - 输入物品名称、数量、维修人
   - 可选上传物品图片（支持 JPG/PNG/GIF）
   - 自动记录登记时间
   - 成功登记后显示提示信息

2. **查询页面 `/query`**
   - 可按物品名称或维修人模糊搜索
   - 显示登记时间、图片（如无图片则显示“无”）
   - 结果按登记 ID 倒序排列（最新记录在前）

---

## 🗂 目录结构
物品登记系统/
│
├── app.py # Flask 主程序
├── config.py # 数据库配置
├── requirements.txt # 依赖包
├── README.md # 项目说明
│
├── templates/ # 页面模板
│ ├── form.html # 登记页
│ └── query.html # 查询页
│
├── static/ # 静态资源
│ └── uploads/ # 上传的物品图片
│
└── .env（可选） # 环境变量配置

---

## 🗄 数据库结构
请先在 MySQL 中创建数据库和数据表：
```sql
CREATE DATABASE warehouse_db DEFAULT CHARSET utf8mb4;

USE warehouse_db;

CREATE TABLE items_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    repair_person VARCHAR(255) NOT NULL,
    image_path VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
