import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title='专业数据分析', page_icon='📋')
st.set_page_config(layout='wide')

st.title("📊专业数据分析")
st.markdown("***")
st.header("1.各专业男女性别比例")
c1, c2 = st.columns([1,2])
with c1:
# 读取数据
   df1 = pd.read_csv('student_data_adjusted_rounded.csv', encoding='utf-8')

# 计算每个专业的性别人数及比例
   gender_data = df1.groupby(['专业', '性别'])['学号'].nunique().reset_index(name='人数')
   gender_data['比例(%)'] = gender_data.groupby('专业')['人数'].transform(
     lambda x: (x / x.sum()) * 100
)

# 绘制柱状图
   fig = px.bar(
    gender_data,
    x='专业',
    y='比例(%)',
    color='性别',
    barmode='group',
    title='各专业男女性别比例',
    labels={'比例(%)': '比例(%)', '性别': '性别'},
    color_discrete_sequence=['#37CEEB', '#4682B4']
)
   st.plotly_chart(fig, use_container_width=True)
with c2:
# 展示透视表数据
  st.subheader("性别比例数据")
  gender_pivot = gender_data.pivot(index='专业', columns='性别', values='比例(%)').fillna(0)
  st.dataframe(gender_pivot, use_container_width=True)



  
st.markdown("***")
st.header("2.各专业学习指标对比")
b1, b2 = st.columns([1,2])
with b1:
   # 读取数据（确保你的CSV包含所需列）
   df = pd.read_csv('student_data_adjusted_rounded.csv', encoding='utf-8')

   # 提取所需数据（按专业分组计算平均值，根据实际数据调整）
   # 假设需要计算各专业的平均学习时间、平均期中成绩、平均期末成绩
   grouped_df = df.groupby('专业').agg({
     '每周学习时长（小时）': 'mean',  # 对应柱状图
     '期中考试分数': 'mean',  # 对应第一条折线
     '期末考试分数': 'mean'   # 对应第二条折线
 }).reset_index()

  # 创建组合图表
   fig = go.Figure()

  # 1. 添加柱状图（平均学习时间）
   fig.add_trace(
      go.Bar(
        x=grouped_df['专业'],
        y=grouped_df['每周学习时长（小时）'],
        name='平均每周学习时长(小时)',  # 图例名称
        marker_color='skyblue',   # 柱状图颜色（接近左图的蓝色）
        yaxis='y1'                # 使用左侧纵轴
    )
)

# 2. 添加第一条折线（期中成绩）
   fig.add_trace(
      go.Scatter(
        x=grouped_df['专业'],
        y=grouped_df['期中考试分数'],
        name='平均期中考试分数',
        mode='lines+markers',     # 线+点
        line=dict(color='green'), # 绿色线
        yaxis='y2'                # 使用右侧纵轴
    )
)

  # 3. 添加第二条折线（期末成绩）
   fig.add_trace(
     go.Scatter(
        x=grouped_df['专业'],
        y=grouped_df['期末考试分数'],
        name='平均期末考试分数',
        mode='lines+markers',
        line=dict(color='orange'),# 橙色线
        yaxis='y2'                # 共享右侧纵轴
    )
)

# 设置双轴
   fig.update_layout(
     title='各专业平均学习时间与成绩对比',
     yaxis=dict(
        title='平均每周学习时长 (小时)',  # 左侧纵轴标题
        side='left'
    ),
    yaxis2=dict(
        title='成绩',              # 右侧纵轴标题
        side='right',
        overlaying='y'             # 与左侧纵轴重叠
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),  # 图例位置
    barmode='group'
)

# 在Streamlit中显示图表
   st.plotly_chart(fig, use_container_width=True)
with b2:
   # 右侧显示详细数据表格（类似左图右侧的"详细数据"）
   st.subheader("详细数据")
   st.dataframe(grouped_df, use_container_width=True)




st.markdown('***')
st.header("3. 各专业出勤率分析")

# 假设数据中包含“出勤率”列，若数据结构不同需调整
# 计算各专业平均出勤率（按专业分组求均值）
attendance_data = df1.groupby('专业')['上课出勤率'].mean().reset_index()
# 保留一位小数（与示例图一致）
attendance_data['平均上课出勤率(%)'] = (attendance_data['上课出勤率']*100).round(1)
# 按出勤率降序排序（用于右侧表格）
attendance_sorted = attendance_data.sort_values('上课出勤率', ascending=False).reset_index(drop=True)
# 添加排名列
attendance_sorted['排名'] = attendance_sorted.index + 1

# 拆分左右两列布局
col_left, col_right = st.columns(2)

with col_left:
    # 绘制带颜色映射的柱状图（左侧）
    fig_attendance = px.bar(
        attendance_data,
        x='专业',
        y='上课出勤率',
        # 用颜色映射表示出勤率高低（与右侧图例一致）
        color='上课出勤率',
        # 颜色渐变：从低到高为紫色→蓝色→青色→绿色→黄色（接近示例图）
        color_continuous_scale=['purple', 'blue', 'cyan', 'green', 'yellow'],
        title='各专业平均上课出勤率',
        labels={'专业': 'major', '上课出勤率': '平均上课出勤率'},
        # 隐藏colorbar标题，更简洁
        color_continuous_midpoint=attendance_data['上课出勤率'].mean()
    )
    # 调整colorbar位置和显示格式
    fig_attendance.update_layout(
        coloraxis_colorbar=dict(
            title='',  # 去掉colorbar标题
            thicknessmode='pixels', thickness=20,
            lenmode='pixels', len=300
        ),
        yaxis=dict(range=[0, 1])
    )
    st.plotly_chart(fig_attendance, use_container_width=True)

with col_right:
    # 展示排序表格（右侧）
    st.subheader("上课出勤率排名")
    # 选择需要展示的列（排名、专业、平均出勤率），并调整列顺序
    display_table = attendance_sorted[['排名', '专业', '平均上课出勤率(%)']]
    # 重命名列名（可选，与示例图一致）
    display_table.columns = ['排名', '专业', '平均上课出勤率(%)']
    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True  # 隐藏默认索引
   )





st.markdown('***')
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 读取数据
df1 = pd.read_csv('student_data_adjusted_rounded.csv', encoding='utf-8')

# 4. 大数据管理专业专项分析
st.header("4. 大数据管理专业专项分析")

# 筛选大数据管理专业的数据
bigdata_df = df1[df1['专业'] == '大数据管理']

# 计算关键指标
if not bigdata_df.empty:
    # 计算各项指标
    avg_attendance = bigdata_df['上课出勤率'].mean() * 100 if '上课出勤率' in bigdata_df.columns else 0
    avg_score = bigdata_df['期末考试分数'].mean() if '期末考试分数' in bigdata_df.columns else 0
    pass_rate = (bigdata_df['期末考试分数'] >= 60).mean() * 100 if '期末考试分数' in bigdata_df.columns else 0
    avg_study_time = bigdata_df['每周学习时长（小时）'].mean() if '每周学习时长（小时）' in bigdata_df.columns else 0

    # 显示关键指标卡片（使用4列布局）
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("平均上课出勤率", f"{avg_attendance:.1f}%")
    
    with kpi2:
        st.metric("平均期末考试分数", f"{avg_score:.1f}分")
    
    with kpi3:
        st.metric("及格率", f"{pass_rate:.1f}%")
    
    with kpi4:
        st.metric("平均每周学习时长（小时）", f"{avg_study_time:.1f}小时")

    # 绘制成绩分布和箱线图（2列布局）
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        # 成绩分布直方图（使用亮青色）
        fig = px.histogram(
            bigdata_df,
            x='期末考试分数',
            title='大数据管理专业期末成绩分布',
            color_discrete_sequence=['#0CEBEB'],  # 亮青色
            template='plotly_dark'
        )
        fig.update_layout(
            font=dict(color='white'),
            xaxis_title='final_score',
            yaxis_title='count'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with fig_col2:
        # 成绩箱线图（使用青绿色渐变）
        fig = px.box(
            bigdata_df,
            y='期末考试分数',
            title='大数据管理专业期末成绩箱线图',
            color_discrete_sequence=['#1DD3B0'],  # 青绿色
            template='plotly_dark'
        )
        fig.update_layout(
            font=dict(color='white'),
            yaxis_title='final_score',
            xaxis=dict(showticklabels=False)  # 隐藏x轴刻度
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("未找到大数据管理专业的数据")
