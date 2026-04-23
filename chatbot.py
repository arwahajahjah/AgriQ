"""
chatbot.py — AgriQ Agricultural Assistant
Powered by Groq API (100% Free)
---------------------------------------
Setup:
  1. Sign up at https://console.groq.com and get a free API key
  2. Set environment variable:  export GROQ_API_KEY="gsk_..."
     OR create a .streamlit/secrets.toml file:
        GROQ_API_KEY = "gsk_......"
  3. Install dependency:  pip install groq
"""

import os
import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

MODEL = "llama3-70b-8192"          # Best free model on Groq for Arabic
MAX_HISTORY = 20                    # Keep last N messages in context window
MAX_TOKENS = 1024                   # Max tokens per response

# ─────────────────────────────────────────────────────────────────────────────
# Groq client — resolves key from env or Streamlit secrets
# ─────────────────────────────────────────────────────────────────────────────

def _get_groq_client():
    """Return a Groq client using the API key from env or st.secrets."""
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


# ─────────────────────────────────────────────────────────────────────────────
# System prompt builder
# ─────────────────────────────────────────────────────────────────────────────

def _build_system_prompt(context: dict) -> str:
    city        = context.get("city", "فلسطين")
    temperature = context.get("temperature", "غير معروف")
    humidity    = context.get("humidity", "غير معروف")
    rec_crop    = context.get("recommended_crop", "")
    soil_n      = context.get("soil_n", "")
    soil_p      = context.get("soil_p", "")
    soil_k      = context.get("soil_k", "")

    crop_line = (
        f"- آخر محصول موصى به من النظام: {rec_crop}\n" if rec_crop else ""
    )
    soil_line = (
        f"- بيانات التربة: نيتروجين={soil_n} ppm، فسفور={soil_p} ppm، بوتاسيوم={soil_k} ppm\n"
        if soil_n else ""
    )

    return f"""أنت مساعد زراعي ذكي اسمه "AgriQ Bot" متخصص في الزراعة الفلسطينية والاقتصاد الزراعي.

معلومات المزارع الحالي:
- المدينة/المنطقة: {city}
- درجة الحرارة الحالية: {temperature}°C
- الرطوبة: {humidity}%
{crop_line}{soil_line}
دورك:
1. تقديم نصائح زراعية دقيقة ومناسبة للبيئة الفلسطينية (الضفة الغربية وغزة).
2. مساعدة المزارعين على اتخاذ قرارات اقتصادية ذكية تتعلق بالمحاصيل.
3. الإجابة عن أسئلة الري والتربة والآفات والأسمدة.
4. تحليل السوق المحلي وتوقعات الأسعار الموسمية.
5. تقديم توصيات لتقليل استهلاك المياه في ظل شح المياه.

قواعد التواصل:
- تحدث دائماً بالعربية الفصحى البسيطة المفهومة للمزارع.
- كن موجزاً ومباشراً، لا تطول الردود دون داعٍ.
- استخدم الأرقام والنسب المئوية عند الحاجة لتوضيح التوصيات.
- إذا سألك عن محصول معين، قارنه بالمحصول الموصى به من نظام AgriQ.
- ابدأ ردودك بـ 🌱 دائماً.
- إذا لم تعرف الإجابة الدقيقة، قل ذلك بوضوح واقترح استشارة مهندس زراعي محلي.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Core chat function
# ─────────────────────────────────────────────────────────────────────────────

def _chat_with_groq(client, messages: list) -> str:
    """Send messages to Groq and return the assistant reply as a string."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_str = str(e)
        if "401" in error_str or "authentication" in error_str.lower():
            return "❌ **خطأ في المصادقة:** مفتاح GROQ_API_KEY غير صحيح أو غير موجود. يرجى التحقق منه."
        elif "429" in error_str or "rate" in error_str.lower():
            return "⏳ **تجاوزت الحد المسموح:** الرجاء الانتظار لحظة ثم أعد المحاولة."
        elif "503" in error_str or "unavailable" in error_str.lower():
            return "🔧 **خدمة Groq غير متاحة مؤقتاً:** الرجاء المحاولة بعد قليل."
        else:
            return f"⚠️ **خطأ غير متوقع:** {error_str}"


# ─────────────────────────────────────────────────────────────────────────────
# Suggested quick questions
# ─────────────────────────────────────────────────────────────────────────────

QUICK_QUESTIONS = [
    "ما أفضل محصول للزراعة في موسم الشتاء؟",
    "كيف أقلل استهلاك المياه في الري؟",
    "ما أسباب اصفرار أوراق النبات وعلاجه؟",
    "كيف أحمي محصولي من الآفات بدون مبيدات كيماوية؟",
    "ما توقع أسعار الطماطم في الموسم القادم؟",
    "ما الفرق بين التسميد العضوي والكيماوي؟",
    "كيف أعرف درجة حموضة التربة وكيف أعدّلها؟",
    "متى أبدأ بالحصاد ومتى أبيع لأحصل على أفضل سعر؟",
]


# ─────────────────────────────────────────────────────────────────────────────
# CSS styles (scoped to chatbot tab)
# ─────────────────────────────────────────────────────────────────────────────

CHATBOT_CSS = """
<style>
/* ── Chat container ── */
.agribot-chat-wrapper {
    direction: rtl;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ── Message bubbles ── */
.agribot-msg {
    display: flex;
    margin: 12px 0;
    align-items: flex-start;
    gap: 10px;
    animation: fadeInUp 0.3s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0);   }
}

.agribot-msg.user  { flex-direction: row-reverse; }
.agribot-msg.bot   { flex-direction: row; }

.agribot-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.agribot-avatar.user-av { background: linear-gradient(135deg, #0c4a6e, #075985); }
.agribot-avatar.bot-av  { background: linear-gradient(135deg, #065f46, #047857); }

.agribot-bubble {
    max-width: 78%;
    padding: 12px 16px;
    border-radius: 16px;
    line-height: 1.7;
    font-size: 14.5px;
}
.agribot-msg.user .agribot-bubble {
    background: linear-gradient(135deg, #0c4a6e 0%, #075985 100%);
    color: #e0f2fe;
    border-top-right-radius: 4px;
    text-align: right;
}
.agribot-msg.bot .agribot-bubble {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: #e2e8f0;
    border-top-left-radius: 4px;
    text-align: right;
    border: 1px solid rgba(16,185,129,0.2);
}

/* ── Typing indicator ── */
.typing-indicator {
    display: flex;
    gap: 5px;
    padding: 10px 14px;
    background: rgba(30,41,59,0.8);
    border-radius: 14px;
    width: fit-content;
    border: 1px solid rgba(16,185,129,0.2);
}
.typing-indicator span {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #10b981;
    display: inline-block;
    animation: bounce 1.2s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0);    }
    30%           { transform: translateY(-8px); }
}

/* ── Quick question pills ── */
.quick-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    direction: rtl;
    margin: 12px 0;
}
.quick-pill-label {
    color: #94a3b8;
    font-size: 12px;
    margin-bottom: 6px;
    direction: rtl;
}

/* ── Header banner ── */
.chatbot-header {
    background: linear-gradient(90deg, #065f46 0%, #047857 100%);
    padding: 18px 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    border: 1px solid rgba(16,185,129,0.3);
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    direction: rtl;
}

/* ── API key warning ── */
.api-key-box {
    background: rgba(245,158,11,0.1);
    border: 1px solid #f59e0b;
    border-radius: 10px;
    padding: 16px;
    direction: rtl;
    color: #fde68a;
    line-height: 1.8;
}

/* ── Divider ── */
.chat-divider {
    border: none;
    border-top: 1px solid #334155;
    margin: 20px 0;
}

/* ── Stats row ── */
.chat-stats {
    display: flex;
    gap: 12px;
    direction: rtl;
    margin-bottom: 16px;
}
.chat-stat-badge {
    background: rgba(30,41,59,0.7);
    border: 1px solid #475569;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: #94a3b8;
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Main UI function
# ─────────────────────────────────────────────────────────────────────────────

def render_chatbot_ui(context: dict = None):
    """
    Render the AgriQ chatbot tab in Streamlit.

    Parameters
    ----------
    context : dict, optional
        Keys: city, temperature, humidity, recommended_crop,
              soil_n, soil_p, soil_k
    """
    if context is None:
        context = {}

    # ── Inject CSS ──────────────────────────────────────────────────────────
    st.markdown(CHATBOT_CSS, unsafe_allow_html=True)

    # ── Session state init ──────────────────────────────────────────────────
    if "agribot_history" not in st.session_state:
        st.session_state.agribot_history = []   # list of {"role", "content"}
    if "agribot_pending" not in st.session_state:
        st.session_state.agribot_pending = None  # message waiting to be sent

    city = context.get("city", "منطقتك")

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="chatbot-header agribot-chat-wrapper">
        <h2 style="margin:0; color:#d1fae5;">🤖 مساعد AgriQ الزراعي</h2>
        <p style="margin:6px 0 0 0; color:#a7f3d0; font-size:14px;">
            مدعوم بـ Groq (LLaMA 3 70B) · مجاني 100% · منطقتك: <b>{city}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── API key check ────────────────────────────────────────────────────────
    client = _get_groq_client()
    if client is None:
        st.markdown("""
        <div class="api-key-box">
            <b>⚠️ مفتاح Groq API غير موجود</b><br><br>
            الخطوات:
            <ol style="padding-right:20px; margin:10px 0 0 0;">
                <li>سجّل في <a href="https://console.groq.com" style="color:#fbbf24;" target="_blank">console.groq.com</a> واحصل على مفتاح مجاني.</li>
                <li>في الطرفية: <code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;">export GROQ_API_KEY="gsk_..."</code></li>
                <li>أو أنشئ ملف <code>.streamlit/secrets.toml</code> وأضف:<br>
                    <code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;">GROQ_API_KEY = "gsk_..."</code></li>
                <li>أعد تشغيل التطبيق.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Context summary strip ────────────────────────────────────────────────
    temp   = context.get("temperature", "—")
    hum    = context.get("humidity",    "—")
    r_crop = context.get("recommended_crop", "—")
    st.markdown(f"""
    <div class="chat-stats agribot-chat-wrapper">
        <span class="chat-stat-badge">🌡️ {temp}°C</span>
        <span class="chat-stat-badge">💧 {hum}%</span>
        <span class="chat-stat-badge">🌱 {r_crop}</span>
        <span class="chat-stat-badge">💬 {len(st.session_state.agribot_history)//2} رسالة</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick question buttons ───────────────────────────────────────────────
    st.markdown('<p class="quick-pill-label agribot-chat-wrapper">💡 أسئلة سريعة — اضغط لإرسالها مباشرة:</p>',
                unsafe_allow_html=True)

    # Split into 2 rows of 4
    row1 = QUICK_QUESTIONS[:4]
    row2 = QUICK_QUESTIONS[4:]
    cols1 = st.columns(4)
    for i, q in enumerate(row1):
        if cols1[i].button(q, key=f"quick_{i}", use_container_width=True):
            st.session_state.agribot_pending = q

    cols2 = st.columns(4)
    for i, q in enumerate(row2):
        if cols2[i].button(q, key=f"quick_{i+4}", use_container_width=True):
            st.session_state.agribot_pending = q

    st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)

    # ── Chat history display ─────────────────────────────────────────────────
    history = st.session_state.agribot_history

    if not history:
        st.markdown("""
        <div class="agribot-chat-wrapper" style="
            text-align:center; padding:30px 20px; color:#64748b;
            background:rgba(30,41,59,0.4); border-radius:12px; margin:10px 0;">
            <p style="font-size:32px; margin:0;">🌱</p>
            <p style="font-size:16px; margin:8px 0; color:#94a3b8;">
                مرحباً! أنا AgriQ Bot، مساعدك الزراعي الذكي.
            </p>
            <p style="font-size:13px; color:#64748b;">
                اسألني عن المحاصيل، التربة، الري، الأسمدة، أو أسعار السوق.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        chat_html_parts = ['<div class="agribot-chat-wrapper">']
        for msg in history:
            role    = msg["role"]     # "user" or "assistant"
            content = msg["content"]
            # Escape HTML in content
            import html as html_lib
            safe_content = html_lib.escape(content).replace("\n", "<br>")

            if role == "user":
                chat_html_parts.append(f"""
                <div class="agribot-msg user">
                    <div class="agribot-avatar user-av">👤</div>
                    <div class="agribot-bubble">{safe_content}</div>
                </div>""")
            else:
                chat_html_parts.append(f"""
                <div class="agribot-msg bot">
                    <div class="agribot-avatar bot-av">🤖</div>
                    <div class="agribot-bubble">{safe_content}</div>
                </div>""")

        chat_html_parts.append("</div>")
        st.markdown("".join(chat_html_parts), unsafe_allow_html=True)

    # ── Chat input + send ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    input_col, btn_col = st.columns([5, 1], gap="small")

    with input_col:
        user_input = st.text_input(
            label="اكتب سؤالك هنا",
            placeholder="مثال: ما أفضل وقت لزراعة الزيتون في منطقتي؟",
            key="agribot_input",
            label_visibility="collapsed",
        )
    with btn_col:
        send_pressed = st.button("إرسال ✉️", type="primary", use_container_width=True)

    # Clear button (smaller, secondary)
    clear_col, _, _ = st.columns([1, 2, 2])
    with clear_col:
        if st.button("🗑️ مسح المحادثة", key="clear_chat"):
            st.session_state.agribot_history = []
            st.session_state.agribot_pending = None
            st.rerun()

    # ── Determine the message to process ────────────────────────────────────
    final_message = None
    if st.session_state.agribot_pending:
        final_message = st.session_state.agribot_pending
        st.session_state.agribot_pending = None
    elif send_pressed and user_input and user_input.strip():
        final_message = user_input.strip()

    # ── Process and call Groq ────────────────────────────────────────────────
    if final_message:
        # Append user message
        st.session_state.agribot_history.append(
            {"role": "user", "content": final_message}
        )

        # Build full messages list for API call
        system_prompt = _build_system_prompt(context)
        api_messages = [{"role": "system", "content": system_prompt}]

        # Trim history to MAX_HISTORY to avoid exceeding context window
        trimmed = st.session_state.agribot_history[-MAX_HISTORY:]
        api_messages.extend(trimmed)

        # Show typing indicator while waiting
        with st.spinner("🤖 AgriQ Bot يكتب..."):
            reply = _chat_with_groq(client, api_messages)

        # Append bot reply to history
        st.session_state.agribot_history.append(
            {"role": "assistant", "content": reply}
        )

        # Rerun to refresh the chat display
        st.rerun()

    # ── Footer note ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="agribot-chat-wrapper" style="
        text-align:center; color:#475569; font-size:11px; margin-top:20px;">
        مدعوم بـ Groq API (مجاني) · نموذج LLaMA 3 70B · لا يُخزّن أي بيانات خارجياً
    </div>
    """, unsafe_allow_html=True)