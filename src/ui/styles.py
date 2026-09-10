import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    :root {
        --navy: #07133F;
        --turquoise: #20E0D0;
        --aqua: #DFFFFB;
        --bg: #F6FBFC;
        --border: #E3EEF0;
        --muted: #718096;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 70% 0%, rgba(32,224,208,.12), transparent 28%),
            var(--bg);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
    }

    .brand-logo {
        width: 54px;
        height: 54px;
        border-radius: 15px;
        background: linear-gradient(135deg, #20E0D0, #8AF5EA);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #07133F;
        font-weight: 900;
        font-size: 16px;
        line-height: 13px;
        box-shadow: 0 8px 24px rgba(32,224,208,.22);
    }

    .brand-name {
        color: var(--navy);
        font-size: 18px;
        font-weight: 800;
    }

    .page-title {
        color: var(--navy);
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 16px;
        margin-bottom: 28px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.94);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 5px 22px rgba(7,19,63,.035);
    }

    [data-testid="stDataFrame"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
    }

    [data-testid="stExpander"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 13px;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: white;
        color: var(--navy);
        text-align: left;
        transition: .15s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: var(--turquoise);
        background: var(--aqua);
        color: var(--navy);
    }

    [data-testid="stSidebar"] .stButton:first-of-type > button {
        background: var(--navy);
        color: white;
        border-color: var(--navy);
        font-weight: 600;
    }

    [data-testid="stChatInput"] {
        border: 1px solid var(--turquoise);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 6px 24px rgba(7,19,63,.08);
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)