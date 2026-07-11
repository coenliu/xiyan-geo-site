# 图片命名规则

把找到的图片按下表文件名存进这个目录，`python build.py` 会自动检测并替换掉对应的
虚线占位框——不需要改代码，也不需要告诉我。支持 `.jpg` / `.jpeg` / `.png` /
`.webp`，四选一即可（选中哪个都行，文件名主干必须完全一致）。

| 文件名（不含扩展名） | 对应内容 |
| --- | --- |
| `hero` | 首页大图（产品图） |
| `ingredient-ergothioneine` | 麦角硫因 |
| `ingredient-astaxanthin` | 虾青素 |
| `ingredient-carnosine` | 肌肽 / 脱羧肌肽 |
| `ingredient-niacinamide` | 烟酰胺 |
| `ingredient-panthenol` | 泛醇（维生素B5） |
| `ingredient-ectoin` | 依克多因 |

例：找到产品图后存成 `hero.jpg`，放进这个目录，跑一次 `python build.py`，首页
hero 图就会自动换成这张图。哪几个先放齐都没关系，没放的会继续显示占位框。
