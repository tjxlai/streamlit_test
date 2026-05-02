import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="统计学就业方向指南",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式，提升视觉精美度
st.markdown("""
<style>
    /* 主色调与圆角 */
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4b5563;
        margin-bottom: 2rem;
        border-left: 4px solid #2a5298;
        padding-left: 1rem;
    }
    .job-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        border: 1px solid #e9ecef;
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.1);
    }
    .skill-badge {
        background: #eef2ff;
        color: #1e3c72;
        border-radius: 30px;
        padding: 0.2rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #eef2f6;
    }
    footer {
        text-align: center;
        margin-top: 3rem;
        color: #6c757d;
        font-size: 0.8rem;
        border-top: 1px solid #dee2e6;
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- 数据定义 ----------
# 职位详情库
job_details = {
    "数据科学家": {
        "icon": "🤖",
        "avg_salary": 48,
        "salary_range": "35-65",
        "growth_rate": "+22%",
        "degree": "硕士/博士优先",
        "skills": ["Python", "R", "SQL", "机器学习", "A/B测试", "统计建模"],
        "description": "利用统计学与机器学习从海量数据中提取洞察，驱动商业决策。需要扎实的统计推断与编程能力。",
        "employers": ["科技巨头", "电商", "金融科技", "咨询公司"],
        "stat_tools": ["回归分析", "贝叶斯推断", "随机森林", "时间序列"]
    },
    "数据分析师": {
        "icon": "📈",
        "avg_salary": 28,
        "salary_range": "20-38",
        "growth_rate": "+18%",
        "degree": "本科及以上",
        "skills": ["SQL", "Excel", "Tableau/Power BI", "Python", "业务思维"],
        "description": "负责数据清洗、可视化与报表制作，为业务团队提供数据支持，是统计学入门的核心岗位。",
        "employers": ["互联网公司", "零售业", "物流", "快消"],
        "stat_tools": ["描述统计", "假设检验", "A/B测试", "方差分析"]
    },
    "生物统计师": {
        "icon": "🧬",
        "avg_salary": 38,
        "salary_range": "28-52",
        "growth_rate": "+15%",
        "degree": "硕士/博士",
        "skills": ["R", "SAS", "临床试验设计", "生存分析", "FDA法规"],
        "description": "在医药、公共卫生领域设计临床试验，分析患者数据，是新药研发的关键角色。",
        "employers": ["药企", "CRO公司", "医院科研部门", "政府卫生机构"],
        "stat_tools": ["生存分析", "纵向数据", "混合效应模型", "贝叶斯"]
    },
    "金融风险分析师": {
        "icon": "⚖️",
        "avg_salary": 45,
        "salary_range": "32-60",
        "growth_rate": "+20%",
        "degree": "硕士优先",
        "skills": ["Python/R", "风险管理", "时间序列", "信用评分模型", "FRM证书"],
        "description": "评估金融机构的信用、市场与操作风险，构建量化风控模型。",
        "employers": ["银行", "券商", "保险", "金融监管机构"],
        "stat_tools": ["逻辑回归", "时间序列", "极值理论", "蒙特卡洛模拟"]
    },
    "市场研究分析师": {
        "icon": "📊",
        "avg_salary": 22,
        "salary_range": "16-30",
        "growth_rate": "+12%",
        "degree": "本科",
        "skills": ["SPSS", "问卷设计", "客户细分", "竞品分析", "Excel"],
        "description": "通过调研与数据分析洞察消费者行为，辅助品牌策略与产品定位。",
        "employers": ["市场咨询公司", "快消巨头", "互联网市场部"],
        "stat_tools": ["因子分析", "聚类分析", "对应分析", "T检验"]
    },
    "政府统计师": {
        "icon": "🏛️",
        "avg_salary": 20,
        "salary_range": "15-26",
        "growth_rate": "+8%",
        "degree": "本科/硕士",
        "skills": ["SAS", "Stata", "抽样调查", "经济统计", "报告撰写"],
        "description": "在统计局、央行等机构从事国民经济核算、人口普查、数据分析与政策支持。",
        "employers": ["国家/地方统计局", "发改委", "财政/税务部门"],
        "stat_tools": ["抽样技术", "调查方法论", "指数构建", "时间序列"]
    }
}

# 就业行业分布数据 (百分比)
industry_df = pd.DataFrame({
    "行业": ["科技/互联网", "金融/保险", "医疗/生物制药", "政府/公共部门", "咨询/市场调研", "其他"],
    "比例": [35, 25, 18, 10, 7, 5]
})

# 所有职位薪资对比数据 (用于柱状图)
salary_df = pd.DataFrame({
    "职位": list(job_details.keys()),
    "平均年薪(万元)": [job_details[job]["avg_salary"] for job in job_details.keys()]
})

# 侧边栏选择
st.sidebar.markdown("## 🧭 探索就业方向")
selected_job = st.sidebar.radio(
    "选择一个统计学职业路径，查看详细信息:",
    options=list(job_details.keys()),
    index=0,
    format_func=lambda x: f"{job_details[x]['icon']} {x}"
)
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 统计专业核心技能")
st.sidebar.markdown("""
- 🔹 概率论与数理统计  
- 🔹 回归分析 / 多元统计  
- 🔹 实验设计 / A/B测试  
- 🔹 R / Python / SQL  
- 🔹 数据可视化与沟通
""")
st.sidebar.markdown("---")
st.sidebar.caption("数据基于行业调研与薪资报告，仅供参考。")

# ---------- 主区域布局 ----------
# 标题区域
col_title, col_empty = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-header">📐 统计学就业全景指南</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">从数据到决策 — 六大热门方向深度解析，薪资趋势与技能图谱</div>',
                unsafe_allow_html=True)

# 第一行：KPI 指标卡片（全局概览）
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📊 平均起薪</h3>
        <h2 style="color:#2a5298;">23.8 <span style="font-size:1rem;">万元/年</span></h2>
        <p>统计学本科应届</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🚀 岗位增长率</h3>
        <h2 style="color:#2a5298;">+16.5%</h2>
        <p>近3年复合增长</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>🏆 最热方向</h3>
        <h2 style="color:#2a5298;">数据科学 & AI</h2>
        <p>需求年增+22%</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>🎓 深造推荐</h3>
        <h2 style="color:#2a5298;">硕士占比 52%</h2>
        <p>高级岗位普遍要求</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 第二行：左侧详细职业卡片 + 右侧薪资对比柱状图
left_col, right_col = st.columns([1.2, 1], gap="large")

# 获取当前选中职位详情
job_info = job_details[selected_job]

with left_col:
    st.markdown(f"""
    <div class="job-card">
        <h2>{job_info['icon']} {selected_job}</h2>
        <p style="color:#4b5563; margin-top:-5px;">{job_info['description']}</p>
        <hr>
        <p><strong>💰 平均年薪:</strong> {job_info['avg_salary']}万元  (范围 {job_info['salary_range']}万元)</p>
        <p><strong>📈 年增长率:</strong> {job_info['growth_rate']}</p>
        <p><strong>🎓 学历要求:</strong> {job_info['degree']}</p>
        <p><strong>🏢 典型雇主:</strong> {', '.join(job_info['employers'])}</p>
        <p><strong>🔧 核心技术工具:</strong></p>
        <div>
    """, unsafe_allow_html=True)
    # 技能badges
    for skill in job_info["skills"]:
        st.markdown(f'<span class="skill-badge">{skill}</span>', unsafe_allow_html=True)
    st.markdown("<br><p><strong>📐 常用统计方法:</strong></p>", unsafe_allow_html=True)
    for stat_meth in job_info["stat_tools"]:
        st.markdown(f'<span class="skill-badge" style="background:#e0e7ff;">{stat_meth}</span>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # 额外建议
    with st.expander("🧠 职业发展建议", expanded=False):
        if "数据科学" in selected_job:
            st.info("✨ 建议补充CS基础与机器学习工程能力，Kaggle项目经历加分。")
        elif "生物统计" in selected_job:
            st.info("✨ 临床试验相关知识 & 熟悉CDISC标准可拓宽药企路径。")
        elif "金融风险" in selected_job:
            st.info("✨ 考取FRM/CFA证书，掌握巴塞尔协议与压力测试。")
        else:
            st.info("✨ 持续提升SQL与数据故事化能力，跨部门沟通是核心竞争力。")

with right_col:
    st.subheader("📊 各职位平均薪资对比 (万元/年)")
    # 创建高亮当前所选职位的柱状图
    salary_df_temp = salary_df.copy()
    salary_df_temp["高亮"] = salary_df_temp["职位"].apply(lambda x: "当前选择" if x == selected_job else "其他职位")
    # 柱状图配色
    fig_bar = px.bar(
        salary_df_temp,
        x="职位",
        y="平均年薪(万元)",
        color="高亮",
        color_discrete_map={"当前选择": "#FF6B6B", "其他职位": "#4A90E2"},
        text="平均年薪(万元)",
        labels={"平均年薪(万元)": "年薪 (万元)"},
        template="plotly_white"
    )
    fig_bar.update_traces(textposition="outside", textfont_size=12)
    fig_bar.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_gridcolor='#e9ecef',
        xaxis_title="",
        yaxis_title="平均年薪 (万元)",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption("数据来源：薪酬调研报告 & 招聘平台综合值 (一线城市参考)")

st.markdown("---")

# 第三行：行业分布饼图 + 核心技能需求雷达图/技能词云风格 (选用简洁仪表)
left_pie, right_skill = st.columns(2)

with left_pie:
    st.subheader("📌 统计学毕业生就业行业分布")
    fig_pie = px.pie(
        industry_df,
        values="比例",
        names="行业",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r,
        template="plotly_white"
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label", pull=[0.02, 0, 0, 0, 0, 0])
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=380)
    st.plotly_chart(fig_pie, use_container_width=True)

with right_skill:
    st.subheader("🌟 统计学人才核心竞争力图谱")
    # 使用水平条形图展示通用技能重要性 (基于雇主调研模拟)
    skill_importance = pd.DataFrame({
        "技能": ["统计建模", "Python/R编程", "SQL取数", "数据可视化", "业务理解", "沟通表达"],
        "重要性评分": [9.5, 9.2, 8.7, 8.5, 9.0, 8.8]
    })
    fig_hor = px.bar(
        skill_importance,
        y="技能",
        x="重要性评分",
        orientation='h',
        text="重要性评分",
        color="重要性评分",
        color_continuous_scale="Blues",
        range_color=[7, 10]
    )
    fig_hor.update_traces(textposition="outside", textfont_size=11)
    fig_hor.update_layout(
        height=380,
        xaxis_title="重要性 (满分10)",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_gridcolor='#e9ecef',
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_hor, use_container_width=True)

st.markdown("---")

# 第四行：学习路径推荐 + 实用资源
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.markdown("### 🎯 统计学高效成长路径")
    st.markdown("""
    1. **夯实基础** → 概率论、数理统计、线性代数  
    2. **编程入门** → Python (Pandas, Numpy) + SQL  
    3. **核心统计建模** → 回归分析、时间序列、实验设计  
    4. **进阶方向** → 机器学习 / 贝叶斯方法 / 大数据工具  
    5. **实战 & 证书** → 参与Kaggle / 考取SAS、CDA、PMP  
    """)
with col_res2:
    st.markdown("### 📚 推荐学习资源")
    st.markdown("""
    - 📖 **书籍**：《统计学》《Introduction to Statistical Learning》  
    - 💻 **在线课程**：Coursera统计专项、DataCamp  
    - 🧰 **工具**：RStudio、Jupyter、Tableau Public  
    - 🗣️ **交流社区**：统计之都、Kaggle、Reddit (r/statistics)  
    - 🧪 **项目实战**：政府开放数据、天池/和鲸社区
    """)

# 页脚
st.markdown("""
<footer>
    <p>📈 数据基于行业整体调研，实际薪资受地域、经验及公司影响 | 统计学赋能数据时代，开启无限可能 ✨</p>
    <p>💡 持续学习与交叉技能是职业跃迁关键 — 用数据科学思维影响世界</p>
</footer>
""", unsafe_allow_html=True)