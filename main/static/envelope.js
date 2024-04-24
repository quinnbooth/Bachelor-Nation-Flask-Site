$(document).ready(function() {

    var $envelope = $('#envelope-container');
    var $nextButton = $('#nextButton');
    var $clickText = $('#click-text');
    var $letter = $('#letter');

    $nextButton.hide();

    $nextButton.click(function(event) {
        window.location.href = data['nextPage'];
    });

    $envelope.click(function() {
        $letter.toggleClass('letter-off'); 
        $envelope.toggleClass('envelope-open envelope-closed');
        if ($envelope.hasClass('envelope-open')) {
            $clickText.hide();
            $nextButton.show();
            $letter.slideDown(500);
        } else {
            $clickText.show();
            $nextButton.hide();
            $letter.slideUp(500);
        }
    });
});
