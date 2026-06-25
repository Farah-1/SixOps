HOME_HTML = r"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>GadgetNest Store</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/static/style.css" />
      </head>
      <body>
        <div class="page-glow glow-one"></div>
        <div class="page-glow glow-two"></div>
        <div class="page-glow glow-three"></div>

        <div class="promo-strip">
          <div class="promo-track">
            <span>⚡ FLASH DEALS LIVE</span>
            <span>🚚 Free delivery over $250</span>
            <span>🛍️ New arrivals every week</span>
            <span>💳 Secure checkout</span>
            <span>⭐ Best gadget picks</span>
            <span>⚡ FLASH DEALS LIVE</span>
            <span>🚚 Free delivery over $250</span>
            <span>⭐ Best gadget picks</span>
          </div>
        </div>

        <header class="navbar">
          <a class="brand" href="#top" aria-label="GadgetNest home">
            <span class="brand-logo">GN</span>
            <span>
              <strong>GadgetNest</strong>
              <small>Tech Gadgets Store</small>
            </span>
          </a>
          <nav>
            <a href="#products">Products</a>
            <a href="#deals">Deals</a>
            <a href="#why">Why GadgetNest</a>
          </nav>
          <button class="cart-button" id="openCart" aria-label="Open cart">
            🛒 Cart <span id="cartCount">0</span>
          </button>
        </header>

        <main id="top">
          <section class="hero reveal">
            <div class="hero-copy">
              <span class="eyebrow">Electronics & smart accessories</span>
              <h1>Your favorite gadgets, delivered with a clean premium store experience.</h1>
              <p>
                Shop laptops, headphones, smart watches, desk accessories, and smart home devices
                with a calm modern interface, clear deals, wishlist, cart, and quick checkout.
              </p>
              <div class="hero-actions">
                <a href="#products" class="primary-cta">Start Shopping</a>
                <a href="#deals" class="secondary-cta">View Hot Deals</a>
              </div>
              <div class="trust-row">
                <span>🚚 Fast delivery</span>
                <span>💳 Secure checkout</span>
                <span>🎁 Flash deals</span>
                <span>⭐ Customer favorites</span>
              </div>
            </div>

            <div class="hero-card store-showcase" aria-label="Featured shopping preview">
              <div class="showcase-top">
                <span class="live-dot"></span>
                New season picks
              </div>

              <div class="featured-device">
                <div class="device-art">🎧</div>
                <div>
                  <span class="product-badge">Noise Canceling · 32% OFF</span>
                  <h3>Pulse Wireless Headphones</h3>
                  <p>Premium sound for study, work, and travel.</p>
                  <strong>$150</strong>
                </div>
              </div>

              <div class="showcase-list">
                <div><span>💻</span><strong>NovaBook Pro 14</strong><small>Top rated laptop</small></div>
                <div><span>⌚</span><strong>FitPulse Watch</strong><small>Smart everyday wear</small></div>
                <div><span>🖥️</span><strong>PixelView 4K</strong><small>Flash sale display</small></div>
              </div>

              <div class="mini-metrics">
                <div><strong>Free</strong><small>Delivery</small></div>
                <div><strong>4.9</strong><small>Rating</small></div>
                <div><strong>35%</strong><small>Sale</small></div>
              </div>

              <div class="floating-sale">SAVE<br><strong>35%</strong></div>
              <div class="floating-bubble bubble-one">Best Seller</div>
              <div class="floating-bubble bubble-two">Low Stock</div>
            </div>
          </section>

          <section class="stats reveal" id="why">
            <article>
              <span>🚚</span>
              <strong>Fast Delivery</strong>
              <p>Clean shopping experience like a real e-commerce app.</p>
            </article>
            <article>
              <span>🎁</span>
              <strong>Flash Offers</strong>
              <p>Catchy badges, discounts, product tags, and lively sections.</p>
            </article>
            <article>
              <span>🔐</span>
              <strong>Secure Checkout</strong>
              <p>A simple checkout flow that makes the app feel like a real store.</p>
            </article>
            <article>
              <span>💎</span>
              <strong>Premium Look</strong>
              <p>Modern cards, hover effects, wishlist, preview modal, and cart drawer.</p>
            </article>
          </section>

          <section class="deal-banner reveal" id="deals">
            <div>
              <span class="eyebrow">Limited time</span>
              <h2>Midnight Gadget Sale</h2>
              <p>Catch limited gadget deals with a live countdown and animated offer card.</p>
            </div>
            <div class="countdown" aria-label="Countdown timer">
              <div><strong id="hours">02</strong><span>Hours</span></div>
              <div><strong id="minutes">30</strong><span>Minutes</span></div>
              <div><strong id="seconds">00</strong><span>Seconds</span></div>
            </div>
          </section>

          <section class="section-head reveal" id="products">
            <span class="eyebrow">Featured products</span>
            <h2>Shop modern tech gadgets</h2>
            <p>Search, filter, preview, favorite, add to cart, and checkout in a clean real-store layout.</p>
          </section>

          <section class="store-toolbar reveal">
            <label class="search-box">
              🔎
              <input id="searchInput" type="search" placeholder="Search products..." />
            </label>
            <div class="sort-box">
              <span>Sort</span>
              <select id="sortSelect" aria-label="Sort products">
                <option value="featured">Featured</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="rating">Top Rated</option>
              </select>
            </div>
            <div class="filter-pills" id="categoryFilters"></div>
          </section>

          <section class="product-grid" id="productGrid" aria-live="polite"></section>
        </main>

        <aside class="cart-drawer" id="cartDrawer" aria-hidden="true">
          <div class="cart-header">
            <div>
              <span class="eyebrow">Your cart</span>
              <h3>GadgetNest bag</h3>
            </div>
            <button id="closeCart" class="icon-button" aria-label="Close cart">×</button>
          </div>
          <div class="cart-items" id="cartItems"></div>
          <div class="cart-footer">
            <div class="cart-total"><span>Total</span><strong id="cartTotal">$0</strong></div>
            <button class="checkout-button" id="checkoutButton">Checkout Now</button>
          </div>
        </aside>

        <div class="modal" id="productModal" aria-hidden="true">
          <div class="modal-card">
            <button class="icon-button modal-close" id="closeModal" aria-label="Close preview">×</button>
            <div id="modalContent"></div>
          </div>
        </div>

        <div class="overlay" id="overlay"></div>
        <div class="toast" id="toast"></div>
        <script src="/static/script.js"></script>
      </body>
    </html>
"""
