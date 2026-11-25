import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Akıllı Kişisel Finans & Karar Destek Paneli | Haydar Efe Demirkan",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CHROME OTOMATİK ÇEVİRİ ENGELLEYİCİ (REACT DOM KORUMASI) ---
components.html(
    """
    <script>
        window.parent.document.documentElement.lang = 'tr';
        window.parent.document.documentElement.setAttribute('translate', 'no');
        window.parent.document.body.classList.add('notranslate');
    </script>
    """,
    height=0,
    width=0,
)

# --- LINEAR / VERCEL SAAS FINTECH CSS (MATTE CHARCOAL & SOFT INDIGO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0F1115;
        color: #F3F4F6;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #0F1115;
    }

    section[data-testid="stSidebar"] {
        background-color: #13161C;
        border-right: 1px solid #232732;
    }

    /* Üst Kurumsal Başlık Çubuğu */
    .top-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #161920;
        border: 1px solid #262A34;
        border-radius: 12px;
        padding: 16px 22px;
        margin-bottom: 18px;
    }
    .live-dot {
        height: 8px;
        width: 8px;
        background-color: #34D399;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
    }

    /* KPI Kartları */
    .kpi-card {
        background: #161920;
        border: 1px solid #262A34;
        border-radius: 12px;
        padding: 18px 20px;
        transition: border-color 0.2s ease, transform 0.2s ease;
        height: 100%;
    }
    .kpi-card:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }
    .kpi-title {
        color: #9CA3AF;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #F9FAFB;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }
    .kpi-sub-green { color: #34D399; font-size: 0.78rem; font-weight: 500; }
    .kpi-sub-red { color: #F87171; font-size: 0.78rem; font-weight: 500; }
    .kpi-sub-indigo { color: #818CF8; font-size: 0.78rem; font-weight: 500; }
    .kpi-sub-amber { color: #FBBF24; font-size: 0.78rem; font-weight: 500; }

    /* AI Yönetici Özeti Kutusu */
    .ai-insight-box {
        background: #161920;
        border: 1px solid #262A34;
        border-left: 3px solid #6366F1;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: #E5E7EB;
        font-size: 0.9rem;
    }

    /* XAI Güven Rozeti */
    .xai-badge {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.28);
        border-radius: 10px;
        padding: 10px 12px;
        margin-top: 8px;
        font-size: 0.82rem;
        color: #E5E7EB;
    }

    /* Anomali Kartı */
    .anomaly-card {
        background: rgba(248, 113, 113, 0.06);
        border: 1px solid rgba(248, 113, 113, 0.25);
        border-left: 3px solid #F87171;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }

    /* Sabit Gider Kartı */
    .recurring-card {
        background: #161920;
        border: 1px solid #262A34;
        border-left: 3px solid #818CF8;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }

    /* Simülasyon Sonuç Kutusu */
    .sim-result-box {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }

    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #161920;
        padding: 5px;
        border-radius: 10px;
        border: 1px solid #262A34;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        padding: 8px 16px;
        color: #9CA3AF;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #232732 !important;
        color: #F9FAFB !important;
    }

    .brand-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.12);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.28);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .stButton > button, .stDownloadButton > button {
        background: #6366F1 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #4F46E5 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }
</style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "last_xai_results" not in st.session_state:
    st.session_state.last_xai_results = []

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def build_executive_html_report(user_name: str, summary: dict) -> str:
    cat_rows = "".join([
        f"<tr><td style='padding:8px;border-bottom:1px solid #e2e8f0;'>{k}</td><td style='padding:8px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:bold;'>₺{v:,.2f}</td></tr>"
        for k, v in summary.get("category_breakdown", {}).items()
    ])
    insight_items = "".join([f"<li style='margin-bottom:8px;'>{i}</li>" for i in summary.get("insights", [])])
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Akıllı Kişisel Finans & Karar Destek Paneli - Yönetici Raporu</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; max-width: 800px; margin: 40px auto; padding: 20px; }}
            .header {{ border-bottom: 3px solid #6366f1; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; }}
            .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }}
            .box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; }}
            .label {{ font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: bold; }}
            .val {{ font-size: 22px; font-weight: bold; margin-top: 4px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background: #161920; color: white; padding: 10px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <h2 style="margin:0;color:#0f172a;">Akıllı Kişisel Finans & Karar Destek Paneli</h2>
                <p style="margin:4px 0 0 0;color:#6366f1;font-weight:600;font-size:13px;">Geliştirici: Haydar Efe Demirkan</p>
            </div>
            <div style="text-align:right;font-size:13px;color:#475569;">
                <b>Kullanıcı:</b> {user_name}<br>
                <b>Rapor Tarihi:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
            </div>
        </div>
        <div class="grid">
            <div class="box"><div class="label">Bu Ay Toplam Harcama</div><div class="val">₺{summary['total_this_month']:,.2f}</div></div>
            <div class="box"><div class="label">Ay Sonu AI Tahmini</div><div class="val">₺{summary['projected_end_of_month']:,.2f}</div></div>
            <div class="box"><div class="label">Finansal Sağlık Skoru</div><div class="val">{summary['health_score']} / 100</div></div>
        </div>
        <h3>🧠 Yapay Zeka Yönetici Özeti & Bulgular</h3>
        <ul>{insight_items}</ul>
        <h3>📊 Kategori Bazlı Harcama Dağılımı</h3>
        <table>
            <thead><tr><th>Kategori</th><th style="text-align:right;">Toplam Tutar</th></tr></thead>
            <tbody>{cat_rows}</tbody>
        </table>
    </body>
    </html>
    """

# ==========================================
# 1. SPLIT-SCREEN MODERN SAAS GİRİŞ & KAYIT EKRANI
# ==========================================
if not st.session_state.token:
    st.markdown("""
    <style>
        .hero-panel {
            background: #161920;
            border: 1px solid #262A34;
            border-radius: 16px;
            padding: 34px 32px;
        }
        .dev-signature {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #1E222B;
            border: 1px solid #2E3340;
            color: #E5E7EB;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.84rem;
            font-weight: 500;
            margin-bottom: 18px;
        }
        .feature-pill {
            background: #13161C;
            border: 1px solid #232732;
            border-left: 3px solid #6366F1;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 12px;
        }
        .feature-title {
            color: #F3F4F6;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 2px;
        }
        .feature-desc {
            color: #9CA3AF;
            font-size: 0.8rem;
        }
        .tech-tag {
            display: inline-block;
            background: #1E222B;
            color: #9CA3AF;
            border: 1px solid #2E3340;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-right: 6px;
            margin-top: 8px;
        }
        .auth-card-header {
            background: #161920;
            border: 1px solid #262A34;
            border-top: 3px solid #6366F1;
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    spacer_l, col_hero, col_gap, col_auth, spacer_r = st.columns([0.25, 1.4, 0.15, 1.15, 0.25])

    with col_hero:
        st.markdown("""
        <div class="hero-panel">
            <div class="brand-badge">💠 YÖNETİM BİLİŞİM SİSTEMLERİ • LİSANS PROJESİ</div>
            <h1 style="font-size: 2.1rem; font-weight: 800; margin: 4px 0 12px 0; line-height: 1.2; color: #F9FAFB; letter-spacing: -0.02em;">
                Akıllı Kişisel Finans & <span style="color: #818CF8;">Karar Destek Paneli</span>
            </h1>
            <div class="dev-signature">
                👨‍💻 Geliştirici: <b>Haydar Efe Demirkan</b>
            </div>
            <p style="color: #9CA3AF; font-size: 0.93rem; line-height: 1.6; margin-bottom: 22px;">
                Harcama verilerini Doğal Dil İşleme (NLP) ile anlamlandıran, istatistiksel sapmaları yakalayan ve geleceğe dönük bütçe projeksiyonları üreten yapay zeka tabanlı karar destek sistemi.
            </p>
            <div class="feature-pill">
                <div class="feature-title">🧠 Açıklanabilir Yapay Zeka (XAI) & NLP Ayrıştırıcı</div>
                <div class="feature-desc">Serbest metin veya toplu fiş girişlerini güven skoruyla otomatik kategorize eder.</div>
            </div>
            <div class="feature-pill" style="border-left-color: #34D399;">
                <div class="feature-title">🚨 Z-Score Anomali & Sabit Gider Dedektörü</div>
                <div class="feature-desc">Olağandışı harcama sapmalarını ve tekrarlayan abonelik yüklerini anında tespit eder.</div>
            </div>
            <div class="feature-pill" style="border-left-color: #FBBF24;">
                <div class="feature-title">🎛️ 'What-If' Tasarruf Simülatörü & 50/30/20 Dengesi</div>
                <div class="feature-desc">Ay sonu bütçe tahmini ve kategori bazlı tasarruf senaryoları oluşturur.</div>
            </div>
            <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid #232732;">
                <span class="tech-tag">⚡ Python & FastAPI</span>
                <span class="tech-tag">🤖 Scikit-Learn NLP</span>
                <span class="tech-tag">🔐 JWT Güvenlik</span>
                <span class="tech-tag">📊 Plotly Analitik</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_auth:
        st.markdown("""
        <div class="auth-card-header">
            <div style="font-size: 0.72rem; color: #818CF8; font-weight: 700; letter-spacing: 0.8px;">SİSTEM ERİŞİM PORTALI</div>
            <h3 style="margin: 4px 0 4px 0; color: #F9FAFB; font-weight: 700;">Karar Destek Paneline Giriş</h3>
            <p style="margin: 0; color: #9CA3AF; font-size: 0.82rem;">Devam etmek için kullanıcı bilgilerinizle oturum açın.</p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔐 Oturum Aç", "✨ Yeni Hesap"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Kullanıcı Adı", placeholder="Örn: efe")
                password = st.text_input("Şifre", type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("Sisteme Giriş Yap", use_container_width=True)

                if submit_login:
                    try:
                        res = requests.post(
                            f"{API_URL}/login",
                            data={"username": username, "password": password}
                        )
                        if res.status_code == 200:
                            st.session_state.token = res.json()["access_token"]
                            profile_res = requests.get(f"{API_URL}/users/me", headers=get_headers())
                            st.session_state.user_info = profile_res.json()
                            st.rerun()
                        else:
                            st.error("Kullanıcı adı veya şifre hatalı.")
                    except Exception:
                        st.error("Backend API sunucusuna bağlanılamadı! Lütfen FastAPI sunucusunu kontrol edin.")

            st.markdown("<div style='text-align:center; color:#6B7280; font-size:0.78rem; margin: 8px 0;'>— veya sunum için tek tıkla —</div>", unsafe_allow_html=True)
            if st.button("⚡ Demo Hesabıyla Hızlı Giriş (efe)", use_container_width=True):
                try:
                    res = requests.post(f"{API_URL}/login", data={"username": "efe", "password": "123"})
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        profile_res = requests.get(f"{API_URL}/users/me", headers=get_headers())
                        st.session_state.user_info = profile_res.json()
                        st.rerun()
                    else:
                        st.warning("Demo hesabı bulunamadı, lütfen manuel giriş yapın.")
                except Exception:
                    st.error("Backend sunucusu çalışmıyor!")

        with tab_register:
            with st.form("register_form"):
                new_fullname = st.text_input("Ad Soyad", placeholder="Örn: Haydar Efe Demirkan")
                new_username = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adı belirleyin")
                new_password = st.text_input("Şifre", type="password", placeholder="Şifre belirleyin")
                submit_reg = st.form_submit_button("Hesabı Oluştur", use_container_width=True)

                if submit_reg:
                    res = requests.post(
                        f"{API_URL}/register",
                        json={"username": new_username, "password": new_password, "full_name": new_fullname}
                    )
                    if res.status_code == 201:
                        st.success("Hesabınız oluşturuldu! 'Oturum Aç' sekmesinden giriş yapabilirsiniz.")
                    else:
                        st.error(res.json().get("detail", "Kayıt sırasında hata oluştu."))

# ==========================================
# 2. KARAR DESTEK PANELİ ANA EKRANI
# ==========================================
else:
    user = st.session_state.user_info or {}

    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 8px 0 18px 0; border-bottom: 1px solid #232732;">
            <div style="font-size:0.7rem; color:#818CF8; font-weight:700; letter-spacing:0.8px;">HAYDAR EFE DEMİRKAN</div>
            <h3 style="margin:4px 0 0 0; color:#F9FAFB; font-size:1.12rem; font-weight:700; line-height:1.35;">
                Akıllı Kişisel Finans & <span style="color:#818CF8;">Karar Destek Paneli</span>
            </h3>
            <p style="margin:8px 0 0 0; color:#9CA3AF; font-size:0.82rem;">Aktif Kullanıcı: <b style="color:#F3F4F6;">{user.get('full_name', 'Kullanıcı')}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚡ Akıllı NLP & Toplu Fiş Girişi")
        st.caption("Tekli veya virgülle toplu yazın; XAI güven skoruyla sınıflandırsın.")
        with st.form("smart_expense_form", clear_on_submit=True):
            raw_input = st.text_area(
                "Harcama Metni",
                placeholder="Örn: Starbucks kahve 145 TL\nveya toplu: Migros 450, Shell 850",
                height=80
            )
            add_btn = st.form_submit_button("Yapay Zeka ile Analiz Et & Kaydet", use_container_width=True)
            if add_btn and raw_input:
                res = requests.post(
                    f"{API_URL}/expenses/smart",
                    json={"raw_text": raw_input},
                    headers=get_headers()
                )
                if res.status_code == 200:
                    st.session_state.last_xai_results = res.json().get("items", [])
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Hata oluştu."))

        if st.session_state.last_xai_results:
            st.markdown("<div style='font-size:0.72rem; color:#9CA3AF; font-weight:700; margin-top:6px;'>🧠 SON XAI SINIFLANDIRMA RAPORU</div>", unsafe_allow_html=True)
            for item in st.session_state.last_xai_results:
                st.markdown(f"""
                <div class="xai-badge">
                    <b>{item['description']}</b> — ₺{item['amount']:,.0f}<br>
                    Kategori: <b style="color:#818CF8;">{item['category']}</b> • Güven: <b>%{item['confidence']}</b>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎯 Aylık Bütçe Limiti")
        current_budget = float(user.get("monthly_budget", 15000.0))
        new_budget = st.number_input("Hedef Limit (₺)", min_value=500.0, value=current_budget, step=500.0)
        if st.button("Bütçe Hedefini Uygula", use_container_width=True):
            res = requests.put(
                f"{API_URL}/users/budget",
                json={"monthly_budget": new_budget},
                headers=get_headers()
            )
            if res.status_code == 200:
                st.session_state.user_info["monthly_budget"] = new_budget
                st.success("Bütçe güncellendi!")
                st.rerun()

        st.markdown("---")
        st.markdown("### 🎛️ Sunum Kontrolleri")
        if st.button("🎲 Demo Verisi Ekle (+45 Kayıt)", use_container_width=True):
            res = requests.post(f"{API_URL}/demo/seed", headers=get_headers())
            if res.status_code == 200:
                st.success("Sunum verileri eklendi!")
                st.rerun()

        if st.button("🚪 Güvenli Çıkış", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_info = None
            st.session_state.last_xai_results = []
            st.rerun()

    # --- API VERİLERİNİ ÇEK ---
    summary_res = requests.get(f"{API_URL}/analytics/summary", headers=get_headers())
    expenses_res = requests.get(f"{API_URL}/expenses", headers=get_headers())

    if summary_res.status_code == 200 and expenses_res.status_code == 200:
        summary = summary_res.json()
        expenses_list = expenses_res.json()

        col_banner, col_report = st.columns([4, 1.2])
        with col_banner:
            st.markdown(f"""
            <div class="top-banner" style="margin-bottom:0;">
                <div>
                    <h2 style="margin:0; font-size:1.42rem; font-weight:700; color:#F9FAFB; letter-spacing:-0.01em;">Akıllı Kişisel Finans & Karar Destek Paneli</h2>
                    <span style="color:#9CA3AF; font-size:0.84rem;">
                        Geliştirici: <b style="color:#E5E7EB;">Haydar Efe Demirkan</b> • Dönem: {datetime.now().strftime('%B %Y')} (Ayın {summary['days_passed']}/{summary['days_in_month']}. Günü)
                    </span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.82rem; color:#F3F4F6; font-weight:600;">
                        <span class="live-dot"></span>XAI Engine & FastAPI Aktif
                    </div>
                    <div style="font-size:0.74rem; color:#6B7280;">Model: TF-IDF + Multinomial Naive Bayes</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_report:
            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
            html_report = build_executive_html_report(user.get("full_name", "Kullanıcı"), summary)
            st.download_button(
                label="📄 Yönetici Raporu Al",
                data=html_report.encode("utf-8"),
                file_name=f"Finans_Karar_Destek_Raporu_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # --- 5'Lİ YÖNETİCİ KPI KARTLARI ---
        change = summary["month_change_pct"]
        badge_class = "kpi-sub-red" if change > 0 else "kpi-sub-green"
        sign = "+" if change > 0 else ""

        proj = summary["projected_end_of_month"]
        budget = summary["monthly_budget"]
        proj_class = "kpi-sub-red" if proj > budget else "kpi-sub-indigo"
        proj_text = "Bütçe aşım riski" if proj > budget else "Lineer AI Tahmini"

        rem = summary["remaining_budget"]
        rem_class = "kpi-sub-green" if rem >= 0 else "kpi-sub-red"

        h_score = summary["health_score"]
        h_class = "kpi-sub-green" if h_score >= 80 else ("kpi-sub-amber" if h_score >= 60 else "kpi-sub-red")

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 18px;">
            <div class="kpi-card">
                <div class="kpi-title">BU AY HARCAMA</div>
                <div class="kpi-value">₺{summary['total_this_month']:,.0f}</div>
                <div class="{badge_class}">{sign}%{change} geçen aya göre</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">AY SONU TAHMİNİ</div>
                <div class="kpi-value">₺{proj:,.0f}</div>
                <div class="{proj_class}">🔮 {proj_text}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">KALAN BÜTÇE</div>
                <div class="kpi-value">₺{rem:,.0f}</div>
                <div class="{rem_class}">Kullanım: %{summary['budget_usage_pct']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">50/30/20 İHTİYAÇ ORANI</div>
                <div class="kpi-value">%{summary.get('needs_pct', 0)}<span style="font-size:0.95rem; color:#6B7280;"> / %{summary.get('wants_pct', 0)}</span></div>
                <div class="kpi-sub-indigo">⚖️ Zorunlu / İstek Dengesi</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">FİNANSAL SAĞLIK SKORU</div>
                <div class="kpi-value">{h_score}<span style="font-size:1rem; color:#6B7280;">/100</span></div>
                <div class="{h_class}">🛡️ {summary['health_label']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- 3 PROFESYONEL SEKME ---
        tab1, tab2, tab3 = st.tabs([
            "📊 Yönetici Özeti & Davranış Analitiği",
            "🔮 AI Simülasyonu, Anomali & Sabit Giderler",
            "🧾 İşlem Defteri & Yönetim"
        ])

        # ==========================================
        # SEKME 1: YÖNETİCİ ÖZETİ & ANALİTİK
        # ==========================================
        with tab1:
            st.markdown("### 🧠 AI Finansal Koç & Yönetici Özeti")
            for insight in summary["insights"]:
                st.markdown(f'<div class="ai-insight-box">{insight}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if expenses_list:
                col_g1, col_g2 = st.columns([1.1, 1.1])

                with col_g1:
                    st.markdown("#### 🎯 Kategori Bazlı Harcama Dağılımı")
                    cat_data = summary["category_breakdown"]
                    if cat_data:
                        fig_pie = px.pie(
                            names=list(cat_data.keys()),
                            values=list(cat_data.values()),
                            hole=0.62,
                            color_discrete_sequence=["#6366F1", "#38BDF8", "#34D399", "#FBBF24", "#A78BFA", "#F472B6", "#94A3B8"]
                        )
                        fig_pie.update_layout(
                            paper_bgcolor="#161920",
                            plot_bgcolor="#161920",
                            font=dict(color="#E5E7EB", family="Inter"),
                            margin=dict(t=20, b=20, l=10, r=10),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.25)
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)

                with col_g2:
                    st.markdown("#### 🧭 Bütçe Kullanım & Risk Göstergesi")
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=summary["total_this_month"],
                        number={"prefix": "₺", "font": {"size": 34, "color": "#F9FAFB"}},
                        delta={"reference": summary["monthly_budget"], "increasing": {"color": "#F87171"}, "decreasing": {"color": "#34D399"}},
                        gauge={
                            "axis": {"range": [0, max(summary["monthly_budget"] * 1.2, summary["projected_end_of_month"] * 1.1)], "tickcolor": "#9CA3AF"},
                            "bar": {"color": "#6366F1" if summary["total_this_month"] <= summary["monthly_budget"] else "#F87171"},
                            "bgcolor": "#232732",
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, summary["monthly_budget"] * 0.75], "color": "rgba(52, 211, 153, 0.14)"},
                                {"range": [summary["monthly_budget"] * 0.75, summary["monthly_budget"]], "color": "rgba(251, 191, 36, 0.16)"},
                                {"range": [summary["monthly_budget"], summary["monthly_budget"] * 1.25], "color": "rgba(248, 113, 113, 0.18)"}
                            ],
                            "threshold": {
                                "line": {"color": "#F87171", "width": 3},
                                "thickness": 0.8,
                                "value": summary["monthly_budget"]
                            }
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor="#161920",
                        font=dict(color="#E5E7EB", family="Inter"),
                        margin=dict(t=30, b=10, l=20, r=20),
                        height=330
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

                col_b1, col_b2 = st.columns(2)

                with col_b1:
                    st.markdown("#### 📊 Dönemsel Kıyaslama: Geçen Ay vs. Bu Ay")
                    curr_cats = summary.get("category_breakdown", {})
                    prev_cats = summary.get("prev_category_breakdown", {})
                    all_cats = sorted(list(set(list(curr_cats.keys()) + list(prev_cats.keys()))))

                    if all_cats:
                        fig_bar = go.Figure(data=[
                            go.Bar(name="Geçen Ay", x=all_cats, y=[prev_cats.get(c, 0) for c in all_cats], marker_color="#374151"),
                            go.Bar(name="Bu Ay", x=all_cats, y=[curr_cats.get(c, 0) for c in all_cats], marker_color="#6366F1")
                        ])
                        fig_bar.update_layout(
                            barmode="group",
                            paper_bgcolor="#161920",
                            plot_bgcolor="#161920",
                            font=dict(color="#E5E7EB", family="Inter"),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor="#232732", title="Tutar (₺)"),
                            margin=dict(t=20, b=20, l=10, r=10),
                            height=290,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

                with col_b2:
                    st.markdown("#### 📅 Haftalık Harcama Yoğunluğu (Gün Bazlı)")
                    w_data = summary.get("weekday_breakdown", {})
                    if w_data:
                        days_list = list(w_data.keys())
                        vals_list = list(w_data.values())
                        colors = ["#818CF8" if d == summary.get("peak_day") else "#2A2F3D" for d in days_list]
                        fig_week = go.Figure(data=[
                            go.Bar(x=days_list, y=vals_list, marker_color=colors)
                        ])
                        fig_week.update_layout(
                            paper_bgcolor="#161920",
                            plot_bgcolor="#161920",
                            font=dict(color="#E5E7EB", family="Inter"),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor="#232732", title="Toplam (₺)"),
                            margin=dict(t=20, b=20, l=10, r=10),
                            height=290
                        )
                        st.plotly_chart(fig_week, use_container_width=True)

        # ==========================================
        # SEKME 2: WHAT-IF SİMÜLATÖRÜ, ANOMALİ & SABİT GİDERLER
        # ==========================================
        with tab2:
            col_sim, col_anom = st.columns([1.15, 1])

            with col_sim:
                st.markdown("### 🎛️ 'What-If' AI Tasarruf Simülatörü")
                st.caption("Belirli bir kategoride harcamalarınızı kıstığınızda ay sonu tahmininizin nasıl değişeceğini canlı simüle edin.")

                cat_breakdown = summary["category_breakdown"]
                if cat_breakdown:
                    target_cat = st.selectbox("Optimize Edilecek Kategori", list(cat_breakdown.keys()))
                    cut_pct = st.slider(f"'{target_cat}' Harcamalarında Kesinti Oranı (%)", min_value=5, max_value=70, value=25, step=5)

                    cat_current = cat_breakdown[target_cat]
                    saved_so_far = round(cat_current * (cut_pct / 100), 2)
                    projected_saving = round((saved_so_far / summary["days_passed"]) * summary["days_in_month"], 2)
                    new_projected_total = round(summary["projected_end_of_month"] - projected_saving, 2)

                    st.markdown(f"""
                    <div class="sim-result-box">
                        <div style="font-size:0.8rem; color:#A5B4FC; font-weight:700; margin-bottom:6px;">SİMÜLASYON SONUCU</div>
                        <div style="font-size:1.35rem; font-weight:700; color:#34D399; margin-bottom:8px;">
                            💰 Ay Sonu Ekstra Tasarruf: +₺{projected_saving:,.2f}
                        </div>
                        <div style="font-size:0.92rem; color:#E5E7EB;">
                            • Mevcut Ay Sonu Tahmini: <b>₺{summary['projected_end_of_month']:,.2f}</b><br>
                            • Simülasyon Sonrası Yeni Tahmin: <b style="color:#34D399;">₺{new_projected_total:,.2f}</b><br>
                            • Yıllık Projeksiyonda Net Kazanç: <b style="color:#818CF8;">₺{projected_saving * 12:,.2f}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Simülasyon için önce harcama kaydı ekleyin.")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔄 Sabit Gider & Abonelik Dedektörü")
                rec_items = summary.get("recurring_items", [])
                if rec_items:
                    for r in rec_items:
                        st.markdown(f"""
                        <div class="recurring-card">
                            <div style="display:flex; justify-content:space-between; font-weight:600; color:#C7D2FE;">
                                <span>📌 {r['description']} ({r['category']})</span>
                                <span>₺{r['amount']:,.2f} / ay</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Bu ay tespit edilen sabit fatura veya abonelik kaydı yok.")

            with col_anom:
                st.markdown("### 🚨 AI Anomali & Sapma Dedektörü")
                st.caption("Standart sapma (Z-Score) analizi ile normal harcama alışkanlığınızın dışına çıkan işlemler.")

                anomalies = summary.get("anomalies", [])
                if anomalies:
                    for item in anomalies:
                        st.markdown(f"""
                        <div class="anomaly-card">
                            <div style="display:flex; justify-content:space-between; font-weight:600; color:#FCA5A5;">
                                <span>⚠️ {item['description']} ({item['category']})</span>
                                <span>₺{item['amount']:,.2f}</span>
                            </div>
                            <div style="font-size:0.82rem; color:#D1D5DB; margin-top:4px;">
                                Tarih: {item['date']} • Ortalama işlem tutarınızın <b>{item['ratio']} katı</b> büyüklüğünde olağandışı harcama.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ Bu ay istatistiksel sapma sınırını aşan olağandışı bir harcama tespit edilmedi.")

        # ==========================================
        # SEKME 3: İŞLEM DEFTERİ & YÖNETİM
        # ==========================================
        with tab3:
            st.markdown("### 🧾 Kurumsal İşlem Defteri & Veri Yönetimi")
            if expenses_list:
                df_manage = pd.DataFrame(expenses_list)
                df_manage["created_at"] = pd.to_datetime(df_manage["created_at"])

                col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 1.2])
                with col_f1:
                    categories = ["Tümü"] + sorted(df_manage["category"].unique().tolist())
                    selected_cat = st.selectbox("Kategori Filtresi", categories)
                with col_f2:
                    search_query = st.text_input("Açıklama Ara", placeholder="Örn: Migros, Kahve...")
                with col_f3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    csv_data = df_manage[["id", "created_at", "description", "category", "amount"]].to_csv(index=False).encode("utf-8-sig")
                    st.download_button(
                        label="📥 Excel / CSV İndir",
                        data=csv_data,
                        file_name=f"Finans_Ekstre_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                filtered = df_manage.copy()
                if selected_cat != "Tümü":
                    filtered = filtered[filtered["category"] == selected_cat]
                if search_query:
                    filtered = filtered[filtered["description"].str.contains(search_query, case=False, na=False)]

                display_df = filtered[["id", "created_at", "description", "category", "amount", "is_ai_categorized"]].copy()
                display_df["created_at"] = display_df["created_at"].dt.strftime("%d.%m.%Y %H:%M")
                display_df["is_ai_categorized"] = display_df["is_ai_categorized"].apply(lambda x: "🤖 AI NLP" if x else "✍️ Manuel")
                display_df.columns = ["ID", "Tarih", "Açıklama", "Kategori", "Tutar (₺)", "Kaynak"]

                st.dataframe(display_df, use_container_width=True, hide_index=True)

                st.markdown("#### 🗑️ Hatalı İşlem Kaydını Sil")
                col_del1, col_del2 = st.columns([1, 3])
                with col_del1:
                    del_id = st.number_input("Silinecek İşlem ID", min_value=1, step=1)
                with col_del2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Seçili Kaydı Kalıcı Olarak Sil"):
                        del_res = requests.delete(f"{API_URL}/expenses/{int(del_id)}", headers=get_headers())
                        if del_res.status_code == 200:
                            st.success(f"#{int(del_id)} numaralı işlem silindi!")
                            st.rerun()
                        else:
                            st.error("Belirtilen ID'ye ait kayıt bulunamadı.")
            else:
                st.info("Henüz kayıtlı harcama bulunmuyor.")