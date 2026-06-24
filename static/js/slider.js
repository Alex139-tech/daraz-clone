const slider = document.querySelector("#carouselExample");

const carousel = new bootstrap.Carousel(slider, {
    interval: 2500,
    ride: "carousel",
    pause: false,
    touch: true,
    wrap: true
});

// Hover and puse the carousel
slider.addEventListener("mouseenter", () => {
    carousel.pause();
});

// Mouse remove p
slider.addEventListener("mouseleave", () => {
    carousel.cycle();
});

// Click the image
slider.addEventListener("click", () => {
    console.log("Slider Clicked");
});