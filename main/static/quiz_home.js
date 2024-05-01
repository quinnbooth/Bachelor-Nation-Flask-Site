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
    $(this).css("background-color", "#ee7e7e");
  });
  $(".unanswered").mouseleave(function () {
    $(this).css("background-color", "#d99e9e");
  });

  if (data.correct.length + data.incorrect.length === 6) {
    $("#quizContainer").append(
      `
        <div class="scoreDiv">
          Total Score: ${data.correct.length}/6 (${Math.round(
        (data.correct.length * 100) / 6
      )}%)
        </div>
        <a href="/" class="d-flex justify-content-center no-underline">
          <div id="start-over">
            Start over
          </div>
        </a>
      `
    );
  }
});
