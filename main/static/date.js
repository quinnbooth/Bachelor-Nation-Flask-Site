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
                }
            },
            over: function(event, ui) {
                $(this).addClass("hovering");
            },
            out: function(event, ui) {
                $(this).removeClass("hovering");
            }
        });
        $("#contestantRow").append(profile);
    });
}

let roses_left = 0;
let rose = $(`<img class="rose" alt="Rose" src="https://icons.iconarchive.com/icons/miniartx/gifts-2/256/rose-icon.png">`).draggable({ revert: "invalid" });
let palmer = $(`<img class="palmer" alt="Jesse Palmer" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX7RRbcZWghn-ZIql1Q8wv-IZXzAwOBahfyT6oRmkJJg&s">`)

$(document).ready(function() { 

    roses_left = parseInt(data['roses']);

    console.log(roses_left);
    let title = data['title'];
    let description = data['description'];

    $("#title").text(title);
    load_contestants(contestants);
    $("#roseRow").append(rose);
    $("#rosesLeft").text(`Roses remaining: ${roses_left}`);
    roses_left -= 1;
    console.log(roses_left);
    $("#interface").text(description);
});
