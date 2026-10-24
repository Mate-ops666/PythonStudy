import os
import streamlit as st
from zhipuai import ZhipuAI

# 页面标题
st.title("💼 AI 简历优化助手")

# 🚨 这里填你的真实 Key，记得保留两边的英文双引号
client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

# 上传文件
uploaded_file = st.file_uploader("上传你的简历文本 (仅支持 txt)", type=["txt"])
resume_text = ""
if uploaded_file is not None:
    try:
        # 第一优先：尝试用国际标准 utf-8 读取
        resume_text = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        # 如果失败，重置指针，尝试用 Windows 常用的 gbk 读取
        uploaded_file.seek(0) 
        resume_text = uploaded_file.read().decode("gbk", errors="ignore")
    st.success("文件读取成功！")

# 输入框
user_input = st.text_input("你想让 AI 怎么帮你改？", "请用 STAR 法则帮我润色这段经历")

# 按钮
if st.button("开始优化"):
    if not resume_text:
        st.warning("请先上传一份 txt 简历文件哦！")
    else:
        with st.spinner("AI 正在疯狂思考中..."):
            prompt = f"这是我的简历内容：\n{resume_text}\n\n我的要求：{user_input}"
            try:
                response = client.chat.completions.create(
                    model="glm-4-flash", 
                    messages=[
                        {"role": "system", "content": "你是一个拥有10年经验的世界500强HR，精通STAR法则。请用专业的口吻帮用户优化简历。"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.markdown("### ✨ AI 优化结果：")
                st.info(response.choices[0].message.content)
            except Exception as e:
                st.error(f"哎呀报错了：{e}")