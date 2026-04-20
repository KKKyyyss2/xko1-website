#!/usr/bin/env python3
"""
金边会所导航 - 每日SEO内容更新脚本
功能：
1. 生成新的文章页面
2. 更新sitemap.xml
3. 更新首页文章列表
4. 提交到GitHub
5. Cloudflare自动部署
"""

import os
import sys
import json
import random
import datetime
import markdown
from pathlib import Path
import shutil
import subprocess

# 配置
BASE_DIR = Path(__file__).parent.parent
WEBSITE_DIR = BASE_DIR
COMPONENTS_DIR = WEBSITE_DIR / "components"
ARTICLES_DIR = WEBSITE_DIR / "articles"
PAGES_DIR = WEBSITE_DIR / "pages"
SEO_DIR = WEBSITE_DIR / "seo"
SCRIPTS_DIR = WEBSITE_DIR / "scripts"

# 确保目录存在
for dir_path in [WEBSITE_DIR, COMPONENTS_DIR, ARTICLES_DIR, PAGES_DIR, SEO_DIR, SCRIPTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# 文章主题库
ARTICLE_TOPICS = [
    {
        "category": "体验分享",
        "templates": [
            "金边{会所}体验分享：详细评测与服务项目",
            "{地区}高端会所真实体验报告",
            "{会所}探店评测：环境、服务、价格全解析"
        ],
        "keywords": ["体验", "评测", "分享", "真实感受"]
    },
    {
        "category": "营业时间",
        "templates": [
            "{地区}会所营业时间全攻略",
            "{会所}最新营业时间调整通知",
            "节假日{地区}会所营业安排"
        ],
        "keywords": ["营业时间", "开放时间", "节假日", "凌晨"]
    },
    {
        "category": "价格指南",
        "templates": [
            "{地区}会所价格行情分析",
            "{会所}最新价格表与服务套餐",
            "如何避免{地区}会所价格陷阱"
        ],
        "keywords": ["价格", "费用", "套餐", "性价比"]
    },
    {
        "category": "文化解析",
        "templates": [
            "柬埔寨按摩文化与传统技法",
            "{地区}会所服务文化特点",
            "高棉传统按摩与现代SPA融合"
        ],
        "keywords": ["文化", "传统", "历史", "特色"]
    },
    {
        "category": "新闻动态",
        "templates": [
            "{地区}会所行业最新动态",
            "{会所}新服务项目上线",
            "柬埔寨按摩行业政策变化"
        ],
        "keywords": ["新闻", "动态", "政策", "更新"]
    }
]

# 地区和会所名称
REGIONS = ["金边", "西港", "波贝", "财通", "木牌", "戈公"]
CLUBS = ["888会所", "皇家水汇", "翡翠SPA", "钻石按摩", "黄金海岸", "水晶宫"]

def markdown_to_html(markdown_text):
    """将Markdown转换为HTML"""
    extensions = ['extra', 'tables', 'codehilite']
    html = markdown.markdown(markdown_text, extensions=extensions)
    return html

def generate_article_content():
    """生成文章内容"""
    topic = random.choice(ARTICLE_TOPICS)
    region = random.choice(REGIONS)
    club = random.choice(CLUBS)
    
    # 生成标题
    title_template = random.choice(topic["templates"])
    title = title_template.format(地区=region, 会所=club)
    
    # 生成slug
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    slug_base = title.replace(" ", "-").replace("：", "-").replace(":", "-").replace("，", "-").replace(",", "-")
    slug = f"{date_str}-{slug_base[:30]}"
    slug = ''.join(c for c in slug if c.isalnum() or c in '-')
    
    # 生成Markdown内容
    markdown_content = f"""# {title}

## 概述
{region}{club}是当地知名的{random.choice(['高端', '特色', '人气'])}场所，提供优质的{random.choice(['按摩', '水疗', 'SPA'])}服务。

## 服务项目
- **基础按摩**：{random.randint(30, 60)}分钟，${random.randint(20, 50)}
- **精油SPA**：{random.randint(60, 90)}分钟，${random.randint(50, 100)}
- **全身理疗**：{random.randint(90, 120)}分钟，${random.randint(80, 150)}
- **特色项目**：{random.choice(['古法按摩', '热石疗法', '草药包'])}，${random.randint(40, 80)}

## 环境设施
- 装修风格：{random.choice(['现代简约', '泰式传统', '豪华欧式'])}
- 房间类型：{random.choice(['标准间', 'VIP包间', '套房'])}
- 卫生条件：{random.choice(['优秀', '良好', '标准'])}
- 隐私保护：{random.choice(['完善', '良好', '标准'])}

## 技师团队
- 技师数量：{random.randint(10, 30)}人
- 培训背景：{random.choice(['专业按摩学校', '泰国培训', '本地经验'])}
- 服务语言：{random.choice(['中文', '英语', '高棉语'])}
- 专业认证：{random.choice(['全部持证', '大部分持证', '部分持证'])}

## 实用信息
- **地址**：{region}{random.choice(['市中心', '商业区', '旅游区'])}
- **电话**：+855 {random.randint(10, 99)} {random.randint(1000000, 9999999)}
- **营业时间**：{random.choice(['14:00-02:00', '12:00-24:00', '10:00-22:00'])}
- **预约方式**：{random.choice(['电话预约', '直接到店', '在线预订'])}

## 注意事项
1. 建议提前预约，特别是周末和节假日
2. 确认价格包含的服务项目
3. 注意个人财物安全
4. 尊重当地文化和工作人员
5. 如有不适及时与技师沟通

## 总结
{club}在{region}地区属于{random.choice(['性价比高', '服务优质', '环境优雅'])}的会所，适合{random.choice(['商务人士', '游客', '本地居民'])}选择。

*本文仅供参考，实际信息以商家为准。*
"""
    
    # 转换为HTML
    html_content = markdown_to_html(markdown_content)
    
    return {
        "title": title,
        "slug": slug,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "category": topic["category"],
        "region": region,
        "club": club,
        "markdown": markdown_content,
        "html": html_content,
        "excerpt": f"{region}{club}是当地知名的高端场所，提供优质的按摩和水疗服务。本文将分享实际体验、价格、服务项目以及注意事项。",
        "reading_time": random.randint(3, 8)
    }

def load_component(component_name):
    """加载组件文件"""
    component_path = COMPONENTS_DIR / f"{component_name}.html"
    if component_path.exists():
        return component_path.read_text(encoding='utf-8')
    return ""

def generate_article_html(article_data):
    """生成文章HTML页面"""
    
    # 加载组件
    hero = load_component("hero")
    nav = load_component("nav")
    footer = load_component("footer")
    
    # 结构化数据
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article_data["title"],
        "description": article_data["excerpt"],
        "author": {
            "@type": "Organization",
            "name": "金边会所导航"
        },
        "publisher": {
            "@type": "Organization",
            "name": "金边会所导航",
            "logo": {
                "@type": "ImageObject",
                "url": "https://xko1.com/logo.png"
            }
        },
        "datePublished": article_data["date"],
        "dateModified": article_data["date"],
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://xko1.com/article-{article_data['slug']}"
        }
    }
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{article_data['title']} - 金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</title>
    <meta name="description" content="{article_data['excerpt']}">
    
    <link rel="stylesheet" href="/style.css">
    <script src="/spa.js" defer></script>
    
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💆</text></svg>">
    
    <script type="application/ld+json">
    {json.dumps(structured_data, ensure_ascii=False, indent=2)}
    </script>
</head>
<body>
    {hero}
    {nav}
    
    <main>
        <div id="spa-container">
            <div class="container">
                <div class="article-header">
                    <h1 class="article-title">{article_data['title']}</h1>
                    <div class="article-meta">
                        <span>发布时间：{article_data['date']}</span>
                        <span>地区：{article_data['region']}</span>
                        <span>分类：{article_data['category']}</span>
                        <span>阅读时间：约{article_data['reading_time']}分钟</span>
                    </div>
                </div>
                
                <div class="article-content">
                    {article_data['html']}
                    
                    <div class="mt-40">
                        <a href="/" class="back-home" data-page="index">← 返回首页</a>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    {footer}
</body>
</html>"""
    
    return html_template

def update_sitemap(articles_list):
    """更新sitemap.xml"""
    sitemap_path = SEO_DIR / "sitemap.xml"
    
    # 基础URL
    base_url = "https://xko1.com"
    
    # 静态页面
    static_pages = [
        "/",
        "/gao-duan",
        "/bi-keng", 
        "/ji-shi",
        "/jia-ge",
        "/xin-shou",
        "/faq"
    ]
    
    # 生成sitemap内容
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
"""
    
    # 添加静态页面
    for page in static_pages:
        sitemap_content += f"""  <url>
    <loc>{base_url}{page}</loc>
    <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{'1.0' if page == '/' else '0.8'}</priority>
  </url>
"""
    
    # 添加文章页面
    for article in articles_list:
        sitemap_content += f"""  <url>
    <loc>{base_url}/article-{article['slug']}</loc>
    <lastmod>{article['date']}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
"""
    
    sitemap_content += "</urlset>"
    
    # 写入文件
    sitemap_path.write_text(sitemap_content, encoding='utf-8')
    print(f"✅ 已更新sitemap.xml，包含{len(static_pages)}个静态页面和{len(articles_list)}篇文章")

def update_homepage_articles(articles_list):
    """更新首页文章列表（简化版，实际需要更复杂的模板更新）"""
    # 这里简化处理，实际应该更新index.html中的文章卡片
    # 现在先记录，后续可以扩展
    print(f"📝 需要更新首页文章列表，最新{min(5, len(articles_list))}篇文章")

def git_commit_and_push():
    """提交到GitHub"""
    try:
        # 添加所有文件
        subprocess.run(["git", "add", "."], cwd=WEBSITE_DIR, check=True)
        
        # 提交
        commit_message = f"每日更新：{datetime.datetime.now().strftime('%Y年%m月%d日')}新文章"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=WEBSITE_DIR, check=True)
        
        # 推送到GitHub
        subprocess.run(["git", "push", "origin", "main"], cwd=WEBSITE_DIR, check=True)
        
        print("✅ 已提交并推送到GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("金边会所导航 - 每日SEO内容更新")
    print("=" * 50)
    
    # 1. 生成新文章
    print("\n📝 生成新文章...")
    article_data = generate_article_content()
    print(f"  标题: {article_data['title']}")
    print(f"  Slug: {article_data['slug']}")
    print(f"  地区: {article_data['region']}")
    print(f"  分类: {article_data['category']}")
    
    # 2. 生成文章HTML文件
    article_html = generate_article_html(article_data)
    article_filename = f"article-{article_data['slug']}.html"
    article_path = ARTICLES_DIR / article_filename
    article_path.write_text(article_html, encoding='utf-8')
    print(f"✅ 文章已保存: {article_path}")
    
    # 3. 获取所有文章列表（用于sitemap）
    articles_list = []
    for article_file in ARTICLES_DIR.glob("article-*.html"):
        # 从文件名提取信息（简化处理）
        filename = article_file.stem
        if filename.startswith("article-"):
            slug = filename[8:]  # 去掉"article-"
            # 尝试从文件名提取日期
            date_part = slug[:8] if len(slug) >= 8 else datetime.datetime.now().strftime("%Y%m%d")
            try:
                article_date = datetime.datetime.strptime(date_part, "%Y%m%d").strftime("%Y-%m-%d")
            except:
                article_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            articles_list.append({
                "slug": slug,
                "date": article_date
            })
    
    # 4. 更新sitemap.xml
    print("\n🗺️ 更新sitemap.xml...")
    update_sitemap(articles_list)
    
    # 5. 更新首页文章列表
    print("\n🏠 更新首页文章列表...")
    update_homepage_articles(articles_list)
    
    # 6. 复制SEO文件到根目录（Cloudflare Pages需要）
    print("\n🔧 复制SEO文件到根目录...")
    seo_files = ["robots.txt", "sitemap.xml", "google518f32604920aa8b.html"]
    for file_name in seo_files:
        src = SEO_DIR / file_name
        dst = WEBSITE_DIR / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ {file_name}")
    
    # 7. 提交到GitHub（可选）
    print("\n🚀 是否提交到GitHub？")
    print("  输入 'y' 自动提交，输入其他跳过")
    choice = input("  选择: ").strip().lower()
    
    if choice == 'y':
        if git_commit_and_push():
            print("\n🎉 更新完成！Cloudflare Pages将自动部署")
            print(f"   新文章URL: https://xko1.com/article-{article_data['slug']}")
            print(f"   sitemap: https://xko1.com/sitemap.xml")
        else:
            print("\n⚠️  Git提交失败，请手动提交")
    else:
        print("\n📋 更新完成，请手动提交到GitHub")
        print(f"   新文章文件: {article_path}")
        print(f"   sitemap文件: {WEBSITE_DIR / 'sitemap.xml'}")
    
    print("\n" + "=" * 50)
    print("完成！")

if __name__ == "__main__":
    main()