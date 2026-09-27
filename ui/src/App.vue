```vue
<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://127.0.0.1:8000/books'

// ====================
// DATA
// ====================
const books = ref([])
const loading = ref(false)
const error = ref(null)

// ====================
// SEARCH & PAGINATION
// ====================
const search = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const totalPages = ref(1)
const totalBooks = ref(0)

// ====================
// FORM
// ====================
const isEditing = ref(false)
const editingId = ref(null)

const form = ref({
  isbn: '',
  judul: '',
  tahun_terbit: ''
})

// ====================
// GET BOOKS
// ====================
const getBooks = async () => {
  loading.value = true
  error.value = null

  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      limit: itemsPerPage,
      search: search.value
    })

    const response = await fetch(`${API_URL}?${params}`)

    if (!response.ok) {
      throw new Error('Gagal mengambil data buku')
    }

    const result = await response.json()

    books.value = result.data
    totalPages.value = result.total_pages
    totalBooks.value = result.total

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// ====================
// SEARCH
// ====================
const doSearch = () => {
  currentPage.value = 1
  getBooks()
}

// ====================
// PAGINATION
// ====================
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    getBooks()
  }
}

// ====================
// SAVE BOOK
// ====================
const saveBook = async () => {
  // Validasi kosong
  if (
    !form.value.isbn ||
    !form.value.judul ||
    !form.value.tahun_terbit
  ) {
    alert('Semua field harus diisi')
    return
  }

  // Validasi ISBN
  if (!/^\d{13}$/.test(form.value.isbn)) {
    alert('ISBN harus terdiri dari 13 digit angka')
    return
  }

  // Validasi tahun
  const year = Number(form.value.tahun_terbit)

  if (year < 1900 || year > 2026) {
    alert('Tahun terbit harus antara 1900-2026')
    return
  }

  const data = {
    isbn: form.value.isbn,
    judul: form.value.judul,
    tahun_terbit: year
  }

  try {
    let response

    // EDIT
    if (isEditing.value) {
      response = await fetch(
        `${API_URL}/${editingId.value}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }
      )
    }

    // CREATE
    else {
      response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
    }

    const result = await response.json()

    if (!response.ok) {
      alert(result.detail || 'Gagal menyimpan buku')
      return
    }

    alert(
      isEditing.value
        ? 'Buku berhasil diedit'
        : 'Buku berhasil ditambahkan'
    )

    resetForm()

    // Refresh data
    await getBooks()

  } catch (err) {
    alert('Tidak dapat terhubung ke server')
  }
}

// ====================
// EDIT BOOK
// ====================
const editBook = (book) => {
  isEditing.value = true
  editingId.value = book.id

  form.value = {
    isbn: book.isbn,
    judul: book.judul,
    tahun_terbit: book.tahun_terbit
  }
}

// ====================
// DELETE BOOK
// ====================
const deleteBook = async (id) => {
  const yakin = confirm(
    'Yakin ingin menghapus buku ini?'
  )

  if (!yakin) {
    return
  }

  try {
    const response = await fetch(
      `${API_URL}/${id}`,
      {
        method: 'DELETE'
      }
    )

    if (!response.ok) {
      throw new Error('Gagal menghapus buku')
    }

    alert('Buku berhasil dihapus')

    // Jika halaman sekarang kosong setelah delete,
    // pindah ke halaman sebelumnya
    if (
      books.value.length === 1 &&
      currentPage.value > 1
    ) {
      currentPage.value--
    }

    await getBooks()

  } catch (err) {
    alert(err.message)
  }
}

// ====================
// RESET FORM
// ====================
const resetForm = () => {
  form.value = {
    isbn: '',
    judul: '',
    tahun_terbit: ''
  }

  isEditing.value = false
  editingId.value = null
}

// ====================
// ON MOUNTED
// ====================
onMounted(() => {
  getBooks()
})
</script>

<template>
  <div class="container">

    <!-- ==================== -->
    <!-- TITLE -->
    <!-- ==================== -->

    <h1>Manajemen Buku</h1>

    <!-- ==================== -->
    <!-- FORM -->
    <!-- ==================== -->

    <div class="form-card">

      <h2>
        {{ isEditing ? 'Edit Buku' : 'Tambah Buku' }}
      </h2>

      <form @submit.prevent="saveBook">

        <!-- ISBN -->
        <div class="form-group">

          <label>ISBN</label>

          <input
            v-model="form.isbn"
            type="text"
            maxlength="13"
            placeholder="ISBN 13 digit"
          >

        </div>

        <!-- JUDUL -->
        <div class="form-group">

          <label>Judul</label>

          <input
            v-model="form.judul"
            type="text"
            placeholder="Judul buku"
          >

        </div>

        <!-- TAHUN -->
        <div class="form-group">

          <label>Tahun Terbit</label>

          <input
            v-model="form.tahun_terbit"
            type="number"
            min="1900"
            max="2026"
            placeholder="1900-2026"
          >

        </div>

        <!-- BUTTON -->
        <button type="submit">

          {{ isEditing
            ? 'Simpan Perubahan'
            : 'Tambah Buku'
          }}

        </button>

        <button
          v-if="isEditing"
          type="button"
          @click="resetForm"
        >
          Batal
        </button>

      </form>

    </div>

    <!-- ==================== -->
    <!-- SEARCH -->
    <!-- ==================== -->

    <div class="search-section">

      <h2>Daftar Buku</h2>

      <div class="search-box">

        <input
          v-model="search"
          type="text"
          placeholder="Cari ISBN, judul, atau tahun..."
          @keyup.enter="doSearch"
        >

        <button @click="doSearch">
          Cari
        </button>

        <button
          v-if="search"
          @click="
            search = '';
            doSearch()
          "
        >
          Reset
        </button>

      </div>

    </div>

    <!-- ==================== -->
    <!-- LOADING -->
    <!-- ==================== -->

    <div
      v-if="loading"
      class="status"
    >
      Loading...
    </div>

    <!-- ==================== -->
    <!-- ERROR -->
    <!-- ==================== -->

    <div
      v-else-if="error"
      class="status error"
    >

      <p>{{ error }}</p>

      <button @click="getBooks">
        Retry
      </button>

    </div>

    <!-- ==================== -->
    <!-- EMPTY -->
    <!-- ==================== -->

    <div
      v-else-if="books.length === 0"
      class="status"
    >
      Data buku tidak ditemukan.
    </div>

    <!-- ==================== -->
    <!-- TABLE -->
    <!-- ==================== -->

    <div v-else>

      <table>

        <thead>

          <tr>
            <th>ID</th>
            <th>ISBN</th>
            <th>Judul</th>
            <th>Tahun</th>
            <th>Aksi</th>
          </tr>

        </thead>

        <tbody>

          <tr
            v-for="book in books"
            :key="book.id"
          >

            <td>
              {{ book.id }}
            </td>

            <td>
              {{ book.isbn }}
            </td>

            <td>
              {{ book.judul }}
            </td>

            <td>
              {{ book.tahun_terbit }}
            </td>

            <td>

              <button
                @click="editBook(book)"
              >
                Edit
              </button>

              <button
                @click="deleteBook(book.id)"
              >
                Hapus
              </button>

            </td>

          </tr>

        </tbody>

      </table>

      <!-- ==================== -->
      <!-- PAGINATION -->
      <!-- ==================== -->

      <div class="pagination">

        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
        >
          Previous
        </button>

        <button
          v-for="page in totalPages"
          :key="page"
          @click="goToPage(page)"
          :class="{
            active: currentPage === page
          }"
        >
          {{ page }}
        </button>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
        >
          Next
        </button>

      </div>

      <!-- INFO -->

      <p class="pagination-info">

        Halaman {{ currentPage }}
        dari {{ totalPages }}

        —
        {{ totalBooks }}
        buku

      </p>

    </div>

  </div>
</template>

<style>
/* ==================== */
/* CONTAINER */
/* ==================== */

.container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* ==================== */
/* FORM */
/* ==================== */

.form-card {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 9px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* ==================== */
/* BUTTON */
/* ==================== */

button {
  margin-right: 8px;
  padding: 8px 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #eee;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ==================== */
/* SEARCH */
/* ==================== */

.search-section {
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  gap: 8px;
}

.search-box input {
  flex: 1;
}

/* ==================== */
/* TABLE */
/* ==================== */

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background: #f2f2f2;
}

/* ==================== */
/* PAGINATION */
/* ==================== */

.pagination {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-top: 20px;
}

.pagination button {
  margin: 0;
}

.pagination button.active {
  font-weight: bold;
  background: #ddd;
}

.pagination-info {
  text-align: center;
  margin-top: 10px;
}

/* ==================== */
/* STATUS */
/* ==================== */

.status {
  padding: 20px;
  text-align: center;
}

.error {
  color: red;
}
</style>
