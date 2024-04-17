$(document).ready(function() {
    var $envelope = $('#envelope-container');
    var $letterContent = $('#letter-content');
    var $nextButton = $('#nextButton');

    $nextButton.click(function(event) {
        window.location.href = data['nextPage'];
    });

    $envelope.on('click', function() {
        
        $letterContent.text("Get in your tennis gear and join me for a group date! Love, Joey");
        $nextButton.show();

        $envelope.toggleClass('envelope-open envelope-closed');
    });
});
