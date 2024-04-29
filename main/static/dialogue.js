// <!-- <div class="dialogueBox">
// <p id="dialogueText">{{ data.text | safe }}</p>
// </div>
// <div class="speakerImage">
// <img src="{{ data['speakerImage'] }}" alt="{{ data['speakerName'] }}">
// <b>{{ data['speakerName'] }}</b>
// </div> -->




$("#document").ready(function() {

    dialogues = []
    for (var key in data) {
        if (parseInt(key)) {

            let dialogue_data = data[key];

            // Create speaker icon
            let speaker = $("<div class='speakerImage'>");
            speaker.append($(`<img src=${dialogue_data['speakerImage']} alt=${dialogue_data['speakerName']}>`));
            speaker.append($(`<b>${dialogue_data['speakerName']}</b>`));

            // Assign left or right
            let dialogue_row = $("<div class='dialogueRow'>");
            let dialogue_box = $("<div>");
            dialogue_box.append($(`<p class="dialogueText">${dialogue_data["dialogue"]}</p>`));
            if (parseInt(key) % 2 == 0) {
                dialogue_box.addClass("dialogueBoxRight");
                dialogue_row.append(dialogue_box);
                dialogue_row.append(speaker);
            } else {
                dialogue_box.addClass("dialogueBoxLeft");
                dialogue_row.append(speaker);
                dialogue_row.append(dialogue_box);
            }
            dialogues.push(dialogue_row);
        }
    }

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
    backgroundDiv.style.zIndex = "-1";
    body.appendChild(backgroundDiv);
    const darkOverlay = document.createElement("div");
    darkOverlay.classList.add("dark-overlay");
    body.appendChild(darkOverlay);

    $("#nextButton").click(function(event) {
        window.location.href = data['nextPage'];
    });

    // Fade in the dialogues from the bottom
    
    let dialogueContainer = $("#dialogueContainer");
    let currentDialogueIndex = 1;
    
    function appendDialogues() {
        if (currentDialogueIndex < dialogues.length) {
            $(dialogues[currentDialogueIndex]).hide().appendTo(dialogueContainer).fadeIn(2000);
            currentDialogueIndex++;
        } 
        if (currentDialogueIndex >= dialogues.length) {
            $("#nextButton").prop("disabled", false);
        }
    }

    $("#nextButton").prop("disabled", true);
    $(dialogues[0]).hide().appendTo(dialogueContainer).fadeIn(2000);
    $(document).on("click", function() {
        appendDialogues();
        $("#dialogueContainer").animate({
            scrollTop: $("#dialogueContainer")[0].scrollHeight
        }, 300);
    });
    
    
    
});
