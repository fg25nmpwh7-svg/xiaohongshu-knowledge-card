# -*- coding: utf-8 -*-
import os, subprocess, html

OUT = r"D:\PYT\project\project-\exports"
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PREFIX = "0617-"

NAVY="#0F1A33"; BLUE="#2563EB"; ACC="#5B9BFF"; WHITE="#FFFFFF"
DIM="#AEB8CC"; TINT="#C7DAFF"; LINE="rgba(91,155,255,.28)"
FONT = "'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif"

def esc(s): return html.escape(s).replace("\n","<br>")

BASE = f"""<!doctype html><html><head><meta charset=utf-8>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px}}
.card{{width:1080px;height:1440px;padding:100px 90px;font-family:{FONT};
  position:relative;overflow:hidden;display:flex;flex-direction:column}}
.eyebrow{{font-size:28px;font-weight:700;letter-spacing:5px;margin-bottom:24px}}
.title{{font-weight:800;line-height:1.1;color:{WHITE}}}
.intro{{font-size:32px;font-weight:500;line-height:1.48;margin-top:28px}}
.pt{{margin-top:0}}
.num{{font-size:28px;font-weight:800;color:{ACC};margin-bottom:10px}}
.judge{{font-size:44px;font-weight:700;color:{WHITE};line-height:1.2}}
.sup{{font-size:30px;font-weight:400;color:{DIM};line-height:1.45;margin-top:12px}}
.quote{{font-size:44px;font-weight:800;color:{ACC};line-height:1.25}}
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
  eyebrow="AI 产品经理 · 数据基础",
  title="关于数据的 6 个概念\nAI产品经理必须搞懂",
  lst=["数据库找关键词，向量数据库找意思",
       "大模型不联知识库，就会瞎编",
       "每个系统单独接入，Agent 会被累死",
       "Agent 不存数据，是个调度员",
       "企业数据不只是表格，数据湖因此出现",
       "数据库存数据，数据仓库看数据"])

items="".join(
  f'<div style="display:flex;gap:26px;align-items:flex-start;margin-bottom:26px">'
  f'<div style="font-size:32px;font-weight:800;color:{TINT};min-width:46px">{i+1:02d}</div>'
  f'<div style="font-size:38px;font-weight:700;color:{WHITE};line-height:1.28">{esc(t)}</div></div>'
  for i,t in enumerate(header["lst"]))

hbody=(f'<div class="card" style="background:{BLUE}">'
  f'<div class="bar"></div>'
  f'<div class="eyebrow" style="color:{TINT}">{esc(header["eyebrow"])}</div>'
  f'<div class="title" style="font-size:82px;line-height:1.14">{esc(header["title"])}</div>'
  f'<div style="margin-top:52px">{items}</div>'
  f'<div style="margin-top:auto;font-size:30px;font-weight:500;color:{TINT}">← 左滑逐条看</div>'
  f'</div>')

# ---- 6 张内容卡：按吸引眼球程度排序 ----
cards=[
 dict(eyebrow="向量数据库 · 01",
   title="数据库找关键词\n向量数据库找意思",
   intro="传统数据库只能精确匹配关键词，但 AI 需要「听懂」用户说的话——这就是向量数据库存在的理由。",
   pts=[("传统数据库不懂「意思」",
         "你问「休假最长多久」，但规定写的是「年假最多15天」——关键词对不上，数据库直接返回空"),
        ("文本要先变成向量再存储",
         "Embedding 把文字转成一串数字（向量），语义相近的内容在数学空间里距离也近，才能做相似度搜索"),
        ("AI 知识库靠它运转",
         "企业把规章制度、产品文档存进向量数据库，用户提问时先在这里找相关内容，再交给大模型回答")],
   quote="数据库找关键词，向量数据库找意思"),

 dict(eyebrow="RAG 检索增强生成 · 02",
   title="大模型不联知识库\n就会瞎编",
   intro="RAG（检索增强生成）解决的是大模型「不知道你的私有信息」这个根本问题。",
   pts=[("没有 RAG，大模型靠记忆猜",
         "你问「公司消防疏散距离是多少」，大模型只能靠训练数据猜，很可能给出错的数字"),
        ("有 RAG，先检索原文再回答",
         "用户提问→转向量→向量数据库找到消防规范PDF→把原文内容附给大模型→生成准确答案"),
        ("向量数据库是 RAG 的检索引擎",
         "RAG = 检索 + 大模型，向量数据库承担「检索」这一环，找不准则答案必然偏")],
   quote="RAG 让大模型有据可查，不再靠猜"),

 dict(eyebrow="MCP · AI 世界的 USB 接口 · 03",
   title="每个系统单独接入\nAgent 会被累死",
   intro="MCP（Model Context Protocol）解决的是「Agent 如何统一接入企业各种工具」这个工程问题。",
   pts=[("没有 MCP，每个系统写一套接口",
         "连 ERP 写一套、连 CRM 再写一套、连飞书又写一套——系统一多，维护成本指数级上涨"),
        ("有了 MCP，一次开发多模型复用",
         "ERP、CRM、飞书各自做成 MCP Server，Agent 统一通过 MCP 接入，换了模型不用重写"),
        ("还统一管权限和上下文",
         "谁能访问什么数据、文档/数据库/API 怎么暴露给 Agent，都由 MCP 层集中管理")],
   quote="MCP 是 AI 世界的 USB 接口，插上即用"),

 dict(eyebrow="Agent 与企业数据 · 04",
   title="Agent 不存数据\n是个调度员",
   intro="大模型本身看不到任何企业数据，Agent 的价值在于「知道去哪儿拿数据」——而不是自己存着。",
   pts=[("大模型训练数据里没有你的业务",
         "你问 GPT「今天有几个待审批项目」，它根本不知道，因为你们公司数据从未进入它的训练集"),
        ("Agent 通过工具调用企业系统",
         "用户提问→Agent 判断调哪个接口→调用 OA 系统 API→拿到审批列表→总结结果返回"),
        ("工具边界就是能力边界",
         "Agent 能访问哪些数据、执行哪些操作，完全取决于它被授权调用哪些工具，不授权就什么都看不见")],
   quote="Agent 不是数据库，是调度员"),

 dict(eyebrow="数据湖 · 05",
   title="企业数据不只是表格\n数据湖因此出现",
   intro="数仓很好用，但只能处理结构化的表格数据——当企业有了 PDF、视频、日志、录音，数仓就放不下了。",
   pts=[("非结构化数据无法直接进数仓",
         "用户合同（PDF）、客服录音（MP3）、监控日志（txt），这些都不是「表格」，数仓没法直接存和分析"),
        ("数据湖的核心思想是先存再分析",
         "什么格式都接受、先全部存进来，等后续有分析需求再处理——成本低、不会丢原始数据"),
        ("数据湖和数仓在企业里并存",
         "原始数据→数据湖；清洗后的结构化数据→数仓供 BI 分析；两者互补，不是谁替代谁")],
   quote="数据仓库是精装修，数据湖是大仓库"),

 dict(eyebrow="数据基础概念 · 06",
   title="数据库存数据\n数据仓库看数据",
   intro="这是 AI 产品经理最基础也最容易混淆的概念——两者不是竞争关系，而是流水线上的不同环节。",
   pts=[("数据库服务实时业务",
         "用户下单→写入数据库→用户查询订单状态，MySQL/PostgreSQL 支撑的是每天千万次的增删改查"),
        ("数据仓库服务管理决策",
         "老板问「过去一年哪个城市收入最高」，数据库查这种聚合很慢，数仓专门为大量统计分析优化"),
        ("ETL 把数据库数据搬进数仓",
         "订单记录每天定时通过 ETL 流程清洗、转化、加载进数仓，再供 BI 工具出报表给老板看")],
   quote="数据库记账，数据仓库出报表"),
]

def card_html(c):
    pts="".join(
      f'<div class="pt" style="margin-top:{0 if i==0 else 38}px">'
      f'<div class="num">{i+1:02d}</div>'
      f'<div class="judge">{esc(j)}</div>'
      f'<div class="sup">{esc(s)}</div></div>'
      for i,(j,s) in enumerate(c["pts"]))
    return (f'<div class="card" style="background:{NAVY}">'
      f'<div class="eyebrow" style="color:{ACC};letter-spacing:6px">{esc(c["eyebrow"])}</div>'
      f'<div class="title" style="font-size:74px">{esc(c["title"])}</div>'
      f'<div class="intro" style="color:{DIM}">{esc(c["intro"])}</div>'
      f'<div style="margin-top:44px">{pts}</div>'
      f'<div style="margin-top:auto">'
      f'<div style="height:2px;background:{LINE};margin-bottom:36px"></div>'
      f'<div class="quote">{esc(c["quote"])}</div></div>'
      f'</div>')

jobs=[(PREFIX+"00-头图", hbody)]
for i,c in enumerate(cards):
    tag = c['eyebrow'].split(' · ')[0].replace('/','-')
    jobs.append((f"{PREFIX}{i+1:02d}-{tag}", card_html(c)))

for name, body in jobs:
    hp=write_html(name, body)
    shoot(hp, name+".png")
    print("OK", name+".png")
print("DONE")
