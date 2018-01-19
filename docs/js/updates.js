function populateReleases(container, url) {
    if (!container || !url)
        return;

    // Used to actually populate the HTML into the dom
    function populateDom(releases) {
        container.innerHTML = `
            <h1>Project Releases</h1>
            <p>All release data pulled from the project's <a href="https://github.com/petetetete/CrossDoc">GitHub Page</a>. Additional release data available on the <a href="https://pypi.org/project/cross-doc/">PyPi project page</a>.</p>
            <ul>
                ${releases.map(tag => 
                    `<li><b>v${tag.name}</b> <i>(commit ${tag.commit.sha.substring(0, 6)})</i>${tag.message ? " - " + tag.message : ""}</li>`
                    ).join("")}
            </ul>`
    }

    // If we've already made this request recently
    var EXPIRATION_TIME = 3600000;
    var releases = localStorage["releases"];
    if (releases) {
        releases = JSON.parse(releases);

        if (new Date().getTime() - releases.date < EXPIRATION_TIME) {
            populateDom(releases.data);
            return;
        }
    }

    // Else get data from GitHub
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = function() {

        if (xhr.status != 200) {
            container.innerHTML = "<span class='error-text'>Error loading releases, view them all <a href='https://github.com/petetetete/CrossDoc/releases'>here</a></span>";
            return;
        }

        localStorage["releases"] = `{"date":"${new Date().getTime()}","data":${xhr.responseText}}`;
        populateDom(JSON.parse(xhr.responseText));
    };

    xhr.send();
}

// "Main" scope

var url = "https://api.github.com/repos/petetetete/CrossDoc/tags";

populateReleases(document.getElementById("js-releases"), url);
