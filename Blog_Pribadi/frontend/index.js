// ============================================
// REELBLOG - BLOG POSTING PLATFORM
// ============================================
// Purpose: Main homepage untuk menampilkan, mencari, dan berinteraksi dengan postingan blog
// Features: View toggle (list/grid), search by title/content, comments, edit/delete posts
// Author: ReelBlog Team
// Version: 2.0.0
// ============================================

// Konfigurasi
const API_URL = 'http://localhost:8000';
let currentUser = null;
let allPosts = [];
let allCategories = []; // Cache untuk kategori
let usersCache = {}; // Cache untuk menyimpan data user
let viewMode = 'list'; // 'list' atau 'grid'
let searchQuery = ''; // Current search query
let selectedCategory = ''; // Selected category filter

// ============================================
// INITIALIZATION
// ============================================

/**
 * Event listener untuk DOMContentLoaded
 * Inisialisasi semua komponen halaman saat DOM selesai loading
 */
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadCategories();
    loadPosts();
    setupEventListeners();
});

/**
 * Setup semua event listeners untuk interaksi user
 * Termasuk: search input, view mode toggle, logout button
 */
function setupEventListeners() {
    // Search event listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            filterAndDisplayPosts();
        });
    }

    // View mode toggle
    const viewToggleRadios = document.querySelectorAll('input[name="viewMode"]');
    viewToggleRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            viewMode = e.target.value;
            applyViewMode();
            localStorage.setItem('preferredViewMode', viewMode);
        });
    });

    // Category filter event listener
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', (e) => {
            selectedCategory = e.target.value;
            filterAndDisplayPosts();
        });
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    // Login / Register navigation
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = '/frontend/login.html';
        });
    }
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            window.location.href = '/frontend/register.html';
        });
    }
}

/**
 * Load preferred view mode dari localStorage
 * Jika user pernah memilih view mode sebelumnya, gunakan itu lagi
 */
function loadPreferredViewMode() {
    const saved = localStorage.getItem('preferredViewMode');
    if (saved) {
        viewMode = saved;
        const radio = document.querySelector(`input[name="viewMode"][value="${saved}"]`);
        if (radio) radio.checked = true;
    }
}

/**
 * Apply view mode (list atau grid) ke posts container
 * List: vertical stack (default)
 * Grid: responsive grid 3 columns
 */
function applyViewMode() {
    const container = document.getElementById('postsContainer');
    container.classList.remove('list-view', 'grid-view');
    container.classList.add(`${viewMode}-view`);
}

/**
 * Filter dan tampilkan postingan berdasarkan search query
 * Mencari di judul dan konten postingan
 * 
 * @param {string} query - Search query (optional, dari global searchQuery)
 */
function filterAndDisplayPosts() {
    const searchInfo = document.getElementById('searchInfo');

    // Start with all posts
    let filteredPosts = allPosts;

    // Filter by kategori jika selected
    if (selectedCategory) {
        filteredPosts = filteredPosts.filter(post => 
            post.category_id === parseInt(selectedCategory)
        );
    }

    // Filter berdasarkan search query
    if (searchQuery) {
        filteredPosts = filteredPosts.filter(post => {
            const title = (post.title || '').toLowerCase();
            const content = (post.content || '').toLowerCase();
            return title.includes(searchQuery) || content.includes(searchQuery);
        });
    }

    // Tampilkan hasil
    if (filteredPosts.length === 0) {
        let message = '';
        if (searchQuery && selectedCategory) {
            message = `❌ Tidak ada postingan yang cocok dengan pencarian "<strong>${escapeHtml(searchQuery)}</strong>" di kategori ini`;
        } else if (searchQuery) {
            message = `❌ Tidak ada postingan yang cocok dengan pencarian "<strong>${escapeHtml(searchQuery)}</strong>"`;
        } else if (selectedCategory) {
            message = `❌ Tidak ada postingan di kategori ini`;
        }
        
        if (message) {
            searchInfo.innerHTML = `<div class="search-results-info no-results">${message}</div>`;
        }
        displayEmptyState(filteredPosts, true);
    } else {
        let message = '';
        if (searchQuery && selectedCategory) {
            message = `✅ Ditemukan <strong>${filteredPosts.length}</strong> postingan cocok dengan "<strong>${escapeHtml(searchQuery)}</strong>" di kategori ini`;
        } else if (searchQuery) {
            message = `✅ Ditemukan <strong>${filteredPosts.length}</strong> postingan cocok dengan "<strong>${escapeHtml(searchQuery)}</strong>"`;
        } else if (selectedCategory) {
            message = `✅ Ditemukan <strong>${filteredPosts.length}</strong> postingan di kategori ini`;
        }
        
        if (message) {
            searchInfo.innerHTML = `<div class="search-results-info">${message}</div>`;
        }
        displayPosts(filteredPosts);
    }
}

/**
 * Escape HTML untuk mencegah XSS attacks
 * Mengkonversi HTML special characters ke entities
 * 
 * @param {string} text - Text untuk di-escape
 * @returns {string} Escaped HTML text
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

/**
 * Cek apakah user sudah login dengan membaca token dari localStorage
 * Jika ada token valid, set currentUser dan update UI
 * 
 * @returns {boolean} True jika user logged in, false sebaliknya
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const userId = localStorage.getItem('user_id');
    
    if (token && username && userId) {
        currentUser = {
            id: parseInt(userId) || userId,  // Convert ke number jika possible
            username: username,
            token: token
        };
        
        console.log('✅ User logged in:', currentUser);
        
        updateNavigation();
        updateProfileInfo();
        return true;
    }
    return false;
}

/**
 * Update navigasi menu berdasarkan status login user
 * Tampilkan/sembunyikan tombol login, register, logout, create post
 */
function updateNavigation() {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const profileInfo = document.getElementById('profileInfo');
    const createPostLink = document.getElementById('createPostLink');

    if (currentUser) {
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
        profileInfo.style.display = 'flex';
        
        if (createPostLink) {
            createPostLink.style.display = 'flex';
        }
    } else {
        loginBtn.style.display = 'inline-block';
        registerBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
        profileInfo.style.display = 'none';
        
        if (createPostLink) {
            createPostLink.style.display = 'none';
        }
    }
}

/**
 * Update tampilan profile info di header
 * Menampilkan username dan avatar dari current user
 */
function updateProfileInfo() {
    const usernameDisplay = document.getElementById('usernameDisplay');
    const userAvatar = document.getElementById('userAvatar');
    
    if (currentUser && currentUser.username) {
        usernameDisplay.textContent = currentUser.username;
        
        // Set avatar dengan huruf pertama username
        const firstLetter = currentUser.username.charAt(0).toUpperCase();
        userAvatar.textContent = firstLetter;
        
        // Simpan ke cache
        if (currentUser.id) {
            usersCache[currentUser.id] = {
                id: currentUser.id,
                username: currentUser.username
            };
        }
    }
}

/**
 * Logout user dengan menghapus token dan data dari localStorage
 * Menampilkan konfirmasi sebelum logout
 */
function logout() {
    if (confirm('Apakah Anda yakin ingin logout?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        currentUser = null;
        updateNavigation();
        showMessage('✅ Logout berhasil!', 'success');
        loadPosts(); // Muat ulang postingan untuk update UI
    }
}

// Tampilkan pesan
function showMessage(message, type = 'info') {
    const container = document.getElementById('messageContainer');
    container.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
            <button class="close-alert-btn" style="background: none; border: none; font-size: 20px; cursor: pointer; margin-left: auto;">×</button>
        </div>
    `;
    
    // Close button event
    container.querySelector('.close-alert-btn').addEventListener('click', () => {
        container.innerHTML = '';
    });
    
    setTimeout(() => {
        if (container.innerHTML.includes('alert')) {
            container.innerHTML = '';
        }
    }, 5000);
}

// ============================================
// FUNGSI UNTUK MENDAPATKAN DATA USER
// ============================================

// Fungsi untuk mendapatkan user by ID (dengan berbagai endpoint)
async function getUserById(userId) {
    if (!userId) return null;
    
    // Cek cache dulu
    if (usersCache[userId]) {
        return usersCache[userId];
    }
    
    console.log(`🔄 Fetching user data for ID: ${userId}`);
    
    // Coba berbagai endpoint untuk get user
    const endpoints = [
        `${API_URL}/users/${userId}`,
        `${API_URL}/user/${userId}`,
        `${API_URL}/auth/users/${userId}`,
        `${API_URL}/auth/user/${userId}`
    ];
    
    for (const endpoint of endpoints) {
        try {
            const response = await fetch(endpoint);
            console.log(`Trying ${endpoint}: ${response.status}`);
            
            if (response.ok) {
                const userData = await response.json();
                console.log(`✅ User data found:`, userData);
                usersCache[userId] = userData;
                return userData;
            }
        } catch (err) {
            console.log(`Endpoint ${endpoint} not accessible`);
        }
    }
    
    // Jika tidak ditemukan, return default
    const defaultUser = { 
        id: userId, 
        username: `User_${userId}`,
        name: `User ${userId}`
    };
    usersCache[userId] = defaultUser;
    return defaultUser;
}

// Fungsi untuk mendapatkan semua users (untuk caching)
async function getAllUsers() {
    console.log('🔄 Fetching all users...');
    
    const endpoints = [
        `${API_URL}/users`,
        `${API_URL}/auth/users`
    ];
    
    for (const endpoint of endpoints) {
        try {
            const response = await fetch(endpoint);
            console.log(`Trying ${endpoint}: ${response.status}`);
            
            if (response.ok) {
                const users = await response.json();
                console.log(`✅ Found ${users.length} users`);
                
                // Simpan ke cache
                users.forEach(user => {
                    if (user.id) {
                        usersCache[user.id] = user;
                    }
                });
                return users;
            }
        } catch (err) {
            console.log(`Endpoint ${endpoint} not accessible`);
        }
    }
    
    console.log('❌ No user endpoint found');
    return [];
}

// ============================================
// FUNGSI UNTUK POSTS
// ============================================

// Ambil semua postingan dari backend
async function fetchPostsFromBackend() {
    try {
        console.log('📡 Fetching posts from:', `${API_URL}/posts`);
        const response = await fetch(`${API_URL}/posts`, {
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const posts = await response.json();
        // Sort posts by newest first (created_at/date/createdAt)
        posts.sort((a, b) => {
            const da = new Date(a.created_at || a.date || a.createdAt || 0).getTime();
            const db = new Date(b.created_at || b.date || b.createdAt || 0).getTime();
            return db - da;
        });
        console.log('📦 Received', posts.length, 'posts');
        
        // Debug: lihat struktur post pertama
        if (posts.length > 0) {
            console.log('🔍 First post structure:', posts[0]);
        }
        
        // Coba ambil semua user untuk caching
        setTimeout(() => {
            getAllUsers().catch(() => {
                console.log('⚠️ Could not fetch all users, will fetch individually');
            });
        }, 1000);
        
        return posts;
        
    } catch (error) {
        console.error('❌ Error fetching posts:', error);
        throw error;
    }
}

// Fungsi untuk mendapatkan author name dari post
function getAuthorInfo(post) {
    // Post API sudah return username langsung
    const authorId = post.author_id || post.user_id;
    const username = post.username || post.author_name || `User_${authorId}`;
    
    console.log('🔍 Author info:', {
        post_id: post.id,
        author_id: authorId,
        username: username,
        current_user_id: currentUser?.id,
        type_match: typeof authorId === typeof currentUser?.id
    });
    
    return {
        id: authorId,
        username: username,
        avatar: (username || 'U').charAt(0).toUpperCase()
    };
}

// Tampilkan postingan
function displayPosts(posts) {
    const container = document.getElementById('postsContainer');
    allPosts = posts;
    
    if (posts.length === 0) {
        displayEmptyState(posts);
        return;
    }
    
    // Apply current view mode
    applyViewMode();
    // Render semua posts
    container.innerHTML = '';
    
    posts.forEach(post => {
        const authorInfo = getAuthorInfo(post);
        
        // Format tanggal
        const postDate = new Date(post.created_at || post.date || post.createdAt);
        const formattedDate = postDate.toLocaleDateString('id-ID', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Cek apakah user adalah pemilik postingan
        const isOwner = currentUser && currentUser.id && 
                       currentUser.id.toString() === authorInfo.id.toString();
        
        console.log(`📝 Post ${post.id}: isOwner=${isOwner}, currentUser.id=${currentUser?.id}, authorInfo.id=${authorInfo.id}`);
        
        // Potong konten untuk preview
        const content = post.content || post.body || '';
        const previewContent = content.length > 200 ? content.substring(0, 200) + '...' : content;
        
        const postElement = document.createElement('div');
        postElement.className = 'post-card';
        
        postElement.innerHTML = `
            ${isOwner ? `
                <div class="post-actions-top">
                    <button class="btn btn-small btn-success edit-post-btn" data-id="${post.id}" title="Edit postingan">
                        ✏️
                    </button>
                    <button class="btn btn-small btn-danger delete-post-btn" data-id="${post.id}" title="Hapus postingan">
                        🗑️
                    </button>
                </div>
            ` : ''}
            
            <div class="post-header">
                <h2 class="post-title">${escapeHtml(post.title || 'No Title')}</h2>
                
                <div class="author-info">
                    <div class="author-avatar" style="background: linear-gradient(135deg, #${stringToColor(authorInfo.username)} 0%, #${stringToColor(authorInfo.username, true)} 100%);">
                        ${authorInfo.avatar}
                    </div>
                    <div class="author-details">
                        <div class="author-name">
                            ${escapeHtml(authorInfo.username)}
                            ${isOwner ? '<span class="owned-badge">Milik Anda</span>' : ''}
                        </div>
                        <div class="post-date">📅 ${formattedDate}</div>
                    </div>
                </div>
                
                <div class="post-meta-complete">
                    ${post.category ? `
                        <span class="post-category">
                            🏷️ ${escapeHtml(typeof post.category === 'object' ? post.category.name : post.category)}
                        </span>
                    ` : post.category_id ? `
                        <span class="post-category">
                            🏷️ Kategori ${post.category_id}
                        </span>
                    ` : ''}
                    <span style="color: #666; font-size: 12px;">
                        ${post.content && post.content.length > 200 ? '📖 Baca selengkapnya...' : ''}
                    </span>
                </div>
            </div>
            
            <div class="post-content-preview">
                ${escapeHtml(previewContent)}
            </div>
            
            <!-- Comments Section -->
            <div class="comments-section" style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="margin: 0;">💬 Komentar</h4>
                    <button class="toggle-comments-btn" data-post-id="${post.id}" title="Sembunyikan/Tampilkan komentar">
                        ▼
                    </button>
                </div>
                
                <!-- Comments List -->
                <div class="comments-list" id="comments-${post.id}" style="margin-bottom: 15px;">
                    <div style="text-align: center; color: #999; padding: 10px;">
                        Memuat komentar...
                    </div>
                </div>
                
                <!-- Add Comment Form -->
                ${currentUser ? `
                    <div class="add-comment-form">
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <input type="text" class="comment-input" placeholder="Tulis komentar..." 
                                   data-post-id="${post.id}" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                            <button class="btn btn-small btn-primary post-comment-btn" data-post-id="${post.id}">
                                📤 Kirim
                            </button>
                        </div>
                    </div>
                ` : `
                    <div style="text-align: center; padding: 10px; background: #f0f0f0; border-radius: 4px; color: #666;">
                        <a href="/frontend/login.html" style="color: #667eea;">Login</a> untuk menambahkan komentar
                    </div>
                `}
            </div>
        `;
        
        container.appendChild(postElement);
        
        // Load comments untuk post ini
        loadCommentsForPost(post.id);
    });
    
    // Tambahkan event listeners
    addPostEventListeners();
    addCommentEventListeners();
    
    // Update footer stats
    updateStats(posts);
}

// Helper function untuk generate color dari string
function stringToColor(str, second = false) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    let color = '';
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 0xFF;
        color += ('00' + value.toString(16)).substr(-2);
    }
    
    // Jika second color, lighten a bit
    if (second) {
        color = color.split('').map((c, i) => {
            const val = parseInt(c, 16);
            return Math.min(15, val + 4).toString(16);
        }).join('');
    }
    
    return color;
}

// Tampilkan state kosong
function displayEmptyState(posts = [], isSearchEmpty = false) {
    const container = document.getElementById('postsContainer');
    
    if (isSearchEmpty) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>Postingan tidak ditemukan</h3>
                <p>Coba gunakan kata kunci lain atau lihat semua postingan</p>
                <button class="btn btn-secondary" onclick="document.getElementById('searchInput').value = ''; filterAndDisplayPosts();">
                    🔄 Hapus Filter Pencarian
                </button>
            </div>
        `;
    } else {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <h3>Belum ada postingan</h3>
                <p>Jadilah yang pertama membuat postingan!</p>
                    ${currentUser ? 
                    `<a href="/frontend/create.html" class="btn btn-primary">✏️ Buat Postingan Pertama</a>` :
                    `<a href="/frontend/register.html" class="btn btn-primary">👤 Daftar untuk Mulai Menulis</a>`
                }
            </div>
        `;
    }
}

// ============================================
// COMMENTS FUNCTIONS
// ============================================

// Load komentar untuk post tertentu
async function loadCommentsForPost(postId) {
    try {
        const response = await fetch(`${API_URL}/comments/posts/${postId}`);
        if (response.ok) {
            const comments = await response.json();
            displayComments(postId, comments);
        }
    } catch (error) {
        console.error('Error loading comments:', error);
    }
}

// Tampilkan komentar
function displayComments(postId, comments) {
    const commentsList = document.getElementById(`comments-${postId}`);
    if (!commentsList) return;
    
    if (comments.length === 0) {
        commentsList.innerHTML = '<p style="color: #999; padding: 10px;">Belum ada komentar</p>';
        return;
    }
    
    commentsList.innerHTML = comments.map(comment => {
        const isCommentOwner = currentUser && currentUser.id && 
                              currentUser.id.toString() === comment.user_id.toString();
        
        return `
            <div class="comment-item" style="background: #f8f9fa; padding: 12px; border-radius: 4px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: start; gap: 10px;">
                    <div style="flex: 1;">
                        <strong style="color: #667eea;">${escapeHtml(comment.username)}</strong>
                        <p style="margin: 5px 0 0 0; color: #333;">${escapeHtml(comment.content)}</p>
                        <small style="color: #999;">📅 ${new Date(comment.created_at).toLocaleDateString('id-ID', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}</small>
                    </div>
                    ${isCommentOwner ? `
                        <div style="display: flex; gap: 5px;">
                            <button class="btn btn-tiny delete-comment-btn" data-id="${comment.id}" data-post-id="${postId}" title="Hapus">🗑️</button>
                            <button class="btn btn-tiny edit-comment-btn" data-id="${comment.id}" data-post-id="${postId}" title="Edit">✏️</button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Tambahkan event listeners untuk comments
function addCommentEventListeners() {
    // Tombol post komentar
    document.querySelectorAll('.post-comment-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const postId = btn.getAttribute('data-post-id');
            const input = document.querySelector(`.comment-input[data-post-id="${postId}"]`);
            const content = input.value.trim();
            
            if (!content) {
                alert('Komentar tidak boleh kosong');
                return;
            }
            
            if (!currentUser || !currentUser.token) {
                alert('Anda harus login terlebih dahulu');
                return;
            }
            
            await addComment(postId, content, input);
        });
    });
    
    // Tombol delete komentar
    document.querySelectorAll('.delete-comment-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const commentId = btn.getAttribute('data-id');
            const postId = btn.getAttribute('data-post-id');
            deleteComment(commentId, postId);
        });
    });
    
    // Tombol edit komentar
    document.querySelectorAll('.edit-comment-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const commentId = btn.getAttribute('data-id');
            const postId = btn.getAttribute('data-post-id');
            editComment(commentId, postId);
        });
    });
    
    // Toggle comments visibility
    document.querySelectorAll('.toggle-comments-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const postId = btn.getAttribute('data-post-id');
            const commentsList = document.getElementById(`comments-${postId}`);
            const commentSection = btn.closest('.comments-section');
            const addCommentForm = commentSection.querySelector('.add-comment-form');
            
            if (commentsList) {
                commentsList.classList.toggle('collapsed');
                
                // Update button display
                if (commentsList.classList.contains('collapsed')) {
                    btn.textContent = '▶';
                } else {
                    btn.textContent = '▼';
                }
            }
            
            // Also toggle add comment form
            if (addCommentForm) {
                addCommentForm.style.display = addCommentForm.style.display === 'none' ? 'block' : 'none';
            }
        });
    });
}

// Tambah komentar
async function addComment(postId, content, inputElement) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/comments/posts/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content: content })
        });
        
        if (response.ok) {
            inputElement.value = '';
            await loadCommentsForPost(postId);
            addCommentEventListeners();
        } else {
            const error = await response.json();
            alert(`Gagal menambah komentar: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error adding comment:', error);
        alert('Gagal menambah komentar');
    }
}

// Edit komentar
async function editComment(commentId, postId) {
    const content = prompt('Edit komentar:');
    if (!content) return;
    
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/comments/${commentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content: content })
        });
        
        if (response.ok) {
            await loadCommentsForPost(postId);
            addCommentEventListeners();
        } else {
            const error = await response.json();
            alert(`Gagal edit komentar: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error editing comment:', error);
        alert('Gagal edit komentar');
    }
}

// Hapus komentar
async function deleteComment(commentId, postId) {
    if (!confirm('Hapus komentar ini?')) return;
    
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/comments/${commentId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            await loadCommentsForPost(postId);
            addCommentEventListeners();
        } else {
            const error = await response.json();
            alert(`Gagal hapus komentar: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error deleting comment:', error);
        alert('Gagal hapus komentar');
    }
}

// Tambahkan event listeners untuk posts
function addPostEventListeners() {
    // Tombol hapus
    document.querySelectorAll('.delete-post-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const postId = e.target.getAttribute('data-id') || 
                          e.target.closest('.delete-post-btn').getAttribute('data-id');
            deletePost(postId);
        });
    });
    
    // Tombol edit
    document.querySelectorAll('.edit-post-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const postId = e.target.getAttribute('data-id') || 
                          e.target.closest('.edit-post-btn').getAttribute('data-id');
            editPost(postId);
        });
    });
}

// Update statistik footer
function updateStats(posts) {
    const statsDiv = document.getElementById('footerStats');
    const totalPosts = posts.length;
    
    // Hitung unique authors
    const authorIds = new Set();
    posts.forEach(post => {
        if (post.author_id) authorIds.add(post.author_id);
    });
    const totalAuthors = authorIds.size;
    
    statsDiv.innerHTML = `📊 ${totalPosts} postingan • 👤 ${totalAuthors} penulis`;
}

/**
 * Load semua kategori dari backend dan populate dropdown
 */
async function loadCategories() {
    try {
        const response = await fetch(`${API_URL}/categories/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const categories = await response.json();
            allCategories = categories;
            
            // Populate category filter dropdown
            const categoryFilter = document.getElementById('categoryFilter');
            if (categoryFilter) {
                // Keep "Semua Kategori" option
                const currentValue = categoryFilter.value;
                categoryFilter.innerHTML = '<option value="">Semua Kategori</option>';
                
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id;
                    option.textContent = cat.name;
                    categoryFilter.appendChild(option);
                });
                
                // Restore selection
                categoryFilter.value = currentValue;
            }
            console.log('✅ Categories loaded:', allCategories);
        } else {
            console.warn('⚠️ Failed to load categories');
        }
    } catch (error) {
        console.error('❌ Error loading categories:', error);
    }
}

// Load postingan
async function loadPosts() {
    const container = document.getElementById('postsContainer');
    
    try {
        container.innerHTML = `
            <div class="loading-spinner"></div>
            <div style="text-align: center; color: #666; margin-top: 10px;">Memuat postingan...</div>
        `;
        
        const posts = await fetchPostsFromBackend();
        
        // Load preferred view mode
        loadPreferredViewMode();
        
        if (posts.length === 0) {
            displayEmptyState(posts);
        } else {
            await displayPosts(posts);
        }
        
    } catch (error) {
        console.error('❌ Error loading posts:', error);
        container.innerHTML = `
            <div class="alert alert-error">
                <strong>❌ Gagal memuat postingan!</strong><br>
                Error: ${error.message}<br>
                Pastikan backend FastAPI berjalan di ${API_URL}
                <div class="mt-20">
                    <button onclick="loadPosts()" class="btn btn-secondary">🔄 Coba Lagi</button>
                    <button onclick="loadSampleData()" class="btn btn-small">Gunakan Data Contoh</button>
                </div>
            </div>
        `;
    }
}

// Hapus postingan
async function deletePost(postId) {
    if (!confirm('Apakah Anda yakin ingin menghapus postingan ini?')) {
        return;
    }
    
    const token = localStorage.getItem('token');
    if (!token) {
        showMessage('Anda harus login terlebih dahulu', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/posts/${postId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showMessage('✅ Postingan berhasil dihapus', 'success');
            loadPosts(); // Muat ulang postingan
        } else {
            const error = await response.json();
            showMessage(`❌ ${error.detail || 'Gagal menghapus postingan'}`, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('❌ Gagal menghapus postingan', 'error');
    }
}

// Edit postingan
function editPost(postId) {
    localStorage.setItem('editPostId', postId);
    window.location.href = `create.html?mode=edit&id=${postId}`;
}

// Load data contoh jika backend error
function loadSampleData() {
    const samplePosts = [
        {
            id: 1,
            title: "Contoh Postingan Pertama",
            content: "Ini adalah contoh postingan pertama untuk demonstrasi.",
            created_at: new Date().toISOString(),
            author_id: 1,
            category: "Demo"
        },
        {
            id: 2,
            title: "Tips Menulis Blog",
            content: "Berikut adalah beberapa tips untuk menulis blog yang menarik...",
            created_at: new Date().toISOString(),
            author_id: 2,
            category: "Tips"
        }
    ];
    
    // Add sample users to cache
    usersCache[1] = { id: 1, username: "Admin" };
    usersCache[2] = { id: 2, username: "Penulis" };
    
    displayPosts(samplePosts);
    showMessage('⚠️ Menggunakan data contoh', 'warning');
}

// Expose functions to global scope
window.deletePost = deletePost;
window.editPost = editPost;
window.loadPosts = loadPosts;
window.loadSampleData = loadSampleData;

// Debug helper function
window.testOwnerCheck = async function() {
    console.log('=== OWNER CHECK DEBUG ===');
    console.log('Current User:', currentUser);
    
    const response = await fetch(`${API_URL}/posts`);
    const posts = await response.json();
    
    if (posts.length > 0) {
        console.log('First Post:', posts[0]);
        console.log('Author ID from post:', posts[0].author_id, typeof posts[0].author_id);
        console.log('Current User ID:', currentUser?.id, typeof currentUser?.id);
        console.log('Match:', posts[0].author_id.toString() === currentUser?.id?.toString());
    }
};
