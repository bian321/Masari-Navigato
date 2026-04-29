import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")
st.title("🗺️ مساري - البوصلة المهنية")

# 1. الأمان والربط
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("تأكدي من وضع GOOGLE_API_KEY في إعدادات Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

@st.cache_resource
def load_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except: return None

model = load_model()

# 2. قائمة الأسئلة
QUESTIONS = [
    "لو كان أمامك يوم إجازة كامل، كيف ستقضيه؟ وما هي الأنشطة التي تمنحك شعوراً بالسعادة والإنجاز دون أن تشعر بالوقت؟",
    "ما هي المواضيع التي تستمتع بالقراءة عنها أو مشاهدة الأفلام الوثائقية حولها؟ هل هناك تقنيات أو ابتكارات معينة تلفت انتباهك؟",
    "هل تجد نفسك تنجذب أكثر للأرقام والتحليل، أم للتصميم والإبداع، أم للتفاعل مع الناس وحل مشاكلهم؟",
    "ما هي المهارات التي تمتلكها حالياً؟ وما الذي يطلب منك أصدقاؤك المساعدة فيه غالباً؟",
    "لو تخيلت بيئة عملك المستقبلية، كيف ستكون؟ (مكتب، فريق، عمل حر، سفر؟)",
    "ما الذي يحفزك أكثر؟ (الإنجاز الشخصي، المال، مساعدة الآخرين؟) وما الأشياء التي تمل منها سريعاً؟"
]

# 3. تهيئة الجلسة
if "messages" not in st.session_state:
    intro_text = (
        "أهلاً بكِ وبك في رحلة اكتشاف الذات! ✨\n\n"
        "أنا **'مساري'**، بوصلتك المهنية الذكية. 🗺️\n"
        "رح أسألك كم سؤال، واحد ورا الثاني، عشان أرسم لك مسارك صح.\n\n"
        "**السؤال الأول:** " + QUESTIONS[0]
    )
    st.session_state.messages = [{"role": "assistant", "content": intro_text}]
    st.session_state.question_index = 0
    st.session_state.user_answers = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. التفاعل (مرة واحدة فقط خارج أي Loop)
if prompt := st.chat_input("اكتب إجابتك هنا..."):
    # إضافة رد المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_answers.append(prompt)
    st.rerun() # لإعادة تحديث الصفحة وعرض رسالة المستخدم فوراً

# 6. معالجة الرد من "مساري"
if len(st.session_state.user_answers) > st.session_state.question_index:
    with st.chat_message("assistant"):
        st.session_state.question_index += 1
        
        if st.session_state.question_index < len(QUESTIONS):
            next_q = QUESTIONS[st.session_state.question_index]
            st.markdown(next_q)
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        else:
            if model:
                try:
                    with st.spinner("جاري تحليل شخصيتك ورسم مسارك..."):
                        summary_data = "\n".join([f"سؤال {i+1}: {st.session_state.user_answers[i]}" for i in range(len(QUESTIONS))])
                        system_instruction = "أنت خبير التوجيه المهني 'مساري'. قدم تحليلاً و3 مهن وخطة عمل بأسلوب ملهم."
                        response = model.generate_content(f"{system_instruction}\n\nبيانات:\n{summary_data}")
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"خطأ: {e}")
