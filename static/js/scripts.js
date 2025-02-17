//Script for fade animation
$(document).ready(function () {
    // Fade-in effect on page load
    $(".fade-content").css("opacity", "1");

    // Fade-out effect before navigating to another page
    $("a").on("click", function (event) {
        var target = $(this).attr("target");
        if (!target || target === "_self") {  // Ignore new tab links
            event.preventDefault();
            var newLocation = this.href;
            $(".fade-content").css("opacity", "0");
            setTimeout(function () {
                window.location.href = newLocation;
            }, 500); // Adjust delay to match transition duration
        }
    });
});

//Script to allow popovers
document.addEventListener("DOMContentLoaded", function() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, { trigger: "focus" }); // Disappears when clicking elsewhere
    });
});
