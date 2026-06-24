document.addEventListener("DOMContentLoaded", function () {
    const dropdownWrapper = document.querySelector('.category-dropdown');
    const dropdownToggle = document.querySelector('#categoryMenu');
    const dropdownMenu = document.querySelector('.category-dropdown .dropdown-menu'); 
    let timeoutId = null; 
    
    if (dropdownWrapper && dropdownToggle && dropdownMenu) {
        const bsDropdown = new bootstrap.Dropdown(dropdownToggle);

        // 1. Jab Categories par mouse aaye
        dropdownWrapper.addEventListener('mouseenter', function () {
            clearTimeout(timeoutId); 
            bsDropdown.show();
            // Dropdown list par orange border lagao
            dropdownMenu.style.setProperty('border', '2px solid #f57224', 'important');
        });

        // 2. Jab mouse pure area se baahar chale jaye
        dropdownWrapper.addEventListener('mouseleave', function () {
            timeoutId = setTimeout(function() {
                bsDropdown.hide();
                // Menu band hote hi border styling saaf karo taaki CSS handle kare
                dropdownMenu.style.removeProperty('border');
            }, 150);
        });
    }

    // 3. Andar ke items ka hover effect
    const catItems = document.querySelectorAll('.custom-cat-item, .custom-cat-item-all');

    catItems.forEach(function (item) {
        item.addEventListener('mouseenter', function () {
            this.style.setProperty('background-color', '#f57224', 'important');
            this.style.setProperty('color', '#ffffff', 'important');

            // Andar ke saare icons aur small arrow ko ek sath white karo
            const elementsToWhite = this.querySelectorAll('i, .arrow-icon');
            elementsToWhite.forEach(el => el.style.setProperty('color', '#ffffff', 'important'));
        });

        item.addEventListener('mouseleave', function () {
            // Mouse hat-te hi saari inline JS styles hata do, taaki CSS ki original styles wapas lag jayein
            this.style.removeProperty('background-color');
            this.style.removeProperty('color');

            // Icons aur arrows ki styles bhi default par reset karo
            const elementsToReset = this.querySelectorAll('i, .arrow-icon');
            elementsToReset.forEach(el => el.style.removeProperty('color'));
        });
    });
});