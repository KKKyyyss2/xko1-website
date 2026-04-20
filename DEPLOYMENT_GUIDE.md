# Cloudflare Pages 部署说明

## 问题
Cloudflare Pages 检测到这是 "静态网站 + Workers" 项目，尝试运行 `npx wrangler deploy`，导致构建失败。

## 解决方案
**必须在 Cloudflare Pages 控制台手动配置：**

### 步骤：
1. 访问 https://dash.cloudflare.com/
2. 进入 `Pages` → `ygsme-seo-website` 项目
3. 点击 `设置` → `构建设置`
4. 修改以下配置：
   - **构建命令**：留空（删除原来的 `npx wrangler deploy`）
   - **构建输出目录**：`.`（点号，表示根目录）
   - **根目录**：`.`（点号，表示根目录）
5. 点击 `保存`
6. 点击 `重新构建`

### 或者通过 Cloudflare CLI：
```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 配置 Pages 项目
wrangler pages project update ygsme-seo-website \
  --production-branch=main \
  --build-command="" \
  --output-directory="."
```

## 验证部署
配置完成后，访问：
- https://xko1.com
- https://xko1.com/gao-duan
- https://xko1.com/sitemap.xml

应该看到新版本的网站。

## 如果还是失败
1. 清除 Cloudflare 缓存
2. 等待 5-10 分钟
3. 检查构建日志