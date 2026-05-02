import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================================
# 页面基础配置
# ============================================================
st.set_page_config(
    page_title="统计学就业方向全景指南",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 自定义 CSS 样式
# ============================================================
custom_css = """
<style>
    /* ---- 全局字体与背景 ---- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Playfair+Display:wght@700;900&display=swap');

    :root {
        --bg-primary: #0a0f1a;
        --bg-secondary: #111827;
        --bg-card: #1a2236;
        --bg-card-hover: #1f2a42;
        --accent: #00e8a2;
        --accent-dim: rgba(0, 232, 162, 0.15);
        --accent-glow: rgba(0, 232, 162, 0.3);
        --text-primary: #f0f4f8;
        --text-secondary: #8899aa;
        --text-muted: #556677;
        --border: rgba(255,255,255,0.06);
        --gradient-1: linear-gradient(135deg, #00e8a2, #00b4d8);
        --gradient-2: linear-gradient(135deg, #f97316, #ef4444);
        --gradient-3: linear-gradient(135deg, #8b5cf6, #ec4899);
        --gradient-4: linear-gradient(135deg, #0ea5e9, #6366f1);
    }

    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* ---- 隐藏默认元素 ---- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ---- 侧边栏 ---- */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    .css-1d391kg {
        color: var(--text-primary) !important;
    }

    /* ---- 英雄区域 ---- */
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -120px;
        left: 50%;
        transform: translateX(-50%);
        width: 700px;
        height: 700px;
        background: radial-gradient(circle, rgba(0,232,162,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-family: 'Playfair Display', 'Noto Sans SC', serif;
        font-size: 3.6rem;
        font-weight: 900;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 300;
        max-width: 680px;
        margin: 0 auto 12px;
        line-height: 1.8;
    }
    .hero-badge {
        display: inline-block;
        padding: 6px 20px;
        border-radius: 999px;
        background: var(--accent-dim);
        color: var(--accent);
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 20px;
        border: 1px solid rgba(0,232,162,0.2);
    }

    /* ---- 统计数字行 ---- */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 36px;
        flex-wrap: wrap;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 900;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 6px;
        font-weight: 400;
    }

    /* ---- 区块标题 ---- */
    .section-header {
        margin: 48px 0 28px;
        padding-left: 18px;
        border-left: 4px solid var(--accent);
    }
    .section-header h2 {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    .section-header p {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 6px 0 0;
        font-weight: 300;
    }

    /* ---- 方向卡片 ---- */
    .direction-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 8px;
    }
    @media (max-width: 900px) {
        .direction-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
        .direction-grid { grid-template-columns: 1fr; }
        .hero-title { font-size: 2.2rem; }
        .stats-row { gap: 24px; }
        .stat-number { font-size: 2rem; }
    }
    .dir-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px 24px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .dir-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--card-accent, var(--gradient-1));
        opacity: 0;
        transition: opacity 0.35s;
    }
    .dir-card:hover {
        background: var(--bg-card-hover);
        transform: translateY(-4px);
        border-color: rgba(255,255,255,0.1);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .dir-card:hover::before { opacity: 1; }
    .dir-card-icon {
        font-size: 2rem;
        margin-bottom: 14px;
        display: block;
    }
    .dir-card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
    }
    .dir-card-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 14px;
    }
    .dir-card-salary {
        font-size: 0.82rem;
        color: var(--accent);
        font-weight: 500;
        padding: 4px 12px;
        background: var(--accent-dim);
        border-radius: 6px;
        display: inline-block;
    }
    .dir-card-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 12px;
    }
    .dir-card-tag {
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 4px;
        background: rgba(255,255,255,0.04);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }

    /* ---- 详情展开区域 ---- */
    .detail-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 20px;
    }
    .detail-section h3 {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
    @media (max-width: 700px) {
        .detail-grid { grid-template-columns: 1fr; }
    }
    .detail-item {
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
    }
    .detail-item-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .detail-item-value {
        font-size: 1rem;
        color: var(--text-primary);
        line-height: 1.7;
    }

    /* ---- 技能条 ---- */
    .skill-bar-container {
        margin-bottom: 12px;
    }
    .skill-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        margin-bottom: 5px;
    }
    .skill-bar-label span:first-child { color: var(--text-primary); font-weight: 500; }
    .skill-bar-label span:last-child { color: var(--text-muted); }
    .skill-bar-track {
        height: 6px;
        background: rgba(255,255,255,0.06);
        border-radius: 3px;
        overflow: hidden;
    }
    .skill-bar-fill {
        height: 100%;
        border-radius: 3px;
        background: var(--gradient-1);
        transition: width 1s ease;
    }

    /* ---- 路径时间线 ---- */
    .timeline {
        position: relative;
        padding-left: 36px;
    }
    .timeline::before {
        content: '';
        position: absolute;
        left: 14px;
        top: 6px;
        bottom: 6px;
        width: 2px;
        background: linear-gradient(to bottom, var(--accent), rgba(0,232,162,0.1));
    }
    .timeline-item {
        position: relative;
        margin-bottom: 28px;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -28px;
        top: 6px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 12px var(--accent-glow);
    }
    .timeline-year {
        font-size: 0.8rem;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 4px;
    }
    .timeline-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    .timeline-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.7;
    }

    /* ---- 建议卡片 ---- */
    .tip-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 14px;
        display: flex;
        gap: 16px;
        align-items: flex-start;
        transition: all 0.3s;
    }
    .tip-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(0,232,162,0.15);
    }
    .tip-icon {
        font-size: 1.6rem;
        flex-shrink: 0;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: var(--accent-dim);
    }
    .tip-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    .tip-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.7;
    }

    /* ---- 页脚 ---- */
    .footer-section {
        text-align: center;
        padding: 48px 20px 32px;
        color: var(--text-muted);
        font-size: 0.82rem;
        border-top: 1px solid var(--border);
        margin-top: 60px;
    }

    /* ---- Plotly 图表容器 ---- */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ---- 侧边栏自定义 ---- */
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }
    .sidebar-nav-item {
        display: block;
        padding: 10px 14px;
        border-radius: 8px;
        color: var(--text-secondary) !important;
        font-size: 0.9rem;
        margin-bottom: 4px;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
    }
    .sidebar-nav-item:hover {
        background: rgba(0,232,162,0.08);
        color: var(--accent) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================
# 数据准备
# ============================================================

# 六大就业方向数据
career_directions = [
    {
        "icon": "🤖",
        "title": "数据科学与人工智能",
        "desc": "利用统计建模、机器学习算法从海量数据中提取洞察，构建智能决策系统，是统计学最热门的出口之一。",
        "salary": "15K - 50K+",
        "color": "#00e8a2",
        "tags": ["Python", "机器学习", "深度学习", "SQL", "Hadoop/Spark"],
        "positions": ["数据科学家", "算法工程师", "机器学习工程师", "AI研究员", "NLP工程师"],
        "companies": ["字节跳动", "腾讯", "阿里巴巴", "华为", "商汤科技", "OpenAI"],
        "growth": "极高",
        "demand": "★★★★★",
    },
    {
        "icon": "💰",
        "title": "金融与量化投资",
        "desc": "将统计方法应用于风险评估、衍生品定价、量化交易策略开发，金融行业对统计学人才的需求持续旺盛。",
        "salary": "20K - 80K+",
        "color": "#f59e0b",
        "tags": ["R/Python", "时间序列", "随机过程", "风控模型", "衍生品"],
        "positions": ["量化分析师", "风控建模师", "精算师", "金融分析师", "投资策略研究员"],
        "companies": ["中金公司", "中信证券", "幻方量化", "九坤投资", "摩根士丹利", "高盛"],
        "growth": "高",
        "demand": "★★★★★",
    },
    {
        "icon": "🏥",
        "title": "生物医药与临床统计",
        "desc": "在制药公司、CRO或医院中负责临床试验设计、统计分析计划制定，是统计学传统且高壁垒的应用领域。",
        "salary": "12K - 40K",
        "color": "#ef4444",
        "tags": ["SAS", "R", "生存分析", "临床试验", "FDA规范"],
        "positions": ["生物统计师", "SAS程序员", "临床数据分析师", "药理统计学家", "流行病学研究员"],
        "companies": ["恒瑞医药", "药明康德", "泰格医药", "辉瑞", "诺华", "强生"],
        "growth": "稳定",
        "demand": "★★★★☆",
    },
    {
        "icon": "🏛️",
        "title": "政府与公共统计",
        "desc": "在国家统计局、各地调查队、政府部门从事国民经济核算、社会调查、政策评估等官方统计工作。",
        "salary": "8K - 20K",
        "color": "#3b82f6",
        "tags": ["抽样调查", "国民经济核算", "SPSS", "政策评估", "普查"],
        "positions": ["统计师", "调查分析师", "政策评估专员", "人口统计学家", "经济预测员"],
        "companies": ["国家统计局", "各省调查总队", "央行研究局", "发改委", "世行", "联合国统计司"],
        "growth": "稳定",
        "demand": "★★★☆☆",
    },
    {
        "icon": "📈",
        "title": "市场研究与用户分析",
        "desc": "运用A/B测试、因果推断、用户行为建模等方法，为产品决策和市场营销提供数据驱动的洞察。",
        "salary": "12K - 35K",
        "color": "#8b5cf6",
        "tags": ["A/B测试", "因果推断", "用户画像", "SQL", "Tableau"],
        "positions": ["数据分析师", "用户研究分析师", "增长分析师", "市场研究顾问", "商业智能分析师"],
        "companies": ["美团", "滴滴", "快手", "尼尔森", "麦肯锡", "宝洁"],
        "growth": "高",
        "demand": "★★★★☆",
    },
    {
        "icon": "🎓",
        "title": "学术研究与教育",
        "desc": "在高校或研究机构从事统计学理论、方法学研究或教学工作，推动学科前沿发展，培养下一代人才。",
        "salary": "10K - 30K+",
        "color": "#ec4899",
        "tags": ["概率论", "高维统计", "贝叶斯方法", "论文写作", "教学"],
        "positions": ["教授/副教授", "博士后研究员", "讲师", "实验室研究员", "学科带头人"],
        "companies": ["北京大学", "清华大学", "中国科学院", "斯坦福", "MIT", "Max Planck研究所"],
        "growth": "稳定",
        "demand": "★★★☆☆",
    },
]

# 薪资数据
salary_df = pd.DataFrame({
    "方向": ["数据科学/AI", "金融/量化", "生物医药", "政府/公共", "市场研究", "学术/教育"],
    "起薪(万/年)": [18, 24, 14, 10, 14, 12],
    "中位数(万/年)": [35, 50, 25, 15, 24, 18],
    "高薪(万/年)": [60, 100, 40, 22, 40, 35],
})

# 技能需求数据
skills_data = {
    "技能": ["Python/R", "SQL", "机器学习", "概率论", "回归分析", "抽样方法", "SAS", "可视化", "深度学习", "因果推断"],
    "数据科学": [95, 85, 98, 80, 85, 40, 20, 80, 90, 60],
    "金融量化": [90, 80, 75, 95, 90, 30, 15, 60, 40, 50],
    "生物医药": [70, 60, 30, 90, 95, 85, 98, 50, 10, 70],
    "市场研究": [80, 90, 50, 60, 75, 70, 10, 90, 15, 85],
}

skills_df = pd.DataFrame(skills_data)

# 行业分布数据
industry_df = pd.DataFrame({
    "行业": ["互联网/科技", "金融", "医药/医疗", "政府/事业单位", "制造业", "咨询", "教育/科研", "其他"],
    "占比": [32, 22, 14, 10, 7, 6, 5, 4],
})

# 历年就业趋势
trend_df = pd.DataFrame({
    "年份": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "数据科学": [15, 20, 25, 32, 38, 42, 45],
    "金融量化": [20, 22, 20, 24, 26, 28, 30],
    "生物医药": [18, 18, 20, 22, 23, 24, 25],
    "市场研究": [22, 20, 18, 16, 15, 14, 13],
    "政府统计": [12, 11, 10, 10, 9, 9, 8],
})

# 发展路径数据
career_paths = {
    "数据科学": [
        {"year": "第1-2年", "title": "数据分析师 / 初级算法工程师", "desc": "掌握SQL、Python数据处理，参与业务分析项目，建立基础建模能力。"},
        {"year": "第3-5年", "title": "高级数据科学家 / 算法专家", "desc": "独立负责核心模型开发，主导A/B实验设计，形成方法论沉淀。"},
        {"year": "第5-8年", "title": "数据科学团队负责人 / 首席科学家", "desc": "带领团队解决战略级问题，推动AI技术在业务中的深度落地。"},
        {"year": "第8年+", "title": "VP级技术高管 / 创业", "desc": "跨界管理，技术战略决策，或以数据技术为核心创办企业。"},
    ],
    "金融量化": [
        {"year": "第1-2年", "title": "量化研究实习生 / 初级分析师", "desc": "学习金融工程知识，复现经典策略论文，搭建回测框架。"},
        {"year": "第3-5年", "title": "量化策略研究员 / 投资经理", "desc": "独立开发交易策略，管理小规模资金，形成稳定alpha来源。"},
        {"year": "第5-8年", "title": "量化团队负责人 / 基金经理", "desc": "管理多策略组合，负责风控体系，管理数十亿级资产。"},
        {"year": "第8年+", "title": "合伙人 / 自营量化基金创始人", "desc": "创立量化私募，构建完整投研体系，实现资本自由。"},
    ],
    "生物医药": [
        {"year": "第1-2年", "title": "生物统计师 I / SAS程序员", "desc": "参与临床试验统计分析，编写SAS程序，学习监管法规要求。"},
        {"year": "第3-5年", "title": "高级生物统计师 / 统计负责人", "desc": "独立撰写统计分析计划，领导临床项目的统计工作。"},
        {"year": "第5-8年", "title": "首席统计师 / 统计部门总监", "desc": "统筹多个临床项目的统计策略，与FDA/NMPA沟通。"},
        {"year": "第8年+", "title": "VP级统计官 / 独立顾问", "desc": "企业级统计战略决策，或成为行业顶尖独立咨询专家。"},
    ],
}

# 求职建议
tips = [
    {
        "icon": "📚",
        "title": "夯实数理基础",
        "desc": "概率论、数理统计、线性代数是统计学的立身之本。无论走向哪个方向，扎实的理论基础决定了你能走多远。推荐教材：Casella & Berger《Statistical Inference》。",
    },
    {
        "icon": "💻",
        "title": "精通至少一门编程语言",
        "desc": "Python是数据科学首选，R在统计建模中仍占优势，SAS在医药行业不可替代。建议主攻Python + SQL组合，再根据方向补充第二语言。",
    },
    {
        "icon": "🏆",
        "title": "积累实战项目经验",
        "desc": "Kaggle竞赛、企业实习、开源贡献、科研论文——至少要有2-3个能展示深度的项目。面试时能清晰讲述分析思路比堆砌技术名词更重要。",
    },
    {
        "icon": "🌐",
        "title": "培养业务理解力",
        "desc": "统计方法的价值在于解决实际问题。主动了解目标行业的业务逻辑：互联网的产品指标、金融的市场机制、医药的临床流程，这是差异化竞争力。",
    },
    {
        "icon": "🤝",
        "title": "建立职业人脉网络",
        "desc": "参加统计学、数据科学相关的学术会议和行业峰会（如CHINA DS、KDD等），加入专业社群，与校友保持联系——很多优质岗位通过内推流转。",
    },
    {
        "icon": "📝",
        "title": "注重表达与写作能力",
        "desc": "能把复杂的统计结论用简洁的语言讲给非技术人员听，是一项被严重低估的能力。练习写分析报告、做技术演讲，这将在面试和职场中给你巨大加分。",
    },
]

# 核心技能详细数据
core_skills = [
    {"name": "Python / R 编程", "level": 95, "desc": "数据处理、建模、自动化的核心工具"},
    {"name": "SQL 数据查询", "level": 88, "desc": "从数据库中高效提取和聚合数据"},
    {"name": "概率论与数理统计", "level": 92, "desc": "假设检验、估计理论、贝叶斯方法"},
    {"name": "回归与分类模型", "level": 90, "desc": "线性回归、逻辑回归、GLM等经典方法"},
    {"name": "机器学习算法", "level": 82, "desc": "随机森林、XGBoost、SVM、聚类等"},
    {"name": "数据可视化", "level": 85, "desc": "matplotlib、seaborn、Plotly、Tableau"},
    {"name": "A/B 实验设计", "level": 78, "desc": "样本量计算、随机化、因果推断"},
    {"name": "时间序列分析", "level": 75, "desc": "ARIMA、状态空间模型、波动率建模"},
]


# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 导航目录</div>', unsafe_allow_html=True)

    nav_items = [
        ("#hero", "首页概览"),
        ("#directions", "六大就业方向"),
        ("#salary", "薪资对比分析"),
        ("#skills", "技能需求图谱"),
        ("#industry", "行业分布"),
        ("#trend", "就业趋势"),
        ("#path", "发展路径"),
        ("#tips", "求职建议"),
    ]
    for href, label in nav_items:
        st.markdown(f'<a href="{href}" class="sidebar-nav-item">{label}</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="padding:16px;background:var(--accent-dim);border-radius:12px;border:1px solid rgba(0,232,162,0.15);">'
        '<div style="font-size:0.85rem;color:var(--accent);font-weight:600;margin-bottom:6px;">💡 数据说明</div>'
        '<div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.7;">'
        '薪资数据综合自各大招聘平台与行业报告（2024年），仅供参考。实际薪资因城市、经验、学历等因素差异较大。'
        '</div></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# 主内容区
# ============================================================

# ---- 英雄区域 ----
st.markdown(
    '''
    <div class="hero-section" id="hero">
        <div class="hero-badge">2024 年度指南 · 持续更新</div>
        <h1 class="hero-title">Statistics Career Guide</h1>
        <p class="hero-subtitle">
            统计学——数据时代的基石学科。从硅谷到华尔街，从实验室到政策大厅，
            统计学人才正以前所未有的速度被各行各业渴求。
            <br>这份指南将为你全面解析统计学的六大就业方向。
        </p>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-number">96%</div>
                <div class="stat-label">毕业生就业率</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">35万+</div>
                <div class="stat-label">年均岗位需求</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">18.6%</div>
                <div class="stat-label">近5年薪资增幅</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">6大</div>
                <div class="stat-label">核心就业方向</div>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

# ---- 六大就业方向 ----
st.markdown(
    '<div class="section-header" id="directions"><h2>六大就业方向</h2><p>涵盖技术、金融、医药、公共、商业、学术六大领域，总有一条路适合你</p></div>',
    unsafe_allow_html=True,
)

cards_html = '<div class="direction-grid">'
for d in career_directions:
    tags_html = "".join(f'<span class="dir-card-tag">{t}</span>' for t in d["tags"])
    cards_html += f'''
    <div class="dir-card" style="--card-accent: {d["color"]};">
        <span class="dir-card-icon">{d["icon"]}</span>
        <div class="dir-card-title">{d["title"]}</div>
        <div class="dir-card-desc">{d["desc"]}</div>
        <span class="dir-card-salary">💰 {d["salary"]} / 月</span>
        <div class="dir-card-tags">{tags_html}</div>
    </div>
    '''
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)


# ---- 方向详情展示（Tab选择） ----
st.markdown("<br>", unsafe_allow_html=True)
selected_direction = st.selectbox(
    "🔍 选择方向查看详情",
    [d["title"] for d in career_directions],
    label_visibility="collapsed",
)
detail_data = next(d for d in career_directions if d["title"] == selected_direction)

st.markdown(
    f'''
    <div class="detail-section">
        <h3>{detail_data["icon"]} {detail_data["title"]} · 详细解读</h3>
        <div class="detail-grid">
            <div class="detail-item">
                <div class="detail-item-label">典型岗位</div>
                <div class="detail-item-value">{"、".join(detail_data["positions"])}</div>
            </div>
            <div class="detail-item">
                <div class="detail-item-label">代表雇主</div>
                <div class="detail-item-value">{"、".join(detail_data["companies"])}</div>
            </div>
            <div class="detail-item">
                <div class="detail-item-label">薪资区间</div>
                <div class="detail-item-value" style="color:var(--accent);font-weight:700;font-size:1.2rem;">{detail_data["salary"]} / 月</div>
            </div>
            <div class="detail-item">
                <div class="detail-item-label">需求热度 & 增长态势</div>
                <div class="detail-item-value">{detail_data["demand"]}　<span style="color:var(--accent);">增长：{detail_data["growth"]}</span></div>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

# ---- 薪资对比 ----
st.markdown(
    '<div class="section-header" id="salary"><h2>薪资对比分析</h2><p>不同方向的薪资水平差异显著，金融量化上限最高，数据科学整体均衡</p></div>',
    unsafe_allow_html=True,
)

fig_salary = go.Figure()
fig_salary.add_trace(
    go.Bar(
        name="起薪",
        x=salary_df["方向"],
        y=salary_df["起薪(万/年)"],
        marker_color="#00e8a2",
        marker_opacity=0.7,
        text=salary_df["起薪(万/年)"],
        textposition="outside",
        textfont=dict(color="#8899aa", size=11),
    )
)
fig_salary.add_trace(
    go.Bar(
        name="中位数",
        x=salary_df["方向"],
        y=salary_df["中位数(万/年)"],
        marker_color="#00b4d8",
        marker_opacity=0.85,
        text=salary_df["中位数(万/年)"],
        textposition="outside",
        textfont=dict(color="#8899aa", size=11),
    )
)
fig_salary.add_trace(
    go.Bar(
        name="高薪",
        x=salary_df["方向"],
        y=salary_df["高薪(万/年)"],
        marker_color="#f59e0b",
        marker_opacity=1,
        text=salary_df["高薪(万/年)"],
        textposition="outside",
        textfont=dict(color="#f59e0b", size=12, family="Noto Sans SC"),
    )
)
fig_salary.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8899aa", family="Noto Sans SC"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.08,
        xanchor="center",
        x=0.5,
        font=dict(size=12),
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="年薪（万元）", titlefont=dict(size=12)),
    margin=dict(l=40, r=40, t=80, b=60),
    height=460,
)
st.plotly_chart(fig_salary, use_container_width=True)

# ---- 技能需求图谱 ----
st.markdown(
    '<div class="section-header" id="skills"><h2>技能需求图谱</h2><p>不同方向对统计技能的需求侧重点截然不同，选对技能组合事半功倍</p></div>',
    unsafe_allow_html=True,
)

skill_cols = st.columns(2)
with skill_cols[0]:
    fig_radar = go.Figure()
    categories = skills_df["技能"].tolist()
    for col, color in zip(
        ["数据科学", "金融量化", "生物医药", "市场研究"],
        ["#00e8a2", "#f59e0b", "#ef4444", "#8b5cf6"],
    ):
        fig_radar.add_trace(
            go.Scatterpolar(
                r=skills_df[col].tolist(),
                theta=categories,
                fill="toself",
                name=col,
                line_color=color,
                opacity=0.75,
            )
        )
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            gridcolor="rgba(255,255,255,0.06)",
            anglecolor="#556677",
            tickfont=dict(size=10, color="#8899aa"),
            radialaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=9, color="#556677")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8899aa", family="Noto Sans SC", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(l=60, r=60, t=40, b=80),
        height=440,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with skill_cols[1]:
    st.markdown(
        '<div style="padding:20px 0 8px;font-size:1rem;font-weight:600;color:var(--text-primary);">核心技能掌握度参考</div>',
        unsafe_allow_html=True,
    )
    for sk in core_skills:
        color_style = "var(--gradient-1)" if sk["level"] >= 85 else "var(--gradient-4)" if sk["level"] >= 75 else "var(--gradient-2)"
        st.markdown(
            f'''
            <div class="skill-bar-container">
                <div class="skill-bar-label">
                    <span>{sk["name"]}</span>
                    <span>{sk["level"]}%</span>
                </div>
                <div class="skill-bar-track">
                    <div class="skill-bar-fill" style="width:{sk["level"]}%;background:{color_style};"></div>
                </div>
                <div style="font-size:0.75rem;color:var(--text-muted);margin-top:3px;">{sk["desc"]}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

# ---- 行业分布 ----
st.markdown(
    '<div class="section-header" id="industry"><h2>行业分布</h2><p>互联网/科技行业吸纳了最多统计学毕业生，金融和医药紧随其后</p></div>',
    unsafe_allow_html=True,
)

ind_cols = st.columns([2, 1])
with ind_cols[0]:
    fig_ind = go.Figure(
        go.Pie(
            labels=industry_df["行业"],
            values=industry_df["占比"],
            hole=0.55,
            marker_colors=["#00e8a2", "#f59e0b", "#ef4444", "#3b82f6", "#8b5cf6", "#ec4899", "#06b6d4", "#556677"],
            textinfo="label+percent",
            textfont=dict(size=12, color="#f0f4f8", family="Noto Sans SC"),
            hoverinfo="label+percent+value",
            textposition="outside",
            pull=[0.05, 0.02, 0.02, 0, 0, 0, 0, 0],
        )
    )
    fig_ind.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8899aa", family="Noto Sans SC"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=420,
        showlegend=False,
    )
    st.plotly_chart(fig_ind, use_container_width=True)

with ind_cols[1]:
    st.markdown(
        '<div style="padding:20px 0 8px;font-size:1rem;font-weight:600;color:var(--text-primary);">分布要点</div>',
        unsafe_allow_html=True,
    )
    insights = [
        ("互联网/科技", "32%", "最大吸纳方，数据驱动决策已成标配"),
        ("金融行业", "22%", "量化与风控岗位持续扩招"),
        ("医药/医疗", "14%", "新药研发推动临床统计需求"),
        ("政府/事业", "10%", "稳定选择，含编制岗位"),
    ]
    for name, pct, note in insights:
        st.markdown(
            f'''
            <div style="margin-bottom:16px;padding:14px;background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-size:0.92rem;font-weight:600;color:var(--text-primary);">{name}</span>
                    <span style="font-size:1.1rem;font-weight:700;color:var(--accent);">{pct}</span>
                </div>
                <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.6;">{note}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

# ---- 就业趋势 ----
st.markdown(
    '<div class="section-header" id="trend"><h2>就业趋势变化</h2><p>近7年各方向就业占比走势，数据科学强势崛起，传统方向相对收缩</p></div>',
    unsafe_allow_html=True,
)

fig_trend = go.Figure()
trend_colors = ["#00e8a2", "#f59e0b", "#ef4444", "#8b5cf6", "#3b82f6"]
for i, col in enumerate(["数据科学", "金融量化", "生物医药", "市场研究", "政府统计"]):
    fig_trend.add_trace(
        go.Scatter(
            x=trend_df["年份"],
            y=trend_df[col],
            name=col,
            line=dict(color=trend_colors[i], width=2.5),
            mode="lines+markers",
            marker=dict(size=6, color=trend_colors[i]),
            fill="tozeroy" if i == 0 else None,
            fillcolor="rgba(0,232,162,0.05)" if i == 0 else None,
        )
    )
fig_trend.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8899aa", family="Noto Sans SC", size=11),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.08,
        xanchor="center",
        x=0.5,
        font=dict(size=11),
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="就业占比（%）", titlefont=dict(size=12)),
    margin=dict(l=40, r=40, t=80, b=60),
    height=440,
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---- 发展路径 ----
st.markdown(
    '<div class="section-header" id="path"><h2>典型发展路径</h2><p>三大热门方向的职业晋升时间线，从入门到顶尖</p></div>',
    unsafe_allow_html=True,
)

path_tabs = st.tabs(["🤖 数据科学", "💰 金融量化", "🏥 生物医药"])
for tab_idx, tab in enumerate(path_tabs):
    with tab:
        key = list(career_paths.keys())[tab_idx]
        path = career_paths[key]
        timeline_html = '<div class="timeline">'
        for item in path:
            timeline_html += f'''
            <div class="timeline-item">
                <div class="timeline-year">{item["year"]}</div>
                <div class="timeline-title">{item["title"]}</div>
                <div class="timeline-desc">{item["desc"]}</div>
            </div>
            '''
        timeline_html += "</div>"
        st.markdown(timeline_html, unsafe_allow_html=True)

# ---- 求职建议 ----
st.markdown(
    '<div class="section-header" id="tips"><h2>求职实战建议</h2><p>来自行业资深人士的六条核心建议，帮你少走弯路</p></div>',
    unsafe_allow_html=True,
)

for tip in tips:
    st.markdown(
        f'''
        <div class="tip-card">
            <div class="tip-icon">{tip["icon"]}</div>
            <div>
                <div class="tip-title">{tip["title"]}</div>
                <div class="tip-desc">{tip["desc"]}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

# ---- 页脚 ----
st.markdown(
    '''
    <div class="footer-section">
        <div style="margin-bottom:8px;">
            <span style="background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;font-size:1rem;">Statistics Career Guide</span>
        </div>
        <div>数据来源：国家统计局、智联招聘、Boss直聘、麦可思研究院、各行业薪酬报告</div>
        <div style="margin-top:4px;">本页面仅供参考，实际就业情况请以最新市场数据为准 · 2024</div>
    </div>
    ''',
    unsafe_allow_html=True,
)
