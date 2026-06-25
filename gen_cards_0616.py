# -*- coding: utf-8 -*-
import os, subprocess, html

OUT = r"D:\PYT\project\project-\exports"
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PREFIX = "0616-"

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

# ---- 头图：按吸引力排序的 5 条目录 ----
header = dict(
  eyebrow="AI 产品 · 认知升级",
  title="关于 Agent 和 MCP\n你可能还没分清楚",
  lst=["100个工具喂给AI，性能反而崩了","Agent不是软件，是员工",
       "提示词的时代，正在结束","大厂买MCP，买的是安全感",
       "MCP管工具，A2A管同事"])

items="".join(
  f'<div style="display:flex;gap:28px;align-items:flex-start;margin-bottom:30px">'
  f'<div style="font-size:34px;font-weight:800;color:{TINT};min-width:48px">{i+1:02d}</div>'
  f'<div style="font-size:42px;font-weight:700;color:{WHITE};line-height:1.25">{esc(t)}</div></div>'
  for i,t in enumerate(header["lst"]))

hbody=(f'<div class="card" style="background:{BLUE}">'
  f'<div class="bar"></div>'
  f'<div class="eyebrow" style="color:{TINT}">{esc(header["eyebrow"])}</div>'
  f'<div class="title" style="font-size:90px;line-height:1.16">{esc(header["title"])}</div>'
  f'<div style="margin-top:64px">{items}</div>'
  f'<div style="margin-top:auto;font-size:32px;font-weight:500;color:{TINT}">← 左滑逐条看</div>'
  f'</div>')

# ---- 5 张内容卡：已按吸引眼球程度从强到弱排序 ----
cards=[
 dict(eyebrow="MCP 规模化 · 工程问题 · 01", title="100个工具喂给AI\n性能反而崩了",
   intro="给 Agent 接的工具越多本该越强，但企业一旦接入上百个 MCP 工具，结果常常是变慢变贵还变笨。",
   pts=[("全塞进 Prompt 是反模式","把 100 个工具的说明书全部塞进每次对话的提示词里，Token 暴涨、成本暴涨，回答反而变慢变差"),
        ("按需加载才是正解","Dynamic Tool Loading：不再一次性塞满，而是这次任务需要什么工具，才临时加载什么工具"),
        ("Router 替你提前筛选","Tool Router 像前台：先看你问题是什么，从 100 个工具里只挑出 3 个相关的交给 Agent，剩下 97 个不打扰")],
   quote="Agent的难点，正从模型变成上下文管理"),
 dict(eyebrow="AI 产品认知升级 · 02", title="Agent不是软件\n是员工",
   intro="很多人把 Agent 当成一款具体软件，但从 ChatGPT 到 OpenClaw，其实是同一条能力升级链路上的不同阶段。",
   pts=[("从单助手到自主执行","ChatGPT 是 Copilot（你问它答），Claude Code 是 Coding Agent（能自己写代码、跑测试），自主程度一路升级"),
        ("从单兵到团队协作","OpenAI Agent 是通用 Agent，OpenClaw 把多个 Agent 组织成 Agent Team，像一个真正的团队在分工"),
        ("A2A 是同事间的沟通","A2A（Agent-to-Agent）协议负责 Agent 之间怎么对话、怎么分工，这是传统软件产品里完全没有的概念")],
   quote="Agent更像员工，而不是软件"),
 dict(eyebrow="AI 产品趋势 · 范式转移 · 03", title="提示词的时代\n正在结束",
   intro="LangGraph、Dify、MCP、A2A、Claude Code 这些反复出现的关键词，背后是同一个趋势：拼的不再是一句神奇 Prompt。",
   pts=[("拼工程能力，不拼一句话","以前比谁的 Prompt 写得巧，现在比谁能把上下文工程、工作流工程、Agent 工程搭得稳"),
        ("壁垒变成系统设计能力","真正难复制的是 Workflow 设计、Agent 架构、Context Engineering，不是某一句提示词"),
        ("岗位也在悄悄转型","从「写提示词的人」变成「设计工作流和Agent架构的人」，title 没变但活儿完全不同")],
   quote="AI产品正从提示词时代，进入系统工程时代"),
 dict(eyebrow="企业级 MCP · 私有生态 · 04", title="大厂买MCP\n买的是安全感",
   intro="公共 MCP Registry 工具又多又能直接用，但很多企业宁愿自己重新搭一套私有版本，图什么？",
   pts=[("公共生态用着方便却不放心","公共 Registry 工具多、开箱即用，但来源不可信、稳不稳定说不准、权限也管不住"),
        ("私有生态换的是可控","企业私有 Registry 慢一点、贵一点，但安全、可审计、权限可治理"),
        ("按系统拆成独立模块","CRM MCP、OA MCP、ERP MCP、知识库 MCP 分开管，出问题能精确定位到哪一块")],
   quote="企业买的不是工具，而是安全感"),
 dict(eyebrow="概念辨析 · MCP vs A2A · 05", title="MCP管工具\nA2A管同事",
   intro="MCP 和 A2A 都是 Agent 领域的协议名词，很多人会混在一起，其实管的是两件完全不同的事。",
   pts=[("MCP解决人和工具的连接","Agent ↔ Tool：调数据库、调天气API、调CRM、调企业系统，靠的都是 MCP"),
        ("A2A解决人和人的协作","Agent ↔ Agent：多个 Agent 之间怎么分工、怎么通信、怎么协作完成任务，靠的是 A2A"),
        ("经典架构两条线并存","Claude Code 走 MCP 调各种工具；多个 Agent 之间走 A2A 协同完成任务，两条线互不替代")],
   quote="MCP管工具，A2A管同事"),
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
      f'<div class="title" style="font-size:76px">{esc(c["title"])}</div>'
      f'<div class="intro" style="color:{DIM}">{esc(c["intro"])}</div>'
      f'<div style="margin-top:48px">{pts}</div>'
      f'<div style="margin-top:auto">'
      f'<div style="height:2px;background:{LINE};margin-bottom:40px"></div>'
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
