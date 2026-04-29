import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")
st.title("🗺️ مساري - البوصلة المهنية")

# جلب المفتاح من السيكريت
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("تأكدي من وضع GOOGLE_API_KEY في إعدادات Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# وظيفة للبحث عن أول موديل متاح يدعم الدردشة
@st.cache_resource
def load_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            # بنطبع أول موديل لقيناه عشان نتأكد
            return genai.GenerativeModel(available_models[0])
        else:
            return None
    except Exception as e:
        st.error(f"خطأ في الوصول للموديلات: {e}")
        return None

model = load_model()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "أهلاً بكِ وبك في رحلة اكتشاف المسار. 🚀 أنا 'مساري'. \n\nاحكي لي شوي عنك: شو درست؟ وشو الإشي اللي بتحب تعمله وبتنسى الوقت وأنت بتسويه؟"
        }
    ]

# الجزء الخاص بتوليد الرد (الذكاء والشخصية)
if prompt := st.chat_input("احكي لي عن تطلعاتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                # تعليمات النظام ليرجع البوت "مساري" الخبير
                system_instruction = (
                    "أنت خبير التوجيه المهني 'مساري'. مهمتك مساعدة الشباب في العثور على تقاطع أحلامهم مع سوق العمل. "
                    "ابدأ دائماً بتحليل كلام المستخدم، قدم خطة عمل (Roadmap) مقسمة لـ 90 يوماً، واقترح مهارات تقنية. "
                    "تحدث بلغة عربية سلسة ومحفزة."
                )
                
                full_prompt = f"{system_instruction}\n\nالمستخدم: {prompt}"
                response = model.generate_content(full_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"فشل في توليد الرد: {e}")
