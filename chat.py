import html

import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="484ba7f228044a8a86f31b9969d0c110.XJ50PifKp79EdDLe")

st.set_page_config(
    page_title="AI 聊天助手",
    page_icon="💬",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 45%, #312e81 100%);
        color: #e2e8f0;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .answer-box {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 1rem;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        line-height: 1.7;
        color: #f1f5f9;
        white-space: pre-wrap;
    }
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">💬 AI 聊天助手</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">基于智谱 AI · glm-4-flash</div>',
    unsafe_allow_html=True,
)

if "answer" not in st.session_state:
    st.session_state.answer = ""
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

question = st.text_input(
    "请输入你的问题",
    placeholder="例如：请根据我上传的简历，帮我改写这段经历",
    label_visibility="collapsed",
)
uploaded_file = st.file_uploader(
    "可选：上传一份 txt 文本（比如简历）",
    type=["txt"],
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    send = st.button("发送", use_container_width=True)

if send:
    if not question.strip():
        st.warning("请先输入问题再发送。")
    else:
        with st.spinner("模型思考中，请稍候…"):
            try:
                file_text = ""
                if uploaded_file is not None:
                    file_text = uploaded_file.getvalue().decode("utf-8", errors="replace")

                user_content = question.strip()
                if file_text.strip():
                    user_content += (
                        "\n\n以下是用户上传的文本内容，请结合这份材料作答：\n"
                        f"{file_text}"
                    )

                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {
                            "role": "system",
                            "content": "你现在是一位拥有10年经验的世界500强HR，精通STAR法则。请用极其专业的口吻，帮用户把粗糙的简历经历改写得高大上，并加上量化数据。如果用户随便聊天，请拒绝并提醒他发送简历。",
                        },
                        {"role": "user", "content": user_content},
                    ],
                )
                st.session_state.answer = response.choices[0].message.content
                st.session_state.last_question = question.strip()
            except Exception as e:
                st.session_state.answer = ""
                st.error(f"调用智谱 AI 失败：{e}")

if st.session_state.last_question:
    st.markdown("#### 你的问题")
    st.info(st.session_state.last_question)

if st.session_state.answer:
    st.markdown("#### 模型回答")
    safe_answer = html.escape(st.session_state.answer)
    st.markdown(
        f'<div class="answer-box">{safe_answer}</div>',
        unsafe_allow_html=True,
    )