import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Sayfa Ayarları
st.set_page_config(page_title="Özel Ses Odası", page_icon="🎙️", layout="centered")

# Sabit Oda Şifresi
ODA_SIFRESI = "981502"

st.title("🎙️ Bizim Özel Ses Odası")
st.write("Şifreli giriş yapabileceğiniz basit ses arayüzü.")

# Sol Menü - Giriş Paneli
st.sidebar.header("🔑 Giriş Bilgileri")
kullanici_adi = st.sidebar.text_input("Kullanıcı Adınız:", placeholder="Örn: Emre")
girilen_sifre = st.sidebar.text_input("Oda Şifresi:", type="password", placeholder="******")

# Kontroller ve Mantık
if not kullanici_adi:
    st.warning("⚡ Lütfen odaya girmek için sol menüden bir **Kullanıcı Adı** belirleyin.")
elif girilen_sifre != ODA_SIFRESI:
    if girilen_sifre:
        st.error("❌ Hatalı şifre! Lütfen doğru şifreyi girin.")
    else:
        st.info("🔒 Bu oda şifrelidir. Lütfen sol menüden şifreyi girin.")
else:
    st.sidebar.success(f"🔓 Hoş geldin, {kullanici_adi}!")
    
    st.info("Aşağıdaki 'START' butonuna basarak mikrofonunuza izin verin. Sesi kapatıp açmak için çalışan oynatıcının üstündeki mikrofon ikonuna tıklayabilirsiniz.")

    # Ücretsiz Google STUN sunucusu
    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    # Düzeltilen doğru fonksiyon: webrtc_streamer
    webrtc_streamer(
        key="ses-odasi",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": False, "audio": True},
    )
    
    st.markdown("---")
    st.caption(f"Şu an odadasınız. Aktif Kullanıcı: {kullanici_adi}")
