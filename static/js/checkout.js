document.addEventListener('DOMContentLoaded', function () {
    // Target the safe JSON context injected via Django template tags
    const contextElement = document.getElementById('django-context-data');
    if (!contextElement) {
        console.error("Critical Error: Core Django context bridge data element is missing.");
        return;
    }

    // Parse raw text stream into a structured JavaScript Object
    const checkoutData = JSON.parse(contextElement.textContent);
    const root = document.getElementById('checkout-dynamic-root');
    root.innerHTML = ''; // Wipe out initialization placeholder spinner

    // --- LEFT WORKSPACE BRANCH (Address + Package Node) ---
    const leftCol = document.createElement('div');
    leftCol.className = 'col-lg-8';

    // Build Shipping Address Interface Component
    const addressCard = document.createElement('div');
    addressCard.className = 'card border-0 rounded-0 mb-3 p-3 bg-white';
    
    let addressHTML = `
        <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-dark fw-normal fs-6">Shipping Address</span>
            <a href="#" class="text-info text-decoration-none small fw-medium" style="color: #00add4 !important;">EDIT</a>
        </div>
    `;

    if (checkoutData.hasAddress) {
        addressHTML += `
            <div class="text-dark fw-normal mb-1" style="font-size: 15px;">
                ${checkoutData.shippingAddress.fullName} <span class="ms-4">${checkoutData.shippingAddress.phoneNumber}</span>
            </div>
            <div class="d-flex align-items-center gap-2 mt-2">
                <span class="badge bg-danger rounded-pill px-2 text-uppercase xtra-small">${checkoutData.shippingAddress.addressType}</span>
                <span class="text-secondary" style="font-size: 14px;">${checkoutData.shippingAddress.addressDetails}</span>
            </div>
            ${checkoutData.shippingAddress.landmark ? `<div class="text-muted xtra-small ps-2 mt-1">${checkoutData.shippingAddress.landmark}</div>` : ''}
        `;
    } else {
        addressHTML += `<p class="text-muted small">No active shipping address found. Please add an address to continue.</p>`;
    }

    // Append collection hub alert box snippet matching layout image
    addressHTML += `
        <div class="border rounded p-2 mt-3 d-flex justify-content-between align-items-center xtra-small" style="border: 1px dashed #00add4 !important; background-color: #fbfeff; color: #00add4;">
            <div>
                Collect your parcels from a nearby location at a minimal delivery fee. <i class="bi bi-chevron-right ms-1"></i>
                <div class="text-muted mt-1">5 suggested collection point(s) nearby <i class="bi bi-question-circle-fill text-secondary"></i></div>
            </div>
        </div>
    `;
    addressCard.innerHTML = addressHTML;
    leftCol.appendChild(addressCard);

    // Build Package Delivery Group Component
    const packageCard = document.createElement('div');
    packageCard.className = 'card border-0 rounded-0 p-3 bg-white';
    
    let packageHTML = `
        <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
            <span class="fw-medium text-dark" style="font-size: 15px;">Package 1 of 1</span>
            <span class="text-muted xtra-small">Shipped by <strong class="text-dark">Fast Dropup</strong></span>
        </div>
        <div class="text-secondary xtra-small mb-2">Delivery or Pickup</div>
        
        <div class="border p-3 mb-4 bg-white position-relative" style="max-width: 320px; border-color: #00add4 !important; border-radius: 4px;">
            <div class="d-flex align-items-center gap-2">
                <i class="bi bi-check-circle-fill" style="color: #00add4; font-size: 16px;"></i>
                <span class="fw-medium text-dark">Rs. ${checkoutData.deliveryFee}</span>
            </div>
            <div class="ps-4 text-dark xtra-small fw-normal mt-1">Standard Delivery</div>
            <div class="ps-4 text-muted xtra-small mt-2">Guaranteed by 30 Jun-2 Jul</div>
        </div>
    `;

    // Process all loop items mapped onto custom dataset structure
    checkoutData.items.forEach(item => {
        let imageTag = item.imageUrl 
            ? `<img src="${item.imageUrl}" alt="product_img" class="img-fluid" style="width: 80px; height: 80px; object-fit: cover;">`
            : `<div class="bg-light text-center d-flex align-items-center justify-content-center" style="width: 80px; height: 80px;"><i class="bi bi-image text-muted fs-3"></i></div>`;

        packageHTML += `
            <div class="d-flex justify-content-between align-items-start py-3 border-bottom" style="border-color: #f1f1f1 !important;">
                <div class="d-flex align-items-start gap-3">
                    ${imageTag}
                    <div>
                        <h6 class="mb-1 text-dark fw-normal" style="font-size: 14px; max-width: 450px; line-height: 1.4;">${item.title}</h6>
                        <span class="text-muted xtra-small d-block mt-1">No Brand, Color Family: Default</span>
                    </div>
                </div>
                <div class="text-end">
                    <span class="fw-medium" style="color: #f57224; font-size: 16px;">Rs. ${item.price}</span>
                    <div class="text-muted text-decoration-line-through xtra-small mt-1">Rs. ${(item.price * 1.5).toFixed(0)}</div>
                    <div class="text-dark xtra-small mt-2">Qty: <strong class="fw-normal">${item.quantity}</strong></div>
                </div>
            </div>
        `;
    });

    packageCard.innerHTML = packageHTML;
    leftCol.appendChild(packageCard);
    root.appendChild(leftCol);


    // --- RIGHT WORKSPACE BRANCH (Order Summary Panel) ---
    const rightCol = document.createElement('div');
    rightCol.className = 'col-lg-4';

    // Build Coupon/Promotion Input Block Component
    const promoCard = document.createElement('div');
    promoCard.className = 'card border-0 rounded-0 mb-3 p-3 bg-white';
    promoCard.innerHTML = `
        <label class="text-dark fw-normal mb-2" style="font-size: 15px;">Promotion</label>
        <div class="input-group gap-2">
            <input type="text" class="form-control rounded-0" placeholder="Enter Store/Daraz Code" style="font-size: 13px; border: 1px solid #ddd;">
            <button class="btn btn-info text-white px-4 fw-normal rounded-0" type="button" style="background-color: #19b4c7; border: none; font-size: 13px;">APPLY</button>
        </div>
    `;
    rightCol.appendChild(promoCard);

    // Build Dynamic Financial Totals Statement Summary Component
    const summaryCard = document.createElement('div');
    summaryCard.className = 'card border-0 rounded-0 p-3 bg-white';
    summaryCard.innerHTML = `
        <div class="text-dark mb-3" style="font-size: 15px;">Invoice and Contact Info <a href="#" class="float-end text-info text-decoration-none small fw-medium" style="color: #00add4 !important; font-size: 13px;">Edit</a></div>
        <h6 class="fw-normal text-dark mb-3" style="font-size: 15px;">Order Detail</h6>
        
        <div class="d-flex justify-content-between mb-2 text-secondary" style="font-size: 13px;">
            <span>Items Total (${checkoutData.items.length} Items)</span>
            <span class="text-dark fw-medium">Rs. ${checkoutData.itemsTotal}</span>
        </div>
        <div class="d-flex justify-content-between mb-3 text-secondary" style="font-size: 13px;">
            <span>Delivery Fee</span>
            <span class="text-dark fw-medium">Rs. ${checkoutData.deliveryFee}</span>
        </div>
        <hr class="text-muted my-2">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <span class="text-dark" style="font-size: 14px;">Total:</span>
            <div class="text-end">
                <span class="fw-medium fs-4" style="color: #f57224;">Rs. ${checkoutData.finalTotal}</span>
                <div class="text-muted xtra-small">All taxes included</div>
            </div>
        </div>
        <button id="checkout-pay-trigger" class="btn w-100 text-white fw-normal py-2 rounded-0 btn-lg" style="background-color: #f57224; border: none; font-size: 15px;">
            Proceed to Pay
        </button>
    `;
    rightCol.appendChild(summaryCard);
    root.appendChild(rightCol);

    // Attach click events to the secure transaction checkout trigger button
    document.getElementById('checkout-pay-trigger').addEventListener('click', function () {
        alert('Proceeding to payment gateway for amount: Rs. ' + checkoutData.finalTotal);
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function(alert){

        setTimeout(function(){

            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();

        },3000);

    });

});