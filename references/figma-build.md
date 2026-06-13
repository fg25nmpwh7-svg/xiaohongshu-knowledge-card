# Figma 建图参考

`use_figma` 工具执行的是 Figma Plugin API 的 JavaScript（有 `figma` 全局对象）。下面是验证过的模板和必避的坑。

## 必避的 API 坑

| 坑 | 错误写法 | 正确写法 |
|---|---|---|
| 字体未加载 | 直接 `setCharacters` | 先 `await figma.loadFontAsync({family,style})` |
| 切页 | `figma.currentPage = page` | `await figma.setCurrentPageAsync(page)` |
| 全量加载页 | `figma.loadAllPagesAsync()` | 不支持，删掉 |
| 读其他 page 的 children | 直接 `page.children` 返回 `[]` | 先 `await figma.setCurrentPageAsync(page)` 再读 |
| 中文不显示 | 以为要装中文字体 | 用 `Inter` 即可，Figma 自动 CJK 回退；导出 PNG 中文正常 |

- `Inter` 字重写法注意空格：`Semi Bold`、`Extra Bold`（不是 `SemiBold`）。
- 每次 `use_figma` 调用都是全新插件上下文，`currentPage` 会重置回第一个 page，字体要重新 load。

## 准备文件

```
whoami            → 拿 plans[].key 作为 planKey
create_new_file   → fileName / planKey / editorType:"design"，返回 file_key
```
View 席位也能编辑自己 drafts 里的文件，能 create_new_file、use_figma、download_assets。

## 通用文字辅助函数（放在每段 use_figma 开头）

```js
const hex=h=>({r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255});
await Promise.all(['Regular','Medium','Semi Bold','Bold'].map(s=>figma.loadFontAsync({family:'Inter',style:s})));
const F=s=>({family:'Inter',style:s});
function txt(p,{x,y,w,s,font='Regular',color,t,lh=1.3,align='LEFT',sp=0}){
  const n=figma.createText();n.fontName=F(font);n.fontSize=s;n.textAutoResize='HEIGHT';
  n.x=x;n.y=y;n.resize(w,10);n.characters=t;n.fills=[{type:'SOLID',color}];
  n.textAlignHorizontal=align;n.lineHeight={value:s*lh,unit:'PIXELS'};
  if(sp)n.letterSpacing={value:sp,unit:'PERCENT'};p.appendChild(n);return n;
}
```

## 形态 B：发布会式单页卡（验证过，推荐起手）

纯黑底、蓝色点缀、判断句+支撑句两层。`cards` 数组里每项：`{eyebrow, title, points:[[判断句,支撑句]×3], quote}`。

```js
const W=1080,H=1440;
const BLACK=hex('#000000'),WHITE=hex('#FFFFFF'),DIM=hex('#B0B0B5'),GREY=hex('#86868B'),BLUE=hex('#2997FF');
// ...txt 辅助函数见上...
let page=figma.root.children.find(p=>p.name==='卡片页');
if(!page){page=figma.createPage();page.name='卡片页';}
await figma.setCurrentPageAsync(page);
[...page.children].forEach(c=>c.remove());   // 重做时清空，避免叠加

const made=[];
cards.forEach((c,i)=>{
  const f=figma.createFrame();f.resize(W,H);f.x=i*(W+120);f.y=0;f.name=`Card-${i+1}`;
  f.fills=[{type:'SOLID',color:BLACK}];f.clipsContent=true;page.appendChild(f);
  txt(f,{x:90,y:140,w:W-180,s:30,font:'Bold',color:BLUE,t:c.eyebrow,sp:18});
  txt(f,{x:90,y:212,w:W-180,s:100,font:'Bold',color:WHITE,t:c.title,lh:1.06});
  const startY=560,blockH=210;
  c.points.forEach((p,pi)=>{
    const y=startY+pi*blockH;
    txt(f,{x:90,y,w:60,s:30,font:'Bold',color:BLUE,t:String(pi+1).padStart(2,'0')});
    txt(f,{x:90,y:y+44,w:W-180,s:48,font:'Semi Bold',color:WHITE,t:p[0],lh:1.2});
    txt(f,{x:90,y:y+108,w:W-180,s:32,font:'Regular',color:DIM,t:p[1],lh:1.35});
  });
  const line=figma.createRectangle();line.resize(W-180,2);line.x=90;line.y=1232;
  line.fills=[{type:'SOLID',color:GREY,opacity:0.4}];f.appendChild(line);
  txt(f,{x:90,y:1280,w:W-180,s:46,font:'Bold',color:BLUE,t:c.quote,lh:1.3});
  made.push(f);
});
figma.viewport.scrollAndZoomIntoView(made);
return {nodes:made.map(c=>({name:c.name,id:c.id}))};   // 拿 nodeId 用于导出
```

调色板可按需换；建议每组卡片用一个主色系，保持克制（黑/白/灰 + 单一强调色）。

## 形态 A：信息流多页卡

每个主题 6 帧横排（封面 + 5 页），多个主题纵向堆叠。封面与金句页用主色满底反白大字，中间页浅色底 + 圆角色标签（chip）+ 正文。结构同上，区别是按 `cards[].pages` 循环生成 6 个 frame、用 `baseY` 控制每行的纵向位置。色标签用带 auto-layout 的小 frame：`layoutMode='HORIZONTAL'`、`primaryAxisSizingMode='AUTO'`、`cornerRadius=999`。

## 导出 PNG

```
download_assets(fileKey, nodeId, defaultFormat:"png")  → 返回临时 url
```
拿到 url 立刻 curl 下载（URL 会过期）：

```bash
curl -s -o exports/Card-1.png "<url>"
file exports/*.png   # 期望: PNG image data, 1080 x 1440
```

需要 2x 高清图时传 `defaultScale:2`。
