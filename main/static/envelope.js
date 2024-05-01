$(document).ready(function() {

    var $envelope = $('#envelope-container');
    var $nextButton = $('#nextButton');
    var $clickText = $('#click-text');
    var $letter = $('#letter');
    var $header = $('#envelope-header');

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
            $header.hide();
            $letter.slideDown(500);
        } else {
            $clickText.show();
            $nextButton.hide();
            $header.show();
            $letter.slideUp(500);
        }
    });
});
