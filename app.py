import streamlit as st
import google.generativeai as genai
import os

# إعداد واجهة الصفحة
st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")

st.title("🗺️ مساري - البوصلة المهنية")
st.markdown("دليلك الذكي لتصميم مسارك المهني بعد التخرج.")

# إعداد المفتاح السري (سنجلبه من إعدادات Streamlit لاحقاً)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# إعداد الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []
    # رسالة الترحيب
    welcome_msg = "أهلاً بكِ وبك في رحلة اكتشاف المسار. 🚀 أنا 'مساري'. احكي لي شوي عنك: شو درست؟ وشو الإشي اللي بتحب تعمله؟"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("كيف بقدر أساعدك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # إرسال المحادثة كاملة للموديل مع توجيهات النظام
        system_instruction = "أنت خبير التوجيه المهني 'مساري'. ساعد المستخدم في وضع خطة عمل. تحدث بالعربية."
        full_prompt = f"{system_instruction}\n\nUser says: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})