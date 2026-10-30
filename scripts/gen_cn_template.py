# -*- coding: utf-8 -*-
"""中文导游词小红书图文 · 模板（2026-10-29，沉淀自 gen_cn.py / gen_angang.py）

===== 使用说明 =====
1. 编辑下方【用户编辑区】：
   - OUT：成品输出目录（默认脚本同目录 output_sample；发布时改为
          Claw/小红书产出/<景点>/中文导游词版/）
   - SPOT / SUB / CAPSULE / KEYPTS：封面信息
   - P1~P6：导游词全文（按上/中/下卡拆分，长段按自然句拆卡）
   - SCORE_SECTIONS / DEDUCT_LEFT / DEDUCT_RIGHT：踩分卡与扣分双栏卡
   - TOTAL：内容卡总数（封面不计，通常 5）
2. 运行：python gen_cn_template.py
3. 生成 6 张 PNG（封面 + 导游词上中下 + 踩分 + 扣分双栏），纯矢量文字卡。

视觉：深蓝渐变 + 珊瑚橙角标（对齐九一八/鞍钢中文版品牌卡）。
下方示例数据以「鞍钢博物馆」为参考实现，替换为你的景点即可。
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ===================== 用户编辑区 =====================
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sample")
os.makedirs(OUT, exist_ok=True)

SPOT   = "鞍钢博物馆"                      # 景点名（封面主标题）
SUB    = "中文导游词"                      # 副标题
CAPSULE = "一座雕塑 · 高粱地 · 无数个第一"  # 封面胶囊锚点
KEYPTS = [                               # 封面底部 3 行关键点
    "建筑面积 1.26 万㎡ · 11 展厅 2 专题",
    "《钢铁之魂》浮雕 36 米 × 8 米",
    "共和国「钢铁长子」· 鞍钢精神",
]
# 导游词全文（示例：鞍钢，按上/中/下拆卡逻辑）
P1 = ("各位游客朋友，大家好！欢迎来到鞍山鞍钢博物馆。我是大家的导游。"
      "这是承载共和国钢铁精神、镌刻钢铁长子记忆的标杆性工业博物馆，"
      "建筑面积 1.26 万平方米，设有 11 个主题展厅和 2 个专题展区。"
      "进馆之前，请大家先记住三个关键词：一座雕塑、高粱地、无数个第一。")
P2 = ("【第一条线 · 一座雕塑】请大家随我步入大厅。迎面那幅气势恢宏的红色浮雕，叫《钢铁之魂》。"
      "它长 36 米、高 8 米，生动刻画了鞍钢工人热火朝天的劳动场景。"
      "浮雕之上，孟泰、王崇伦、雷锋、郭明义等一代代劳模的形象静静伫立。")
P3 = ("【第二条线 · 高粱地】1916 年振兴铁矿无限公司，1918 年设立鞍山制铁所，1933 年改组为昭和制钢所。"
      "1944 年工厂遭多轮轰炸瘫痪，战后工厂设备大量被拆运，生产设施损毁严重。"
      "当年甚至有日本专家断言：「这片土地将来只能长高粱。」")
P4a = ("【第三条线 · 无数个第一】1948 年 2 月 19 日鞍山解放，同年 12 月 26 日鞍山钢铁公司正式成立。"
       "勤劳智慧的鞍钢工人炼出了新中国首批工业化冶炼产出的铁水、钢水，还有第一根钢轨、第一根无缝钢管。")
P4b = ("从南京长江大桥的钢梁，到北京十大建筑的钢筋铁骨；从神舟飞船的精密部件，到蛟龙号、复兴号、国产航母的关键材料——"
       "鞍钢，不仅是共和国的「钢铁长子」，更是撑起中国建设的钢铁脊梁。")
P5 = ("【收束 · 精神】尾厅墙上镌刻着八个大字，这就是鞍钢精神：创新、求实、拼争、奉献。"
      "自强才能自立，实干方能兴邦。我们铭记历史，是为了把眼下的强盛稳稳握在自己手里。")
P6 = ("亲爱的游客朋友们，今天的旅程即将结束。鞍钢博物馆的魅力远不止这些，它就像一本厚重的教科书。"
      "感谢大家的陪伴，祝各位旅途愉快，一路顺风！谢谢各位。")

SCORE_SECTIONS = [    # 踩分卡：必背得分点 + 高频失分坑
    ("必背核心得分点", [
        ("check", "开场锚点：一座雕塑、高粱地、无数个第一，三条线串起全馆。"),
        ("check", "场馆概况：建筑面积 1.26 万㎡，11 个主题展厅 + 2 个专题展区。"),
        ("check", "一座雕塑：《钢铁之魂》浮雕长 36 米、高 8 米，孟泰等劳模形象。"),
        ("check", "高粱地线索：1916→1918→1933→1944 遭轰炸→战后设备大量拆运（「只能长高粱」断言）。"),
        ("check", "无数个第一：1948.2.19 解放、1948.12.26 成立；首批工业化铁水钢水+第一根钢轨/无缝钢管（文中「第一」为史实记录，非营销）。"),
        ("check", "鞍钢精神：尾厅八字——创新、求实、拼争、奉献。"),
    ]),
    ("高频失分坑", [
        ("warn", "时间线讲错——1916/1918/1933/1944/1948.2.19/1948.12.26 别临场编数字。"),
        ("warn", "四位劳模人名张冠李戴（孟泰/王崇伦/雷锋/郭明义）。"),
        ("warn", "漏讲《钢铁之魂》浮雕数据（36 米 × 8 米）或「钢铁长子」定位。"),
        ("warn", "漏讲鞍钢精神八字（创新、求实、拼争、奉献）。"),
        ("warn", "机考录制限时 5 分钟，建议 4 分钟左右收尾，防超时扣分。"),
    ]),
]
DEDUCT_LEFT = [       # 扣分双栏卡 · 左栏
    ("严重扣分项 · 直接大幅丢分", [
        ((235, 87, 87), "史实错误：年份、面积、浮雕尺寸、劳模人名、事件表述出错。"),
        ((235, 87, 87), "超时：导游词录制限时 5 分钟，超过直接扣分，建议控制在 4 分钟左右。"),
        ((235, 87, 87), "内容缺项：漏掉雕塑、高粱地、无数个第一、鞍钢精神任一核心板块。"),
        ((235, 87, 87), "表述不严谨：工业红色题材讲解语气轻浮、用词随意。"),
    ]),
    ("一般扣分项", [
        ((255, 200, 60), "长时间卡顿、频繁忘词、多次重复同一句话。"),
        ((255, 200, 60), "语速过快或过慢，节奏杂乱，缺少合理停顿。"),
        ((255, 200, 60), "断句生硬，没有导游讲解的语感，纯生硬背书感。"),
        ((255, 200, 60), "开头、结尾缺少标准导游问候与结束致谢。"),
    ]),
]
DEDUCT_RIGHT = [      # 扣分双栏卡 · 右栏
    ("加分细节", [
        ("check", "开场先抛三条线，考官一听结构就清楚。"),
        ("check", "数据脱口而出：1.26 万㎡ / 36 米 × 8 米 / 1948.2.19 / 1948.12.26。"),
        ("check", "讲劳模与「钢铁长子」语气自豪有力，节奏张弛有度。"),
        ("check", "结尾鞍钢精神八字收束，完整闭环。"),
    ]),
    ("考场须知", [
        ("dot", "辽宁导考为机考录制，导游词环节无问答，一录定分。"),
        ("dot", "工业题材庄重自豪优先，史实不出错是底线。"),
        ("dot", "录制前多遍跟读全文，掐表练到 4 分钟左右更稳妥。"),
    ]),
]
TOTAL = 5
# =================== 用户编辑区结束 ===================

W, H = 1080, 1440
NAVY1, NAVY2 = (30, 58, 95), (60, 90, 160)
CORAL = (255, 122, 51)
WHITE = (255, 255, 255)
SOFT = (200, 214, 235)
GOLD = (245, 205, 120)
RED = (235, 87, 87)
YELLOW = (255, 200, 60)
FONT_DIR = r"C:\Windows\Fonts"

def font(sz):
    path = os.path.join(FONT_DIR, "simhei.ttf")
    if not os.path.exists(path):
        path = os.path.join(FONT_DIR, "msyh.ttc")
    return ImageFont.truetype(path, sz)

def vgrad(h, top, bot):
    im = Image.new("RGB", (W, h))
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return im

PUNCT_HANG = "，。、；：？！」』）…—%"

def wrap_cn(text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if fnt.getlength(cur + ch) <= max_w or not cur:
            cur += ch
        elif ch in PUNCT_HANG:
            cur += ch
            lines.append(cur)
            cur = ""
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines

def badge(d):
    d.rounded_rectangle([40, 36, 290, 100], radius=14, fill=CORAL)
    d.text((165, 68), "金玉满屋97", font=font(34), fill=WHITE, anchor="mm")

def banner(d, txt):
    d.rectangle([0, 150, W, 240], fill=CORAL)
    d.text((W // 2, 195), txt, font=font(46), fill=WHITE, anchor="mm")

def bottom_title(d, num, total, title):
    cy, r = 1230, 40
    d.ellipse([80, cy - r, 80 + 2 * r, cy + r], fill=NAVY1, outline=CORAL, width=3)
    d.text((80 + r, cy), f"{num}/{total}", font=font(34), fill=WHITE, anchor="mm")
    d.text((80 + 2 * r + 24, cy), title, font=font(38), fill=WHITE, anchor="lm")
    d.text((W // 2, H - 58), "金玉满屋97 · 辽宁文旅观察", font=font(28), fill=GOLD, anchor="mm")

def check(d, x, y):
    d.rounded_rectangle([x, y - 16, x + 32, y + 16], radius=8, fill=CORAL)
    d.line([(x + 8, y + 1), (x + 14, y + 8), (x + 25, y - 8)], fill=WHITE, width=4)

def warn(d, x, y):
    d.polygon([(x + 16, y - 19), (x + 35, y + 15), (x - 3, y + 15)], fill=YELLOW)
    d.line([(x + 16, y - 7), (x + 16, y + 2)], fill=NAVY1, width=4)
    d.ellipse([x + 13, y + 5, x + 19, y + 11], fill=NAVY1)

def dot(d, x, y, color):
    d.ellipse([x, y - 12, x + 24, y + 12], fill=color)

def sec_title(d, y, txt):
    d.text((80, y), "【" + txt + "】", font=font(30), fill=CORAL, anchor="lm")
    return y + 46

def li(d, y, icon, txt, icon_color=None, fsz=28, lh=36, gap=8):
    if icon == "check":
        check(d, 80, y)
    elif icon == "warn":
        warn(d, 80, y)
    else:
        dot(d, 80, y, icon_color or CORAL)
    f = font(fsz)
    lines = wrap_cn(txt, f, W - 200)
    d.text((128, y), lines[0], font=f, fill=WHITE, anchor="lm")
    for ln in lines[1:]:
        y += lh
        d.text((128, y), ln, font=f, fill=WHITE, anchor="lm")
    return y + lh + gap

def guide_card(num, title, paras, fname):
    cv = vgrad(H, NAVY1, NAVY2).convert("RGB")
    d = ImageDraw.Draw(cv)
    badge(d); banner(d, title)
    y = 285
    f_body, f_head = font(29), font(30)
    for p in paras:
        if p.startswith("【"):
            head, rest = p.split("】", 1)
            d.text((80, y), head + "】", font=f_head, fill=GOLD, anchor="lm"); y += 44
            for ln in wrap_cn(rest, f_body, W - 160):
                d.text((80, y), ln, font=f_body, fill=WHITE, anchor="lm"); y += 43
        else:
            for ln in wrap_cn(p, f_body, W - 160):
                d.text((80, y), ln, font=f_body, fill=WHITE, anchor="lm"); y += 43
        y += 22
    bottom_title(d, num, TOTAL, "")
    cv.save(os.path.join(OUT, fname), quality=95)
    print(f"{fname} saved, content_end={y}")
    return y

def point_card(num, bt_title, sections, fname):
    cv = vgrad(H, NAVY1, NAVY2).convert("RGB")
    d = ImageDraw.Draw(cv)
    badge(d); banner(d, bt_title)
    y = 285
    for st, items in sections:
        y = sec_title(d, y, st)
        for icon, txt in items:
            if icon == "check":
                y = li(d, y, "check", txt)
            elif icon == "warn":
                y = li(d, y, "warn", txt)
            else:
                y = li(d, y, "dot", txt, icon_color=icon if isinstance(icon, tuple) else CORAL)
    bottom_title(d, num, TOTAL, "")
    cv.save(os.path.join(OUT, fname), quality=95)
    print(f"{fname} saved, content_end={y}")
    return y

def sec_title_col(d, y, txt, x, w):
    d.text((x, y), "【" + txt + "】", font=font(27), fill=CORAL, anchor="lm")
    return y + 42

def li_col(d, y, icon, txt, x, w, icon_color=None, fsz=22, lh=28, gap=10):
    if icon == "check":
        check(d, x, y)
    elif icon == "warn":
        warn(d, x, y)
    else:
        dot(d, x, y, icon_color or CORAL)
    f = font(fsz)
    lines = wrap_cn(txt, f, w - 48)
    tx = x + 48
    d.text((tx, y), lines[0], font=f, fill=WHITE, anchor="lm")
    for ln in lines[1:]:
        y += lh
        d.text((tx, y), ln, font=f, fill=WHITE, anchor="lm")
    return y + lh + gap

def point_card_merged(num, bt_title, left_sections, right_sections, fname):
    cv = vgrad(H, NAVY1, NAVY2).convert("RGB")
    d = ImageDraw.Draw(cv)
    badge(d); banner(d, bt_title)
    col_x = [80, 560]; col_w = [440, 440]
    yl = 285
    for st, items in left_sections:
        yl = sec_title_col(d, yl, st, col_x[0], col_w[0])
        for icon, txt in items:
            yl = li_col(d, yl, icon, txt, col_x[0], col_w[0])
    yr = 285
    for st, items in right_sections:
        yr = sec_title_col(d, yr, st, col_x[1], col_w[1])
        for icon, txt in items:
            yr = li_col(d, yr, icon, txt, col_x[1], col_w[1])
    bottom_title(d, num, TOTAL, "")
    cv.save(os.path.join(OUT, fname), quality=95)
    print(f"{fname} saved, L={yl}, R={yr}")
    return max(yl, yr)

# ---------------- 封面 ----------------
def make_cover():
    cv = vgrad(H, NAVY1, NAVY2).convert("RGB")
    d = ImageDraw.Draw(cv)
    badge(d)
    d.text((W // 2, 330), SPOT, font=font(132), fill=WHITE, anchor="mm")
    d.text((W // 2, 470), SUB, font=font(64), fill=WHITE, anchor="mm")
    d.text((W // 2, 560), "5 分钟口试 · 讲解版", font=font(46), fill=CORAL, anchor="mm")
    cy, cw, ch = 660, 760, 86
    cx = (W - cw) // 2
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=43, fill=CORAL)
    d.text((W // 2, cy + ch // 2), CAPSULE, font=font(38), fill=WHITE, anchor="mm")
    d.text((W // 2, 820), "中文讲解示范 · 可直接背诵", font=font(36), fill=SOFT, anchor="mm")
    yy = 1000
    for p in KEYPTS:
        d.text((W // 2, yy), "· " + p, font=font(30), fill=WHITE, anchor="mm"); yy += 54
    d.text((W // 2, H - 90), "金玉满屋97 · 辽宁文旅观察", font=font(30), fill=GOLD, anchor="mm")
    cv.save(os.path.join(OUT, f"XHS_{SPOT}中文_封面.png"), quality=95)
    print("封面 saved")

if __name__ == "__main__":
    make_cover()
    guide_card(1, "完整版导游词（上）", [P1, P2], "XHS_鞍钢中文_图2_导游词上.png")
    guide_card(2, "完整版导游词（中）", [P3, P4a], "XHS_鞍钢中文_图3_导游词中.png")
    guide_card(3, "完整版导游词（下）", [P4b, P5, P6], "XHS_鞍钢中文_图4_导游词下.png")
    point_card(4, "口试踩分要点", SCORE_SECTIONS, "XHS_鞍钢中文_图5_踩分要点.png")
    point_card_merged(5, "考场扣分提醒", DEDUCT_LEFT, DEDUCT_RIGHT, "XHS_鞍钢中文_图6_扣分提醒.png")
    total = sum(len(p) for p in [P1, P2, P3, P4a, P4b, P5, P6])
    print(f"导游词全文 {total} 字 -> {OUT}")
