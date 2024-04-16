let current_choice = null;

// The plan is to have this function be the main function
// that checks what type of question it is. Then it will
// call the corresponding helper function to render
// the page.
$("#document").ready(function () {
  if (data.questionType === "mult_choice") {
    multChoiceHandler(data.choices, data.answer[0]);
  } else if (data.questionType === "true_false") {
    trueFalseHandler(data.answer[0]);
  } else if (data.questionType === "fill_blank") {
    fillBlankHandler(data.answer[0]);
  } else if (data.questionType === "mult_select") {
    multSelectHandler(data.choices, data.answer);
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

function trueFalseHandler(answer) {
  $("#questionBody").append(
    `
      <div id="trueFalseContainer"></div>
    `
  );
  $("#trueFalseContainer").append(
    `
      <div id="true" class="quizChoice">
          True
      </div>
      <div id="false" class="quizChoice">
          False
      </div>
    `
  );
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
    if (id === answer.toString()) {
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

function fillBlankHandler(answer) {
  $("#questionBody").append(
    `
      <div id="fillBlankContainer"></div>
    `
  );
  $("#fillBlankContainer").append(
    `
      <input class="form-control" id="fillAnswer" placeholder="Type here">
    `
  );

  $("#quizSubmit").on("click", function () {
    let guess = $("#fillAnswer").val();
    if (guess.toLowerCase() === answer.toString().toLowerCase()) {
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

function multSelectHandler(choices, answer) {
  $("#questionBody").append(
    `
      <div id="multChoiceContainer"></div>
    `
  );
  for (let i = 0; i < choices.length; i++) {
    $("#multChoiceContainer").append(
      `
        <input type="checkbox" id="choice${i}" class="btn-check mult-select">
        <label class="btn btn-outline-primary" for="choice${i}">${choices[i]}</label> 
      `
    );
  }
  $(".mult-select").hover(function () {
    $(this).css("background-color", "gray");
  });
  $(".mult-select").mouseleave(function () {
    $(this).css("background-color", "lightgray");
  });

  $("#quizSubmit").on("click", function () {
    let guesses = [];

    for (let i = 0; i < choices.length; i++) {
      if ($(`#choice${i}`).prop("checked")) {
        guesses.push(1);
      } else {
        guesses.push(0);
      }
    }

    for (let i = 0; i < answer.length; i++) {
      guesses[answer[i]]--;
    }

    if (guesses.every((element) => element === 0)) {
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
// selecting multiple choices. Used for mult choice question and true false.
function makeSelection(element) {
  if (!current_choice) {
    element.css("border", "6px solid yellow");
    current_choice = element;

    element.off("click");
    element.on("click", function () {
      removeSelection(element);
    });
  } else {
    element.css("border", "6px solid yellow");
    removeSelection(current_choice);
    current_choice = element;

    element.off("click");
    current_choice.on("click", function () {
      removeSelection(element);
    });
  }
}

function removeSelection(element) {
  element.css("border", "1px solid black");
  element.off("click");
  element.on("click", function () {
    makeSelection(element);
  });
  current_choice = null;
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
