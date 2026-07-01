document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // ELEMENTS
    // ==========================
    const selectAll = document.getElementById("selectAll");
    const itemCheckboxes = document.querySelectorAll(".item-checkbox");
    const cartItems = document.querySelectorAll(".cart-item");
    const subtotalElement = document.getElementById("subtotal-val");
    const shippingElement = document.getElementById("shipping-val");
    const totalElement = document.getElementById("grand-total-val");
    const totalItemsElement = document.getElementById("total-items");
    const checkoutCount = document.getElementById("checkout-count");
    const selectedCount = document.getElementById("selected-count-header");
    const navbarCounter = document.getElementById("navbar-cart-count");

    // HTML से सीधे शिपिंग चार्ज उठाएं (डिफ़ॉल्ट 200)
    const DB_SHIPPING = shippingElement ? parseFloat(shippingElement.innerText) : 200;
    let discount = 0;

    // ==========================
    // DARAZ STYLE CALCULATE CART
    // ==========================
    function calculateCart() {
        let subtotal = 0;
        let quantity = 0;
        let selectedProducts = 0;

        cartItems.forEach(function (item) {
            const checkbox = item.querySelector(".item-checkbox");

            // Daraz Behavior: जो चेक नहीं है, उसे छोड़ दो
            if (!checkbox || !checkbox.checked) return;

            const price = parseFloat(item.dataset.price) || 0;
            const qtyInput = item.querySelector(".quantity");
            const qty = qtyInput ? parseInt(qtyInput.value) : 1;

            subtotal += price * qty;
            quantity += qty;
            selectedProducts++;
        });

        // वैल्यूज अपडेट करें
        if (subtotalElement) subtotalElement.innerText = subtotal.toFixed(2);
        if (totalItemsElement) totalItemsElement.innerText = quantity;
        if (checkoutCount) checkoutCount.innerText = quantity;
        if (selectedCount) selectedCount.innerText = selectedProducts;

        // अगर कोई प्रोडक्ट चुना है तभी शिपिंग जोड़ें, वरना 0
        const shipping = selectedProducts > 0 ? DB_SHIPPING : 0;
        if (shippingElement) shippingElement.innerText = shipping.toFixed(2);

        // फाइनल ग्रैंड टोटल
        const grandTotal = subtotal + shipping - discount;
        if (totalElement) totalElement.innerText = grandTotal.toFixed(2);

        // नेवबार काउंटर अपडेट
        if (navbarCounter && checkoutCount) {
            navbarCounter.innerText = checkoutCount.innerText;
        }
    }

    // ==========================
    // SELECT ALL
    // ==========================
    if (selectAll) {
        selectAll.addEventListener("change", function () {
            itemCheckboxes.forEach(function (checkbox) {
                checkbox.checked = selectAll.checked;
            });
            calculateCart();
        });
    }

    // ==========================
    // SINGLE CHECKBOX
    // ==========================
    itemCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const allChecked = [...itemCheckboxes].every(cb => cb.checked);
            if (selectAll) selectAll.checked = allChecked;
            calculateCart();
        });
    });

    // ==========================================
    // QUANTITY CHANGED EVENT (FOR DIRECT INPUT TYPING)
    // ==========================================
    const quantityInputs = document.querySelectorAll(".quantity");
    quantityInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            if (parseInt(input.value) < 1 || input.value === "" || isNaN(input.value)) {
                input.value = 1; // 1 से कम न होने दें
            }
            calculateCart(); // तुरंत टोटल अपडेट करें
        });
    });

    // ==========================================
    // PLUS BUTTON (AJAX NO-RELOAD)
    // ==========================================
    const plusButtons = document.querySelectorAll(".btn-plus");
    plusButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // पेज रीलोड होने से रोकेगा
            
            const url = button.getAttribute("data-url"); // HTML से URL उठाएं
            const cartItem = button.closest(".cart-item");
            const quantityInput = cartItem ? cartItem.querySelector(".quantity") : null;

            if (url && quantityInput) {
                // बैकएंड को चुपके से रिक्वेस्ट भेजें
                fetch(url, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        quantityInput.value = data.quantity; // डेटाबेस वाली लाइव क्वांटिटी सेट करें
                        calculateCart(); // बिना रीलोड टोटल अपडेट करें
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    });

    // ==========================================
    // MINUS BUTTON (AJAX NO-RELOAD)
    // ==========================================
    const minusButtons = document.querySelectorAll(".btn-minus");
    minusButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // पेज रीलोड होने से रोकेगा
            
            const url = button.getAttribute("data-url"); // HTML से URL उठाएं
            const cartItem = button.closest(".cart-item");
            const quantityInput = cartItem ? cartItem.querySelector(".quantity") : null;

            if (url && quantityInput) {
                // बैकएंड को चुपके से रिक्वेस्ट भेजें
                fetch(url, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        quantityInput.value = data.quantity; // डेटाबेस वाली लाइव क्वांटिटी सेट करें
                        calculateCart(); // बिना रीलोड टोटल अपडेट करें
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    });

    // ==========================================
    // DELETE SELECTED
    // ==========================================
    const deleteSelectedBtn = document.getElementById("deleteSelected");
    if (deleteSelectedBtn) {
        deleteSelectedBtn.addEventListener("click", function () {
            const checkedItems = document.querySelectorAll(".item-checkbox:checked");
            if (checkedItems.length === 0) {
                alert("Please select at least one product.");
                return;
            }
            if (!confirm("Remove selected products?")) return;

            checkedItems.forEach(function (checkbox) {
                const cartItem = checkbox.closest(".cart-item");
                const deleteLink = cartItem ? cartItem.querySelector(".remove-item-btn") : null;
                if (deleteLink) {
                    window.location.href = deleteLink.href;
                }
            });
        });
    }

    // ==========================================
    // REMOVE BUTTON CONFIRM
    // ==========================================
    const removeButtons = document.querySelectorAll(".remove-item-btn");
    removeButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            if (!confirm("Remove this product from cart?")) {
                event.preventDefault();
            }
        });
    });

    // ==========================================
    // VOUCHER SYSTEM
    // ==========================================
    const voucherButton = document.getElementById("applyVoucher");
    const voucherInput = document.getElementById("voucherCode");
    const discountRow = document.getElementById("discount-row");
    const discountValue = document.getElementById("discount-val");

    if (voucherButton && voucherInput) {
        voucherButton.addEventListener("click", function () {
            const code = voucherInput.value.trim().toUpperCase();

            if (code === "") {
                alert("Enter voucher code.");
                return;
            }

            if (code === "DARAZ100") {
                discount = 100;
            } else if (code === "SAVE200") {
                discount = 200;
            } else {
                discount = 0;
                alert("Invalid voucher.");
                if (discountRow) discountRow.classList.add("d-none");
                calculateCart();
                return;
            }

            if (discountValue) discountValue.innerText = discount.toFixed(2);
            if (discountRow) discountRow.classList.remove("d-none");

            calculateCart();
        });
    }

    // =====================================
    // INITIALIZATION (Daraz Style)
    // =====================================
    if (cartItems.length === 0 && selectAll) {
        selectAll.disabled = true;
    }

    // लोड होते ही सारे चेकबॉक्स को Uncheck रखें
    if (selectAll) selectAll.checked = false;
    itemCheckboxes.forEach(cb => cb.checked = false);

    calculateCart();
});