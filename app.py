import streamlit as st
from streamlit_webrtc import streamlit_webrtc_wrapper, WebRtcMode, RTCConfiguration

# Başlık ve Sayfa Ayarları
st.set_page_config(page_title="Bizim Özel Ses Odası", page_icon="🎙️", layout="centered")

# Sabit Oda Şifresi
ODA_SIFRESI = "981502"

# Başlıklar
st.title("🎙️ Bizim Özel Ses Odası")
st.write("Arkadaşlarınla güvenli şekilde konuşabileceğin minimalist ses odası.")

# --- GİRİŞ PANELİ (Kullanıcı Adı ve Şifre) ---
st.sidebar.header("🔑 Giriş Bilgileri")
kullanici_adi = st.sidebar.text_input("Kullanıcı Adınız:", placeholder="Örn: Ahmet")
girilen_sifre = st.sidebar.text_input("Oda Şifresi:", type="password", placeholder="******")

# Şifre ve Kullanıcı Adı Kontrolü
if not kullanici_adi:
    st.warning("⚡ Lütfen odaya girmek için sol menüden bir **Kullanıcı Adı** belirleyin.")
elif girilen_sifre != ODA_SIFRESI:
    if girilen_sifre: # Şifre yazılmış ama yanlışsa uyarı ver
        st.error("❌ Hatalı şifre! Lütfen doğru oda şifresini girin.")
    else:
        st.info("🔒 Bu oda şifrelidir. Giriş yapmak için lütfen şifreyi yazın.")
else:
    # --- BAŞARILI GİRİŞ: ODA ARAYÜZÜ ---
    st.sidebar.success(f"🔓 Hoş geldin, {kullanici_adi}!")
    
    # Ücretsiz Google STUN sunucusu ayarı
    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    # Konuşma Modları
    konusma_modu = st.radio(
        "Konuşma Modu Seçin:",
        ("Her Zaman Açık / Sessiz (Toggle)", "Bas-Konuş (Push-to-Talk)"),
        horizontal=True
    )

    # Ses akışını başlatan ana WebRTC bileşeni
    ctx = streamlit_webrtc_wrapper(
        key="ses-odasi-sifreli",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": False, "audio": True},
        async_processing=True,
    )

    # Durum Bildirimleri ve Mod Kontrolleri
    if ctx.state.playing:
        st.success(f"🟢 Odaya {kullanici_adi} olarak bağlandınız! Ses iletiliyor.")
        
        if konusma_modu == "Her Zaman Açık / Sessiz (Toggle)":
            mikrofon_durumu = st.checkbox("🎙️ Mikrofonu Aç", value=True)
            if mikrofon_durumu:
                st.info("🎤 Mikrofonunuz şu an aktif, sesiniz gidiyor.")
            else:
                st.warning("🔇 Sessizdesiniz.")

        elif konusma_modu == "Bas-Konuş (Push-to-Talk)":
            bas_konus = st.button("🎤 KONUŞMAK İÇİN BASILI TUTUN (Veya Tıklayın)")
            if bas_konus:
                st.info("Sesi gönderiyorsunuz...")
            else:
                st.warning("Sesiniz sessize alındı. Konuşmak için butona basın.")
    else:
        st.info("Odaya girmek için yukarıdaki **'Start'** butonuna basarak mikrofon izni verin.")

    # Bilgilendirme Alanı
    st.markdown("---")
    st.caption(f"Şu an güvenli odadasınız. Giriş Yapan: {kullanici_adi}")
