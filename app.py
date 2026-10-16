import streamlit as st
import time

st.set_page_config(page_title="देवदूत केअर - RedBus Style Demo", layout="wide", initial_sidebar_state="collapsed")

# १. इन-मेमरी डेटा व स्टेट
if "selected_slot" not in st.session_state:
    st.session_state.selected_slot = None
if "current_serving" not in st.session_state:
    st.session_state.current_serving = 2
if "tokens_data" not in st.session_state:
    # RedBus Style Seat/Token Layout: 1 to 10
    # Odd = Counter (Reserved/Grey), Even = Online (Available/Booked)
    st.session_state.tokens_data = {
        1: {"type": "Counter", "status": "COMPLETED", "name": "रमेश पाटील"},
        2: {"type": "Online", "status": "IN_CABIN", "name": "सुनीता देशमुख"},
        3: {"type": "Counter", "status": "WAITING", "name": "काऊंटर वॉक-इन"},
        4: {"type": "Online", "status": "AVAILABLE", "name": None},
        5: {"type": "Counter", "status": "WAITING", "name": "काऊंटर वॉक-इन"},
        6: {"type": "Online", "status": "AVAILABLE", "name": None},
        7: {"type": "Counter", "status": "WAITING", "name": "काऊंटर वॉक-इन"},
        8: {"type": "Online", "status": "AVAILABLE", "name": None},
    }

# २. वरचा हेडर आणि ब्रँडिंग
st.markdown("""
<div style="text-align: center; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px;">
    <h2 style="color: #0b2545; margin: 0;">🏥 DEVDOOT CARE</h2>
    <p style="color: #00a896; font-size: 13px; font-weight: bold; margin: 2px 0;">YOUR DIGITAL HEALTHCARE PARTNER</p>
    <p style="color: #555; font-size: 12px; margin: 0;">मार्गदर्शक: डॉ. संजय कदम (माजी संचालक, शासकीय रुग्णालय, नांदेड)</p>
</div>
""", unsafe_allow_html=True)

# मोड स्विच (रेडबस रुग्ण व्ह्यू किंवा डॉक्टर कंट्रोल)
mode = st.radio("मोड निवडा:", ["📱 रुग्ण बुकिंग व थेट ट्रॅकर (RedBus View)", "👨‍⚕️ डॉक्टर केबिन कंट्रोल (Next Patient)"], horizontal=True)

st.markdown("---")

# =============================================================================
# मोड १: रेडबस स्टाईल रुग्ण बुकिंग व टोकन ग्रिड (RedBus View)
# =============================================================================
if mode == "📱 रुग्ण बुकिंग व थेट ट्रॅकर (RedBus View)":
    
    # डॉक्टर सर्च कार्ड
    st.markdown("""
    <div style="background-color: #f8f9fa; border-left: 5px solid #00a896; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
        <h3 style="margin: 0; color: #0b2545;">👨‍⚕️ डॉ. सचिन काळे (M.D. Medicine)</h3>
        <p style="margin: 2px 0; color: #666; font-size: 13px;">मौर्या हॉस्पिटल, वजिराबाद, नांदेड | ओपीडी वेळ: १०:०० AM ते ०२:०० PM</p>
        <span style="background-color: #e8f5e9; color: #2e7d32; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟢 ओपीडी वेळेवर सुरू आहे</span>
        <span style="color: #d90429; font-weight: bold; float: right; font-size: 15px;">फी: ₹३००</span>
    </div>
    """, unsafe_allow_html=True)

    # RedBus Style Live Radar Bar
    curr = st.session_state.current_serving
    st.markdown(f"""
    <div style="background-color: #e3f2fd; border: 1px solid #90caf9; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
        <span style="color: #1565c0; font-weight: bold; font-size: 14px;">📍 थेट ओपीडी रडार (Live Queue):</span><br>
        सध्या केबिनमध्ये: <b>टोकन #{curr}</b> | अंदाजे तपासणी वेग: <b>८ मि./रुग्ण</b>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("💺 तुमची वेळ / टोकन निवडा (RedBus Token Map)")
    st.caption("⚪ राखाडी = काऊंटर राखीव (Odd) | 🔴 लाल = बुक | 🟢 हिरवा = ऑनलाईन उपलब्ध (Even)")

    # रेडबस स्टाईल सीट ग्रिड (२-कॉलम रचना)
    cols = st.columns(4)
    for idx, (t_no, data) in enumerate(st.session_state.tokens_data.items()):
        col = cols[idx % 4]
        with col:
            if data["status"] == "COMPLETED":
                st.button(f"#{t_no}\nपूर्ण", key=f"btn_{t_no}", disabled=True)
            elif data["status"] == "IN_CABIN":
                st.button(f"#{t_no}\nचालू 🟢", key=f"btn_{t_no}", disabled=True)
            elif data["type"] == "Counter":
                st.button(f"#{t_no}\nकाऊंटर", key=f"btn_{t_no}", disabled=True)
            elif data["status"] == "BOOKED":
                st.button(f"#{t_no}\nबुक 🔴", key=f"btn_{t_no}", disabled=True)
            else:
                # उपलब्ध ऑनलाईन टोकन
                if st.button(f"#{t_no}\nनिवडा 🟢", key=f"btn_{t_no}"):
                    st.session_state.selected_slot = t_no

    # टोकन निवडल्यानंतर बुकिंग फॉर्म
    if st.session_state.selected_slot:
        sel = st.session_state.selected_slot
        st.markdown("---")
        st.success(f"तुम्ही **टोकन क्रमांक #{sel}** निवडला आहे.")
        
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("रुग्णाचे नाव:", "आनंद जोशी")
        with c2:
            p_phone = st.text_input("व्हॉट्सॲप नंबर:", "98XXXXXXXX")
        
        st.markdown("""
        **भाडे व फी तपशील (RedBus Summary):**  
        • डॉक्टर तपासणी फी: **₹३००**  
        • देवदूत केअर सुविधा शुल्क: **₹२०**  
        • **एकूण देय रक्कम: ₹३२०**
        """)
        
        if st.button("💳 ₹३२० भरा आणि कन्फर्म करा", type="primary"):
            st.session_state.tokens_data[sel]["status"] = "BOOKED"
            st.session_state.tokens_data[sel]["name"] = p_name
            st.session_state.selected_slot = None
            st.balloons()
            st.success("टोकन यशस्वीरित्या बुक झाले आहे!")
            
            # बनावट व्हॉट्सॲप मेसेज कार्ड
            st.markdown(f"""
            <div style="background-color: #dcf8c6; border: 1px solid #25d366; border-radius: 8px; padding: 12px; margin-top: 10px;">
                <b>💬 व्हॉट्सॲप अलर्ट पाठवला:</b><br>
                नमस्कार <b>{p_name}</b>, आपले टोकन <b>#{sel}</b> निश्चित झाले आहे.<br>
                हॉस्पिटल: मौर्या हॉस्पिटल, वजिराबाद, नांदेड.<br>
                अंदाजे वेळ: सकाळी १०:३० AM.
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# मोड २: डॉक्टर केबिन कंट्रोल (Next Patient & Audio)
# =============================================================================
else:
    st.title("👨‍⚕️ डॉक्टर केबिन कन्सोल")
    st.write(f"सध्या केबिनमध्ये चालू टोकन: **#{st.session_state.current_serving}**")
    
    if st.button("🔔 पुढील रुग्ण बोलवा (Next Patient)", type="primary"):
        st.session_state.current_serving += 1
        st.rerun()
        
    # मराठी व्हॉईस अनाउन्समेंट
    curr = st.session_state.current_serving
    announcement = f"टोकन नंबर {curr}... कृपया डॉक्टर सचिन काळे यांच्या केबिनमध्ये यावे."
    st.components.v1.html(f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{announcement}');
        msg.lang = 'mr-IN';
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
    st.info(f"टीव्हीवर घोषणा झाली: '{announcement}'")
