function scrollToTop(duration) {

    // easeOutQuad
    function timeFunction(t) {
        return t * (2 - t);
    }

    var start = window.pageYOffset;
    var startTime = "now" in window.performance ? performance.now() : new Date().getTime();

    var documentHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);
    var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.getElementsByTagName("body")[0].clientHeight;
    var destinationOffsetToScroll = Math.round(documentHeight < windowHeight ? documentHeight - windowHeight : 0);

    if ("requestAnimationFrame" in window === false) {
        window.scroll(0, destinationOffsetToScroll);
        return;
    }

    function scroll() {
        var now = "now" in window.performance ? performance.now() : new Date().getTime();
        var time = Math.min(1, ((now - startTime) / duration));
        window.scroll(0, Math.ceil((timeFunction(time) * (destinationOffsetToScroll - start)) + start));

        if (window.pageYOffset === destinationOffsetToScroll) {
            return;
        }

        requestAnimationFrame(scroll);
    }

    scroll();
}

function updateBackToTop() {
    if (window.pageYOffset > 300) {
        backToTop.classList.add("visible");
    } else {
        backToTop.classList.remove("visible");
    }
}

var backToTop = document.getElementById("js-backToTop");

window.addEventListener("scroll", updateBackToTop);
backToTop.addEventListener("click", function() { scrollToTop(400) });
