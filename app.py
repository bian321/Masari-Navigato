import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")

# استدعاء المفتاح السري من Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح السري (API Key) غير موجود في الإعدادات!")

# تحديد اسم الموديل بدقة (هنا حل مشكلة الـ NotFound)
# استخدمنا الإصدار الثابت والأكثر توافقاً
MODEL_NAME = 'gemini-1.5-flash-latest' 

st.title("🗺️ مساري - البوصلة المهنية")

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "أهلاً بكِ وبك في رحلة اكتشاف المسار. 🚀 أنا 'مساري'. احكي لي عن تخصصك وهواياتك لنرسم طريقك سوا!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا أفكر؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعريف الموديل داخل المحادثة للتأكد من استدعاء الخدمة صح
            model = genai.GenerativeModel(MODEL_NAME)
            
            # توجيهات النظام
            system_instruction = "أنت خبير توجيه مهني اسمك 'مساري'. لغتك ودودة ومهنية."
            
            response = model.generate_content(f"{system_instruction}\n\nالمستخدم: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("لم أستطع توليد رد، حاول مرة أخرى.")
        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
