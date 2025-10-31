import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 设置中文字体
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 页面配置
st.set_page_config(page_title="期末成绩预测", page_icon="🔮", layout="wide")
st.title("🔮 期末成绩预测")

# 输入提示文字
st.markdown("***:green[请输入学生的学习信息，系统将根据模型预测期末成绩并提供学习建议]***")

# 输入表单
with st.form("student_form", clear_on_submit=False):
    # 学号输入
    student_id = st.text_input("学号")
    
    # 两列布局
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("性别", ["男", "女"])
        major = st.selectbox("专业", ["大数据管理", "人工智能", "电子商务", "财务管理", "工商管理"])  # 补充专业选项
    with col2:
        study_hours = st.slider("每周学习时长（小时）", 0, 100, 20)
        attendance = st.slider("上课出勤率", 0.0, 1.0, 0.8, 0.01)
        midterm_score = st.slider("期中考试分数", 0.0, 100.0, 70.0, 1.0)
        homework_rate = st.slider("作业完成率", 0.0, 1.0, 0.8, 0.01)
    
    # 预测按钮
    submit_button = st.form_submit_button("预测期末成绩", use_container_width=True)

# 读取真实CSV数据
def load_real_data():
    df = pd.read_csv("student_data_adjusted_rounded.csv", encoding='utf-8')
    # 对类别型特征进行独热编码
    df = pd.get_dummies(df, columns=["性别", "专业"])
    return df

# 训练模型
def train_model(df):
    # 特征和目标变量
    X = df.drop(columns=["学号", "期末考试分数"])
    y = df["期末考试分数"]
    model = LinearRegression()
    model.fit(X, y)
    # 评估模型（可选）
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    return model

# 加载数据并训练模型
real_df = load_real_data()
model = train_model(real_df)

# 预测逻辑
if submit_button:
    # 构造输入数据（包含独热编码的性别和专业）
    input_dict = {
        "每周学习时长（小时）": study_hours,
        "上课出勤率": attendance,
        "期中考试分数": midterm_score,
        "作业完成率": homework_rate,
        "性别_男": 1 if gender == "男" else 0,
        "性别_女": 1 if gender == "女" else 0,
    }
    # 补充专业的独热编码
    for m in ["大数据管理", "人工智能", "电子商务", "财务管理", "工商管理"]:
        input_dict[f"专业_{m}"] = 1 if major == m else 0
    # 转换为DataFrame并确保列顺序与训练数据一致
    input_df = pd.DataFrame([input_dict], columns=real_df.drop(columns=["学号", "期末考试分数"]).columns)
    predicted_score = model.predict(input_df)[0]
    predicted_score = max(0, min(100, predicted_score))  # 确保分数在合理范围
    
    st.subheader("📊 预测结果")
    st.write(f"预测期末分数：{predicted_score:.2f}分")
    
    # 展示图片
    if predicted_score >= 60:
        st.image(
            "https://www.wishesquotesimages.com/wp-content/uploads/2018/09/congratulations-image-free.jpg",
            caption="Congratulations!",
            use_container_width=True
        )
    else:
        st.image(
            "https://img.lovepik.com/free-png/20220109/lovepik-come-on-png-image_401352383_wh860.png",
            caption="继续加油！",
            use_container_width=True
        )
