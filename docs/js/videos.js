function changeVideo() {
    links.forEach(link => link.classList.remove("videos__link--selected"));
    this.classList.add("videos__link--selected");
    window.location.hash = this.dataset.src;
    video.src = `videos/${this.dataset.src}.mp4#t=0.01`;
}

function setVideoHeight() {
    video.removeAttribute("height");
    video.height = video.getBoundingClientRect().height;
}

// Grab DOM elements
var video = document.getElementById("js-video");
var links = document.querySelectorAll("[data-src]");

// Add event listeners
links.forEach(link => link.addEventListener("click", changeVideo));
video.addEventListener("loadeddata", setVideoHeight);
window.addEventListener("resize", setVideoHeight);

// Select video that is in window hash
var selectedVideo = window.location.hash.substr(1);
links.forEach(link => {
    if (link.dataset.src == selectedVideo) {
        link.click();
        link.scrollIntoView()
    }
})
