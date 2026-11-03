# PIZA STORE — Demo website top up game

## Jalankan di komputer
1. Install Python 3.10 atau lebih baru.
2. Ekstrak ZIP ini, lalu buka terminal di folder `piza_store`.
3. Buat virtual environment (opsional tetapi disarankan):
   - Windows: `python -m venv .venv` lalu `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` lalu `source .venv/bin/activate`
4. Install dependensi: `pip install -r requirements.txt`
5. Jalankan: `python app.py`
6. Buka `http://127.0.0.1:5000`.

## Login admin demo
- URL: `http://127.0.0.1:5000/admin/login`
- Username: `admin`
- Password: `GantiPassword123!`

Ubah kredensial sebelum dipublikasikan dengan environment variables `ADMIN_USER`, `ADMIN_PASSWORD`, dan `SECRET_KEY`.

## Penting tentang QRIS dan operasional
Halaman QRIS pada proyek ini adalah placeholder DEMO, bukan kode QR pembayaran aktif. Untuk menerima pembayaran sungguhan, daftar ke payment gateway resmi yang mendukung QRIS (misalnya penyedia berizin), lalu integrasikan pembuatan invoice/QR dinamis dan webhook verifikasi pembayaran. Jangan mengubah status menjadi lunas hanya berdasarkan screenshot bukti transfer. Sesuaikan daftar produk dan harga di variabel `GAMES` pada `app.py`.

## Sebelum online
- Gunakan hosting yang mendukung Python/Flask.
- Set `SECRET_KEY`, `ADMIN_USER`, dan `ADMIN_PASSWORD` yang kuat melalui environment variables.
- Matikan debug mode (ubah `app.run(debug=True)` menjadi `app.run()` atau gunakan server produksi seperti Gunicorn).
- Gunakan HTTPS, backup database, validasi webhook, rate limiting, dan kebijakan privasi/ketentuan layanan.
- Database SQLite cocok untuk demo kecil; pertimbangkan PostgreSQL untuk produksi.
- Pastikan kamu memiliki izin/akses reseller atau API distributor untuk pengiriman top up otomatis. Website ini belum mengirim item game secara otomatis.

## Deploy di Render (contoh)
- Hubungkan repository GitHub ke Render sebagai Web Service.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Tambahkan environment variables `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASSWORD`.
- Catatan: filesystem disk pada hosting gratis bisa bersifat sementara. Untuk data pesanan yang harus awet, gunakan database PostgreSQL terkelola dan ubah koneksi aplikasi sebelum menerima pelanggan.
