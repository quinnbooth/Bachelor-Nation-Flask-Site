let current_choice = null;

// The plan is to have this function be the main function
// that checks what type of question it is. Then it will
// call the corresponding helper function to render
// the page.
$("#document").ready(function () {
  if (data.questionType === "mult_choice") {
    multChoiceHandler(data.choices, data.answer[0]);
  } else {
    console.log(data.questionType);
  }
});

function multChoiceHandler(choices, answer) {
  $("#questionBody").append(
    `
        <div id="multChoiceContainer"></div>
    `
  );
  for (let i = 0; i < choices.length; i++) {
    $("#multChoiceContainer").append(
      `
        <div id="choice${i}" class="quizChoice">
            ${choices[i]}
        </div>
      `
    );
  }
  $(".quizChoice").hover(function () {
    $(this).css("background-color", "gray");
  });
  $(".quizChoice").mouseleave(function () {
    $(this).css("background-color", "lightgray");
  });
  $(".quizChoice").on("click", function () {
    makeSelection($(this));
  });

  $("#quizSubmit").on("click", function () {
    let id = current_choice.attr("id");
    if (id.charAt(id.length - 1) === answer.toString()) {
      submitHandler({
        isCorrect: true,
        id: data.questionId,
      });
    } else {
      submitHandler({
        isCorrect: false,
        id: data.questionId,
      });
    }
  });
}

// Keeps track of which choice was selected and prevents users from
// selecting multiple choices. Used for mult choice question.
// Could probably be used for true false too.
// TODO: When selection is made, maybe turn off hover highlight for the other options?
// Alternatively, could make it so that clicking other options changes the current
// selection to the new selection.
function makeSelection(element) {
  if (!(current_choice && current_choice !== element)) {
    element.css("border", "6px solid yellow");
    current_choice = element;

    element.off("click");
    element.on("click", function () {
      element.css("border", "1px solid black");
      current_choice = null;
      console.log(element);
      element.off("click");
      element.on("click", function () {
        makeSelection(element);
      });
    });
  }
}

// Pass in a JSON object with the following key-val pairs:
//   KEY NAME  |  VAL TYPE
// --------------------------
//  isCorrect  |  boolean
//     id      |    int
function submitHandler(json) {
  $.ajax({
    type: "POST",
    url: "/quiz_handler",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(json),
    success: function (result) {
      window.location.href = result.redirect;
    },
    error: function (request, status, error) {
      console.log("Error");
      console.log(request);
      console.log(status);
      console.log(error);
    },
  });
}
