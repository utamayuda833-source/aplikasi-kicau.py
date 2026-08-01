import streamlit as st
import json
import os
from datetime import datetime
import time

DATA_FILE = "kicau_data.json"

# Inisialisasi file data jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        # Data awal berupa list kosong
        json.dump([], f)

def load_tweets():
    """Memuat kicauan dari file JSON."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Jika file rusak atau tidak ditemukan, kembalikan list kosong
        return []

def save_tweet(author, content):
    """Menyimpan kicauan baru ke file JSON."""
    tweets = load_tweets()
    
    # Buat objek kicauan baru
    new_tweet = {
        "id": int(time.time()), # Gunakan timestamp sebagai ID unik
        "author": author,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Tambahkan ke awal list (agar muncul paling atas)
    tweets.insert(0, new_tweet)
    
    # Simpan kembali ke file
    with open(DATA_FILE, "w") as f:
        json.dump(tweets, f, indent=4)

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Kicau", 
    page_icon="🐦", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Kustomisasi CSS untuk tampilan yang lebih mirip aplikasi mobile/Twitter
st.markdown("""
    <style>
        /* Mengubah font dasar */
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Container utama kicauan */
        .tweet-container {
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: background-color 0.2s ease;
        }
        
        /* Efek hover pada kicauan */
        .tweet-container:hover {
            background-color: #f5f8fa;
        }
        
        /* Nama pembuat kicauan */
        .tweet-author {
            font-weight: bold;
            color: #14171a;
            font-size: 1.1em;
            margin-bottom: 2px;
        }
        
        /* Waktu kicauan */
        .tweet-time {
            color: #657786;
            font-size: 0.8em;
            margin-bottom: 10px;
        }
        
        /* Isi kicauan */
        .tweet-content {
            color: #14171a;
            font-size: 1em;
            line-height: 1.4;
            white-space: pre-wrap; /* Mempertahankan line breaks */
        }
        
        /* Tombol interaksi (Like/Retweet - dummy) */
        .tweet-actions {
            margin-top: 10px;
            color: #657786;
            font-size: 0.9em;
            display: flex;
            gap: 20px;
        }
        
        /* Header utama */
        .main-header {
            color: #1da1f2;
            text-align: center;
            font-weight: 800;
            padding-bottom: 20px;
            border-bottom: 1px solid #e1e8ed;
            margin-bottom: 20px;
        }
        
        /* Menyembunyikan elemen bawaan Streamlit yang tidak perlu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Support Dark Mode Streamlit */
        @media (prefers-color-scheme: dark) {
            .tweet-container {
                background-color: #15202b;
                border-color: #38444d;
            }
            .tweet-container:hover {
                background-color: #1c2732;
            }
            .tweet-author { color: #ffffff; }
            .tweet-content { color: #ffffff; }
            .tweet-time { color: #8899a6; }
            .tweet-actions { color: #8899a6; }
            .main-header { border-color: #38444d; }
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Navigasi 🐦")
    # State untuk melacak halaman aktif
    if 'page' not in st.session_state:
        st.session_state.page = 'Beranda'
    
    # Tombol navigasi
    if st.button("🏠 Beranda", use_container_width=True):
        st.session_state.page = 'Beranda'
    if st.button("✍️ Kicau Baru", use_container_width=True):
        st.session_state.page = 'Tulis'
    if st.button("👤 Profil Saya", use_container_width=True):
        st.session_state.page = 'Profil'
        
    st.divider()
    st.write("Masuk sebagai:")
    # Input nama pengguna sementara
    current_user = st.text_input("Username", value="@pengguna_baru", max_chars=20)

st.markdown("<h1 class='main-header'>🐦 Kicau</h1>", unsafe_allow_html=True)

# Halaman 1: Tulis Kicau Baru
if st.session_state.page == 'Tulis':
    st.subheader("Apa yang sedang terjadi?")
    
    # Form untuk membuat kicauan
    with st.form("new_tweet_form", clear_on_submit=True):
        tweet_text = st.text_area("Tuliskan kicauan Anda di sini...", max_chars=280, height=150)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            submit_button = st.form_submit_button("Kicaukan!", use_container_width=True)
            
        if submit_button:
            if tweet_text.strip(): # Pastikan tidak hanya spasi
                save_tweet(current_user, tweet_text.strip())
                st.success("Kicauan berhasil diposting!")
                time.sleep(1) # Jeda sejenak agar pesan sukses terbaca
                st.session_state.page = 'Beranda'
                st.rerun()
            else:
                st.error("Kicauan tidak boleh kosong.")

# Halaman 2: Beranda (Timeline)
elif st.session_state.page == 'Beranda':
    st.subheader("Beranda")
    
    # Tombol pintas untuk kicau baru (mirip FAB di mobile)
    if st.button("✍️ Buat Kicauan Baru", type="primary", use_container_width=True):
         st.session_state.page = 'Tulis'
         st.rerun()
         
    st.divider()
    
    # Memuat dan menampilkan data kicauan
    tweets = load_tweets()
    
    if not tweets:
        st.info("Belum ada kicauan. Jadilah yang pertama!")
    else:
        for tweet in tweets:
            # Merender setiap kicauan menggunakan HTML/CSS kustom
            st.markdown(f"""
                <div class="tweet-container">
                    <div class="tweet-author">{tweet['author']}</div>
                    <div class="tweet-time">{tweet['timestamp']}</div>
                    <div class="tweet-content">{tweet['content']}</div>
                    <div class="tweet-actions">
                        <span>💬 0</span>
                        <span>🔁 0</span>
                        <span>❤️ 0</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Halaman 3: Profil
elif st.session_state.page == 'Profil':
    st.subheader(f"Profil: {current_user}")
    
    tweets = load_tweets()
    # Filter kicauan hanya untuk user yang sedang aktif
    my_tweets = [t for t in tweets if t['author'] == current_user]
    
    st.write(f"Total Kicauan: **{len(my_tweets)}**")
    st.divider()
    
    if not my_tweets:
        st.info("Anda belum membuat kicauan.")
    else:
        for tweet in my_tweets:
            st.markdown(f"""
                <div class="tweet-container">
                    <div class="tweet-time">{tweet['timestamp']}</div>
                    <div class="tweet-content">{tweet['content']}</div>
                    <div class="tweet-actions">
                        <span>❤️ 0</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
