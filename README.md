# 金边会所导航 - 新网站架构

## 项目结构
```
new_website/
├── index.html              # 首页（卡片布局）
├── style.css              # 样式文件（黑金主题）
├── spa.js                 # SPA导航脚本
├── components/            # 公共组件
│   ├── hero.html         # Hero区域
│   ├── nav.html          # 导航栏
│   └── footer.html       # 页脚
├── pages/                # 静态页面
│   ├── gao-duan.html     # 高端推荐
│   ├── bi-keng.html      # 避坑指南
│   ├── ji-shi.html       # 技师质量
│   ├── jia-ge.html       # 价格指南
│   ├── xin-shou.html     # 新手指南
│   └── faq.html          # FAQ
├── articles/             # 文章页面（自动生成）
├── scripts/              # 工具脚本
│   └── daily_seo_update.py  # 每日更新脚本
├── seo/                  # SEO文件
│   ├── robots.txt        # 爬虫规则
│   ├── sitemap.xml       # 网站地图（自动更新）
│   └── google518f32604920aa8b.html  # 谷歌验证
└── README.md             # 本文件
```

## 功能特性

### 1. 界面设计
- ✅ **黑金主题**：高端深色设计，金色点缀
- ✅ **响应式布局**：适配手机、平板、电脑
- ✅ **卡片式文章**：首页文章卡片布局
- ✅ **SPA导航**：无刷新页面切换
- ✅ **加载动画**：平滑的过渡效果

### 2. SEO优化
- ✅ **结构化数据**：Schema.org标记
- ✅ **sitemap.xml**：自动包含所有页面
- ✅ **robots.txt**：优化爬虫规则
- ✅ **meta标签**：完整的标题、描述、关键词
- ✅ **Open Graph**：社交媒体分享优化
- ✅ **谷歌验证**：Search Console验证文件

### 3. 自动化功能
- ✅ **文章生成**：自动生成新文章页面
- ✅ **sitemap更新**：每次更新自动刷新
- ✅ **GitHub集成**：一键提交推送
- ✅ **Cloudflare部署**：自动构建发布

## 使用说明

### 1. 手动更新文章
```bash
cd /home/tenbox/new_website
python scripts/daily_seo_update.py
```

### 2. 自动每日更新（cron）
```bash
# 编辑cron任务
crontab -e

# 添加以下行（每天9点运行）
0 9 * * * cd /home/tenbox/new_website && python scripts/daily_seo_update.py
```

### 3. 部署到Cloudflare Pages

#### 步骤1：创建GitHub仓库
```bash
cd /home/tenbox/new_website
git init
git add .
git commit -m "初始提交：金边会所导航新网站"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

#### 步骤2：配置Cloudflare Pages
1. 登录 Cloudflare Dashboard
2. 进入 Pages → Create a project
3. 连接 GitHub 仓库
4. 配置构建设置：
   - **Build command**: (留空，纯静态网站)
   - **Build output directory**: /
   - **Root directory**: /
5. 点击 "Save and Deploy"

#### 步骤3：绑定自定义域名
1. 在 Pages 项目设置中点击 "Custom domains"
2. 添加你的域名：xko1.com
3. Cloudflare 会自动配置 DNS

## 文件说明

### 核心文件
- **index.html**：首页，包含文章卡片和SPA容器
- **style.css**：所有样式定义，黑金主题
- **spa.js**：SPA导航系统，处理页面切换

### 组件文件
- **components/hero.html**：网站头部（标题、副标题、Telegram按钮）
- **components/nav.html**：导航栏（首页+6个指南页）
- **components/footer.html**：页脚（版权、链接）

### 静态页面
- **pages/gao-duan.html**：高端推荐指南
- **pages/bi-keng.html**：避坑指南
- **pages/ji-shi.html**：技师质量指南
- **pages/jia-ge.html**：价格指南
- **pages/xin-shou.html**：新手指南
- **pages/faq.html**：常见问题解答

### SEO文件
- **seo/robots.txt**：爬虫规则，允许所有页面
- **seo/sitemap.xml**：网站地图，包含所有页面
- **seo/google518f32604920aa8b.html**：谷歌验证文件

### 自动化脚本
- **scripts/daily_seo_update.py**：每日更新脚本，功能：
  1. 生成新文章（Markdown转HTML）
  2. 更新sitemap.xml
  3. 更新首页文章列表
  4. 提交到GitHub
  5. Cloudflare自动部署

## 文章系统

### 文章生成
- 每天自动生成1篇新文章
- 文章主题随机（体验分享、营业时间、价格指南等）
- 包含完整的SEO优化（标题、描述、结构化数据）
- 文章URL格式：`/article-YYYYMMDD-slug`

### 文章收录
- 所有文章自动加入sitemap.xml
- 谷歌爬虫可以索引所有文章
- 首页显示最新文章卡片
- 文章页有返回首页链接

## 技术细节

### SPA导航
- 无刷新页面切换
- 支持浏览器前进/后退
- 页面内容缓存（提高性能）
- 加载状态显示
- 错误处理

### SEO优化
- 每篇文章都有独立的Schema.org标记
- 首页有网站级结构化数据
- 所有页面都有规范的meta标签
- 支持Open Graph（社交媒体分享）
- 移动端友好

### 性能优化
- CSS和JS文件预加载
- 图片懒加载（预留接口）
- 页面内容缓存
- 响应式图片（预留接口）
- 代码分割（SPA按需加载）

## 维护说明

### 日常维护
1. **每日更新**：脚本自动运行，无需手动操作
2. **内容审核**：定期检查生成的文章内容
3. **SEO监控**：使用Google Search Console跟踪收录
4. **性能监控**：检查页面加载速度

### 内容定制
1. **修改组件**：编辑components/目录下的文件
2. **更新样式**：修改style.css
3. **添加页面**：在pages/目录创建新HTML文件
4. **调整导航**：修改components/nav.html

### 故障排除
1. **SPA不工作**：检查spa.js是否正确加载
2. **样式问题**：检查CSS文件路径
3. **文章不生成**：检查Python脚本依赖
4. **部署失败**：检查Cloudflare Pages日志

## 依赖项
- Python 3.6+
- markdown库：`pip install markdown`
- Git
- Cloudflare Pages账户

## 许可证
仅供金边会所导航项目使用

## 更新日志
- 2026-04-20：初始版本，完整重构
- 包含：SPA导航、黑金主题、SEO优化、自动化脚本