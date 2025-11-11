// Shopping Cart JavaScript - localStorage based

// Cart storage functions
function getCart() {
    const cart = localStorage.getItem('shopping_cart');
    return cart ? JSON.parse(cart) : [];
}

function saveCart(cart) {
    localStorage.setItem('shopping_cart', JSON.stringify(cart));
}

// Add item to cart
function addToCart(productId, productName, price) {
    let cart = getCart();
    
    // Check if item already exists
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: parseFloat(price),
            quantity: 1
        });
    }
    
    saveCart(cart);
    updateCartCount();
    
    // Show feedback (like restaurant flash messages)
    alert(`${productName} added to cart!`);
}

// Remove item from cart
function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    updateCartCount();
    displayCart(); // Refresh cart display
}

// Update item quantity
function updateQuantity(productId, newQuantity) {
    let cart = getCart();
    const item = cart.find(item => item.id === productId);
    
    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(productId);
        } else {
            item.quantity = newQuantity;
            saveCart(cart);
            updateCartCount();
            displayCart();
        }
    }
}

// Calculate cart total
function calculateTotal() {
    const cart = getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

// Update cart count in header
function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((count, item) => count + item.quantity, 0);
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = totalItems;
    }
}

// Clear entire cart
function clearCart() {
    localStorage.removeItem('shopping_cart');
    updateCartCount();
    displayCart();
}

// Display cart items (for cart.html page)
function displayCart() {
    const cart = getCart();
    const cartContainer = document.getElementById('cart-items');
    
    if (!cartContainer) return;
    
    if (cart.length === 0) {
        cartContainer.innerHTML = '<p>Your cart is empty</p>';
        return;
    }
    
    let cartHTML = '';
    cart.forEach(item => {
        cartHTML += `
            <div class="cart-item">
                <h4>${item.name}</h4>
                <p>Price: $${item.price.toFixed(2)}</p>
                <p>Quantity: 
                    <button onclick="updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                    ${item.quantity}
                    <button onclick="updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
                </p>
                <p>Subtotal: $${(item.price * item.quantity).toFixed(2)}</p>
                <button onclick="removeFromCart('${item.id}')" class="remove-btn">Remove</button>
            </div>
        `;
    });
    
    cartHTML += `
        <div class="cart-total">
            <h3>Total: $${calculateTotal().toFixed(2)}</h3>
            <button onclick="clearCart()" class="btn">Clear Cart</button>
            <a href="/checkout" class="btn">Checkout</a>
        </div>
    `;
    
    cartContainer.innerHTML = cartHTML;
}

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    displayCart();
});