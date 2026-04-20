# Cloudflare Pages 重新配置指南

## 当前问题
Cloudflare Pages 错误地将项目识别为 "静态网站 + Workers"，尝试运行 `npx wrangler deploy`，导致构建失败。

## 根本原因
Cloudflare Pages 缓存了错误的项目类型配置。

## 解决方案
**删除现有 Cloudflare Pages 项目，重新创建：**

### 步骤：
1. **访问** https://dash.cloudflare.com/
2. **进入** `Pages` → `ygsme-seo-website` 项目
3. **点击** `设置` → `常规`
4. **滚动到底部**，点击 `删除项目`
5. **确认删除**

### 重新创建项目：
1. **回到 Pages 主页**
2. **点击** `创建项目`
3. **选择** `直接上传`（不要选GitHub）
4. **项目名称**：`ygsme-seo-website`
5. **生产分支**：`main`
6. **构建设置**：
   - **构建命令**：留空
   - **构建输出目录**：`.`（点号）
   - **根目录**：`.`（点号）
7. **点击** `保存并部署`

### 或者使用 GitHub 连接：
1. **创建项目时选择** `连接到 Git`
2. **选择仓库**：`KKKyyyss2/ygsme-seo-website`
3. **构建设置保持默认**（留空）

## 验证
部署完成后，访问：
- https://xko1.com
- https://xko1.com/gao-duan

应该看到新版本的网站。

## 备选方案
如果还是失败，可以：
1. **使用 Wrangler CLI 手动部署**：
   ```bash
   npm install -g wrangler
   wrangler pages deploy . --project-name=ygsme-seo-website
   ```
2. **联系 Cloudflare 支持**

## 注意事项
- 删除项目不会影响域名绑定
- 重新创建后需要等待 DNS 传播（几分钟）