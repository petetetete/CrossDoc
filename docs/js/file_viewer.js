var fileContainer = document.getElementById("js-files");
var files = [
    {
        title: "Requirements Specification",
        versions: ["Requirements Specification v1"]
    },
    {
        title: "Team Inventory",
        versions: ["Team Inventory"]
    },
    {
        title: "Technological Feasibility Analysis",
        versions: ["Technological Feasibility Analysis"]
    }
]

if (fileContainer) {

    files.forEach((f, i) => {

        // Construct the elements in javascript to encapsulate opening logic
        var file = document.createElement("div");
        file.className = "file";

        var head = document.createElement("div");
        head.className = "file__head";

        var info = document.createElement("div");
        info.className = "file__info";

        var title = document.createElement("h2");
        title.className = "file__title";
        title.innerText = f.title;

        var versions = document.createElement("div");
        versions.className = "file__versions";
        versions.innerHTML = f.versions.map((v, i) => 
            "<a href='deliverables/" + v + ".pdf' title='View version'>v" + (i + 1) + "</a>");

        var viewButton = document.createElement("a");
        viewButton.className = "file__button";
        viewButton.href = "#";
        viewButton.title = "View document in-line";
        viewButton.innerHTML = "<span class='fa fa-eye'></span>";
        viewButton.onclick = function(e) {
            e.preventDefault();
            file.classList.toggle("file--open");
        }

        var downloadButton = document.createElement("a");
        downloadButton.className = "file__button";
        downloadButton.href = "deliverables/" + f.versions[f.versions.length - 1] + ".pdf";
        downloadButton.title = "Download document";
        downloadButton.innerHTML = "<span class='fa fa-download'></span>";

        var viewer = document.createElement("div");
        viewer.className = "file__viewer";

        var iframe = document.createElement("object");
        iframe.className = "file__iframe";
        iframe.data = "deliverables/" + f.versions[f.versions.length - 1] + ".pdf";
        iframe.type = "application/pdf";
        iframe.innerText = "This browser does not support PDFs viewers."

        // Create structure
        viewer.appendChild(iframe);
        info.appendChild(title);
        info.appendChild(versions);
        head.appendChild(info);
        head.appendChild(viewButton);
        head.appendChild(downloadButton);
        file.appendChild(head);
        file.appendChild(viewer);

        fileContainer.appendChild(file)


        /*return "\
        <div class='file'>\
            <div class='file__head'>\
                <div class='file__info'>\
                    <h2 class='file__title'>" + file.title + "</h2>\
                    <div class='file__versions'>\
                        " + file.versions.map((v, i) => "<a href='deliverables/" + v + ".pdf'>v" + (i + 1) + "</a>") + "\
                    </div>\
                </div>\
                <a class='file__button' href='deliverables/" + file.versions[file.versions.length - 1] + ".pdf' title='View' data-opens='js-" + i + "'>\
                    <span class='fa fa-eye'></span>\
                    </a>\
                <a class='file__button' href='deliverables/" + file.versions[file.versions.length - 1] + ".pdf' title='Download' download>\
                    <span class='fa fa-download'></span>\
                </a>\
            </div>\
            <div class='file__viewer'>\
                <object class='file__iframe' data='deliverables/" + file.versions[file.versions.length - 1] + ".pdf' type='application/pdf'>\
                    This browser does not support PDFs viewers.\
                </object>\
            </div>\
        </div>"*/
    });
}
