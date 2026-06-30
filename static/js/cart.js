document.addEventListener("DOMContentLoaded", function () {

    // Remove confirmation
    const removeButtons = document.querySelectorAll(".remove-item-btn");

    removeButtons.forEach(button => {
        button.addEventListener("click", function (event) {

            if (!confirm("Are you sure you want to remove this product from your cart?")) {
                event.preventDefault();
            }

        });
    });

    // Auto hide Django messages after 3 seconds
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function(alert){

        setTimeout(function(){

            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();

        },4000);

    });

});