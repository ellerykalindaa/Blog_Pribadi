/**
 * Class BlogAPI - Menangani semua request ke Backend FastAPI
 */
class BlogAPI {
  constructor() {
    this.baseURL = "http://localhost:8000/posts";
  }

  async fetchPosts() {
    try {
      const response = await fetch(this.baseURL);
      return await response.json();
    } catch (error) {
      console.error("Gagal mengambil data:", error);
      return [];
    }
  }

  async createPost(postData) {
    try {
      const response = await fetch(this.baseURL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(postData),
      });
      return await response.json();
    } catch (error) {
      console.error("Gagal mengirim data:", error);
    }
  }
}

/**
 * UI Manager - Mengatur tampilan dan event listener
 */
class UIManager {
  constructor() {
    this.api = new BlogAPI();
    this.container = document.getElementById("blog-container");
    this.form = document.getElementById("blog-form");
    this.modal = document.getElementById("modal-overlay");

    this.initEvents();
    this.loadPosts();
  }

  initEvents() {
    // Buka modal
    document.getElementById("btn-open-modal").onclick = () =>
      this.modal.classList.remove("hidden");

    // Tutup modal
    document.getElementById("btn-close-modal").onclick = () =>
      this.modal.classList.add("hidden");

    // Submit Form
    this.form.onsubmit = async (e) => {
      e.preventDefault();
      const data = {
        title: document.getElementById("title").value,
        content: document.getElementById("content").value,
        author: document.getElementById("author").value,
        // Kategori bisa ditambahkan di schema backend nanti
      };

      await this.api.createPost(data);
      this.form.reset();
      this.modal.classList.add("hidden");
      this.loadPosts(); // Refresh list
    };
  }

  async loadPosts() {
    this.container.innerHTML = '<div class="loader">Memuat...</div>';
    const posts = await this.api.fetchPosts();

    if (posts.length === 0) {
      this.container.innerHTML = "<p>Belum ada postingan.</p>";
      return;
    }

    this.container.innerHTML = posts
      .map(
        (post) => `
            <article class="post-card">
                <span class="category-tag">General</span>
                <h2>${post.title}</h2>
                <p>${post.content}</p>
                <div class="meta">
                    <span>Oleh <strong>${
                      post.author || "Anonim"
                    }</strong></span>
                </div>
            </article>
        `
      )
      .join("");
  }
}

// Jalankan Aplikasi
document.addEventListener("DOMContentLoaded", () => {
  new UIManager();
});
