$("#document").ready(function() {

    const body = document.body;
    const backgroundDiv = document.createElement("div");
    backgroundDiv.style.position = "fixed";
    backgroundDiv.style.top = "0";
    backgroundDiv.style.left = "0";
    backgroundDiv.style.width = "100%";
    backgroundDiv.style.height = "100%";
    backgroundDiv.style.backgroundImage = "url('" + data.backgroundImg + "')";
    backgroundDiv.style.backgroundSize = "cover";
    backgroundDiv.style.backgroundRepeat = "no-repeat";
    // backgroundDiv.style.filter = "blur(1px)";
    backgroundDiv.style.zIndex = "-1";
    body.appendChild(backgroundDiv);
    const darkOverlay = document.createElement("div");
    darkOverlay.classList.add("dark-overlay");
    body.appendChild(darkOverlay);

    $("#nextButton").click(function(event) {
        window.location.href = data['nextPage'];
    });
});
