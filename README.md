# Simulasi Kombinasi Sinyal (Rust + Qt)

Dibuat oleh 

Rafi Sadad Ar-Rabbani 2042241105

Reksa Putra A 2042241126

Luthfiana Alzenayu Gyonina 2042241117

Ini adalah proyek mata kuliah Sistem Pengolahan Sinyal yang mengimplementasikan simulasi kombinasi sinyal (Penjumlahan, Pengurangan, Perkalian) secara real-time.

Arsitektur sistem ini menggunakan:
* **Backend:** Server API menggunakan **Rust** dengan `actix-web` untuk logika pemrosesan sinyal.
* **Frontend:** GUI interaktif menggunakan **Python** dengan `PyQt` dan `PyQtGraph` untuk visualisasi.

## Prasyarat

Sebelum menjalankan, pastikan Anda telah menginstal:
* [Git](https://git-scm.com/)
* [Rust & Cargo](https://rustup.rs/)
* [Python 3](https://www.python.org/) (dan `pip`)

## Cara Menjalankan

Proyek ini terdiri dari dua bagian (backend dan frontend) yang harus dijalankan secara bersamaan di dua terminal terpisah.

### 1. Menjalankan Backend (Rust)

Terminal pertama akan menjalankan server Rust.

```bash
# 1. Masuk ke folder backend
cd signal_backend

# 2. Jalankan server (mode debug)
cargo run
````

Server akan berjalan di `http://127.0.0.1:8080`. Biarkan terminal ini tetap terbuka.

### 2\. Menjalankan Frontend (Python)

Buka **terminal baru** untuk menjalankan GUI Python.

```bash
# 1. Masuk ke folder frontend
cd signal_frontend

# 2. (Opsional tapi disarankan) Buat dan aktifkan virtual environment
python -m venv venv

# Aktivasi di Windows (CMD/PowerShell)
.\venv\Scripts\activate
# Aktivasi di macOS/Linux
# source venv/bin/activate

# 3. Instal dependensi yang diperlukan
pip install -r requirements.txt

# 4. Jalankan aplikasi frontend
python frontend_app.py
```

Sebuah jendela GUI akan muncul. Tekan "Start Simulation" untuk menghubungkan frontend ke backend Rust.

