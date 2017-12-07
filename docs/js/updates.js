function populateReleases(container, url) {
    if (!container || !url)
        return;

    // Used to actually populate the HTML into the dom
    function populateDom(releases) {
        container.innerHTML = releases.map(tag => 
            `<li><b>v${tag.name}</b> <i>(commit ${tag.commit.sha.substring(0, 6)})</i>${tag.message ? " - " + tag.message : ""}</li>`
            ).join("");
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

function populateUpdates(container, posts) {
    if (!container || !posts)
        return;

    var out = "";
    for (var i = 0; i < posts.length; i += 2) {
        out += `
            <div class="row">
                <div class="col">
                    <div class='post'>
                        <div class='post__head'>
                            <div class='post__title'>${posts[i].title}</div>
                            <div class='post__info'>${posts[i].date}</div>
                        </div>
                        <div class='post__body'>${posts[i].body}</div>
                    </div>
                </div>`;

        if (i + 1 < posts.length) {
            out += `
                <div class="col">
                    <div class='post'>
                        <div class='post__head'>
                            <div class='post__title'>${posts[i + 1].title}</div>
                            <div class='post__info'>${posts[i + 1].date}</div>
                        </div>
                        <div class='post__body'>${posts[i + 1].body}</div>
                    </div>
                </div>`;
        }

        out += "</div>";
    }

    container.innerHTML = out;
}


// "Main" scope

// Try to keep posts a similar length
var posts = [{
        title: "Requirements v1 Completed",
        date: "11/23/17",
        body: "We completed the final edits of our Requirements Document rough draft (<a href='deliverables/Requirements Specification v1.pdf'>available here</a>) and turned it in to Dr. Palmer. Requirements drafting will continue until we finalize a working specification."
    }, {
        title: "First Design Review Presentation",
        date: "11/21/17",
        body: "Today we finalized our <a href='deliverables/Design Review 1.pdf'>design review slides</a> and completed our first design review presentation. We received valuable feedback regarding our content and delivery that we will apply to our future presentations."
    }, {
        title: "Feasibility Analysis Completed",
        date: "10/26/17",
        body: "After analyzing potential risks to our product, and proving feasibility of our implementation, we created our <a href='deliverables/Technological Feasibility Analysis.pdf'>Technological Feasilibity Analysis</a> paper addressing this. We plan to further address these risks before our prototype demo."
    }];
var url = "https://api.github.com/repos/petetetete/CrossDoc/tags";

populateUpdates(document.getElementById("js-updates"), posts);
populateReleases(document.getElementById("js-releases"), url);
