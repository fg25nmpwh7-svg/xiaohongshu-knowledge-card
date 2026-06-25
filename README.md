# 小红书知识卡片生成器

Python 脚本，批量生成适合小红书发布的知识卡片图片（1080×1440 PNG）。以 AI 产品相关内容为主，风格为深蓝色系，强观点、判断句。

## 输出示例

- 「关于 AI 产品选型，你可能一直想错了」
- 「AI 笔记工具的护城河在哪里」
- 每组卡片包含头图 + 多张内容卡，适合直接发布为图文笔记

## 工作原理

1. Python 用字符串模板生成 HTML（内嵌 CSS，1080×1440 固定尺寸）
2. 调用 Microsoft Edge headless 渲染 HTML 并截图为 PNG
3. 所有图片输出到 `exports/` 目录

## 依赖

- Python 3.x（标准库，无第三方依赖）
- Microsoft Edge（`msedge.exe`，路径在脚本顶部配置）

## 使用

```bash
python gen_cards.py
```

输出文件在 `exports/` 目录，同时保留对应 `.html` 中间文件便于调试。
