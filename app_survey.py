import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime
from questions_data import (
    BERPIKIR_KRITIS
)

# ==========================================
# CONFIG & STYLES
# ==========================================
st.set_page_config(
    page_title="Instrumen Berpikir Kritis",
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
        background: linear-gradient(135deg, #e0f2fe 0%, #ffffff 100%);
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    h1, h2, h3 { 
        color: #1e3a8a; 
        font-weight: 800; 
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        color: white !important;
        border-radius: 12px;
        padding: 14px;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.3);
    }

    .header-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 35px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.15);
    }

    .aspect-card {
        background: #eff6ff;
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin: 25px 0 15px 0;
        font-weight: bold;
        color: #1e3a8a;
        font-size: 1.1rem;
    }
    
    .success-card {
        background: #eff6ff;
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        border: 2px solid #bfdbfe;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "biodata"  # biodata, kritis_page_X, kritis_summary, finish
if "biodata" not in st.session_state:
    st.session_state.biodata = {}
if "kritis_answers" not in st.session_state:
    st.session_state.kritis_answers = {}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def reset_state():
    st.session_state.page = "biodata"
    st.session_state.biodata = {}
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

def build_unified_payload(biodata, essay_answers):
    # Builds the exact 80-column payload matching the previous Minat & Sikap schema
    # to prevent spreadsheet column shifts.
    payload = {}
    payload["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload["Jenis_Instrumen"] = "Berpikir Kritis Mahasiswa"
    
    # Biodata
    payload["Nama"] = biodata.get("nama", "")
    payload["Lembaga_PPG"] = biodata.get("lembaga_ppg", "")
    payload["Program_Studi"] = biodata.get("program_studi", "")
    payload["Semester"] = biodata.get("semester", "")
    payload["Usia"] = biodata.get("usia", "")
    
    payload["Skor_Total"] = 0
    
    # Likert items (1 to 28) - all blank
    for i in range(1, 29):
        payload[f"Q{i}_Skor"] = ""
        payload[f"Q{i}_Teks"] = ""
        
    # Open questions / qualitative responses (1 to 6) - all N/A
    for i in range(1, 7):
        payload[f"Respon_Terbuka_{i}"] = "N/A"
        
    # Berpikir Kritis Essay Questions (1 to 10) - filled
    for i in range(1, 11):
        payload[f"Kritis_Essay_{i}"] = essay_answers.get(f"kritis_{i}", "")
        
    return payload

# ==========================================
# PAGE ROUTER
# ==========================================

# 1. BIODATA PAGE
if st.session_state.page == "biodata":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.8rem; font-weight:800;">SOAL BERPIKIR KRITIS</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">PENDIDIKAN PROFESI GURU (PPG)</p>
            <div style="background-color:rgba(255,255,255,0.2); height:1px; margin: 15px 0;"></div>
            <h3 style="margin:0; color:white; font-size:1.2rem; font-weight:700;">📋 Data Responden</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("Silakan lengkapi identitas responden Anda sebelum memulai pengerjaan soal.")
    
    with st.form("form_biodata_kritis"):
        nama = st.text_input("Nama", value=st.session_state.biodata.get("nama", ""))
        lembaga_ppg = st.text_input("Lembaga PPG", value=st.session_state.biodata.get("lembaga_ppg", ""))
        program_studi = st.text_input("Program Studi", value=st.session_state.biodata.get("program_studi", ""))
        
        sem_list = ["1", "2", "3", "4", "5", "6", "7", "8", ">8"]
        existing_sem = st.session_state.biodata.get("semester", "1")
        semester = st.selectbox("Semester", sem_list, index=sem_list.index(existing_sem) if existing_sem in sem_list else 0)
        
        usia = st.text_input("Usia (Tahun)", value=st.session_state.biodata.get("usia", ""))
        
        submit_bio = st.form_submit_button("Mulai Jawab Soal ➡️")
        
        if submit_bio:
            if nama.strip() and lembaga_ppg.strip() and program_studi.strip() and usia.strip():
                st.session_state.biodata = {
                    "nama": nama,
                    "lembaga_ppg": lembaga_ppg,
                    "program_studi": program_studi,
                    "semester": semester,
                    "usia": usia
                }
                st.session_state.page = "kritis_page_0"
                st.rerun()
            else:
                st.warning("Mohon lengkapi semua field biodata.")

# 2. QUESTIONS PAGES (2 questions per page, 5 pages)
elif st.session_state.page.startswith("kritis_page_"):
    page_idx = int(st.session_state.page.split("_")[-1])
    questions = BERPIKIR_KRITIS["questions"]
    
    # Each page gets 2 questions
    q1_idx = page_idx * 2
    q2_idx = q1_idx + 1
    
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1e3a8a;">✍️ SOAL BERPIKIR KRITIS</h3>
            <div style="background-color: #e2e8f0; height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background-color: #3b82f6; height: 6px; border-radius: 3px; width: {((page_idx + 1) / 5) * 100}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#6b7280; text-align:right; margin-top:4px;">Halaman {page_idx + 1} dari 5</p>
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
                st.session_state.page = "biodata"
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

# 3. REVIEW SUMMARY PAGE
elif st.session_state.page == "kritis_summary":
    st.markdown("""
        <div class="header-section">
            <h1 style="margin:0; color:white; font-size:1.6rem; font-weight:800;">✅ RINGKASAN JAWABAN</h1>
            <p style="margin-top:8px; font-size:1.1rem; opacity:0.95; font-weight:600;">Silakan tinjau kembali seluruh jawaban esai Anda sebelum mengirim.</p>
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
    
    questions = BERPIKIR_KRITIS["questions"]
    for i in range(10):
        question_text = questions[i]
        ans_text = st.session_state.kritis_answers.get(f"kritis_{i+1}", "")
        
        with st.expander(f"Soal {i+1}: {question_text[:70]}..."):
            st.write(f"**Pertanyaan:** {question_text}")
            st.info(ans_text if ans_text.strip() else "*(Belum diisi)*")
            
    st.markdown("---")
    
    col_back, col_submit = st.columns(2)
    with col_back:
        if st.button("⬅ Edit Jawaban"):
            st.session_state.page = "kritis_page_4"
            st.rerun()
            
    with col_submit:
        if st.button("🚀 Kirim Jawaban Sekarang"):
            any_empty = False
            for i in range(1, 11):
                if not st.session_state.kritis_answers.get(f"kritis_{i}", "").strip():
                    any_empty = True
                    break
                    
            if any_empty:
                st.warning("Ada jawaban esai yang masih kosong. Silakan periksa kembali.")
                
            payload = build_unified_payload(
                st.session_state.biodata,
                st.session_state.kritis_answers
            )
            with st.spinner("Mengirim data ke Google Sheet..."):
                if submit_payload(payload):
                    st.session_state.page = "finish"
                    st.rerun()
                else:
                    st.error("Gagal mengirimkan data otomatis.")
                    st.info("Salinan cadangan respons Anda:")
                    st.code(json.dumps(payload, indent=2, ensure_ascii=False))

# 4. FINISH PAGE
elif st.session_state.page == "finish":
    st.balloons()
    st.markdown(f"""
        <div class="success-card">
            <h1 style="font-size: 5.5rem; margin:0;">🏆</h1>
            <h1 style="color:#1e3a8a; margin-top:10px;">SELESAI!</h1>
            <h3 style="color:#1e40af; font-weight:700;">Terima Kasih, {st.session_state.biodata.get('nama', '')}!</h3>
            <p style="font-size: 1.15rem; color: #1e40af; font-weight:600; margin-bottom:10px;">
                Jawaban Soal Berpikir Kritis Anda telah berhasil disimpan di database.
            </p>
            <p style="color:#4b5563;">
                Partisipasi Anda sangat berharga bagi kelancaran dan validitas analisis data penelitian ini.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Mulai Baru / Isi Data Responden Lain"):
        reset_state()
        st.rerun()
