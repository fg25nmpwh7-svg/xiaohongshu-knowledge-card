# -*- coding: utf-8 -*-
import os, subprocess, html

OUT = r"D:\PYT\project\project-\exports"
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

NAVY="#0F1A33"; BLUE="#2563EB"; ACC="#5B9BFF"; WHITE="#FFFFFF"
DIM="#AEB8CC"; TINT="#C7DAFF"; LINE="rgba(91,155,255,.28)"
FONT = "'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif"

def esc(s): return html.escape(s).replace("\n","<br>")

BASE = f"""<!doctype html><html><head><meta charset=utf-8>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px}}
.card{{width:1080px;height:1440px;padding:104px 90px;font-family:{FONT};
  position:relative;overflow:hidden;display:flex;flex-direction:column}}
.eyebrow{{font-size:28px;font-weight:700;letter-spacing:5px;margin-bottom:26px}}
.title{{font-weight:800;line-height:1.1;color:{WHITE}}}
.intro{{font-size:33px;font-weight:500;color:{TINT};line-height:1.45;margin-top:30px}}
.pt{{margin-top:0}}
.num{{font-size:28px;font-weight:800;color:{ACC};margin-bottom:10px}}
.judge{{font-size:46px;font-weight:700;color:{WHITE};line-height:1.2}}
.sup{{font-size:31px;font-weight:400;color:{DIM};line-height:1.42;margin-top:14px}}
.quote{{font-size:46px;font-weight:800;color:{ACC};line-height:1.25}}
.bar{{width:100px;height:10px;border-radius:6px;background:{WHITE};margin-bottom:34px}}
</style></head><body>{{body}}</body></html>"""

def write_html(name, body):
    p = os.path.join(OUT, name+".html")
    with open(p,"w",encoding="utf-8") as f: f.write(BASE.replace("{body}",body))
    return p

def shoot(htmlpath, png):
    subprocess.run([EDGE,"--headless=new","--disable-gpu","--hide-scrollbars",
        "--force-device-scale-factor=1","--window-size=1080,1440",
        f"--screenshot={os.path.join(OUT,png)}", "file:///"+htmlpath.replace('\\','/')],
        check=True, timeout=60)

# ---- 头图 ----
header = dict(
  eyebrow="AI 产品 · 反直觉认知",
  title="关于 AI 产品选型\n你可能一直想错了",
  lst=["选 AI 工具，先别比功能强弱","自主性越高，质量就越好？错",
       "同样做 AI 笔记，护城河天差地别","别再为 AI 造一个新 App 了",
       "上 Agent 前，先别碰技术选型"])

items="".join(
  f'<div style="display:flex;gap:28px;align-items:flex-start;margin-bottom:30px">'
  f'<div style="font-size:34px;font-weight:800;color:{TINT};min-width:48px">{i+1:02d}</div>'
  f'<div style="font-size:42px;font-weight:700;color:{WHITE};line-height:1.25">{esc(t)}</div></div>'
  for i,t in enumerate(header["lst"]))

hbody=(f'<div class="card" style="background:{BLUE}">'
  f'<div class="bar"></div>'
  f'<div class="eyebrow" style="color:{TINT}">{esc(header["eyebrow"])}</div>'
  f'<div class="title" style="font-size:96px;line-height:1.16">{esc(header["title"])}</div>'
  f'<div style="margin-top:64px">{items}</div>'
  f'<div style="margin-top:auto;font-size:32px;font-weight:500;color:{TINT}">← 左滑逐条看</div>'
  f'</div>')

cards=[
 dict(eyebrow="AI 编程助手选型 · 01", title="选 AI 工具\n先别比功能强弱",
   intro="Claude Code、Codex、OpenClaw 都是 AI 编程助手，差别在「跑在哪」和「多自主」。",
   pts=[("大院要并发与合规","大型设计院几十人同时用、数据不能出内网，选自托管多智能体：部署在自家服务器，多个 AI 分工协作"),
        ("中型所要效率与交付","中型事务所人少活急，选云端自主执行：托管在云端、AI 自己跑完整个任务，省运维又出活快"),
        ("小团队要可控低运维","小团队没人专门维护，选本地被动响应：装在本机、你问一句它答一句，功能够用、不怕跑不动")],
   quote="选型不是比功能，是比匹配"),
 dict(eyebrow="AI 产品横向对比 · 02", title="自主性越高\n质量就越好？错",
   intro="Munus、CC、Coze 是三款 AI 智能体产品，常被拿来比「谁更能自己干活」。",
   pts=[("高自主 ≠ 高质量","Munus 自己跑得最顺、输出最漂亮，但只支持海外平台，国内场景根本用不了"),
        ("黑盒过程伤可用性","Coze 能调度多个工具，但你看不到它中间怎么做的，还会把中英文内容混排，得返工"),
        ("可信度看内容识别","CC 自主性中等，却能识别并过滤掉软文广告，给你的信息更干净、更可信")],
   quote="高自主，不等于高质量"),
 dict(eyebrow="AI 知识管理 · 03", title="同样做 AI 笔记\n护城河天差地别",
   intro="NotebookLM（Google）和 IMA（腾讯）都是 AI 知识管理工具，却走了两条路。",
   pts=[("一个走工具深度","NotebookLM 升级 Gemini 3.5 + 代码执行，从「文档问答」变成能跑分析的研究助手"),
        ("一个走生态关系","IMA 用四层记忆记住你的习惯、越用越懂你，还能直接读微信里的文章和公众号"),
        ("护城河看入口","真正的壁垒不是功能，是 IMA 背靠微信、拿得到别人拿不到的内容入口")],
   quote="护城河不在功能，在入口"),
 dict(eyebrow="AI Agent 交互设计 · 04", title="别再为 AI\n造一个新 App 了",
   intro="OpenClaw 是 2026 年爆火的开源个人 AI Agent，它偏偏没做新 App。",
   pts=[("新界面 = 迁移成本","让用户为 AI 专门学一个全新界面，等于在增长路上自己设了一道坎"),
        ("融入已有习惯","OpenClaw 不造新入口，直接嵌进你本来就在用的工具里，零迁移"),
        ("渠道无关架构","普通人用浏览器、开发者用终端、想聊天就用微信/飞书/Discord，哪儿顺手在哪儿用")],
   quote="别造新 App，嵌进旧习惯"),
 dict(eyebrow="企业级 Agent 选型 · 05", title="上 Agent 前\n先别碰技术选型",
   intro="以格林酒店集团上 Agent 为例，企业落地最容易把第一步做反。",
   pts=[("数据质量定生死","知识库数据脏，AI 就答得乱——数据决定 Agent 八成可用性，所以选型前先盘数据"),
        ("按部门划职责","一个 Agent 啥都干会「上下文爆炸」，该按客服、运营这些真实部门拆成多个"),
        ("生成自动、输出把关","AI 生成可以全自动，但对外输出的内容必须人工审一遍；见效快的部门先上")],
   quote="选型之前，先盘数据"),
]

def card_html(c):
    pts="".join(
      f'<div class="pt" style="margin-top:{0 if i==0 else 42}px">'
      f'<div class="num">{i+1:02d}</div>'
      f'<div class="judge">{esc(j)}</div>'
      f'<div class="sup">{esc(s)}</div></div>'
      for i,(j,s) in enumerate(c["pts"]))
    return (f'<div class="card" style="background:{NAVY}">'
      f'<div class="eyebrow" style="color:{ACC};letter-spacing:6px">{esc(c["eyebrow"])}</div>'
      f'<div class="title" style="font-size:78px">{esc(c["title"])}</div>'
      f'<div class="intro" style="color:{DIM}">{esc(c["intro"])}</div>'
      f'<div style="margin-top:48px">{pts}</div>'
      f'<div style="margin-top:auto">'
      f'<div style="height:2px;background:{LINE};margin-bottom:40px"></div>'
      f'<div class="quote">{esc(c["quote"])}</div></div>'
      f'</div>')

jobs=[("00-头图", hbody)]
for i,c in enumerate(cards):
    jobs.append((f"{i+1:02d}-{c['eyebrow'].split(' · ')[0].replace('/','-')}", card_html(c)))

for name, body in jobs:
    hp=write_html(name, body)
    shoot(hp, name+".png")
    print("OK", name+".png")
print("DONE")
