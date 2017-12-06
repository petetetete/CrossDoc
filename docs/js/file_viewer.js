function populateFiles(container, files) {
    if (!container || !files)
        return;

    container.innerHTML = "";
    files.forEach((f, i) => {

        // Construct the elements in javascript to encapsulate opening logic
        var file = document.createElement("div");
        file.className = "file";

        var head = document.createElement("div");
        head.className = "file__head";

        var info = document.createElement("div");
        info.className = "file__info";

        var title = document.createElement("div");
        title.className = "file__title";
        title.innerText = f.title;

        var versions = document.createElement("div");
        versions.className = "file__versions";
        versions.innerHTML = f.versions.map((v, i) => 
            "<a href='deliverables/" + v + ".pdf' title='View version'>v"
             + (i + 1) + "</a>");

        var viewButton = document.createElement("a");
        viewButton.className = "file__button";
        viewButton.href = "#";
        viewButton.title = "View document in-line";
        viewButton.innerHTML = "<span class='fa fa-eye file__open'></span><span class='fa fa-eye-slash file__close'></span>";
        viewButton.onclick = function(e) {
            e.preventDefault();
            file.classList.toggle("file--open");
        }

        var downloadButton = document.createElement("a");
        downloadButton.className = "file__button";
        downloadButton.href = "deliverables/"
         + f.versions[f.versions.length - 1] + ".pdf";
        downloadButton.title = "Download document";
        downloadButton.innerHTML = "<span class='fa fa-download'></span>";

        var viewer = document.createElement("div");
        viewer.className = "file__viewer";

        var iframe = document.createElement("object");
        iframe.className = "file__iframe";
        iframe.data = "deliverables/"
         + f.versions[f.versions.length - 1] + ".pdf";
        iframe.type = "application/pdf";
        iframe.innerText = "This browser does not support PDFs viewers."

        // Asynchronously set the data to improve inital load time
        setTimeout(() => iframe.data = "deliverables/"
         + f.versions[f.versions.length - 1] + ".pdf", 0);

        // Create structure
        viewer.appendChild(iframe);
        info.appendChild(title);
        info.appendChild(versions);
        head.appendChild(info);
        head.appendChild(viewButton);
        head.appendChild(downloadButton);
        file.appendChild(head);
        file.appendChild(viewer);

        container.appendChild(file)
    });
}


// "Main" scope

var documents = [{
        title: "Requirements Specification",
        versions: ["Requirements Specification v1"]
    }, {
        title: "Technological Feasibility Analysis",
        versions: ["Technological Feasibility Analysis"]
    }, {
        title: "Team Inventory",
        versions: ["Team Inventory"]
    }];

var presentations = [{
        title: "Design Review #1",
        versions: ["Design Review 1"]
    }];

// Populate file containers
populateFiles(document.getElementById("js-documents"), documents);
populateFiles(document.getElementById("js-presentations"), presentations);
