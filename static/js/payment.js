function resetPaymentCards() {
        const checkedRadios = document.querySelectorAll('.btn-check');
        checkedRadios.forEach(radio => {
            const card = radio.nextElementSibling;
            if (!radio.checked) {
                card.style.borderColor = '#dee2e6';
                card.style.backgroundColor = '#f8f9fa';
            }
        });
    }
    // Initialize correct active background on load
    document.addEventListener("DOMContentLoaded", function() {
        const checkedActive = document.querySelector('.btn-check:checked');
        if(checkedActive) {
            checkedActive.nextElementSibling.style.borderColor = '#f57224';
            checkedActive.nextElementSibling.style.backgroundColor = '#fffaf7';
        }
    });