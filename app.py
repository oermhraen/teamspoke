import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

PASSWORD = "981502"

st.set_page_config(
    page_title="Sesli Oda",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 Arkadaş Odası")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    username = st.text_input("Kullanıcı Adı")

    password = st.text_input(
        "Şifre",
        type="password"
    )

    if st.button("Odaya Katıl"):

        if password == PASSWORD and username.strip():
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()

        else:
            st.error("Kullanıcı adı veya şifre hatalı.")

    st.stop()

st.success(
    f"Hoş geldin {st.session_state.username}"
)

st.subheader("Ses Kontrolü")

mic_enabled = st.toggle(
    "Mikrofon Açık",
    value=True
)

if mic_enabled:

    webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={
            "video": False,
            "audio": True
        },
        async_processing=True
    )

else:
    st.info("Mikrofon kapalı.")

st.divider()

st.subheader("Oda Bilgisi")

st.info(
    """
    Oda Adı: Genel Oda

    Şifre: 981502

    Bu sürüm yalnızca temel yapıdır.
    Gerçek çok kullanıcılı ses paylaşımı için
    ek WebRTC sinyalizasyon sistemi gerekir.
    """
)
