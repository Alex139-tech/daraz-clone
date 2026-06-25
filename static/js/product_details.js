document.addEventListener("DOMContentLoaded", function () {
    // --- 1. Category Dropdown Hover System ---
    const dropdownWrapper = document.querySelector('.category-dropdown');
    const dropdownToggle = document.querySelector('#categoryMenu');
    const dropdownMenu = document.querySelector('.category-dropdown .dropdown-menu'); 
    let timeoutId = null; 
    
    if (dropdownWrapper && dropdownToggle && dropdownMenu) {
        const bsDropdown = new bootstrap.Dropdown(dropdownToggle);

        // Open dropdown on hover and add active border
        dropdownWrapper.addEventListener('mouseenter', function () {
            clearTimeout(timeoutId); 
            bsDropdown.show();
            dropdownMenu.style.setProperty('border', '2px solid #f57224', 'important');
        });

        // Close dropdown after a short delay when mouse leaves the wrapper
        dropdownWrapper.addEventListener('mouseleave', function () {
            timeoutId = setTimeout(function() {
                bsDropdown.hide();
                dropdownMenu.style.removeProperty('border');
            }, 150);
        });
    }

    // --- 2. Category Dropdown Items Hover Effects ---
    const catItems = document.querySelectorAll('.custom-cat-item, .custom-cat-item-all');

    catItems.forEach(function (item) {
        // Highlight active item and its nested icons on hover
        item.addEventListener('mouseenter', function () {
            this.style.setProperty('background-color', '#f57224', 'important');
            this.style.setProperty('color', '#ffffff', 'important');

            const elementsToWhite = this.querySelectorAll('i, .arrow-icon');
            elementsToWhite.forEach(el => el.style.setProperty('color', '#ffffff', 'important'));
        });

        // Revert to original CSS rules when mouse leaves
        item.addEventListener('mouseleave', function () {
            this.style.removeProperty('background-color');
            this.style.removeProperty('color');

            const elementsToReset = this.querySelectorAll('i, .arrow-icon');
            elementsToReset.forEach(el => el.style.removeProperty('color'));
        });
    });

    // --- 3. Dynamic Product Quantity Selector Engine ---
    const qtyInput = document.getElementById('qtyInput');
    const plusBtn = document.getElementById('plusBtn');
    const minusBtn = document.getElementById('minusBtn');

    // Safe check to ensure controls exist on the active layout
    if (qtyInput && plusBtn && minusBtn) {
        // Increment quantity step
        plusBtn.addEventListener('click', () => {
            qtyInput.value = parseInt(qtyInput.value) + 1;
        });

        // Decrement quantity step safely (Minimum limit of 1 item)
        minusBtn.addEventListener('click', () => {
            if (parseInt(qtyInput.value) > 1) {
                qtyInput.value = parseInt(qtyInput.value) - 1;
            }
        });
    }
});