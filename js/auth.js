// ============================================
// ShopBee - Authentication Module
// Uses localStorage + SHA-256 hash
// ============================================

// SHA-256 hash using Web Crypto API
async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Get all users from localStorage
function getUsers() {
  const data = localStorage.getItem('shopbee_users');
  return data ? JSON.parse(data) : [];
}

// Save users to localStorage
function saveUsers(users) {
  localStorage.setItem('shopbee_users', JSON.stringify(users));
}

// Register new user
async function register(name, email, password) {
  const users = getUsers();

  // Check if email already exists
  if (users.find(u => u.email === email)) {
    return { success: false, message: 'Email này đã được đăng ký!' };
  }

  const hashedPassword = await sha256(password);
  users.push({ name, email, password: hashedPassword });
  saveUsers(users);

  return { success: true, message: `Tạo tài khoản thành công!\nChào mừng ${name}!` };
}

// Login
async function login(email, password) {
  const users = getUsers();
  const hashedPassword = await sha256(password);

  const user = users.find(u => u.email === email && u.password === hashedPassword);
  if (!user) {
    return { success: false, message: 'Email hoặc mật khẩu không đúng!' };
  }

  // Set session
  sessionStorage.setItem('shopbee_session', JSON.stringify({
    name: user.name,
    email: user.email,
    loggedIn: true
  }));

  return { success: true, message: 'Đăng nhập thành công!' };
}

// Logout
function logout() {
  sessionStorage.removeItem('shopbee_session');
  window.location.href = 'index.html';
}

// Check if user is authenticated
function checkAuth() {
  const session = sessionStorage.getItem('shopbee_session');
  if (!session) return null;

  const data = JSON.parse(session);
  if (!data.loggedIn) return null;

  return data;
}

// Redirect to shop if already logged in (for login/register pages)
function redirectIfLoggedIn() {
  if (checkAuth()) {
    window.location.href = 'shop.html';
  }
}

// Redirect to login if not logged in (for shop page)
function requireAuth() {
  if (!checkAuth()) {
    window.location.href = 'index.html';
    return null;
  }
  return checkAuth();
}

// ============================================
// LOGIN PAGE LOGIC
// ============================================
function initLoginPage() {
  redirectIfLoggedIn();

  const form = document.getElementById('loginForm');
  const errorEl = document.getElementById('errorMessage');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const agreed = document.getElementById('terms').checked;

    // Validation
    if (!email || !password) {
      showError(errorEl, 'Vui lòng nhập Email và Mật khẩu!');
      return;
    }

    if (!agreed) {
      showError(errorEl, 'Bạn phải đồng ý với điều khoản!');
      return;
    }

    const result = await login(email, password);

    if (!result.success) {
      showError(errorEl, result.message);
      return;
    }

    window.location.href = 'shop.html';
  });
}

// ============================================
// REGISTER PAGE LOGIC
// ============================================
function initRegisterPage() {
  redirectIfLoggedIn();

  const form = document.getElementById('registerForm');
  const errorEl = document.getElementById('errorMessage');
  const successEl = document.getElementById('successMessage');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const agreed = document.getElementById('terms').checked;

    // Validation
    if (!name || !email || !password) {
      showError(errorEl, 'Vui lòng nhập đầy đủ thông tin!');
      return;
    }

    if (!agreed) {
      showError(errorEl, 'Bạn phải đồng ý với điều khoản!');
      return;
    }

    const result = await register(name, email, password);

    if (!result.success) {
      showError(errorEl, result.message);
      return;
    }

    // Show success and redirect
    hideError(errorEl);
    showSuccess(successEl, result.message);

    setTimeout(() => {
      window.location.href = 'index.html';
    }, 1500);
  });
}

// ============================================
// HELPERS
// ============================================
function showError(el, message) {
  if (!el) return;
  el.textContent = message;
  el.style.display = 'block';
}

function hideError(el) {
  if (!el) return;
  el.style.display = 'none';
}

function showSuccess(el, message) {
  if (!el) return;
  el.textContent = message;
  el.style.display = 'block';
}
