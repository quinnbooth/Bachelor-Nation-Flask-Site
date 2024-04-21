$("#document").ready(function () {
  $("#quizContainer").append(
    `
        <div id="quizQuestions"></div>
      `
  );
  for (let i = 1; i < 7; i++) {
    $("#quizQuestions").append(
      `
        <div class="questionBox" id="question${i}">
            Question ${i}
        </div>
      `
    );
    if (data.correct.includes(i.toString())) {
      $(`#question${i}`).addClass("correct");
    } else if (data.incorrect.includes(i.toString())) {
      $(`#question${i}`).addClass("incorrect");
    } else {
      $(`#question${i}`).addClass("unanswered");
    }
    $(`#question${i}`).on("click", function () {
      window.location.href = `/quiz/${i}`;
    });
  }
  $(".unanswered").hover(function () {
    $(this).css("background-color", "#f7b776");
  });
  $(".unanswered").mouseleave(function () {
    $(this).css("background-color", "#f9cb9c");
  });

  if (data.correct.length + data.incorrect.length === 6) {
    $("#quizContainer").append(
      `
        <div>
          Total Score: ${data.correct.length}/6 (${Math.round(
        (data.correct.length * 100) / 6
      )}%)
        </div>
      `
    );
  }
});
