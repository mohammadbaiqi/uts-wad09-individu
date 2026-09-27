# Books CRUD Application

Aplikasi CRUD buku menggunakan **FastAPI** sebagai backend dan **Vue 3 + Vite** sebagai frontend.

## 1. Teknologi

* Backend: FastAPI
* Frontend: Vue 3 + Vite
* Data: JSON
* API format: REST + JSON

## 2. Struktur Project

```text
UTS Wad09 Individu/
├── server/
│   ├── .venv/
│   ├── main.py
│   ├── buku.json
│   ├── requirements.txt
│   └── schema/
│       └── book.py
│
└── frontend/
    ├── src/
    │   └── App.vue
    ├── package.json
    └── vite.config.js
```

---

# 3. Menjalankan Backend

Masuk ke folder backend:

```bash
cd server
```

Aktifkan virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan FastAPI:

```bash
uvicorn main:app --reload
```

Backend berjalan pada:

```text
http://127.0.0.1:8000
```

Dokumentasi API:

```text
http://127.0.0.1:8000/docs
```

---

# 4. Menjalankan Frontend

Buka terminal baru agar backend tetap berjalan.

Masuk ke folder frontend:

```bash
cd frontend
```

Install dependency:

```bash
npm install
```

Jalankan Vite:

```bash
npm run dev
```

Frontend akan berjalan pada:

```text
http://localhost:5173
```

Buka alamat tersebut melalui browser.

---

# 5. API Endpoint

Base URL:

```text
http://127.0.0.1:8000
```

| Method | Endpoint      | Fungsi                |
| ------ | ------------- | --------------------- |
| GET    | `/books`      | Mengambil daftar buku |
| GET    | `/books/{id}` | Mengambil satu buku   |
| POST   | `/books`      | Menambah buku         |
| PUT    | `/books/{id}` | Mengubah buku         |
| DELETE | `/books/{id}` | Menghapus buku        |

API juga mendukung:

```text
GET /books?page=1&limit=5
```

untuk pagination.

Search:

```text
GET /books?search=python&page=1&limit=5
```

---

# 6. Verifikasi Requirement

## Requirement 1 — Menampilkan Daftar Buku

Frontend mengambil data dari:

```text
GET /books
```

Cara verifikasi:

1. Jalankan backend.
2. Jalankan frontend.
3. Buka `http://localhost:5173`.
4. Daftar buku ditampilkan pada tabel.

Backend dapat diverifikasi melalui:

```text
http://127.0.0.1:8000/docs
```

---

## Requirement 2 — Search Buku

Search dapat dilakukan berdasarkan:

* ISBN
* Judul
* Tahun terbit

Contoh:

```text
GET /books?search=python&page=1&limit=5
```

Cara verifikasi:

1. Buka frontend.
2. Masukkan kata kunci pada kotak pencarian.
3. Klik **Cari**.
4. Data yang ditampilkan hanya data yang sesuai dengan kata kunci.

Search dilakukan oleh backend, bukan dengan mengambil seluruh data ke frontend terlebih dahulu.

---

## Requirement 3 — Pagination

Pagination dilakukan oleh backend menggunakan parameter:

```text
page
limit
```

Contoh:

```text
GET /books?page=1&limit=5
```

Halaman berikutnya:

```text
GET /books?page=2&limit=5
```

Response API menyediakan informasi:

```json
{
  "data": [],
  "page": 1,
  "limit": 5,
  "total": 12,
  "total_pages": 3
}
```

Cara verifikasi:

1. Buka halaman frontend.
2. Klik tombol **Next**.
3. Data pada tabel berubah ke halaman berikutnya.
4. Klik **Previous** untuk kembali.

---

## Requirement 4 — Tambah Buku

Method:

```text
POST /books
```

Contoh request:

```json
{
  "isbn": "9786020320099",
  "judul": "Belajar FastAPI",
  "tahun_terbit": 2026
}
```

Cara verifikasi:

1. Isi ISBN 13 digit.
2. Isi judul buku.
3. Isi tahun terbit.
4. Klik **Tambah Buku**.
5. Buku baru muncul pada daftar.

Validasi:

* ISBN harus 13 digit.
* Tahun terbit harus berada pada rentang 1900–2026.
* Semua field wajib diisi.

---

## Requirement 5 — Edit Buku

Method:

```text
PUT /books/{id}
```

Cara verifikasi:

1. Klik tombol **Edit** pada salah satu buku.
2. Form akan terisi dengan data buku.
3. Ubah data.
4. Klik **Simpan Perubahan**.
5. Data buku pada tabel berubah.

---

## Requirement 6 — Hapus Buku

Method:

```text
DELETE /books/{id}
```

Cara verifikasi:

1. Klik tombol **Hapus**.
2. Konfirmasi penghapusan.
3. Data buku dihapus.
4. Tabel diperbarui.

Frontend menggunakan konfirmasi sebelum melakukan penghapusan.

---

## Requirement 7 — Loading State

Saat frontend sedang mengambil data dari API, frontend menampilkan:

```text
Loading...
```

Cara verifikasi:

1. Refresh halaman.
2. Saat request API sedang berlangsung, status `Loading...` ditampilkan.

---

## Requirement 8 — Error State dan Retry

Jika terjadi kesalahan ketika mengambil data dari API, frontend menampilkan pesan error dan tombol:

```text
Retry
```

Cara verifikasi:

1. Hentikan server FastAPI.
2. Refresh frontend.
3. Pesan error akan ditampilkan.
4. Tombol **Retry** tersedia.
5. Jalankan kembali backend.
6. Klik **Retry** untuk mencoba request kembali.

---

# 7. Pengujian API

API dapat diuji melalui Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Contoh pengujian:

### GET

```text
GET /books?page=1&limit=5
```

### Search

```text
GET /books?search=python&page=1&limit=5
```

### POST

```json
{
  "isbn": "9786020320099",
  "judul": "Belajar FastAPI",
  "tahun_terbit": 2026
}
```

### PUT

```text
PUT /books/1
```

### DELETE

```text
DELETE /books/1
```

---

# 8. Ringkasan Verifikasi

| Requirement       | Implementasi             | Status |
| ----------------- | ------------------------ | ------ |
| Daftar buku       | `GET /books`             | ✅      |
| Search            | `search` query parameter | ✅      |
| Pagination        | `page` dan `limit`       | ✅      |
| Tambah buku       | `POST /books`            | ✅      |
| Edit buku         | `PUT /books/{id}`        | ✅      |
| Hapus buku        | `DELETE /books/{id}`     | ✅      |
| Loading state     | Vue `loading` state      | ✅      |
| Error state       | Vue `error` state        | ✅      |
| Retry             | Tombol Retry             | ✅      |
| Validasi form     | ISBN dan tahun terbit    | ✅      |
| API documentation | FastAPI Swagger          | ✅      |

---

# 9. Menjalankan Project dari Awal

### Terminal 1 — Backend

```bash
cd server
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Kemudian buka:

```text
http://localhost:5173
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```
