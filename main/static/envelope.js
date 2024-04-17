$(document).ready(function() {
    var $envelope = $('#envelope-container');
    var $nextButton = $('#nextButton');
    var $envelopeContainer = $('#envelope-container');
    var $clickText = $('#click-text');
    var $letter = $('#letter');
    $letter.toggle();

    $nextButton.click(function(event) {
        window.location.href = data['nextPage'];
    });

    $envelope.on('click', function() {
        $letter.toggle();
        $envelope.toggleClass('envelope-open envelope-closed');
        if ($envelope.hasClass('envelope-open')) {
            $clickText.hide(); 
            $nextButton.show(); 
        } else {
            $clickText.show(); 
            $nextButton.hide(); 
        }
    });
    $envelopeContainer.click(function() {
        $(this).css('z-index', 10);  // Bring to front when clicked
    });
});
