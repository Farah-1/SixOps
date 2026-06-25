const productGrid = document.getElementById("productGrid");
const categoryFilters = document.getElementById("categoryFilters");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const cartDrawer = document.getElementById("cartDrawer");
const overlay = document.getElementById("overlay");
const openCart = document.getElementById("openCart");
const closeCart = document.getElementById("closeCart");
const cartItems = document.getElementById("cartItems");
const cartCount = document.getElementById("cartCount");
const cartTotal = document.getElementById("cartTotal");
const checkoutButton = document.getElementById("checkoutButton");
const toast = document.getElementById("toast");
const productModal = document.getElementById("productModal");
const modalContent = document.getElementById("modalContent");
const closeModal = document.getElementById("closeModal");

let products = [];
let selectedCategory = "All";
let cart = JSON.parse(localStorage.getItem("gadgetnest-cart") || "[]");
let favorites = JSON.parse(localStorage.getItem("gadgetnest-favorites") || "[]");

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2800);
}

function saveCart() {
  localStorage.setItem("gadgetnest-cart", JSON.stringify(cart));
}

function saveFavorites() {
  localStorage.setItem("gadgetnest-favorites", JSON.stringify(favorites));
}

function discount(product) {
  return Math.round(((product.old_price - product.price) / product.old_price) * 100);
}

function sortedProducts(list) {
  const sorted = [...list];
  if (sortSelect.value === "price-low") sorted.sort((a, b) => a.price - b.price);
  if (sortSelect.value === "price-high") sorted.sort((a, b) => b.price - a.price);
  if (sortSelect.value === "rating") sorted.sort((a, b) => b.rating - a.rating);
  return sorted;
}

function renderCategories() {
  const categories = ["All", ...new Set(products.map((product) => product.category))];
  categoryFilters.innerHTML = categories
    .map((category) => `<button class="${category === selectedCategory ? "active" : ""}" data-category="${category}">${category}</button>`)
    .join("");

  categoryFilters.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedCategory = button.dataset.category;
      renderProducts();
      renderCategories();
    });
  });
}

function renderProducts() {
  const query = searchInput.value.toLowerCase().trim();
  const filtered = products.filter((product) => {
    const matchesCategory = selectedCategory === "All" || product.category === selectedCategory;
    const matchesSearch = `${product.name} ${product.category} ${product.description} ${product.tag}`.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });

  const list = sortedProducts(filtered);

  if (!list.length) {
    productGrid.innerHTML = `<div class="empty-cart">No products found. Try another search.</div>`;
    return;
  }

  productGrid.innerHTML = list
    .map((product, index) => {
      const isFavorite = favorites.includes(product.id);
      return `
        <article class="product-card ${product.color || ""}" style="animation-delay: ${index * 80}ms">
          <button class="favorite-button ${isFavorite ? "active" : ""}" data-favorite="${product.id}" aria-label="Favorite ${product.name}">${isFavorite ? "♥" : "♡"}</button>
          <span class="product-tag">${product.tag}</span>
          <div class="product-icon">${product.icon}</div>
          <div class="product-meta">
            <span>${product.category}</span>
            <span>⭐ ${product.rating}</span>
          </div>
          <span class="product-badge">${product.badge} · ${discount(product)}% OFF</span>
          <h3>${product.name}</h3>
          <p>${product.description}</p>
          <div class="price-row">
            <div class="price">
              <strong>${money(product.price)}</strong>
              <del>${money(product.old_price)}</del>
            </div>
            <span class="stock">${product.stock} left</span>
          </div>
          <div class="card-actions">
            <button class="add-button" data-id="${product.id}">Add to Cart</button>
            <button class="view-button" data-view="${product.id}" aria-label="Preview ${product.name}">👀</button>
          </div>
        </article>
      `;
    })
    .join("");

  productGrid.querySelectorAll(".add-button").forEach((button) => {
    button.addEventListener("click", () => addToCart(Number(button.dataset.id)));
  });

  productGrid.querySelectorAll(".view-button").forEach((button) => {
    button.addEventListener("click", () => openProductModal(Number(button.dataset.view)));
  });

  productGrid.querySelectorAll(".favorite-button").forEach((button) => {
    button.addEventListener("click", () => toggleFavorite(Number(button.dataset.favorite)));
  });
}

function toggleFavorite(productId) {
  if (favorites.includes(productId)) {
    favorites = favorites.filter((id) => id !== productId);
    showToast("Removed from wishlist");
  } else {
    favorites.push(productId);
    showToast("Added to wishlist ❤️");
  }
  saveFavorites();
  renderProducts();
}

function openProductModal(productId) {
  const product = products.find((item) => item.id === productId);
  if (!product) return;

  modalContent.innerHTML = `
    <div class="modal-product-icon">${product.icon}</div>
    <span class="eyebrow">${product.category} · ${product.tag}</span>
    <h2>${product.name}</h2>
    <p>${product.description}</p>
    <div class="price-row">
      <div class="price">
        <strong>${money(product.price)}</strong>
        <del>${money(product.old_price)}</del>
      </div>
      <span class="stock">Only ${product.stock} left</span>
    </div>
    <div class="modal-actions">
      <button class="primary-cta" data-modal-add="${product.id}">Add to Cart</button>
      <button class="secondary-cta" data-modal-fav="${product.id}">Add Wishlist</button>
    </div>
  `;

  modalContent.querySelector("[data-modal-add]").addEventListener("click", () => {
    addToCart(product.id);
    closeProductModal();
    openCartDrawer();
  });

  modalContent.querySelector("[data-modal-fav]").addEventListener("click", () => toggleFavorite(product.id));

  productModal.classList.add("open");
  productModal.setAttribute("aria-hidden", "false");
  overlay.classList.add("show");
}

function closeProductModal() {
  productModal.classList.remove("open");
  productModal.setAttribute("aria-hidden", "true");
  if (!cartDrawer.classList.contains("open")) overlay.classList.remove("show");
}

function addToCart(productId) {
  const product = products.find((item) => item.id === productId);
  const existing = cart.find((item) => item.id === productId);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ ...product, quantity: 1 });
  }

  saveCart();
  renderCart();
  showToast(`${product.icon} ${product.name} added to GadgetNest bag`);
}

function updateQuantity(productId, change) {
  const item = cart.find((product) => product.id === productId);
  if (!item) return;

  item.quantity += change;
  if (item.quantity <= 0) {
    cart = cart.filter((product) => product.id !== productId);
  }

  saveCart();
  renderCart();
}

function renderCart() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  cartCount.textContent = count;
  cartTotal.textContent = money(total);

  if (!cart.length) {
    cartItems.innerHTML = `<div class="empty-cart">🛒<br>Your GadgetNest bag is empty.<br>Add products to start shopping.</div>`;
    return;
  }

  cartItems.innerHTML = cart
    .map((item) => `
      <div class="cart-item">
        <div class="cart-item-left">
          <div class="cart-item-icon">${item.icon}</div>
          <div>
            <h4>${item.name}</h4>
            <p>${money(item.price)} each</p>
            <div class="quantity-controls">
              <button class="qty-button" data-change="-1" data-id="${item.id}">−</button>
              <strong>${item.quantity}</strong>
              <button class="qty-button" data-change="1" data-id="${item.id}">+</button>
            </div>
          </div>
        </div>
        <strong>${money(item.price * item.quantity)}</strong>
      </div>
    `)
    .join("");

  cartItems.querySelectorAll(".qty-button").forEach((button) => {
    button.addEventListener("click", () => updateQuantity(Number(button.dataset.id), Number(button.dataset.change)));
  });
}

function openCartDrawer() {
  cartDrawer.classList.add("open");
  cartDrawer.setAttribute("aria-hidden", "false");
  overlay.classList.add("show");
}

function closeCartDrawer() {
  cartDrawer.classList.remove("open");
  cartDrawer.setAttribute("aria-hidden", "true");
  if (!productModal.classList.contains("open")) overlay.classList.remove("show");
}

async function checkout() {
  if (!cart.length) {
    showToast("Add at least one product before checkout");
    return;
  }

  checkoutButton.disabled = true;
  checkoutButton.textContent = "Processing...";
  try {
    const response = await fetch("/api/v1/store/checkout", { method: "POST" });
    const data = await response.json();
    showToast(`✅ ${data.message}`);
    cart = [];
    saveCart();
    renderCart();
  } catch (error) {
    showToast("Checkout failed. Make sure the API is running.");
  } finally {
    checkoutButton.disabled = false;
    checkoutButton.textContent = "Checkout Now";
  }
}

function startCountdown() {
  let remaining = 2 * 60 * 60 + 30 * 60;
  const hours = document.getElementById("hours");
  const minutes = document.getElementById("minutes");
  const seconds = document.getElementById("seconds");

  setInterval(() => {
    remaining = remaining <= 0 ? 2 * 60 * 60 + 30 * 60 : remaining - 1;
    const h = Math.floor(remaining / 3600);
    const m = Math.floor((remaining % 3600) / 60);
    const s = remaining % 60;
    hours.textContent = String(h).padStart(2, "0");
    minutes.textContent = String(m).padStart(2, "0");
    seconds.textContent = String(s).padStart(2, "0");
  }, 1000);
}

async function init() {
  try {
    const response = await fetch("/api/v1/store/products");
    const data = await response.json();
    products = data.products;
    renderCategories();
    renderProducts();
    renderCart();
    startCountdown();
  } catch (error) {
    productGrid.innerHTML = `<div class="empty-cart">Could not load products. Check FastAPI server.</div>`;
  }
}

openCart.addEventListener("click", openCartDrawer);
closeCart.addEventListener("click", closeCartDrawer);
closeModal.addEventListener("click", closeProductModal);
overlay.addEventListener("click", () => {
  closeCartDrawer();
  closeProductModal();
});
checkoutButton.addEventListener("click", checkout);
searchInput.addEventListener("input", renderProducts);
sortSelect.addEventListener("change", renderProducts);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeCartDrawer();
    closeProductModal();
  }
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
init();
