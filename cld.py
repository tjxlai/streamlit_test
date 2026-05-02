import streamlit as st

st.set_page_config(
    page_title="统计学就业方向",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 全局样式 ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif;
    background: #0a0a0f !important;
    color: #e8e4dc;
}
.stApp { background: #0a0a0f !important; }
.block-container {
    padding: 0 2rem 4rem 2rem !important;
    max-width: 1280px !important;
}

/* hero */
.hero {
    position: relative;
    padding: 6rem 2rem 5rem;
    text-align: center;
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, #1a2a6c55, transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, #b21f1f22, transparent),
        radial-gradient(ellipse 50% 50% at 20% 60%, #fdbb2d22, transparent);
    border-bottom: 1px solid #1e1e2a;
    margin-bottom: 3rem;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.35em;
    color: #fdbb2d;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Noto Serif SC', serif;
    font-size: clamp(3rem, 8vw, 6.5rem);
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #fff 30%, #fdbb2d 65%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-family: 'Noto Serif SC', serif;
    font-size: clamp(1.2rem, 2.5vw, 1.9rem);
    color: #9a958d;
    margin: 0.4rem 0 2rem;
    letter-spacing: 0.06em;
}
.hero-stats {
    display: inline-flex;
    gap: 3.5rem;
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 1rem;
    padding: 1.5rem 3rem;
    margin-top: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}
.hero-stat { text-align: center; }
.hero-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #fdbb2d;
    display: block;
    line-height: 1;
}
.hero-stat-label {
    font-size: 0.75rem;
    color: #5a5650;
    margin-top: 0.35rem;
    letter-spacing: 0.06em;
}

/* section header */
.sec-title {
    font-family: 'Noto Serif SC', serif;
    font-size: clamp(1.6rem, 3.5vw, 2.5rem);
    font-weight: 700;
    color: #f0ece4;
    margin: 0;
}
.sec-line {
    width: 2.8rem;
    height: 3px;
    background: linear-gradient(90deg, #fdbb2d, #ff6b6b);
    border-radius: 2px;
    margin: 0.5rem 0 2rem;
}

/* career card */
.career-card {
    background: linear-gradient(145deg, #13131a, #1c1c28);
    border-radius: 1rem;
    padding: 1.6rem 1.5rem;
    border-left: 1px solid #22222e;
    border-right: 1px solid #22222e;
    border-bottom: 1px solid #22222e;
}
.cc-icon { font-size: 2rem; margin-bottom: 0.8rem; display: block; }
.cc-title {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f0ece4;
    margin-bottom: 0.3rem;
}
.cc-en {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    color: #fdbb2d;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.cc-body {
    font-size: 0.88rem;
    line-height: 1.85;
    color: #7a7870;
}
.cc-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 1rem;
}
.cc-tag {
    font-size: 0.7rem;
    padding: 0.18rem 0.55rem;
    border-radius: 0.25rem;
    background: #1a1a26;
    border: 1px solid #2a2a3a;
    color: #6a6870;
    font-family: 'Space Mono', monospace;
}

/* salary bar */
.sal-row {
    display: grid;
    grid-template-columns: 160px 1fr 120px;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
.sal-label {
    font-size: 0.88rem;
    color: #b8b4ac;
    text-align: right;
    font-weight: 500;
    white-space: nowrap;
}
.sal-track {
    height: 9px;
    background: #1a1a26;
    border-radius: 5px;
    overflow: hidden;
}
.sal-fill { height: 100%; border-radius: 5px; }
.sal-value {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #fdbb2d;
    white-space: nowrap;
}

/* skill bar */
.sk-wrap { margin-bottom: 0.8rem; }
.sk-top { display: flex; justify-content: space-between; margin-bottom: 0.3rem; }
.sk-name { font-size: 0.88rem; color: #c0bcb4; }
.sk-pct  { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: #5a5650; }
.sk-track { height: 6px; background: #1a1a26; border-radius: 3px; overflow: hidden; }
.sk-fill  { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #fdbb2d, #ff6b6b); }

/* timeline */
.tl-wrap { position: relative; padding-left: 2rem; margin-top: 1rem; }
.tl-wrap::before {
    content: '';
    position: absolute;
    left: 0; top: 0.5rem; bottom: 0;
    width: 2px;
    background: linear-gradient(180deg, #fdbb2d, #ff6b6b, #4facfe, transparent);
}
.tl-item { position: relative; padding-left: 1.5rem; margin-bottom: 2.2rem; }
.tl-item::before {
    content: '';
    position: absolute;
    left: -2.42rem; top: 0.38rem;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #fdbb2d;
    box-shadow: 0 0 0 3px #0a0a0f, 0 0 0 5px #fdbb2d44;
}
.tl-year { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: #fdbb2d; letter-spacing: 0.15em; margin-bottom: 0.25rem; }
.tl-title { font-family: 'Noto Serif SC', serif; font-size: 1.08rem; font-weight: 700; color: #f0ece4; margin-bottom: 0.35rem; }
.tl-body  { font-size: 0.88rem; color: #6a6860; line-height: 1.85; }

/* quote */
.quote-box {
    border-left: 3px solid #fdbb2d;
    background: #13131a;
    border-radius: 0 0.75rem 0.75rem 0;
    padding: 1.4rem 1.8rem;
    margin: 2rem 0 3rem;
    font-family: 'Noto Serif SC', serif;
    font-size: 1.08rem;
    font-style: italic;
    color: #9a9890;
    line-height: 1.9;
}

/* footer */
.footer {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-top: 1px solid #1a1a2a;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #2e2e28;
    letter-spacing: 0.1em;
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Career Guide · 2025 Edition</div>
  <div class="hero-title">统计学就业方向</div>
  <div class="hero-subtitle">数据时代的核心竞争力</div>
  <div class="hero-stats">
    <div class="hero-stat">
      <span class="hero-stat-num">8+</span>
      <div class="hero-stat-label">核心就业方向</div>
    </div>
    <div class="hero-stat">
      <span class="hero-stat-num">35%</span>
      <div class="hero-stat-label">岗位年均增长率</div>
    </div>
    <div class="hero-stat">
      <span class="hero-stat-num">¥30K+</span>
      <div class="hero-stat-label">顶尖岗位月薪中位数</div>
    </div>
    <div class="hero-stat">
      <span class="hero-stat-num">TOP 5</span>
      <div class="hero-stat-label">最受欢迎专业排名</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# CAREER CARDS
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-title">八大就业方向</div>
<div class="sec-line"></div>
""", unsafe_allow_html=True)

careers = [
    ("📊", "数据科学家", "Data Scientist",
     "运用统计建模、机器学习和可视化技术，从海量数据中挖掘业务价值。广泛就职于互联网大厂、金融机构及科技公司，是当下最热门的统计学出口之一。",
     ["Python / R", "机器学习", "统计推断", "可视化"], "#fdbb2d"),

    ("💹", "金融量化分析师", "Quantitative Analyst",
     "构建定价模型、风险管理系统和算法交易策略。深度融合概率论、随机过程与金融理论，是薪资天花板最高的方向之一。",
     ["随机过程", "时间序列", "衍生品定价", "C++/Python"], "#ff6b6b"),

    ("🧬", "生物统计学家", "Biostatistician",
     "服务于临床试验设计、流行病学研究与药物研发。在制药企业、医疗机构和公共卫生部门有稳定且高薪的需求。",
     ["临床试验", "生存分析", "SAS / R", "FDA法规"], "#4facfe"),

    ("🎯", "数据分析师", "Data Analyst",
     "深入业务场景，通过数据驱动产品迭代与运营决策。门槛相对亲和，但对业务理解与沟通能力要求较高，晋升空间广阔。",
     ["SQL", "Tableau", "A/B 测试", "业务洞察"], "#43e97b"),

    ("🏛️", "政府与政策研究", "Policy & Research",
     "参与国家统计局、央行、社科院等机构的数据采集、指数编制与政策评估，以严谨的统计方法支撑宏观决策。",
     ["抽样调查", "经济计量", "政策评估", "报告撰写"], "#a18cd1"),

    ("🤖", "算法 / ML 工程师", "ML / Algorithm Engineer",
     "将统计模型工程化落地，负责推荐系统、搜索排序、风控模型的训练与部署，是统计与工程融合的复合型岗位。",
     ["深度学习", "特征工程", "模型部署", "Spark"], "#f093fb"),

    ("🎓", "学术科研 / 高校教职", "Academia & Teaching",
     "攻读统计学或数学博士，投身统计方法论、贝叶斯推断、高维数据等前沿研究，或回归高校从事教学与人才培养。",
     ["贝叶斯方法", "高维统计", "论文发表", "科研基金"], "#fdbb2d"),

    ("📡", "精算师 / 市场调研", "Actuarial & Market Research",
     "精算师深度运用概率与金融数学为保险定价；市场调研分析师通过抽样与问卷设计洞察消费者行为，均是统计学传统优势出口。",
     ["精算考试", "抽样设计", "问卷分析", "SPSS"], "#4facfe"),
]

# 每行 4 列
for i in range(0, len(careers), 4):
    row = careers[i:i+4]
    cols = st.columns(len(row))
    for col, (icon, title, en, body, tags, color) in zip(cols, row):
        tags_html = "".join(f'<span class="cc-tag">{t}</span>' for t in tags)
        with col:
            st.markdown(
                f'<div class="career-card" style="border-top:3px solid {color};">'
                f'<span class="cc-icon">{icon}</span>'
                f'<div class="cc-title">{title}</div>'
                f'<div class="cc-en">{en}</div>'
                f'<div class="cc-body">{body}</div>'
                f'<div class="cc-tags">{tags_html}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# SALARY CHART
# ════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background:linear-gradient(160deg,#0d0d15,#131320);border-radius:1rem;
            padding:2.5rem 2.5rem 2rem;border:1px solid #1a1a2a;">
<div class="sec-title">薪资水平对比</div>
<div class="sec-line"></div>
""", unsafe_allow_html=True)

salary_data = [
    ("金融量化分析师", 95, "linear-gradient(90deg,#fdbb2d,#f5a623)", "¥30–80K/月"),
    ("数据科学家",     88, "linear-gradient(90deg,#ff6b6b,#ee0979)", "¥25–60K/月"),
    ("算法工程师",     82, "linear-gradient(90deg,#4facfe,#00f2fe)", "¥20–55K/月"),
    ("生物统计学家",   72, "linear-gradient(90deg,#43e97b,#38f9d7)", "¥18–45K/月"),
    ("精算师",         68, "linear-gradient(90deg,#a18cd1,#fbc2eb)", "¥15–40K/月"),
    ("数据分析师",     62, "linear-gradient(90deg,#f093fb,#f5576c)", "¥12–35K/月"),
    ("政策研究员",     50, "linear-gradient(90deg,#ffecd2,#fcb69f)", "¥10–25K/月"),
    ("高校教职",       45, "linear-gradient(90deg,#84fab0,#8fd3f4)", "¥8–30K/月"),
]

for name, pct, grad, label in salary_data:
    st.markdown(
        f'<div class="sal-row">'
        f'<div class="sal-label">{name}</div>'
        f'<div class="sal-track"><div class="sal-fill" style="width:{pct}%;background:{grad};"></div></div>'
        f'<div class="sal-value">{label}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("""
<p style="font-size:.72rem;color:#2e2e28;margin-top:1.2rem;
          font-family:'Space Mono',monospace;letter-spacing:.08em;">
  * 综合各招聘平台2024–2025年数据，含应届至5年经验，因城市、公司及个人能力差异较大
</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# SKILLS
# ════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="sec-title" style="margin-top:2.5rem">核心技能图谱</div>
<div class="sec-line"></div>
""", unsafe_allow_html=True)

skills = [
    ("概率论与数理统计", 95), ("回归分析 / 广义线性模型", 90),
    ("机器学习理论", 85),     ("贝叶斯统计", 80),
    ("时间序列分析", 82),     ("Python 编程", 88),
    ("R 语言", 80),           ("SQL 与数据库", 75),
    ("实验设计 / A/B 测试", 78), ("数据可视化", 72),
    ("深度学习基础", 70),     ("沟通与报告撰写", 68),
]

for i in range(0, len(skills), 3):
    row = skills[i:i+3]
    cols = st.columns(3)
    for col, (name, pct) in zip(cols, row):
        with col:
            st.markdown(
                f'<div class="sk-wrap">'
                f'<div class="sk-top"><span class="sk-name">{name}</span>'
                f'<span class="sk-pct">{pct}%</span></div>'
                f'<div class="sk-track"><div class="sk-fill" style="width:{pct}%;"></div></div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ════════════════════════════════════════════════════════════════════════
# CAREER TIMELINE
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-title" style="margin-top:3.5rem">典型职业成长路径</div>
<div class="sec-line"></div>
<div class="quote-box">
  "统计学的美妙之处在于：它不仅教会你如何描述世界，更教会你如何在不确定性中做出理性决策。"
  <br><small style="font-size:.8rem;font-style:normal;color:#4a4840;">—— 数据科学职业发展观察</small>
</div>
<div class="tl-wrap">
  <div class="tl-item">
    <div class="tl-year">本科阶段 · Year 1–4</div>
    <div class="tl-title">夯实数学与统计基础</div>
    <div class="tl-body">修读概率论、数理统计、回归分析、时间序列等核心课程；同步学习 Python / R 编程，参与课题组科研，建立数据思维框架。</div>
  </div>
  <div class="tl-item">
    <div class="tl-year">毕业前 · Year 3–4</div>
    <div class="tl-title">实习积累：选择赛道</div>
    <div class="tl-body">在互联网、金融或咨询公司完成 1–2 段数据相关实习；明确自己偏好工业界还是学术界，决定是否继续深造。</div>
  </div>
  <div class="tl-item">
    <div class="tl-year">入职 1–3 年</div>
    <div class="tl-title">初级分析师 / 研究员</div>
    <div class="tl-body">独立负责数据提取、建模分析与报告输出，深度理解业务逻辑，积累行业 domain knowledge，建立个人方法论体系。</div>
  </div>
  <div class="tl-item">
    <div class="tl-year">工作 3–7 年</div>
    <div class="tl-title">高级分析师 / 技术专家</div>
    <div class="tl-body">主导复杂建模项目，带领小团队，参与产品或策略的核心决策；薪资进入快速上升区间，有机会转型管理或深耕技术专家通道。</div>
  </div>
  <div class="tl-item">
    <div class="tl-year">7 年以上</div>
    <div class="tl-title">首席科学家 / 数据总监</div>
    <div class="tl-body">战略层面定义数据文化与团队建设，或在学术领域成为独立 PI。部分人选择自主创业，将数据能力转化为商业价值。</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  STATISTICS CAREERS GUIDE · 2025 · MADE WITH STREAMLIT &amp; 💛<br>
  数据仅供参考，实际情况因人因时而异
</div>
""", unsafe_allow_html=True)