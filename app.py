import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")
st.title("🗺️ مساري - البوصلة المهنية")

# جلب المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# دالة لاكتشاف الموديل الشغال تلقائياً
def get_working_model():
    try:
        # محاولة أولى بالاسم الشائع
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        try:
            # محاولة البحث في القائمة المتاحة للحساب
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return genai.GenerativeModel(m.name)
        except Exception as e:
            st.error(f"فشل الاتصال بجوجل: {e}")
            return None

model = get_working_model()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً بك في 'مساري'. كيف أساعدك اليوم؟"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا أفكر؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطأ في التوليد: {e}")
        else:
            st.error("لم يتم العثور على موديل متاح لهذا المفتاح.")
