# 天王寺 · 生活口袋指南

面向中国学生与家长的独立中文静态网站，主题为大阪市立天王寺中学校；对比大阪市立阿倍野中学校、高津中学校。非学校官方网站。

## 本地开发

无需 npm、构建框架或外部字体。直接打开 `index.html`，或：

```sh
python3 -m http.server 8000
```

打开 http://localhost:8000 。所有页面正文均在 HTML 内，关闭 JavaScript 仍可阅读；JS 只提供口语搜索与打印按钮。

## 内容与文件

- `scripts/build.py`：页面内容、模板、来源目录与规模图表的维护入口。
- `assets/css/style.css`：响应式排版、打印和减少动画偏好。
- `assets/js/main.js`：口语筛选与打印。
- `data/schools.json`：生成的来源化规模数据，未知人数及升学率为 null。
- `sources.html`：公开来源、日期和数据口径。
- `.github/workflows/pages.yml`：GitHub Actions 发布配置。

修改模板后运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
```

校验检查输出一致性、本地链接、片段链接和年级人数合计。外部链接与事实需人工核验；校验不保证外部网站一直可访问。

## GitHub Pages

在新仓库根目录放置本项目内容（不要多套一层目录）。默认发布分支 `main`。

推荐：Settings → Pages → Source 选择 **GitHub Actions**，推送后由工作流检查并发布。工作流只打包 HTML、assets、data 及 .nojekyll，不发布开发文档。

也支持无 Actions 部署：Settings → Pages → Deploy from a branch → `main` / `(root)`。手动更新时不要删除 assets 或遗漏页面。

项目网址格式：`https://<用户名>.github.io/tennoji-school-guide/`。只在确认部署成功后对外传播。

## 内容更新规则

1. 使用学校、区役所、大阪市与大阪府的原始资料，给出年度与链接。
2. 三校人数用同一日期；特别支援班与普通班分列。
3. 不把中国籍、中文母语、外国籍或需日语指导学生混为同一指标。
4. 未取得数据保留 null，不能画成0；没有同届完整分子、分母，不计算升学率。
5. 历史活动写明年份，勿当作未来活动预告。
6. 不上传可识别个别未成年学生的资料。

学校统计资料来源：大阪市教育委员会，2025-05-01学校现况调查，按原页面 CC BY 4.0 标识署名；本站图表为整理重绘。其他链接资料权利归原发布方。原创源码暂无另行授权许可。
