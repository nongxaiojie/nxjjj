import streamlit as st
st.set_page_config(page_title='项目介绍', page_icon='📋')
st.set_page_config(layout='wide')
st.title('🎓学生成绩分析与预测系统')
st.markdown('***')
c1, c2 = st.columns([1,2])
with c1:
    st.header('📋项目概述')
    st.markdown("""***:blue[本项目是一个基于Streamlit的学生成绩分析平台，通过数据可视化和机器学习技术，帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。]***""")
    st.subheader('主要特点：')
    st.markdown('''- 📊:blue[数据可视化]：多维度展示学生的学业数据''')
    st.markdown('''- 💯:blue[专业分析]：按专业分类的详细统计分析''')
    st.markdown('''- 🈯:blue[智能预测]：基于机器学习模型的成绩预测''')
    st.markdown('''- 💡:blue[学习建议]：根据预测结果提供个性化反馈''')
with c2:
    images = [
    {
        'url': 'xiaojie/pages/images/1.jpg',
        'parm': '图一'
     },
    {
        'url': 'xiaojie/pages/images/2.jpg',
        'parm':'图二'
    },
    {
        'url':'xiaojie/pages/images/3.jpg',
        'parm': '图三'
    },
    {
        
        'url':'xiaojie/pages/images/4.jpg',
        'parm': '图四'}
]
    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0
    def nextImg():
        st.session_state['ind'] = (st.session_state['ind'] + 1) % len(images)
    def prevImg():
        st.session_state['ind'] = (st.session_state['ind'] - 1) % len(images)
    st.image(images[st.session_state['ind']]['url'], caption=images[st.session_state['ind']]['parm'])
    s1, s2 = st.columns(2)
    with s1:
        st.button('⏮上一张', on_click=prevImg, use_container_width=True)
    with s2:
        st.button('⏭下一张', on_click=nextImg, use_container_width=True)

st.markdown('***')
st.header('🚩项目目标')
a1, a2, a3 = st.columns(3)
with a1:
    st.subheader('⭐目标一')
    st.markdown('***:blue[分析影响因素]***')
    st.markdown('''- 识别关键学习指标''')
    st.markdown('''- 探索成绩相关因素''')
    st.markdown('''- 提供数据支持决策''')
with a2:
    st.subheader('📈目标二')
    st.markdown('***:blue[可视化展示]***')
    st.markdown('''- 专业对比分析''')
    st.markdown('''- 性别差异研究''')
    st.markdown('''- 学习模式识别''')
with a3:
    st.subheader('📍目标三')
    st.markdown('***:blue[成绩预测]***')
    st.markdown('''- 机器学习模型''')
    st.markdown('''- 个性化预测''')
    st.markdown('''- 及时干预预警''')
st.markdown('***')
st.header('🔧技术架构')
b1, b2, b3, b4 = st.columns(4)
with b1:
    st.text('前端架构')
    python_code = '''Streamlit'''
    st.code(python_code)
with b2:
    st.text('数据处理')
    python_code = '''Pandas
NumPy'''
    st.code(python_code)
with b3:
    st.text('可视化')
    python_code = '''Ploty
Matplotlib'''
    st.code(python_code)
with b4:
    st.text('机器学习')
    python_code = '''Scikit-learn'''
    st.code(python_code)
