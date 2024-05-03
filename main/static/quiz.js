let current_choice = null;
let answered = false;

// The plan is to have this function be the main function
// that checks what type of question it is. Then it will
// call the corresponding helper function to render
// the page.
$("#document").ready(function () {
  console.log(answers);
  console.log(answers[parseInt(data.questionId) - 1]);
  if (answers[parseInt(data.questionId) - 1]) {
    answered = true;
  }
  if (data.questionType === "mult_choice") {
    multChoiceHandler(data.choices, data.answer[0]);
  } else if (data.questionType === "true_false") {
    trueFalseHandler(data.answer[0]);
  } else if (data.questionType === "fill_blank") {
    fillBlankHandler(data.answer[0]);
  } else if (data.questionType === "mult_select") {
    multSelectHandler(data.choices, data.answer);
  } else if (data.questionType === "sort") {
    sortHandler(data.choices, data.answer);
  } else {
    console.log(data.questionType);
  }
});

function multChoiceHandler(choices, answer) {
  $("#questionBody").append(`
        <div id="multChoiceContainer"></div>
    `);
  for (let i = 0; i < choices.length; i++) {
    $("#multChoiceContainer").append(
      `
        <div id="choice${i}" class="quizChoice">
            ${choices[i]}
        </div>
      `
    );
  }
  if (!answered) {
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
          answer: [id.charAt(id.length - 1)],
        });
      } else {
        submitHandler({
          isCorrect: false,
          id: data.questionId,
          answer: [id.charAt(id.length - 1)],
        });
      }
    });
  } else {
    if (answers[parseInt(data.questionId) - 1] !== answer.toString()) {
      $(`#choice${answers[parseInt(data.questionId) - 1]}`).addClass(
        "incorrect"
      );
    }
    $(`#choice${answer.toString()}`).addClass("correct");
  }
}

function trueFalseHandler(answer) {
  $("#questionBody").append(
    `
      <div id="trueFalseContainer"></div>
    `
  );
  $("#trueFalseContainer").append(
    `
      <div id="true" class="quizChoice trueFalseChoice">
          True
      </div>
      <div id="false" class="quizChoice trueFalseChoice">
          False
      </div>
    `
  );
  if (!answered) {
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
          answer: id,
        });
      } else {
        submitHandler({
          isCorrect: false,
          id: data.questionId,
          answer: id,
        });
      }
    });
  } else {
    if (answers[parseInt(data.questionId) - 1] !== answer.toString()) {
      $(`#${answers[parseInt(data.questionId) - 1]}`).addClass("incorrect");
    }
    $(`#${answer.toString()}`).addClass("correct");
  }
}

function fillBlankHandler(answer) {
  $("#questionBody").append(
    `
      <div id="fillBlankContainer" class="text-start"></div>
    `
  );
  $("#fillBlankContainer").append(
    `
      <input class="form-control position-absolute w-25" id="fillAnswer" maxlength="20" placeholder="Type here">
    `
  );

  if (!answered) {
    $("#quizSubmit").on("click", function () {
      let guess = $("#fillAnswer").val();
      if (guess.toLowerCase() === answer.toString().toLowerCase()) {
        submitHandler({
          isCorrect: true,
          id: data.questionId,
          answer: guess,
        });
      } else {
        submitHandler({
          isCorrect: false,
          id: data.questionId,
          answer: guess,
        });
      }
    });
  } else {
    $("#fillAnswer").prop("readonly", true);
    $("#fillAnswer").val("");
    $("#fillAnswer").attr("placeholder", "");
    $("#fillAnswer").css("z-index", "1");
    let user_ans = answers[parseInt(data.questionId) - 1];
    if (user_ans.toLowerCase() !== answer.toString().toLowerCase()) {
      $("#fillBlankContainer").append(
        `
          <span class="incorrect-text position-relative"><s>${user_ans}</s></span>
        `
      );
      $("#fillAnswer").addClass("is-invalid");
    } else {
      $("#fillAnswer").addClass("is-valid");
    }
    $("#fillBlankContainer").append(
      `
          <span class="correct-text position-relative">${answer.toString()}</span>
        `
    );
  }
}

function multSelectHandler(choices, answer) {
  current_choice = Array();

  $("#questionBody").append(`
        <div id="multChoiceContainer"></div>
    `);
  for (let i = 0; i < choices.length; i++) {
    $("#multChoiceContainer").append(
      `
        <div id="choice${i}" class="quizChoice">
            ${choices[i]}
        </div>
      `
    );
  }

  if (!answered) {
    $(".quizChoice").hover(function () {
      $(this).css("background-color", "gray");
    });
    $(".quizChoice").mouseleave(function () {
      $(this).css("background-color", "lightgray");
    });
    $(".quizChoice").on("click", function () {
      makeSelectionMult($(this));
    });
    $("#quizSubmit").on("click", function () {
      if (current_choice.sort().join(",") === answer.sort().join(",")) {
        submitHandler({
          isCorrect: true,
          id: data.questionId,
          answer: current_choice,
        });
      } else {
        submitHandler({
          isCorrect: false,
          id: data.questionId,
          answer: current_choice,
        });
      }
    });
  } else {
    let user_ans = answers[parseInt(data.questionId) - 1];
    console.log(user_ans);
    for (let i = 0; i < 4; i++) {
      console.log(answer);
      if (answer.includes(i)) {
        $(`#choice${i}`).addClass("correct");
      } else {
        $(`#choice${i}`).addClass("incorrect");
      }
      if (user_ans.includes(i.toString())) {
        $(`#choice${i}`).css("border", "12px solid #f9abab");
      }
    }
  }
}

function sortHandler(choices, answer) {
  current_choice = Array(choices.length);

  $("#questionBody").append(
    `
      <div id="sortBody">
        <div id="choicesContainer"></div>
        <div id="answerContainer"></div>
      </div>
    `
  );
  for (let i = 0; i < choices.length; i++) {
    $("#choicesContainer").append(
      `
        <div id="choice${i}" class="draggable sortItem">
            ${choices[i]}
        </div>
      `
    );
  }

  for (let i = 0; i < choices.length; i++) {
    $("#answerContainer").append(
      `
        <div id="answer${i}" class="sortItem droppable">
        </div>
      `
    );
  }

  $(function () {
    $(".draggable").draggable({
      revert: "invalid",
      snap: ".droppable",
      snapMode: "inner",
    });
    $(".droppable").droppable({
      drop: function (event, ui) {
        let id = $(this).attr("id");
        let id_answer = $(ui.draggable).attr("id");
        current_choice[parseInt(id.charAt(id.length - 1))] = parseInt(
          id_answer.charAt(id_answer.length - 1)
        );
      },
    });
  });

  if (!answered) {
    $("#quizSubmit").on("click", function () {
      let succeed = true;
      for (let i = 0; i < current_choice.length; i++) {
        if (current_choice[i] !== answer[i]) {
          succeed = false;
          submitHandler({
            isCorrect: false,
            id: data.questionId,
            answer: current_choice,
          });
          break;
        }
      }
      if (succeed) {
        submitHandler({
          isCorrect: true,
          id: data.questionId,
          answer: current_choice,
        });
      }
    });
  } else {
    let user_ans = answers[parseInt(data.questionId) - 1];
    $("#choicesContainer").remove();
    $("#sortBody").prepend(
      `
      <h3>Correct Answer:</h3>
      <div id="correctContainer"></div>
      `
    );
    for (let i = 0; i < choices.length; i++) {
      $("#correctContainer").append(
        `
        <div class="sortItem">
            ${choices[answer[i]]}
        </div>
        `
      );
      $(`#answer${i}`).text(choices[user_ans[i]]);
      if (user_ans[i] === answer[i]) {
        $(`#answer${i}`).addClass("correct");
      } else {
        $(`#answer${i}`).addClass("incorrect");
      }
    }
  }
}

// Keeps track of which choice was selected and prevents users from
// selecting multiple choices. Used for mult choice question and true false.
function makeSelection(element) {
  if (!current_choice) {
    element.css("border", "12px solid #ee7e7e");
    current_choice = element;

    element.off("click");
    element.on("click", function () {
      removeSelection(element);
    });
  } else {
    element.css("border", "12px solid #ee7e7e");
    removeSelection(current_choice);
    current_choice = element;

    element.off("click");
    current_choice.on("click", function () {
      removeSelection(element);
    });
  }
}

function makeSelectionMult(element) {
  element.css("border", "12px solid #ee7e7e");
  let id = element.attr("id");
  current_choice.push(id.charAt(id.length - 1));

  element.off("click");
  element.on("click", function () {
    removeSelectionMult(element);
  });
}

function removeSelection(element) {
  element.css("border", "1px solid white");
  element.off("click");
  element.on("click", function () {
    makeSelection(element);
  });
  current_choice = null;
}

function removeSelectionMult(element) {
  let id = element.attr("id");
  let val = id.charAt(id.length - 1);
  let index = current_choice.indexOf(val);
  current_choice.splice(index, 1);
  element.css("border", "1px solid white");
  element.off("click");
  element.on("click", function () {
    makeSelectionMult(element);
  });
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
      location.reload();

      // window.location.href = result.redirect;
    },
    error: function (request, status, error) {
      console.log("Error");
      console.log(request);
      console.log(status);
      console.log(error);
    },
  });
}
