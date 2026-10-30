---
name: xhs-guideword-cn
description: >-
  This skill should be used when generating Xiaohongshu (小红书) image-text posts for
  Chinese-language tour guide scripts (导游词) of Liaoning scenic spots, especially for the
  2026 Liaoning tour guide qualification oral exam (口试/机考). It produces a 6-card brand
  visual series (deep-blue gradient + coral badge) covering cover + guide text (上/中/下) +
  scoring points + deduction reminders, plus a publish-ready markdown package with title
  scoring, compliance checks, and a self-inspection checklist. Trigger when the user provides
  a Chinese 导游词 docx/text and asks to "制作小红书图文 / 按九一八或断桥格式做中文导游词".
agent_created: true
---

# 中文导游词小红书图文生成

## 用途

将辽宁景区**中文**导游词（用户定稿 docx 或纯文本）转化为小红书图文发布包：深蓝品牌卡 6 图（封面 + 导游词上/中/下 + 踩分要点 + 扣分提醒双栏）+ 发布包 md（标题评分 / 正文 / 标签 / 置顶 / 自检清单）。专用于 2026 辽宁导游资格证口试（机考）备考内容。

## 何时使用

- 收到用户中文《XXX 导游词.docx》或纯文本，要求"制作小红书图文""按九一八/断桥格式做中文导游词""生成辽宁口试中文导游词小红书"。
- 区分：英文口试稿走 `xhs-guideword-en`；本 skill 只处理**中文**讲解稿。

## 输入

- 中文导游词全文（docx 或文本）。若为 docx，用 Python `zipfile` 解压读取 `word/document.xml` 提取正文（只读，不改动源文件）。
- 史实红线清单（如厂名"鞍钢"禁"安钢"、年份口径等），来自用户定稿 docx 或项目 working memory 的"内容合规红线"。

## 工作流程

1. 提取文本，确认全文结构与字数（中文按字符计）。
2. 按 6 图结构拆分：封面 + 导游词上/中/下（**全文进图卡**）+ 踩分要点（必背得分点 6 + 高频失分坑 5）+ 扣分提醒（双栏合并：严重扣分项 4 + 一般扣分项 4 ｜ 加分细节 4 + 考场须知 3）。
3. 若最长段 >520 字超单卡容量，按**自然句**拆分到相邻卡（如 P4 拆为 P4a 入中卡 / P4b 入下卡），不得硬塞导致 `content_end` 溢出。拆分后逐卡 `content_end` 须 < 底部序号圆顶沿（约 1190）上方留白。
4. 运行 `scripts/gen_cn_template.py` 生成 6 张 PNG（深蓝品牌视觉）。
5. 写发布包 md（字段结构见 `references/publish_template.md`，复制后替换占位符）。

## 视觉规范（深蓝品牌卡，强制）

| 元素 | 取值 | 说明 |
|------|------|------|
| 比例 | 3:4（1080×1440px） | 小红书图文最佳尺寸 |
| 主背景 | 深蓝渐变 #1e3a5f → #3c5aa0 | 品牌识别色 |
| 主强调色 | 珊瑚橙 #ff7a33 | banner / 角标 / 序号圆描边 / 矢量图标 |
| 账号角标 | 橙底白字「金玉满屋97」 | 每张图左上固定 |
| 标题 banner | 珊瑚橙底白字 | 各内容卡顶部 |
| 序号圆 | 深蓝填充 + 珊瑚橙描边 + 白字「N/5」 | 左下 |
| 页脚 | 金色「金玉满屋97 · 辽宁文旅观察」 | 底部居中 |
| 正文 | 黑体 simhei 29px，白字 | 中文清晰 |
| 小标题 | 金色「【XXX】」（对应原稿线索标记） | 原样保留用户 docx 的【】标记 |
| 矢量图标 | 珊瑚橙 ✓（check）/ 黄 △（warn）/ 圆点 dot | 纯 PIL 绘制，无 emoji 豆腐块风险 |

详细函数与色值见 `references/visual_spec.md`。**纯矢量文字卡，零实景图、零 AI 图，无需 AI 标识。**

## 合规红线（发布前必查）

- **专名红线**：按项目红线（如「鞍钢」禁「安钢」），全篇检索错别字。
- **极限词**：史实类「第一」（如第一根钢轨、无缝钢管）豁免营销法；但正文需加一句"文中「第一」均为新中国工业史客观史实，非营销宣传用语"；单句"第一炉铁水/钢水"弱化为"首批工业化冶炼产出的铁水、钢水"。禁"最/唯一/顶级"等广告绝对化。
- **历史措辞**：中立客观，不做评价。"苏军拆走 X 万吨设备"类直白表述弱化为"战后工厂设备大量被拆运，生产设施损毁严重"。
- **保过承诺**：全文禁"包过/稳上岸/必通关"，只写"减少扣分/规避失分"。
- **站外引流**：正文零"公众号/私信/加微信/外链"；真实领取动作只走评论区置顶（零引流版纯免责话术）。
- **标题 ≤20 字**；**正文 ≤950 字符**；时长以口试 5 分钟为准（描述栏首行写"机考录制限时 5 分钟，建议 4 分钟左右完成"）。
- **自检清单**：逐项打勾后随发布包交付（见模板第七节）。

## 产出文件

- `XHS_<景点>中文_封面.png` + `XHS_<景点>中文_图2_导游词上.png` … `图6_扣分提醒.png`（共 6 张）
- `XHS_<景点>中文_笔记成品.md`（发布包）
- 落地路径：`Claw\小红书产出\<景点>\中文导游词版\`

## 冷启动风控（红色/工业题材）

红色、工业题材初始流量池偏小、"自见不外放"属平台常态风控非账号违规。发布实操：① 工作日上午 9:30–11:00 发，避开夜间审核高峰；② 首发"仅自己可见"停留 30 分钟查无违规再公开；③ 发布后半小时内只贴一条置顶评论，不刷评论；④ 同系列（九一八/断桥/辽沈/鞍钢）隔天交替发降同质化；⑤ 各篇分段换行微调降重复度。
