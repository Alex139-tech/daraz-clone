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

    const SHIPPING = 390;



    // ==========================
    // CALCULATE CART
    // ==========================

    function calculateCart() {

        let subtotal = 0;

        let quantity = 0;

        let selectedProducts = 0;



        cartItems.forEach(function (item) {

            const checkbox = item.querySelector(".item-checkbox");



            if (!checkbox.checked) return;



            const price = parseFloat(item.dataset.price);

            const qty = parseInt(

                item.querySelector(".quantity").value

            );



            subtotal += price * qty;

            quantity += qty;

            selectedProducts++;

        });



        subtotalElement.innerText = subtotal.toFixed(2);



        totalItemsElement.innerText = quantity;

        checkoutCount.innerText = quantity;

        selectedCount.innerText = selectedProducts;



        const shipping =

            selectedProducts > 0

                ? SHIPPING

                : 0;



        shippingElement.innerText = shipping.toFixed(2);



        totalElement.innerText =

            (subtotal + shipping).toFixed(2);

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

            const allChecked =

                [...itemCheckboxes].every(

                    cb => cb.checked

                );



            selectAll.checked = allChecked;



            calculateCart();

        });

    });



    // ==========================
    // INITIAL LOAD
    // ==========================

    calculateCart();

});
// ==========================================
// DELETE SELECTED
// ==========================================

const deleteSelectedBtn = document.getElementById("deleteSelected");

if (deleteSelectedBtn) {

    deleteSelectedBtn.addEventListener("click", function () {

        const checkedItems = document.querySelectorAll(
            ".item-checkbox:checked"
        );

        if (checkedItems.length === 0) {

            alert("Please select at least one product.");

            return;
        }

        if (!confirm("Remove selected products?")) {

            return;
        }

        checkedItems.forEach(function (checkbox) {

            const cartItem = checkbox.closest(".cart-item");

            const deleteLink = cartItem.querySelector(".remove-item-btn");

            if (deleteLink) {

                window.location.href = deleteLink.href;

            }

        });

    });

}



// ==========================================
// PREVENT QUANTITY BELOW 1
// ==========================================

const minusButtons = document.querySelectorAll(".btn-minus");

minusButtons.forEach(function (button) {

    button.addEventListener("click", function (event) {

        const quantityInput = button
            .querySelector(".quantity");

        const quantity = parseInt(quantityInput.value);

        if (quantity <= 1) {

            event.preventDefault();

            alert("Minimum quantity is 1.");

        }

    });

});



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
// VOUCHER
// ==========================================

const voucherButton = document.getElementById("applyVoucher");

const voucherInput = document.getElementById("voucherCode");

const discountRow = document.getElementById("discount-row");

const discountValue = document.getElementById("discount-val");

let discount = 0;



if (voucherButton) {

    voucherButton.addEventListener("click", function () {

        const code = voucherInput.value.trim().toUpperCase();



        if (code === "") {

            alert("Enter voucher code.");

            return;

        }



        if (code === "DARAZ100") {

            discount = 100;

        }

        else if (code === "SAVE200") {

            discount = 200;

        }

        else {

            discount = 0;

            alert("Invalid voucher.");

            discountRow.classList.add("d-none");

            calculateCart();

            return;

        }



        discountValue.innerText = discount.toFixed(2);

        discountRow.classList.remove("d-none");



        calculateCart();

    });

}

// =====================================
// SAVE CHECKBOX STATE
// =====================================

itemCheckboxes.forEach(function (checkbox, index) {

    const saved = localStorage.getItem("cart-check-" + index);

    if (saved !== null) {

        checkbox.checked = saved === "true";

    }

    checkbox.addEventListener("change", function () {

        localStorage.setItem(
            "cart-check-" + index,
            checkbox.checked
        );

        calculateCart();

    });

});

// =====================================
// NAVBAR COUNT
// =====================================

const navbarCounter = document.getElementById(
    "navbar-cart-count"
);

function updateNavbarCount(){

    if(navbarCounter){

        navbarCounter.innerText =
            checkoutCount.innerText;

    }

}

updateNavbarCount();

totalElement.innerText = grandTotal.toFixed(2);

updateNavbarCount();

// =====================================
// AUTO HIDE MESSAGE
// =====================================

const alerts = document.querySelectorAll(".alert");

alerts.forEach(function(alert){

    setTimeout(function(){

        alert.classList.remove("show");

        setTimeout(function(){

            alert.remove();

        },300);

    },3000);

});

// =====================================
// EMPTY CART
// =====================================

if(cartItems.length===0){

    if(selectAll){

        selectAll.disabled=true;

    }

}