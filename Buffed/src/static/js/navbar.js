const navbarContainer = $("#navbar-items");

$(document).ready(function() {
    resize();
});

$(window).on("resize", function() {
    resize();
});

function resize() {
    if ($(window).width() < 992) {
        navbarContainer.removeClass("sticky-top");
    } else if (!navbarContainer.hasClass("sticky-top")) {
        navbarContainer.addClass("sticky-top");
    }
}