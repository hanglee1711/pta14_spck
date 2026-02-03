// ============================================
// ShopBee - Shop & Cart Module
// ============================================

// Product data (matching original PyQt5 app)
const PRODUCTS = [
  {
    name: 'PlayStation 5',
    price: 12990000,
    image: 'images/fab763309ba5fd53478e9dda2268c79a.webp'
  },
  {
    name: 'Nintendo Switch',
    price: 6990000,
    image: 'images/tendo_switch_oled_model_white_set_-_nang_cap_moi__choi_game_da_hon__1__0942cc7c792d45d886026c7b4549059c_grande.jpg'
  },
  {
    name: 'Xbox Series X',
    price: 11990000,
    image: 'images/May-choi-game-Xbox-Series-X.webp'
  },
  {
    name: 'Steam Deck',
    price: 12500000,
    image: 'images/Valve-Steam-Deck-1.webp'
  },
  {
    name: 'Tay cầm PS5',
    price: 1690000,
    image: 'images/61MCVrX7qiL.jpg'
  },
  {
    name: 'Tai nghe gaming',
    price: 990000,
    image: 'images/tai-nghe-havit-h2029u-rgb-6_516c4b28a6704bbcbdb571da6c5ff54e_grande.jpg'
  },
  {
    name: 'GTA V',
    price: 600000,
    image: 'images/grand-theft-auto-v-ps5-700x700h.webp'
  },
  {
    name: 'Elden Ring',
    price: 1000000,
    image: 'images/Dia-game-Elden-Ring-PlayStation-5.webp'
  },
  {
    name: 'Resident Evil 4',
    price: 1200000,
    image: 'images/712XPl7+qKL.jpg'
  },
  {
    name: 'The Witcher 3',
    price: 650000,
    image: 'images/game-the-witcher-3-wild-hunt-complete-edition-ps5-1_92872_63eb3b4f7742b5.46420401.jpg'
  },
  {
    name: 'Keyboard RGB',
    price: 1990000,
    image: 'images/z7489168695247_5ca581326a753a76ac385a6553d837d6.jpg'
  },
  {
    name: 'Logitech G502',
    price: 1500000,
    image: 'images/z7489169335837_0b2862f177754779ff5094d62bf1a2ef.jpg'
  },
  {
    name: 'HyperX Cloud',
    price: 1900000,
    image: 'images/hyperx_cloud_alpha_wireless_1_main.webp'
  },
  {
    name: 'SteelSeries Rival',
    price: 1900000,
    image: 'images/imgbuy_rival5_005.png__1920x1080_q100_crop-fit_optimize_subsampling-2_077e84827db14b4e889706b4a71a3084_master.jpg'
  }
];

// Cart state
let cart = {};

// ============================================
// FORMAT HELPERS
// ============================================
function formatVND(amount) {
  return amount.toLocaleString('vi-VN') + 'đ';
}

// ============================================
// PRODUCT GRID
// ============================================
function renderProducts() {
  const grid = document.getElementById('productGrid');
  if (!grid) return;

  grid.innerHTML = PRODUCTS.map((product, index) => `
    <div class="product-card">
      <img class="product-img" src="${product.image}" alt="${product.name}"
           onerror="this.src='images/shopping.webp'">
      <div class="product-info">
        <div class="product-name" title="${product.name}">${product.name}</div>
        <div class="product-price">${formatVND(product.price)}</div>
        <button class="btn-add-cart" onclick="addToCart(${index})">
          Thêm vào giỏ
        </button>
      </div>
    </div>
  `).join('');
}

// ============================================
// CART LOGIC
// ============================================
function addToCart(productIndex) {
  const product = PRODUCTS[productIndex];
  if (!product) return;

  if (cart[product.name]) {
    cart[product.name].qty += 1;
  } else {
    cart[product.name] = { price: product.price, qty: 1 };
  }

  updateCartUI();
  showToast(`Đã thêm "${product.name}" vào giỏ hàng`);
}

function removeFromCart(productName) {
  delete cart[productName];
  updateCartUI();
}

function updateQuantity(productName, delta) {
  if (!cart[productName]) return;

  cart[productName].qty += delta;
  if (cart[productName].qty <= 0) {
    delete cart[productName];
  }

  updateCartUI();
}

function clearCart() {
  cart = {};
  updateCartUI();
}

function getCartTotal() {
  return Object.values(cart).reduce((sum, item) => sum + item.price * item.qty, 0);
}

function getCartCount() {
  return Object.values(cart).reduce((sum, item) => sum + item.qty, 0);
}

// ============================================
// CART UI
// ============================================
function updateCartUI() {
  updateBadge();
  renderCartTable();
  updateCartTotal();
}

function updateBadge() {
  const badge = document.getElementById('cartBadge');
  if (!badge) return;

  const count = getCartCount();
  if (count === 0) {
    badge.classList.remove('show');
    badge.textContent = '';
  } else {
    badge.classList.add('show');
    badge.textContent = count > 99 ? '99+' : count;
  }
}

function renderCartTable() {
  const tbody = document.getElementById('cartTableBody');
  if (!tbody) return;

  const items = Object.entries(cart);

  if (items.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="cart-empty">Giỏ hàng trống</td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = items.map(([name, info]) => {
    const subtotal = info.price * info.qty;
    return `
      <tr>
        <td>${name}</td>
        <td class="qty-cell">
          <button class="btn-remove" onclick="updateQuantity('${name.replace(/'/g, "\\'")}', -1)" style="padding:3px 8px;">-</button>
          ${info.qty}
          <button class="btn-remove" onclick="updateQuantity('${name.replace(/'/g, "\\'")}', 1)" style="padding:3px 8px;background:rgba(46,204,113,0.7);">+</button>
        </td>
        <td class="price-cell">${formatVND(info.price)}</td>
        <td class="price-cell">${formatVND(subtotal)}</td>
        <td>
          <button class="btn-remove" onclick="removeFromCart('${name.replace(/'/g, "\\'")}')">Xóa</button>
        </td>
      </tr>
    `;
  }).join('');
}

function updateCartTotal() {
  const totalEl = document.getElementById('cartTotal');
  if (totalEl) {
    totalEl.textContent = `Tổng tiền: ${formatVND(getCartTotal())}`;
  }
}

// ============================================
// SIDEBAR TOGGLE
// ============================================
function openCartSidebar() {
  const overlay = document.getElementById('cartOverlay');
  const sidebar = document.getElementById('cartSidebar');
  if (!overlay || !sidebar) return;

  overlay.classList.add('open');
  sidebar.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCartSidebar() {
  const overlay = document.getElementById('cartOverlay');
  const sidebar = document.getElementById('cartSidebar');
  if (!overlay || !sidebar) return;

  overlay.classList.remove('open');
  sidebar.classList.remove('open');
  document.body.style.overflow = '';
}

function toggleCartSidebar() {
  const sidebar = document.getElementById('cartSidebar');
  if (sidebar && sidebar.classList.contains('open')) {
    closeCartSidebar();
  } else {
    openCartSidebar();
  }
}

// ============================================
// PAYMENT
// ============================================
function handlePay() {
  if (Object.keys(cart).length === 0) {
    showModal('Giỏ hàng trống', '<p>Vui lòng thêm sản phẩm vào giỏ hàng!</p>', false);
    return;
  }

  const items = Object.entries(cart);
  const total = getCartTotal();

  let bodyHTML = '<ul>';
  items.forEach(([name, info]) => {
    bodyHTML += `<li>- ${name} x${info.qty} = ${formatVND(info.price * info.qty)}</li>`;
  });
  bodyHTML += '</ul>';
  bodyHTML += `<div class="modal-total">Tổng tiền: ${formatVND(total)}</div>`;
  bodyHTML += '<p style="margin-top:10px;">Xác nhận thanh toán?</p>';

  showModal('Thanh toán', bodyHTML, true, () => {
    clearCart();
    closeCartSidebar();
    showToast('Thanh toán thành công! Cảm ơn bạn đã mua hàng!');
  });
}

function handleClearCart() {
  if (Object.keys(cart).length === 0) return;

  showModal('Xóa giỏ hàng', '<p>Bạn có chắc muốn xóa toàn bộ giỏ hàng?</p>', true, () => {
    clearCart();
  }, true);
}

// ============================================
// LOGOUT
// ============================================
function handleLogout() {
  showModal('Đăng xuất', '<p>Bạn có chắc muốn đăng xuất?</p>', true, () => {
    logout();
  }, true);
}

// ============================================
// MODAL
// ============================================
function showModal(title, bodyHTML, showConfirm = true, onConfirm = null, isDanger = false) {
  const modal = document.getElementById('modalOverlay');
  const modalTitle = document.getElementById('modalTitle');
  const modalBody = document.getElementById('modalBody');
  const btnConfirm = document.getElementById('modalConfirm');
  const btnCancel = document.getElementById('modalCancel');

  if (!modal) return;

  modalTitle.textContent = title;
  modalBody.innerHTML = bodyHTML;

  if (showConfirm) {
    btnConfirm.style.display = 'block';
    btnCancel.textContent = 'Hủy';

    btnConfirm.className = 'btn-confirm' + (isDanger ? ' danger' : '');
    btnConfirm.textContent = isDanger ? 'Xác nhận' : 'Thanh toán';

    btnConfirm.onclick = () => {
      hideModal();
      if (onConfirm) onConfirm();
    };
  } else {
    btnConfirm.style.display = 'none';
    btnCancel.textContent = 'Đóng';
  }

  btnCancel.onclick = hideModal;
  modal.classList.add('show');
}

function hideModal() {
  const modal = document.getElementById('modalOverlay');
  if (modal) modal.classList.remove('show');
}

// ============================================
// TOAST
// ============================================
function showToast(message) {
  // Remove existing toast
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast success';
  toast.textContent = message;
  document.body.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// ============================================
// INIT
// ============================================
function initShopPage() {
  // Check auth
  const user = requireAuth();
  if (!user) return;

  renderProducts();
  updateCartUI();

  // Event listeners
  document.getElementById('btnCartToggle').addEventListener('click', toggleCartSidebar);
  document.getElementById('cartOverlay').addEventListener('click', closeCartSidebar);
  document.getElementById('btnCloseSidebar').addEventListener('click', closeCartSidebar);
  document.getElementById('btnClearCart').addEventListener('click', handleClearCart);
  document.getElementById('btnPay').addEventListener('click', handlePay);
  document.getElementById('btnLogout').addEventListener('click', handleLogout);

  // Keyboard: Escape to close sidebar/modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCartSidebar();
      hideModal();
    }
  });
}
