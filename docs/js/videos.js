function changeVideo() {
    links.forEach(link => link.classList.remove("videos__link--selected"))
    this.classList.add("videos__link--selected")
    video.src = `videos/${this.dataset.src}.mp4`;
}

function setVideoHeight() {
    video.removeAttribute("height")
    video.height = video.getBoundingClientRect().height
}

var video = document.getElementById("js-video");
var links = document.querySelectorAll("[data-src]");

links.forEach(link => link.addEventListener("click", changeVideo))

video.addEventListener("loadeddata", setVideoHeight)
window.addEventListener("resize", setVideoHeight)
