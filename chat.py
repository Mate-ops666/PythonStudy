import streamlit as st
import base64
from zhipuai import ZhipuAI
import pdfplumber
from docx import Document
import io

# 初始化客户端
client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

st.title("AI 简历优化助手")

# 1. 文件上传组件，现在支持图片了
uploaded_file = st.file_uploader("上传简历文件 (支持 PDF/TXT/Word/图片)", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])

resume_text = ""

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    # 如果是纯文本、PDF 或 Word，用原来的方式读取
    if file_type in ["txt", "pdf", "docx"]:
        try:
            if file_type == "txt":
                resume_text = uploaded_file.read().decode("utf-8")
            elif file_type == "pdf":
                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                    resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            elif file_type == "docx":
                doc = Document(io.BytesIO(uploaded_file.read()))
                resume_text = "\n".join(para.text for para in doc.paragraphs)
            st.success("文档读取成功！")
        except Exception as e:
            st.error(f"文档读取失败：{e}")
            
    # 如果是图片，调用 GLM-4V-Flash 视觉模型
    elif file_type in ["jpg", "jpeg", "png"]:
        with st.spinner("正在用 AI 视觉模型识别图片中的文字..."):
            try:
                # 将图片转换为 Base64 编码
                img_bytes = uploaded_file.getvalue()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                
                # 智谱 API 需要带上图片前缀
                img_url = f"data:image/{file_type};base64,{img_base64}"
                
                # 调用视觉模型进行 OCR
                response = client.chat.completions.create(
                    model="glm-4v-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "请提取这张简历图片中的所有文字，保持原有格式，不要添加任何额外解释。"},
                                {"type": "image_url", "image_url": {"url": img_url}}
                            ]
                        }
                    ]
                )
                resume_text = response.choices[0].message.content
                st.success("图片文字识别成功！")
                st.text_area("识别出的原始文字 (可手动修正)", resume_text, height=200)
            except Exception as e:
                st.error(f"图片识别失败：{e}")

# 2. 用户输入和优化按钮
user_input = st.text_input("你想让 AI 怎么帮你改？", "请用 STAR 法则帮我润色这段经历")

if st.button("开始优化"):
    if not resume_text:
        st.warning("请先上传文件或图片！")
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
                st.error(f"优化失败：{e}")