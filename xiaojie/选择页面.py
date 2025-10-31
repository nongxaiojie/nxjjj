import streamlit as st

# 在侧边栏生成导航按钮
st.sidebar.header("🎓导航菜单")
page = st.sidebar.radio(
    "选择页面：",
    ["项目介绍", "专业数据分析", "成绩预测"]
)

# 根据选择跳转对应的页面（通过运行对应 py 文件实现）
if page == "项目介绍":
    exec(open("xiaojie/项目介绍.py", encoding="utf-8").read())
elif page == "专业数据分析":
    exec(open("xiaojie/专业数据分析.py", encoding="utf-8").read())
elif page == "成绩预测":
    exec(open("xiaojie/成绩预测.py", encoding="utf-8").read())




