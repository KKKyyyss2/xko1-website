/**
 * 金边会所导航 - SPA导航系统
 * 无刷新页面切换，保持URL清洁，支持前进/后退
 */

(function() {
    'use strict';
    
    // 配置
    const CONFIG = {
        containerId: 'spa-container',
        loadingClass: 'spa-loading',
        navActiveClass: 'active',
        defaultPage: 'index',
        articlePathPrefix: '/article-',
        articleFilePrefix: '/articles/article-',
        fileExtension: '.html'
    };
    
    // 状态管理
    const state = {
        currentPage: CONFIG.defaultPage,
        isLoading: false,
        history: [],
        cache: new Map()
    };
    
    // DOM元素
    const elements = {
        container: null,
        loading: null,
        navLinks: []
    };
    
    /**
     * 初始化SPA系统
     */
    function init() {
        console.log('🔧 SPA系统初始化...');
        
        // 获取DOM元素
        elements.container = document.getElementById(CONFIG.containerId);
        elements.loading = document.querySelector(`.${CONFIG.loadingClass}`);
        elements.navLinks = document.querySelectorAll('.nav-link[data-page]');
        
        if (!elements.container) {
            console.error('❌ 找不到SPA容器:', CONFIG.containerId);
            return;
        }
        
        // 绑定导航点击事件
        elements.navLinks.forEach(link => {
            link.addEventListener('click', handleNavClick);
        });
        
        // 绑定文章卡片点击事件（委托）
        document.addEventListener('click', handleArticleClick);
        
        // 监听浏览器前进/后退
        window.addEventListener('popstate', handlePopState);
        
        // 初始加载当前页面
        const initialPath = window.location.pathname;
        if (initialPath === '/' || initialPath === '') {
            loadPage(CONFIG.defaultPage);
        } else {
            const page = pathToPage(initialPath);
            loadPage(page, initialPath, false); // 不推历史记录
        }
        
        console.log('✅ SPA系统就绪');
    }
    
    /**
     * 处理导航点击
     */
    function handleNavClick(event) {
        event.preventDefault();
        
        const link = event.currentTarget;
        const page = link.getAttribute('data-page');
        const path = `/${page === 'index' ? '' : page}`;
        
        // 更新导航状态
        updateNavActive(page);
        
        // 加载页面
        loadPage(page, path, true);
    }
    
    /**
     * 处理文章卡片点击
     */
    function handleArticleClick(event) {
        const card = event.target.closest('.article-card');
        if (!card) return;
        
        const readMoreBtn = event.target.closest('.read-more');
        if (!readMoreBtn) return;
        
        event.preventDefault();
        
        const articleSlug = readMoreBtn.getAttribute('data-slug');
        if (!articleSlug) return;
        
        // 文章路径格式: /article-YYYYMMDD-slug
        const articlePath = `${CONFIG.articlePathPrefix}${articleSlug}`;
        
        // 加载文章页
        loadArticle(articleSlug, articlePath, true);
    }
    
    /**
     * 处理浏览器前进/后退
     */
    function handlePopState(event) {
        const path = window.location.pathname;
        const page = pathToPage(path);
        
        updateNavActive(page);
        loadPage(page, path, false);
    }
    
    /**
     * 加载页面
     */
    async function loadPage(page, path = null, pushHistory = true) {
        if (state.isLoading || state.currentPage === page) return;
        
        state.isLoading = true;
        state.currentPage = page;
        
        // 显示加载状态
        showLoading(true);
        
        // 确定文件路径
        let filePath;
        if (page.startsWith('article-')) {
            // 文章页
            filePath = `${CONFIG.articleFilePrefix}${page}${CONFIG.fileExtension}`;
        } else if (page === 'index') {
            // 首页
            filePath = `/index${CONFIG.fileExtension}`;
        } else {
            // 静态页面
            filePath = `/pages/${page}${CONFIG.fileExtension}`;
        }
        
        // 使用路径或生成路径
        path = path || (page === 'index' ? '/' : `/${page}`);
        
        try {
            // 检查缓存
            let content;
            if (state.cache.has(filePath)) {
                content = state.cache.get(filePath);
                console.log('📦 使用缓存:', filePath);
            } else {
                // 获取页面内容
                const response = await fetch(filePath);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                content = await response.text();
                
                // 缓存内容
                state.cache.set(filePath, content);
            }
            
            // 提取主要内容（spa-container内的内容）
            const parser = new DOMParser();
            const doc = parser.parseFromString(content, 'text/html');
            const newContent = doc.getElementById(CONFIG.containerId)?.innerHTML;
            
            if (!newContent) {
                throw new Error('页面中找不到SPA容器内容');
            }
            
            // 更新页面内容
            elements.container.innerHTML = newContent;
            
            // 更新页面标题
            const newTitle = doc.querySelector('title')?.textContent || document.title;
            document.title = newTitle;
            
            // 更新URL（如果需要）
            if (pushHistory) {
                window.history.pushState({ page, path }, '', path);
                state.history.push({ page, path });
            }
            
            // 滚动到顶部（保持平滑）
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            console.log(`✅ 页面加载完成: ${page}`);
            
        } catch (error) {
            console.error('❌ 页面加载失败:', error);
            showError(`页面加载失败: ${page}`);
        } finally {
            // 隐藏加载状态
            showLoading(false);
            state.isLoading = false;
            
            // 重新绑定新内容中的事件
            rebindEvents();
        }
    }
    
    /**
     * 加载文章页（专用函数）
     */
    async function loadArticle(articleSlug, path, pushHistory = true) {
        await loadPage(articleSlug, path, pushHistory);
    }
    
    /**
     * 更新导航激活状态
     */
    function updateNavActive(page) {
        elements.navLinks.forEach(link => {
            const linkPage = link.getAttribute('data-page');
            if (linkPage === page || (page.startsWith('article-') && linkPage === 'index')) {
                link.classList.add(CONFIG.navActiveClass);
            } else {
                link.classList.remove(CONFIG.navActiveClass);
            }
        });
    }
    
    /**
     * 显示/隐藏加载状态
     */
    function showLoading(show) {
        if (elements.loading) {
            elements.loading.classList.toggle('active', show);
        }
        
        if (show) {
            elements.container.style.opacity = '0.5';
        } else {
            elements.container.style.opacity = '1';
        }
    }
    
    /**
     * 显示错误信息
     */
    function showError(message) {
        elements.container.innerHTML = `
            <div class="page-header">
                <h1>加载失败</h1>
                <p class="description">${message}</p>
                <a href="/" class="back-home" data-page="index">
                    ← 返回首页
                </a>
            </div>
        `;
    }
    
    /**
     * 重新绑定事件（新加载内容中的交互元素）
     */
    function rebindEvents() {
        // 重新绑定返回首页按钮
        const backButtons = document.querySelectorAll('.back-home[data-page]');
        backButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const page = this.getAttribute('data-page');
                updateNavActive(page);
                loadPage(page, page === 'index' ? '/' : `/${page}`, true);
            });
        });
        
        // 重新绑定文章内的导航链接
        const articleNavLinks = elements.container.querySelectorAll('.nav-link[data-page]');
        articleNavLinks.forEach(link => {
            link.addEventListener('click', handleNavClick);
        });
    }
    
    /**
     * 路径转换为页面标识
     */
    function pathToPage(path) {
        if (path === '/' || path === '') return 'index';
        if (path.startsWith(CONFIG.articlePathPrefix)) {
            return path.substring(1); // 去掉开头的/
        }
        return path.substring(1); // 去掉开头的/
    }
    
    /**
     * 预加载页面（性能优化）
     */
    function preloadPages() {
        const pagesToPreload = ['gao-duan', 'bi-keng', 'ji-shi', 'jia-ge', 'xin-shou', 'faq'];
        
        pagesToPreload.forEach(page => {
            const filePath = `/pages/${page}${CONFIG.fileExtension}`;
            fetch(filePath).then(response => {
                if (response.ok) {
                    return response.text();
                }
            }).then(content => {
                if (content) {
                    state.cache.set(filePath, content);
                    console.log(`📦 预加载完成: ${page}`);
                }
            }).catch(() => {
                // 静默失败
            });
        });
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // 空闲时预加载其他页面
    if ('requestIdleCallback' in window) {
        window.requestIdleCallback(() => {
            setTimeout(preloadPages, 1000);
        });
    } else {
        setTimeout(preloadPages, 3000);
    }
    
    // 暴露API（可选）
    window.SPANavigator = {
        loadPage,
        loadArticle,
        clearCache: () => state.cache.clear(),
        getCurrentPage: () => state.currentPage
    };
    
})();