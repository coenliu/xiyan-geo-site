# 栖妍研究内容站点

这是一个独立的 public 仓库，通过 GitHub Pages 发布。它和私有研究仓库 `real_GEO`
是两个完全独立的 git 历史——本仓库只包含要公开发布的文章和建站代码，不包含任何
采集数据、评分逻辑或 API 密钥。

内容来源：`real_GEO` 仓库里 `scripts/promote_articles_to_site.py` 从本地研究产物
（AutoGEO 规则改写后的 target_doc）导出到本仓库的 `content/` 目录。

本站内容为品牌研究草案，非最终配方、备案或功效宣称。

## 结构

```
content/       # 导出的文章（front matter + 正文）
templates/     # 页面模板
static/        # CSS
build.py       # content/*.md -> 根目录下的 *.html（无第三方依赖）
```

## 本地构建

```bash
python build.py
```

生成的 `index.html`、`<slug>.html` 直接提交到仓库根目录。

## 部署

GitHub 仓库设置 → Pages → Build and deployment source 选 "Deploy from a
branch"，分支选 `main`，目录选 `/ (root)`。push 到 `main` 即自动生效，无需
GitHub Actions。
