document.addEventListener("DOMContentLoaded", function () {

    const carouselElement =
        document.querySelector("#carouselExample");

    if (carouselElement) {

        const carousel =
            new bootstrap.Carousel(
                carouselElement,
                {
                    interval: 3000,
                    ride: "carousel",
                    pause: false,
                    wrap: true
                }
            );

        carouselElement.addEventListener(
            "mouseenter",
            function () {
                carousel.pause();
            }
        );

        carouselElement.addEventListener(
            "mouseleave",
            function () {
                carousel.cycle();
            }
        );
    }

});