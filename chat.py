import streamlit as st
from zhipuai import ZhipuAI
import pdfplumber
from docx import Document
import io

# 从云端保险箱获取 Key
client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

st.title("AI 简历优化助手")

uploaded_file = st.file_uploader("上传简历文件", type=["txt", "pdf", "docx"])
resume_text = ""

if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == "txt":
            resume_text = uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif file_type == "docx":
            doc = Document(io.BytesIO(uploaded_file.read()))
            resume_text = "\n".join(para.text for para in doc.paragraphs)
        st.success("文件读取成功！")
    except Exception as e:
        st.error(f"读取失败：{e}")

user_input = st.text_input("你想让 AI 怎么帮你改？", "请用 STAR 法则帮我润色这段经历")

if st.button("开始优化"):
    if not resume_text:
        st.warning("请先上传简历文件！")
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