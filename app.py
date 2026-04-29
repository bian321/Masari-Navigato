import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساري | Masari", page_icon="🗺️")
st.title("🗺️ مساري - البوصلة المهنية")

# 1. الأمان: جلب المفتاح (نفس طريقتك القديمة الشغالة)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("تأكدي من وضع GOOGLE_API_KEY في إعدادات Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. الأمان: دالة تحميل الموديل (اللي حلت مشكلة 404)
@st.cache_resource
def load_model():
    try:
        # بتبحث عن أي موديل شغال عند جوجل وبتحفظه
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            return genai.GenerativeModel(available_models[0])
        return None
    except Exception as e:
        st.error(f"خطأ في الوصول للموديلات: {e}")
        return None

model = load_model()

# 3. الأسئلة المتسلسلة (اللي طلبتيها)
QUESTIONS = [
    "لو كان أمامك يوم إجازة كامل، كيف ستقضيه؟ وما هي الأنشطة التي تمنحك شعوراً بالسعادة والإنجاز دون أن تشعر بالوقت؟",
    "ما هي المواضيع التي تستمتع بالقراءة عنها أو مشاهدة الأفلام الوثائقية حولها؟ هل هناك تقنيات أو ابتكارات معينة تلفت انتباهك؟",
    "هل تجد نفسك تنجذب أكثر للأرقام والتحليل، أم للتصميم والإبداع، أم للتفاعل مع الناس وحل مشاكلهم؟",
    "ما هي المهارات التي تمتلكها حالياً؟ وما الذي يطلب منك أصدقاؤك المساعدة فيه غالباً؟",
    "لو تخيلت بيئة عملك المستقبلية، كيف ستكون؟ (مكتب، فريق، عمل حر، سفر؟)",
    "ما الذي يحفزك أكثر؟ (الإنجاز الشخصي، المال، مساعدة الآخرين؟) وما الأشياء التي تمل منها سريعاً؟"
]

# 4. تهيئة الجلسة (نفس منطق الكود الشغال)
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

# 5. عرض الرسائل (الضروري لظهور الترحيب)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. معالجة الإجابات (سؤال بسؤال)
if prompt := st.chat_input("اكتب إجابتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_answers.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.session_state.question_index += 1
        
        # إذا لسه في أسئلة، اطرح السؤال التالي
        if st.session_state.question_index < len(QUESTIONS):
            next_q = QUESTIONS[st.session_state.question_index]
            st.markdown(next_q)
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        
        # إذا خلصنا، حلل النتائج بذكاء مساري
        else:
            if model:
                try:
                    with st.spinner("جاري تحليل شخصيتك ورسم مسارك..."):
                        summary_data = "\n".join([f"سؤال {i+1}: {st.session_state.user_answers[i]}" for i in range(len(QUESTIONS))])
                        system_instruction = (
                            "أنت خبير التوجيه المهني 'مساري'. حلل إجابات المستخدم بدقة وقدم له "
                            "تحليل شخصي، 3 مهن عصرية، وخطة عمل 90 يوم. تحدث بلغة ملهمة وعربية."
                        )
                        response = model.generate_content(f"{system_instruction}\n\nبيانات المستخدم:\n{summary_data}")
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"فشل في التحليل النهائي: {e}")
            else:
                st.error("الموديل غير متوفر حالياً.")

# 4. تهيئة الجلسة (نفس منطق الكود الشغال)
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

# 5. عرض الرسائل (الضروري لظهور الترحيب)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. معالجة الإجابات (سؤال بسؤال)
if prompt := st.chat_input("اكتب إجابتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_answers.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.session_state.question_index += 1
        
        # إذا لسه في أسئلة، اطرح السؤال التالي
        if st.session_state.question_index < len(QUESTIONS):
            next_q = QUESTIONS[st.session_state.question_index]
            st.markdown(next_q)
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        
        # إذا خلصنا، حلل النتائج بذكاء مساري
        else:
            if model:
                try:
                    with st.spinner("جاري تحليل شخصيتك ورسم مسارك..."):
                        summary_data = "\n".join([f"سؤال {i+1}: {st.session_state.user_answers[i]}" for i in range(len(QUESTIONS))])
                        system_instruction = (
                            "أنت خبير التوجيه المهني 'مساري'. حلل إجابات المستخدم بدقة وقدم له "
                            "تحليل شخصي، 3 مهن عصرية، وخطة عمل 90 يوم. تحدث بلغة ملهمة وعربية."
                        )
                        response = model.generate_content(f"{system_instruction}\n\nبيانات المستخدم:\n{summary_data}")
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"فشل في التحليل النهائي: {e}")
            else:
                st.error("الموديل غير متوفر حالياً.")          
        
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
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
