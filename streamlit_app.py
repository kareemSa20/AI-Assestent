import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# --- Config ---
API_URL = "http://localhost:8000/api/v1"
st.set_page_config(page_title="Nasseh AI Assistant", layout="wide", page_icon="🤖")

# --- CSS / Styling (RTL for Arabic) ---
st.markdown("""
<style>
    .main { direction: rtl; }
    h1, h2, h3, p, div { text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stChatMessage { text-align: right; direction: rtl; }
    .stTextInput input { text-align: right; direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🤖 مساعد النظام الذكي")
page = st.sidebar.radio("القائمة", ["المحادثة الذكية", "لوحة القيادة", "محاكاة الأحداث"])

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNCTIONS ---
def get_status():
    try:
        return requests.get(f"{API_URL}/system/status").json()
    except:
        return {"error": "System Offline"}

def get_stock():
    try:
        return requests.get(f"{API_URL}/system/stock").json()
    except:
        return []

# --- PAGE: CHAT ---
if page == "المحادثة الذكية":
    st.header("💬 ناصح: العقل المدبر للنظام")
    
    # Display Status Badge
    status = get_status()
    if "error" in status:
        st.error("⚠️ النظام غير متصل بالخادم (Backend Offline)")
    else:
        st.success(f"✅ النظام متصل | Vision: {'Active' if status.get('vision_system_active') else 'Down'}")

    # Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call API
        with st.spinner("ناصح يفكر..."):
            try:
                resp = requests.post(f"{API_URL}/chat", json={"message": prompt})
                if resp.status_code == 200:
                    answer = resp.json()["response"]
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    with st.chat_message("assistant"):
                        st.markdown(answer)
                        
                        # Show Explanation/Context (Explainable AI)
                        with st.expander("🔍 لماذا قلت ذلك؟ (Context)"):
                            st.code(resp.json()["retrieved_context"])
                else:
                    st.error(f"Error {resp.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- PAGE: DASHBOARD ---
elif page == "لوحة القيادة":
    st.header("📊 حالة النظام الحية")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("المخزون الحالي")
        stock = get_stock()
        if stock:
            df = pd.DataFrame(stock)
            st.dataframe(df)
        else:
            st.info("No stock data")
            
    with col2:
        st.subheader("الأحداث الأخيرة")
        try:
            events = requests.get(f"{API_URL}/system/events").json()
            for evt in events:
                severity_color = "red" if evt['severity'] == "High" else "orange"
                st.markdown(f"**{evt['event_type']}** <span style='color:{severity_color}'>({evt['severity']})</span> - {evt['timestamp']}", unsafe_allow_html=True)
                st.text(evt['details'])
                st.divider()
        except:
            st.info("No events")

# --- PAGE: SIMULATOR ---
elif page == "محاكاة الأحداث":
    st.header("⚡ محرك اتخاذ القرار (Simulation)")
    
    st.info("هذه الصفحة لتجربة رد فعل الذكاء الاصطناعي تجاه أحداث النظام.")
    
    col1, col2 = st.columns(2)
    with col1:
        event_type = st.selectbox("نوع الحدث", ["Damage", "MissingLabel", "Expired", "HighTemp"])
    with col2:
        severity = st.selectbox("الخطورة", ["Low", "Medium", "High", "Critical"])
        
    details = st.text_area("تفاصيل الحدث", "مثال: GlassBroken inside pallet #55")
    
    if st.button("تحليل الحدث واقتراح قرار"):
        event_payload = {
            "event_id": "SIM-001",
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "event_type": event_type,
            "details": details,
            "severity": severity
        }
        
        with st.spinner("جاري التحليل..."):
            try:
                resp = requests.post(f"{API_URL}/analyze/event", json=event_payload)
                if resp.status_code == 200:
                    dec = resp.json()
                    
                    st.subheader("💡 القرار المقترح")
                    
                    # Visual Card
                    st.markdown(f"""
                    <div style="padding: 20px; border-left: 5px solid {'green' if dec['action'] != 'IMMEDIATE_DISPOSAL' else 'red'}; background-color: #f0f2f6;">
                        <h3>{dec['action']}</h3>
                        <p>{dec['reasoning']}</p>
                        <hr>
                        <small><b>Source:</b> {dec['source']} | <b>Confidence:</b> {dec['confidence']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error("Error analyzing event")
            except Exception as e:
                st.error(e)
