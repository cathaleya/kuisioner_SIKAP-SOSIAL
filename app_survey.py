import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime
from questions_data import (
    MINAT_BELAJAR,
    SIKAP_SOSIAL,
    LIKERT_OPTIONS_MINAT,
    LIKERT_OPTIONS_SIKAP
)

# ==========================================
# CONFIG & STYLES
# ==========================================
st.set_page_config(
    page_title="Instrumen Penelitian PPG",
    page_icon="📝",
    layout="centered"
)

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    .stRadio > div {
        background: #ffffff;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #d1fae5;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        border-color: #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }
    
    h1, h2, h3 { 
        color: #064e3b; 
        font-weight: 800; 
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important;
        border-radius: 12px;
        padding: 14px;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.3);
    }

    .header-section {
        background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
        padding: 35px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(6, 78, 59, 0.15);
    }

    .aspect-card {
        background: #ecfdf5;
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin: 25px 0 15px 0;
        font-weight: bold;
        color: #064e3b;
        font-size: 1.1rem;
    }
    
    .success-card {
        background: #f0fdf4;
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        border: 2px solid #bbf7d0;
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.1);
    }

    .selection-card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .selection-card:hover {
        border-color: #10b981;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "instrument" not in st.session_state:
    st.session_state.instrument = None  # "minat" or "sikap" or None
if "page" not in st.session_state:
    st.session_state.page = "select_instrument"  # select_instrument, biodata, aspect_idx, summary, finish
if "biodata" not in st.session_state:
    st.session_state.biodata = {}
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "essay_answers" not in st.session_state:
    st.session_state.essay_answers = {}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def reset_state():
    st.session_state.instrument = None
    st.session_state.page = "select_instrument"
    st.session_state.biodata = {}
    st.session_state.answers = {}
    st.session_state.essay_answers = {}

def get_apps_script_url():
    # Attempt to load from Streamlit secrets
    url = None
    if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    elif "gsheets_url" in st.secrets:
        url = st.secrets["gsheets_url"]
    elif "spreadsheet" in st.secrets:
        url = st.secrets["spreadsheet"]
    return url

def submit_payload(payload):
    url = get_apps_script_url()
    if not url:
        st.error("Konfigurasi URL Google Apps Script tidak ditemukan di secrets.toml!")
        return False
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            try:
                res_json = response.json()
                if res_json.get("result") == "success":
                    return True
                else:
                    # Fallback if Apps Script replies with error
                    return res_json.get("status") == "ok" or res_json.get("result") == "ok"
            except Exception:
                # Fallback if response is successful status but not JSON
                return True
        else:
            st.error(f"Koneksi gagal (Status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        st.error(f"Gagal koneksi ke server: {e}")
        return False

def build_unified_payload(instrument_type, biodata, answers, essay_answers):
    payload = {}
    payload["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload["Jenis_Instrumen"] = "Minat Belajar Mahasiswa" if instrument_type == "minat" else "Sikap Sosial Mahasiswa"
    
    # Biodata
    payload["Nama"] = biodata.get("nama", "")
    payload["Lembaga_PPG"] = biodata.get("lembaga_ppg", "")
    payload["Program_Studi"] = biodata.get("program_studi", "") if instrument_type == "minat" else "N/A"
    payload["Semester"] = biodata.get("semester", "")
    payload["Usia"] = biodata.get("usia", "") if instrument_type == "sikap" else "N/A"
    
    total_score = 0
    
    # Likert items (1 to 28)
    if instrument_type == "minat":
        for i in range(1, 21):
            ans = answers.get(f"q_{i}", None)
            if ans is not None:
                payload[f"Q{i}_Skor"] = ans["score"]
                payload[f"Q{i}_Teks"] = ans["text"]
                total_score += ans["score"]
            else:
                payload[f"Q{i}_Skor"] = ""
                payload[f"Q{i}_Teks"] = ""
        # 21-28 are blank for Minat Belajar
        for i in range(21, 29):
            payload[f"Q{i}_Skor"] = ""
            payload[f"Q{i}_Teks"] = ""
    else:
        for i in range(1, 29):
            ans = answers.get(f"q_{i}", None)
            if ans is not None:
                payload[f"Q{i}_Skor"] = ans["score"]
                payload[f"Q{i}_Teks"] = ans["text"]
                total_score += ans["score"]
            else:
                payload[f"Q{i}_Skor"] = ""
                payload[f"Q{i}_Teks"] = ""
                
    payload["Skor_Total"] = total_score
    
    # Open questions / scenarios (1 to 6)
    if instrument_type == "minat":
        # Minat has 3 open questions
        for i in range(1, 4):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"essay_{i}", "")
        for i in range(4, 7):
            payload[f"Respon_Terbuka_{i}"] = "N/A"
    else:
        # Sikap has 3 scenarios (Open 1-3) and 3 reflections (Open 4-6)
        for i in range(1, 4):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"scenario_{i}", "")
        for i in range(4, 7):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"reflection_{i-3}", "")
            
    return payload

# ==========================================
# PAGE CONTROLLERS
# ==========================================

# 1. SELECT INSTRUMENT PAGE
if st.session_state.page == "select_instrument":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white;">🎓 SISTEM ANGKET PENELITIAN</h1>
            <p style="margin-top:10px; font-size:1.1rem; opacity:0.9;">Silakan pilih instrumen kuisioner di bawah ini untuk memulai pengisian.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="selection-card">
                <h3 style="margin-top:0; color:#064e3b;">📚 Minat Belajar</h3>
                <p style="color:#374151; font-size:0.9rem; min-height:60px;">Mengukur perasaan senang, ketertarikan, relevansi, keterlibatan, dan dorongan ekstrinsik mahasiswa selama perkuliahan PPG.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mulai Angket Minat", key="btn_minat"):
            st.session_state.instrument = "minat"
            st.session_state.page = "biodata"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class="selection-card">
                <h3 style="margin-top:0; color:#064e3b;">🤝 Sikap Sosial</h3>
                <p style="color:#374151; font-size:0.9rem; min-height:60px;">Mengukur aspek tanggung jawab, empati, kerja sama, keteladanan, komunikasi, dan adaptasi sosial calon guru SD.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Mulai Angket Sikap Sosial", key="btn_sikap"):
            st.session_state.instrument = "sikap"
            st.session_state.page = "biodata"
            st.rerun()

# 2. BIODATA ENTRY PAGE
elif st.session_state.page == "biodata":
    inst = MINAT_BELAJAR if st.session_state.instrument == "minat" else SIKAP_SOSIAL
    
    st.markdown(f"""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.6rem; font-weight:800;">{inst['title']}</h1>
            <p style="margin-top:8px; font-size:1rem; opacity:0.95; font-weight:600;">{inst['subtitle']}</p>
            <div style="background-color:rgba(255,255,255,0.2); height:1px; margin: 15px 0;"></div>
            <h3 style="margin:0; color:white; font-size:1.2rem; font-weight:700;">📋 {inst['biodata_title']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("Silakan isi biodata Anda sebelum melanjutkan pengisian angket.")
    
    with st.form("form_biodata"):
        biodata_entries = {}
        for field in inst["biodata_fields"]:
            if field["type"] == "text":
                biodata_entries[field["id"]] = st.text_input(field["label"])
            elif field["type"] == "select":
                biodata_entries[field["id"]] = st.selectbox(field["label"], field["options"])
        
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali Ke Menu")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ➡️")
            
        if back_clicked:
            reset_state()
            st.rerun()
            
        if next_clicked:
            # Validate required inputs
            missing = False
            for field in inst["biodata_fields"]:
                if field["type"] == "text" and not biodata_entries[field["id"]].strip():
                    missing = True
                    break
            
            if missing:
                st.warning("Mohon lengkapi seluruh field biodata.")
            else:
                st.session_state.biodata = biodata_entries
                st.session_state.page = 0  # index of first aspect/page of questions
                st.rerun()

# 3. ASPECT QUESTIONNAIRE PAGES (STEPPED)
elif isinstance(st.session_state.page, int):
    inst_type = st.session_state.instrument
    inst = MINAT_BELAJAR if inst_type == "minat" else SIKAP_SOSIAL
    options_dict = LIKERT_OPTIONS_MINAT if inst_type == "minat" else LIKERT_OPTIONS_SIKAP
    
    aspects_keys = list(inst["likert_aspects"].keys())
    current_aspect_idx = st.session_state.page
    total_aspects = len(aspects_keys)
    
    # Determine what is the next step:
    # After the last Likert aspect, we go to qualitative questions (Open Questions / Scenarios)
    # The qualitative section can be page index = total_aspects.
    
    # Helper to calculate progress percentage
    total_steps = total_aspects + (1 if inst_type == "minat" else 2) # Minat has 1 essay page, Sikap has 2 (scenarios + reflections)
    progress_val = (current_aspect_idx + 1) / total_steps
    
    if current_aspect_idx < total_aspects:
        # Likert Aspect Page
        aspect_name = aspects_keys[current_aspect_idx]
        questions_list = inst["likert_aspects"][aspect_name]
        
        # Calculate overall question index offset
        prev_questions_count = 0
        for i in range(current_aspect_idx):
            prev_questions_count += len(inst["likert_aspects"][aspects_keys[i]])
            
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <h3 style="margin: 0; color: #064e3b;">{inst['title']}</h3>
                <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                    <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {progress_val * 100}%;"></div>
                </div>
                <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Halaman {current_aspect_idx + 1} dari {total_steps}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="aspect-card">{aspect_name}</div>', unsafe_allow_html=True)
        
        with st.form(f"form_aspect_{current_aspect_idx}"):
            page_responses = {}
            for i, question_text in enumerate(questions_list):
                q_num = prev_questions_count + i + 1
                q_key = f"q_{q_num}"
                
                existing_ans = st.session_state.answers.get(q_key, None)
                existing_idx = None
                if existing_ans is not None:
                    existing_idx = [5, 4, 3, 2, 1].index(existing_ans["score"])
                
                choice = st.radio(
                    f"{q_num}. {question_text}",
                    options=[5, 4, 3, 2, 1],
                    format_func=lambda x: options_dict[x],
                    index=existing_idx,
                    key=f"ui_{q_key}",
                    horizontal=True
                )
                page_responses[q_key] = choice
                
            col_back, col_next = st.columns(2)
            with col_back:
                back_clicked = st.form_submit_button("⬅ Kembali")
            with col_next:
                next_clicked = st.form_submit_button("Lanjutkan ➡️")
                
            if back_clicked:
                if current_aspect_idx == 0:
                    st.session_state.page = "biodata"
                else:
                    st.session_state.page = current_aspect_idx - 1
                st.rerun()
                
            if next_clicked:
                # Save page responses to state
                for q_key, score in page_responses.items():
                    st.session_state.answers[q_key] = {
                        "score": score,
                        "text": options_dict[score]
                    }
                st.session_state.page = current_aspect_idx + 1
                st.rerun()

    else:
        # QUALITATIVE QUESTIONS PAGES (index >= total_aspects)
        # Minat has 1 page of open questions
        # Sikap has Scenario page (index = total_aspects) and Reflection page (index = total_aspects + 1)
        
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <h3 style="margin: 0; color: #064e3b;">{inst['title']}</h3>
                <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                    <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {progress_val * 100}%;"></div>
                </div>
                <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Halaman {current_aspect_idx + 1} dari {total_steps}</p>
            </div>
        """, unsafe_allow_html=True)

        if inst_type == "minat":
            # Minat Belajar Open Questions Page
            st.markdown('<div class="aspect-card">D. Pertanyaan Terbuka</div>', unsafe_allow_html=True)
            
            with st.form("form_open_questions"):
                responses = {}
                for i, q_text in enumerate(inst["open_questions"]):
                    essay_key = f"essay_{i+1}"
                    existing_text = st.session_state.essay_answers.get(essay_key, "")
                    responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
                
                col_back, col_next = st.columns(2)
                with col_back:
                    back_clicked = st.form_submit_button("⬅ Kembali")
                with col_next:
                    next_clicked = st.form_submit_button("Lanjutkan ke Ringkasan 🏁")
                    
                if back_clicked:
                    st.session_state.page = total_aspects - 1
                    st.rerun()
                    
                if next_clicked:
                    st.session_state.essay_answers.update(responses)
                    st.session_state.page = "summary"
                    st.rerun()
                    
        else:
            # Sikap Sosial qualitative pages
            # If current index == total_aspects, show Scenarios
            # If current index == total_aspects + 1, show Reflections
            if current_aspect_idx == total_aspects:
                st.markdown('<div class="aspect-card">H. Skenario Situasional</div>', unsafe_allow_html=True)
                
                with st.form("form_scenarios"):
                    responses = {}
                    for i, q_text in enumerate(inst["scenarios"]):
                        essay_key = f"scenario_{i+1}"
                        existing_text = st.session_state.essay_answers.get(essay_key, "")
                        responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
                    
                    col_back, col_next = st.columns(2)
                    with col_back:
                        back_clicked = st.form_submit_button("⬅ Kembali")
                    with col_next:
                        next_clicked = st.form_submit_button("Lanjutkan ➡️")
                        
                    if back_clicked:
                        st.session_state.page = total_aspects - 1
                        st.rerun()
                        
                    if next_clicked:
                        st.session_state.essay_answers.update(responses)
                        st.session_state.page = total_aspects + 1
                        st.rerun()
            else:
                # Reflections
                st.markdown('<div class="aspect-card">I. Refleksi Diri</div>', unsafe_allow_html=True)
                
                with st.form("form_reflections"):
                    responses = {}
                    for i, q_text in enumerate(inst["reflections"]):
                        essay_key = f"reflection_{i+1}"
                        existing_text = st.session_state.essay_answers.get(essay_key, "")
                        responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
                    
                    col_back, col_next = st.columns(2)
                    with col_back:
                        back_clicked = st.form_submit_button("⬅ Kembali")
                    with col_next:
                        next_clicked = st.form_submit_button("Lanjutkan ke Ringkasan 🏁")
                        
                    if back_clicked:
                        st.session_state.page = total_aspects
                        st.rerun()
                        
                    if next_clicked:
                        st.session_state.essay_answers.update(responses)
                        st.session_state.page = "summary"
                        st.rerun()

# 4. SUMMARY PAGE
elif st.session_state.page == "summary":
    inst_type = st.session_state.instrument
    inst = MINAT_BELAJAR if inst_type == "minat" else SIKAP_SOSIAL
    
    st.markdown(f"""
        <div class="header-section">
            <h1 style="margin:0; color:white;">✅ RINGKASAN JAWABAN</h1>
            <p style="margin-top:8px; font-size:1rem; opacity:0.95;">Silakan tinjau kembali data Anda sebelum mengirimkan hasil.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👤 Biodata Responden")
    for field in inst["biodata_fields"]:
        val = st.session_state.biodata.get(field["id"], "")
        st.markdown(f"**{field['label']}:** {val}")
        
    st.markdown("---")
    
    # Calculate Score Info
    total_q = 20 if inst_type == "minat" else 28
    scores = [st.session_state.answers[f"q_{i}"]["score"] for i in range(1, total_q + 1) if f"q_{i}" in st.session_state.answers]
    sum_score = sum(scores)
    max_score = total_q * 5
    mean_score = sum_score / total_q if total_q > 0 else 0
    
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric("Total Skor", f"{sum_score} / {max_score}")
    with col_metric2:
        st.metric("Rata-rata Skor", f"{mean_score:.2f} / 5.00")
        
    st.markdown("---")
    
    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("⬅ Edit Jawaban"):
            # Go back to the qualitative page
            if inst_type == "minat":
                st.session_state.page = len(inst["likert_aspects"])
            else:
                st.session_state.page = len(inst["likert_aspects"]) + 1
            st.rerun()
            
    with col_submit:
        if st.button("🚀 Kirim Hasil Sekarang"):
            payload = build_unified_payload(
                inst_type,
                st.session_state.biodata,
                st.session_state.answers,
                st.session_state.essay_answers
            )
            
            with st.spinner("Sedang mengirimkan data ke Google Sheet..."):
                if submit_payload(payload):
                    st.session_state.page = "finish"
                    st.rerun()
                else:
                    st.error("Gagal mengirimkan data otomatis. Silakan coba klik tombol kirim kembali.")
                    st.info("Sebagai cadangan, Anda dapat menyalin data respons Anda di bawah ini:")
                    st.code(json.dumps(payload, indent=2, ensure_ascii=False))

# 5. FINISH SUCCESS PAGE
elif st.session_state.page == "finish":
    st.balloons()
    st.markdown(f"""
        <div class="success-card">
            <h1 style="font-size: 5rem; margin:0;">🎉</h1>
            <h1 style="color:#064e3b; margin-top:10px;">TERIMA KASIH!</h1>
            <p style="font-size: 1.2rem; color: #166534; font-weight:600; margin-bottom:10px;">
                Jawaban Anda berhasil dikirim dan disimpan.
            </p>
            <p style="color:#4b5563;">
                Partisipasi Anda sangat berharga bagi peningkatan kualitas pembelajaran Pendidikan Profesi Guru (PPG).
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Isi Angket Lain / Mulai Baru"):
        reset_state()
        st.rerun()
