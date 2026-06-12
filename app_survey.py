import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime
from questions_data import (
    MINAT_BELAJAR,
    SIKAP_SOSIAL,
    BERPIKIR_KRITIS,
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
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "biodata"  # biodata, minat_aspect_X, minat_open, minat_summary, minat_success, sikap_aspect_X, sikap_scenario, sikap_reflection, sikap_summary, sikap_success, kritis_page_X, kritis_summary, finish
if "biodata" not in st.session_state:
    st.session_state.biodata = {}
if "minat_answers" not in st.session_state:
    st.session_state.minat_answers = {}
if "minat_essays" not in st.session_state:
    st.session_state.minat_essays = {}
if "sikap_answers" not in st.session_state:
    st.session_state.sikap_answers = {}
if "sikap_essays" not in st.session_state:
    st.session_state.sikap_essays = {}
if "kritis_answers" not in st.session_state:
    st.session_state.kritis_answers = {}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def reset_state():
    st.session_state.page = "biodata"
    st.session_state.biodata = {}
    st.session_state.minat_answers = {}
    st.session_state.minat_essays = {}
    st.session_state.sikap_answers = {}
    st.session_state.sikap_essays = {}
    st.session_state.kritis_answers = {}

def get_apps_script_url():
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
                    return res_json.get("status") == "ok" or res_json.get("result") == "ok"
            except Exception:
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
    payload["Jenis_Instrumen"] = (
        "Minat Belajar Mahasiswa" if instrument_type == "minat" else 
        ("Sikap Sosial Mahasiswa" if instrument_type == "sikap" else "Berpikir Kritis Mahasiswa")
    )
    
    # Biodata
    payload["Nama"] = biodata.get("nama", "")
    payload["Lembaga_PPG"] = biodata.get("lembaga_ppg", "")
    payload["Program_Studi"] = biodata.get("program_studi", "")
    payload["Semester"] = biodata.get("semester", "")
    payload["Usia"] = biodata.get("usia", "")
    
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
        for i in range(21, 29):
            payload[f"Q{i}_Skor"] = ""
            payload[f"Q{i}_Teks"] = ""
    elif instrument_type == "sikap":
        for i in range(1, 29):
            ans = answers.get(f"q_{i}", None)
            if ans is not None:
                payload[f"Q{i}_Skor"] = ans["score"]
                payload[f"Q{i}_Teks"] = ans["text"]
                total_score += ans["score"]
            else:
                payload[f"Q{i}_Skor"] = ""
                payload[f"Q{i}_Teks"] = ""
    else:  # Berpikir Kritis
        for i in range(1, 29):
            payload[f"Q{i}_Skor"] = ""
            payload[f"Q{i}_Teks"] = ""
            
    payload["Skor_Total"] = total_score
    
    # Open questions / scenarios (1 to 6)
    if instrument_type == "minat":
        for i in range(1, 4):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"essay_{i}", "")
        for i in range(4, 7):
            payload[f"Respon_Terbuka_{i}"] = "N/A"
    elif instrument_type == "sikap":
        for i in range(1, 4):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"scenario_{i}", "")
        for i in range(4, 7):
            payload[f"Respon_Terbuka_{i}"] = essay_answers.get(f"reflection_{i-3}", "")
    else:  # Berpikir Kritis
        for i in range(1, 7):
            payload[f"Respon_Terbuka_{i}"] = "N/A"
            
    # Berpikir Kritis Essay Questions (1 to 10)
    if instrument_type == "kritis":
        for i in range(1, 11):
            payload[f"Kritis_Essay_{i}"] = essay_answers.get(f"kritis_{i}", "")
    else:
        for i in range(1, 11):
            payload[f"Kritis_Essay_{i}"] = "N/A"
            
    return payload

# ==========================================
# PAGE ROUTER
# ==========================================

# 1. BIODATA PAGE
if st.session_state.page == "biodata":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.8rem; font-weight:800;">ANGKET RESPON & EVALUASI MAHASISWA PPG</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">PENDIDIKAN PROFESI GURU (PPG)</p>
            <div style="background-color:rgba(255,255,255,0.2); height:1px; margin: 15px 0;"></div>
            <h3 style="margin:0; color:white; font-size:1.2rem; font-weight:700;">📋 Data Responden</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("Silakan lengkapi identitas responden Anda. Data ini akan otomatis digunakan untuk seluruh instrumen.")
    
    with st.form("form_biodata_combined"):
        nama = st.text_input("Nama", value=st.session_state.biodata.get("nama", ""))
        lembaga_ppg = st.text_input("Lembaga PPG", value=st.session_state.biodata.get("lembaga_ppg", ""))
        program_studi = st.text_input("Program Studi", value=st.session_state.biodata.get("program_studi", ""))
        
        sem_list = ["1", "2", "3", "4", "5", "6", "7", "8", ">8"]
        existing_sem = st.session_state.biodata.get("semester", "1")
        semester = st.selectbox("Semester", sem_list, index=sem_list.index(existing_sem) if existing_sem in sem_list else 0)
        
        usia = st.text_input("Usia (Tahun)", value=st.session_state.biodata.get("usia", ""))
        
        submit_bio = st.form_submit_button("Mulai Angket ➡️")
        
        if submit_bio:
            if nama.strip() and lembaga_ppg.strip() and program_studi.strip() and usia.strip():
                st.session_state.biodata = {
                    "nama": nama,
                    "lembaga_ppg": lembaga_ppg,
                    "program_studi": program_studi,
                    "semester": semester,
                    "usia": usia
                }
                st.session_state.page = "minat_aspect_0"
                st.rerun()
            else:
                st.warning("Mohon lengkapi semua field biodata.")

# --- SECTION 1: MINAT BELAJAR ---

# Minat Belajar Aspects
elif st.session_state.page.startswith("minat_aspect_"):
    aspect_idx = int(st.session_state.page.split("_")[-1])
    aspects = list(MINAT_BELAJAR["likert_aspects"].keys())
    aspect_name = aspects[aspect_idx]
    questions_list = MINAT_BELAJAR["likert_aspects"][aspect_name]
    
    q_offset = 0
    for i in range(aspect_idx):
        q_offset += len(MINAT_BELAJAR["likert_aspects"][aspects[i]])
        
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">📚 ANGKET MINAT BELAJAR MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {((aspect_idx + 1) / 6) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 1: Halaman {aspect_idx + 1} dari 6</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="aspect-card">{aspect_name}</div>', unsafe_allow_html=True)
    
    with st.form(f"form_minat_aspect_{aspect_idx}"):
        page_responses = {}
        for i, q_text in enumerate(questions_list):
            q_num = q_offset + i + 1
            q_key = f"q_{q_num}"
            
            existing = st.session_state.minat_answers.get(q_key, None)
            existing_idx = [5, 4, 3, 2, 1].index(existing["score"]) if existing else 0
            
            choice = st.radio(
                f"{q_num}. {q_text}",
                options=[5, 4, 3, 2, 1],
                format_func=lambda x: LIKERT_OPTIONS_MINAT[x],
                index=existing_idx,
                key=f"ui_minat_{q_key}",
                horizontal=True
            )
            page_responses[q_key] = choice
            
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ➡️")
            
        if back_clicked:
            if aspect_idx == 0:
                st.session_state.page = "biodata"
            else:
                st.session_state.page = f"minat_aspect_{aspect_idx - 1}"
            st.rerun()
            
        if next_clicked:
            for q_key, val in page_responses.items():
                st.session_state.minat_answers[q_key] = {
                    "score": val,
                    "text": LIKERT_OPTIONS_MINAT[val]
                }
            st.session_state.page = f"minat_aspect_{aspect_idx + 1}" if aspect_idx < 3 else "minat_open"
            st.rerun()

# Minat Belajar Open Questions
elif st.session_state.page == "minat_open":
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">📚 ANGKET MINAT BELAJAR MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {(5 / 6) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 1: Halaman 5 dari 6</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="aspect-card">Pertanyaan Terbuka</div>', unsafe_allow_html=True)
    
    with st.form("form_minat_open"):
        responses = {}
        for i, q_text in enumerate(MINAT_BELAJAR["open_questions"]):
            essay_key = f"essay_{i+1}"
            existing_text = st.session_state.minat_essays.get(essay_key, "")
            responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
            
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ke Ringkasan 🏁")
            
        if back_clicked:
            st.session_state.page = "minat_aspect_3"
            st.rerun()
            
        if next_clicked:
            st.session_state.minat_essays.update(responses)
            st.session_state.page = "minat_summary"
            st.rerun()

# Minat Belajar Summary
elif st.session_state.page == "minat_summary":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.6rem; font-weight:800;">✅ RINGKASAN ANGKET MINAT</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">Silakan tinjau jawaban Minat Belajar Anda.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👤 Identitas Responden")
    st.write(f"**Nama:** {st.session_state.biodata.get('nama', '')}")
    st.write(f"**Lembaga PPG:** {st.session_state.biodata.get('lembaga_ppg', '')}")
    st.write(f"**Program Studi:** {st.session_state.biodata.get('program_studi', '')}")
    st.write(f"**Semester:** {st.session_state.biodata.get('semester', '')}")
    
    st.markdown("---")
    
    # Calculate Score
    scores = [st.session_state.minat_answers[f"q_{i}"]["score"] for i in range(1, 21) if f"q_{i}" in st.session_state.minat_answers]
    sum_score = sum(scores)
    max_score = 100
    mean_score = sum_score / 20 if len(scores) > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Skor Minat", f"{sum_score} / {max_score}")
    with col2:
        st.metric("Rata-rata Skor", f"{mean_score:.2f} / 5.00")
        
    st.markdown("---")
    
    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("⬅ Edit Jawaban Minat"):
            st.session_state.page = "minat_open"
            st.rerun()
            
    with col_submit:
        if st.button("🚀 Kirim Angket Minat Belajar"):
            payload = build_unified_payload(
                "minat",
                st.session_state.biodata,
                st.session_state.minat_answers,
                st.session_state.minat_essays
            )
            with st.spinner("Mengirim data..."):
                if submit_payload(payload):
                    st.session_state.page = "minat_success"
                    st.rerun()
                else:
                    st.error("Gagal mengirimkan data otomatis.")
                    st.info("Salinan cadangan respons Anda:")
                    st.code(json.dumps(payload, indent=2, ensure_ascii=False))

# Minat Belajar Success Screen
elif st.session_state.page == "minat_success":
    st.balloons()
    st.markdown("""
        <div class="success-card">
            <h1 style="font-size: 4.5rem; margin:0;">🎉</h1>
            <h2 style="color:#064e3b; margin-top:10px;">ANGKET MINAT BELAJAR BERHASIL DIKIRIM</h2>
            <p style="font-size: 1.1rem; color: #166534; font-weight:600; margin-bottom:15px;">
                Terima kasih! Angket pertama Anda telah berhasil disimpan di database peneliti.
            </p>
            <p style="color:#4b5563; margin-bottom: 25px;">
                Silakan klik tombol di bawah ini untuk langsung melanjutkan ke angket kedua (**Angket Sikap Sosial**).
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Mulai Angket Kedua: Sikap Sosial ➔"):
        st.session_state.page = "sikap_aspect_0"
        st.rerun()


# --- SECTION 2: SIKAP SOSIAL ---

# Sikap Sosial Aspects
elif st.session_state.page.startswith("sikap_aspect_"):
    aspect_idx = int(st.session_state.page.split("_")[-1])
    aspects = list(SIKAP_SOSIAL["likert_aspects"].keys())
    aspect_name = aspects[aspect_idx]
    questions_list = SIKAP_SOSIAL["likert_aspects"][aspect_name]
    
    q_offset = 0
    for i in range(aspect_idx):
        q_offset += len(SIKAP_SOSIAL["likert_aspects"][aspects[i]])
        
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">🤝 ANGKET SIKAP SOSIAL MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {((aspect_idx + 1) / 10) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 2: Halaman {aspect_idx + 1} dari 10</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="aspect-card">{aspect_name}</div>', unsafe_allow_html=True)
    
    with st.form(f"form_sikap_aspect_{aspect_idx}"):
        page_responses = {}
        for i, q_text in enumerate(questions_list):
            q_num = q_offset + i + 1
            q_key = f"q_{q_num}"
            
            existing = st.session_state.sikap_answers.get(q_key, None)
            existing_idx = [5, 4, 3, 2, 1].index(existing["score"]) if existing else 0
            
            choice = st.radio(
                f"{q_num}. {q_text}",
                options=[5, 4, 3, 2, 1],
                format_func=lambda x: LIKERT_OPTIONS_SIKAP[x],
                index=existing_idx,
                key=f"ui_sikap_{q_key}",
                horizontal=True
            )
            page_responses[q_key] = choice
            
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ➡️")
            
        if back_clicked:
            if aspect_idx == 0:
                st.session_state.page = "minat_success"
            else:
                st.session_state.page = f"sikap_aspect_{aspect_idx - 1}"
            st.rerun()
            
        if next_clicked:
            for q_key, val in page_responses.items():
                st.session_state.sikap_answers[q_key] = {
                    "score": val,
                    "text": LIKERT_OPTIONS_SIKAP[val]
                }
            st.session_state.page = f"sikap_aspect_{aspect_idx + 1}" if aspect_idx < 6 else "sikap_scenario"
            st.rerun()

# Sikap Sosial Scenarios
elif st.session_state.page == "sikap_scenario":
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">🤝 ANGKET SIKAP SOSIAL MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {(8 / 10) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 2: Halaman 8 dari 10</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="aspect-card">Skenario Situasional</div>', unsafe_allow_html=True)
    
    with st.form("form_sikap_scenarios"):
        responses = {}
        for i, q_text in enumerate(SIKAP_SOSIAL["scenarios"]):
            essay_key = f"scenario_{i+1}"
            existing_text = st.session_state.sikap_essays.get(essay_key, "")
            responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
            
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ➡️")
            
        if back_clicked:
            st.session_state.page = "sikap_aspect_6"
            st.rerun()
            
        if next_clicked:
            st.session_state.sikap_essays.update(responses)
            st.session_state.page = "sikap_reflection"
            st.rerun()

# Sikap Sosial Reflections
elif st.session_state.page == "sikap_reflection":
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">🤝 ANGKET SIKAP SOSIAL MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {(9 / 10) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 2: Halaman 9 dari 10</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="aspect-card">Refleksi Diri</div>', unsafe_allow_html=True)
    
    with st.form("form_sikap_reflections"):
        responses = {}
        for i, q_text in enumerate(SIKAP_SOSIAL["reflections"]):
            essay_key = f"reflection_{i+1}"
            existing_text = st.session_state.sikap_essays.get(essay_key, "")
            responses[essay_key] = st.text_area(q_text, value=existing_text, height=120)
            
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ke Ringkasan 🏁")
            
        if back_clicked:
            st.session_state.page = "sikap_scenario"
            st.rerun()
            
        if next_clicked:
            st.session_state.sikap_essays.update(responses)
            st.session_state.page = "sikap_summary"
            st.rerun()

# Sikap Sosial Summary
elif st.session_state.page == "sikap_summary":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.6rem; font-weight:800;">✅ RINGKASAN ANGKET SIKAP SOSIAL</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">Silakan tinjau jawaban Sikap Sosial Anda.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👤 Identitas Responden")
    st.write(f"**Nama:** {st.session_state.biodata.get('nama', '')}")
    st.write(f"**Lembaga PPG:** {st.session_state.biodata.get('lembaga_ppg', '')}")
    st.write(f"**Semester:** {st.session_state.biodata.get('semester', '')}")
    st.write(f"**Usia:** {st.session_state.biodata.get('usia', '')} Tahun")
    
    st.markdown("---")
    
    # Calculate Score
    scores = [st.session_state.sikap_answers[f"q_{i}"]["score"] for i in range(1, 29) if f"q_{i}" in st.session_state.sikap_answers]
    sum_score = sum(scores)
    max_score = 140
    mean_score = sum_score / 28 if len(scores) > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Skor Sikap Sosial", f"{sum_score} / {max_score}")
    with col2:
        st.metric("Rata-rata Skor", f"{mean_score:.2f} / 5.00")
        
    st.markdown("---")
    
    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("⬅ Edit Jawaban Sikap"):
            st.session_state.page = "sikap_reflection"
            st.rerun()
            
    with col_submit:
        if st.button("🚀 Kirim Angket Sikap Sosial"):
            payload = build_unified_payload(
                "sikap",
                st.session_state.biodata,
                st.session_state.sikap_answers,
                st.session_state.sikap_essays
            )
            with st.spinner("Mengirim data..."):
                if submit_payload(payload):
                    st.session_state.page = "sikap_success"
                    st.rerun()
                else:
                    st.error("Gagal mengirimkan data otomatis.")
                    st.info("Salinan cadangan respons Anda:")
                    st.code(json.dumps(payload, indent=2, ensure_ascii=False))

# Sikap Sosial Success Screen
elif st.session_state.page == "sikap_success":
    st.balloons()
    st.markdown("""
        <div class="success-card">
            <h1 style="font-size: 4.5rem; margin:0;">🎉</h1>
            <h2 style="color:#064e3b; margin-top:10px;">ANGKET SIKAP SOSIAL BERHASIL DIKIRIM</h2>
            <p style="font-size: 1.1rem; color: #166534; font-weight:600; margin-bottom:15px;">
                Terima kasih! Angket kedua Anda telah berhasil disimpan di database peneliti.
            </p>
            <p style="color:#4b5563; margin-bottom: 25px;">
                Silakan klik tombol di bawah ini untuk melanjutkan ke bagian terakhir (**Soal Berpikir Kritis**).
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Mulai Bagian Ketiga: Berpikir Kritis ➔"):
        st.session_state.page = "kritis_page_0"
        st.rerun()


# --- SECTION 3: BERPIKIR KRITIS ---

# Berpikir Kritis Pages (2 questions per page, 5 pages)
elif st.session_state.page.startswith("kritis_page_"):
    page_idx = int(st.session_state.page.split("_")[-1])
    questions = BERPIKIR_KRITIS["questions"]
    
    # Each page gets 2 questions
    q1_idx = page_idx * 2
    q2_idx = q1_idx + 1
    
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #064e3b;">✍️ SOAL BERPIKIR KRITIS MAHASISWA</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #10b981; height: 6px; border-radius: 3px; width: {((page_idx + 1) / 6) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Bagian 3: Halaman {page_idx + 1} dari 6</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="aspect-card">Analisis Deskriptif - Soal {q1_idx + 1} & {q2_idx + 1}</div>', unsafe_allow_html=True)
    
    with st.form(f"form_kritis_page_{page_idx}"):
        responses = {}
        
        # Question 1 on page
        existing_val1 = st.session_state.kritis_answers.get(f"kritis_{q1_idx + 1}", "")
        responses[f"kritis_{q1_idx + 1}"] = st.text_area(
            f"Soal {q1_idx + 1}: {questions[q1_idx]}",
            value=existing_val1,
            height=180,
            key=f"kritis_ta_{q1_idx}"
        )
        
        # Question 2 on page
        existing_val2 = st.session_state.kritis_answers.get(f"kritis_{q2_idx + 1}", "")
        responses[f"kritis_{q2_idx + 1}"] = st.text_area(
            f"Soal {q2_idx + 1}: {questions[q2_idx]}",
            value=existing_val2,
            height=180,
            key=f"kritis_ta_{q2_idx}"
        )
        
        col_back, col_next = st.columns(2)
        with col_back:
            back_clicked = st.form_submit_button("⬅ Kembali")
        with col_next:
            next_clicked = st.form_submit_button("Lanjutkan ➡️")
            
        if back_clicked:
            if page_idx == 0:
                st.session_state.page = "sikap_success"
            else:
                st.session_state.page = f"kritis_page_{page_idx - 1}"
            st.rerun()
            
        if next_clicked:
            st.session_state.kritis_answers.update(responses)
            if page_idx < 4:
                st.session_state.page = f"kritis_page_{page_idx + 1}"
            else:
                st.session_state.page = "kritis_summary"
            st.rerun()

# Berpikir Kritis Summary
elif st.session_state.page == "kritis_summary":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.6rem; font-weight:800;">✅ RINGKASAN JAWABAN BERPIKIR KRITIS</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">Silakan tinjau jawaban esai Anda sebelum mengirim.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👤 Identitas Responden")
    st.write(f"**Nama:** {st.session_state.biodata.get('nama', '')}")
    st.write(f"**Lembaga PPG:** {st.session_state.biodata.get('lembaga_ppg', '')}")
    st.write(f"**Program Studi:** {st.session_state.biodata.get('program_studi', '')}")
    st.write(f"**Semester:** {st.session_state.biodata.get('semester', '')}")
    st.write(f"**Usia:** {st.session_state.biodata.get('usia', '')} Tahun")
    
    st.markdown("---")
    st.subheader("📝 Tinjauan Jawaban Esai")
    
    for i in range(10):
        question_text = BERPIKIR_KRITIS["questions"][i]
        ans_text = st.session_state.kritis_answers.get(f"kritis_{i+1}", "")
        
        with st.expander(f"Soal {i+1}: {question_text[:70]}..."):
            st.write(f"**Pertanyaan:** {question_text}")
            st.info(ans_text if ans_text.strip() else "*(Belum diisi)*")
            
    st.markdown("---")
    
    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("⬅ Edit Jawaban Kritis"):
            st.session_state.page = "kritis_page_4"
            st.rerun()
            
    with col_submit:
        if st.button("🚀 Kirim Jawaban Berpikir Kritis"):
            # Check if any answer is empty
            any_empty = False
            for i in range(1, 11):
                if not st.session_state.kritis_answers.get(f"kritis_{i}", "").strip():
                    any_empty = True
                    break
                    
            if any_empty:
                st.warning("Ada jawaban esai yang masih kosong. Silakan periksa kembali.")
                
            payload = build_unified_payload(
                "kritis",
                st.session_state.biodata,
                None,
                st.session_state.kritis_answers
            )
            with st.spinner("Mengirim data..."):
                if submit_payload(payload):
                    st.session_state.page = "finish"
                    st.rerun()
                else:
                    st.error("Gagal mengirimkan data otomatis.")
                    st.info("Salinan cadangan respons Anda:")
                    st.code(json.dumps(payload, indent=2, ensure_ascii=False))

# Tri-Instrument Finish Page
elif st.session_state.page == "finish":
    st.balloons()
    st.markdown(f"""
        <div class="success-card">
            <h1 style="font-size: 5.5rem; margin:0;">🏆</h1>
            <h1 style="color:#064e3b; margin-top:10px;">SELESAI LENGKAP!</h1>
            <h3 style="color:#166534; font-weight:700;">Terima Kasih, {st.session_state.biodata.get('nama', '')}!</h3>
            <p style="font-size: 1.15rem; color: #166534; font-weight:600; margin-bottom:15px;">
                Ketiga instrumen evaluasi (Minat Belajar, Sikap Sosial, & Berpikir Kritis) telah berhasil disimpan secara lengkap di database.
            </p>
            <p style="color:#4b5563;">
                Partisipasi dan kontribusi Anda sangat berharga bagi kelancaran dan validitas analisis data penelitian ini.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Mulai Baru / Isi Data Responden Lain"):
        reset_state()
        st.rerun()
