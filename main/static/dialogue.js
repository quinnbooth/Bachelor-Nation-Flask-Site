// <!-- <div class="dialogueBox">
// <p id="dialogueText">{{ data.text | safe }}</p>
// </div>
// <div class="speakerImage">
// <img src="{{ data['speakerImage'] }}" alt="{{ data['speakerName'] }}">
// <b>{{ data['speakerName'] }}</b>
// </div> -->
function load_contestants(contestants) {
    $("#contestantRow").empty();
    contestants.forEach(function(contestant) {
        let profile = $('<div class="profile">');
        profile.data('id', contestant.id);
        profile.data('name', contestant.name);
        profile.data('description', contestant.description);
        profile.append(`<img src=${contestant.image} alt=${contestant.name}>`);
        profile.append(`<div class="profileName">${contestant.name}</div>`);
        profile.append(`<div class="popup">${contestant.description}</div>`);
        if (!(page_num === '1')) {
            profile.droppable({
                drop: function(event, ui) {
                    if (roses_left > 0) {
                        let new_rose = rose.clone().draggable({ revert: "invalid" }).css({
                            "position": "absolute",
                            "top": "0px",
                            "left": "calc(50% - 50px)"
                        });
                        $("#roseRow").append(new_rose);
                        $("#rosesLeft").text(`Roses remaining: ${roses_left}`);
                        roses_left -= 1;
                        ui.helper.draggable('destroy');
                        $(this).droppable('disable');
                    } else {
                        $("#rosesLeft").text(`Roses remaining: 0`);
                        ui.helper.draggable('destroy');
                        $(this).droppable('disable');
    
                        let nextPopup = $(`<div id='nextPopup'>`);
                        nextPopup.text("You gave out all of your roses!")
                        let nextBtn = $(`<button id='nextBtn'>`);
                        nextBtn.text("Exit");
                        nextBtn.click(function(event) {
                            $('#handbookModal').modal('hide');
                        });
                        
                        nextPopup.append(nextBtn);
                        $("#contestantRow").append(nextPopup);
                    }
                },
                over: function(event, ui) {
                    $(this).addClass("hovering");
                },
                out: function(event, ui) {
                    $(this).removeClass("hovering");
                }
            });
            profile.on('click', function() {
                console.log("before",rose_data);
                console.log("url", rose_data['videos'][contestant.name]);
                var videoUrl = rose_data['videos'][contestant.name];
                $('#videoFrame').attr('src', videoUrl);
    
                // var myModal = new bootstrap.Modal(document.getElementById('profileVideoModal'));
                // myModal.show();
                $('#embeddedVideo').attr('src', videoUrl);
                $('#videoInsert').css('display', 'block');
            });
        }
        $("#contestantRow").append(profile);
    });
}

let roses_left = 0;
let rose = $(`<img class="rose" alt="Rose" src="https://icons.iconarchive.com/icons/miniartx/gifts-2/256/rose-icon.png">`).draggable({ revert: "invalid" });


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

            // append video
            if (dialogue_data['videoURL']) {
                let iframe = $(`<iframe width="400" height="315" src="${dialogue_data['videoURL']}"frameborder="0" allowfullscreen></iframe>`);
                dialogue_box.append(iframe);
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
            $("#handbookButton").prop("disabled", false);
        }
    }

    $("#nextButton").prop("disabled", true);
    $("#handbookButton").prop("disabled", true);
    $(dialogues[0]).hide().appendTo(dialogueContainer).fadeIn(2000);
    $(document).on("click", function() {
        appendDialogues();
        $("#dialogueContainer").animate({
            scrollTop: $("#dialogueContainer")[0].scrollHeight
        }, 300);
    });
    // rose.js 
    roses_left = parseInt(rose_data['roses']);
    console.log("rose left: ", roses_left);

    let title = data['title'];
    let description = data['description'];

    $("#title").text(title);
    load_contestants(contestants);
    if (page_num === '2' || page_num === '3' ||  page_num === '4') {
        $("#handbookButton").text("Explore the date!");
        $("#handbookModalLabel").html("Date Example");
        $("#roseRow").append(rose);
        $("#rosesLeft").text(`Roses remaining: ${roses_left}`);
        roses_left -= 1; 
        $("#interface").text(description);
        if ( page_num ==='2') {
            $("#instruction").html("Click on any woman to get a sneak peek of the group's time with Joey!<br>Then drag the rose to who you want to ensure stays!<br>For this date, contestants who don't get a rose still stay - elimination happens at the rose ceremony later.")
        } else if ( page_num ==='3') {
            $("#instruction").html("Click on the lucky contestant to get a sneak peek of her time with Joey!<br>Then drag the rose to her if you want to ensure she stays!<br>For this date, contestants who don't get a rose still stay - elimination happens at the rose ceremony later.")
        } else {
            $("#instruction").html("Click on each woman to get a sneak peek of her time with Joey!<br>Then drag the rose(s) to who you want to stay!<br>For this date, the contestant that doesn't get a rose is eliminated.")
        }
    } else if (!(page_num === '1')) {
        $("#roseRow").append(rose);
        $("#rosesLeft").text(`Roses remaining: ${roses_left}`);
        roses_left -= 1; 
        $("#interface").text(description);
        $("#instruction").html("Click on each woman to get a sneak peek of her time with Joey!<br>Then drag the rose(s) to who you want to stay!")
    } else {
        $("#handbookButton").text("Meet the contestants!");
        $("#handbookModalLabel").html("Limo Entrance");
        $("#instruction").html("Below are all the contestants! Hover over their pictures to see more background information.")
    }

    
});
