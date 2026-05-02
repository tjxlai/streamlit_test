import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 设置页面配置（宽屏模式）
st.set_page_config(page_title="统计学就业方向", layout="wide", page_icon="📊")

# 自定义CSS样式（可选，提升美观）
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 标题
st.title("📊 统计学就业方向全景图")
st.markdown("探索统计学专业的多元职业路径与发展前景")

# 模拟数据
directions = [
    "数据分析师", "数据科学家", "机器学习工程师",
    "金融量化分析师", "生物统计师", "市场研究员",
    "风险精算师", "商业智能分析师"
]
avg_salary = [18, 25, 28, 22, 20, 15, 24, 16]  # 单位：万元/年
demand = [90, 95, 88, 80, 75, 70, 85, 82]  # 需求热度（0-100）
skills = [
    "Python, SQL, Excel",
    "Python, R, ML, Deep Learning",
    "Python, TensorFlow, PyTorch",
    "R, Python, 金融建模",
    "R, SAS, 临床试验设计",
    "SPSS, 问卷设计, 数据可视化",
    "精算模型, R, Python",
    "SQL, Tableau, PowerBI"
]

df = pd.DataFrame({
    "就业方向": directions,
    "平均年薪（万元）": avg_salary,
    "需求热度": demand,
    "核心技能": skills
})

# 侧边栏：筛选
st.sidebar.header("🔍 筛选条件")
min_salary = st.sidebar.slider("最低年薪（万元）", 10, 30, 15)
min_demand = st.sidebar.slider("最低需求热度", 0, 100, 70)

# 筛选数据
filtered_df = df[(df["平均年薪（万元）"] >= min_salary) & (df["需求热度"] >= min_demand)]

# 主内容区
tab1, tab2, tab3, tab4 = st.tabs(["📈 薪资对比", "🔥 需求热度", "📚 技能要求", "📋 详细数据"])

with tab1:
    st.subheader("各方向平均年薪对比")
    fig = px.bar(
        filtered_df,
        x="就业方向",
        y="平均年薪（万元）",
        color="平均年薪（万元）",
        color_continuous_scale="Blues",
        title="统计学就业方向薪资分布"
    )
    fig.update_layout(xaxis_title="就业方向", yaxis_title="年薪（万元）")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("市场需求热度分析")
    fig2 = px.scatter(
        filtered_df,
        x="就业方向",
        y="需求热度",
        size="平均年薪（万元）",
        color="需求热度",
        color_continuous_scale="Reds",
        title="需求热度 vs 薪资水平（气泡大小=薪资）"
    )
    fig2.update_layout(xaxis_title="就业方向", yaxis_title="需求热度")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("核心技能要求")
    for _, row in filtered_df.iterrows():
        with st.expander(f"🎯 {row['就业方向']} 所需技能"):
            st.write(f"**核心技能**：{row['核心技能']}")
            st.write(f"**平均年薪**：{row['平均年薪（万元）']} 万元")
            st.write(f"**需求热度**：{row['需求热度']}/100")

with tab4:
    st.subheader("完整数据表格")
    st.dataframe(
        filtered_df.style.format({"平均年薪（万元）": "{:.1f}"}).background_gradient(subset=["需求热度"], cmap="YlOrRd"),
        use_container_width=True
    )

# 顶部指标卡片
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("最高薪资方向", f"{df.loc[df['平均年薪（万元）'].idxmax(), '就业方向']}")
with col2:
    st.metric("最高需求方向", f"{df.loc[df['需求热度'].idxmax(), '就业方向']}")
with col3:
    st.metric("平均薪资", f"{df['平均年薪（万元）'].mean():.1f} 万元")
with col4:
    st.metric("方向总数", len(df))

# 页脚
st.markdown("---")
st.caption("数据来源：模拟数据 | 制作工具：Streamlit + Plotly | 更新时间：2026年5月")