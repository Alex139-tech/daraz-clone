// Separate JS File: flash_sale_timer.js

document.addEventListener("DOMContentLoaded", function () {
    const timerContainer = document.getElementById('flash-sale-timer');
    const hoursEl = document.getElementById('timer-hours');
    const minutesEl = document.getElementById('timer-minutes');
    const secondsEl = document.getElementById('timer-seconds');

    // Agar HTML elements page par hain, tabhi run karein (error se bachne ke liye)
    if (timerContainer && hoursEl && minutesEl && secondsEl) {
        
        // Target Time: Aaj raat ke 11:59:59 PM tak ka automatic timer
        const targetDate = new Date();
        targetDate.setHours(23, 59, 59, 0);

        function updateTimer() {
            const now = new Date().getTime();
            const difference = targetDate.getTime() - now;

            // Agar sale khatam ho jaye
            if (difference <= 0) {
                timerContainer.innerHTML = "<span class='text-danger fw-bold'>Sale Ended!</span>";
                clearInterval(timerInterval);
                return;
            }

            // Time calculate karna
            const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((difference % (1000 * 60)) / 1000);

            // Double digits me HTML me display karna (e.g. 05)
            hoursEl.innerText = hours < 10 ? '0' + hours : hours;
            minutesEl.innerText = minutes < 10 ? '0' + minutes : minutes;
            secondsEl.innerText = seconds < 10 ? '0' + seconds : seconds;
        }

        // Har 1 second me update hoga
        updateTimer();
        const timerInterval = setInterval(updateTimer, 1000);
    }
});