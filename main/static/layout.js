function updateTimeline(progress) {
    const timeline = $("#timeline");
    timeline.empty();

    const stages = [
        "Introduction",
        "Limo Entrances",
        "Group Dates",
        "1-1 Dates",
        "2-1 Dates",
        "Hometowns",
        "Fantasy Suites",
        "Engagement",
        "Quiz"
    ];

    const routes = [
        "/learn/1",
        "/learn/3",
        "/learn/4",
        "/envelope/2",
        "/envelope/3",
        "/learn/5",
        "/learn/6",
        "/learn/7",
        "/learn/8"
    ];

    for (let i = 0; i < stages.length; i++) {
        const dot = $("<div></div>").addClass("timeline-dot");
        const dotColor = (i < progress) ? "#ff6666" : "#ffffff";
        dot.css("background-color", dotColor);
        dot.data("original-color", dotColor);
        dot.data("stage", stages[i]);
        dot.data("route", routes[i]);

        dot.on("click", function() {
            window.location.href = $(this).data("route");
        });
        
        dot.text(i + 1);
        timeline.append(dot);
        const popup = $("<div></div>").addClass("timelinePopup").text(stages[i]);
        popup.data("stage", stages[i]);
        timeline.append(popup);
        popup.css("left", dot.position().left + 10);
        popup.hide();

        if (i < stages.length - 1) {
            const line = $("<div></div>").addClass("timeline-line");
            const lineColor = (i+1 < progress) ? "#ff6666" : "#ffffff";
            line.css("background-color", lineColor)
            timeline.append(line);
        }

        dot.on("mouseenter", function() {
            popup.show();
        });

        dot.on("mouseleave", function() {
            popup.hide();
        });

    }

    timeline.on("mouseenter", ".timeline-dot", function() {
        $(this).css("background-color", "#f9abab");
    });

    timeline.on("mouseleave", ".timeline-dot", function() {
        const originalColor = $(this).data("original-color");
        $(this).css("background-color", originalColor);
    });
}


$("#document").ready(function() {

    updateTimeline(data['timeline']);

});


