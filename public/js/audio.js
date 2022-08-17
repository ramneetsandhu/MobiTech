$(function() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    function process(speechText) {
        let text = speechText.toLowerCase();
        text = encodeURI(text);
        window.location.href = "/search?q="+text;
    }

    if (SpeechRecognition) {
        let mic = document.getElementById("mic");
        mic.innerHTML += '<span class="left-pan" id="bi-mic"><i class="bi bi-mic"></i></span>';
    }

    $('#bi-mic').click(function() {
        let listening = false;
        $('#bi-mic').hide();
        $('#bi-mic-listen').show();
        const searchBar = document.getElementById('searchBar');
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.maxAlternatives = 5;
        recognition.start();
        recognition.onresult = event => {
           const last = event.results.length - 1;
           const res = event.results[last];
           const text = res[0].transcript;
           if (res.isFinal) {
               searchBar.value += text;
           }
           setInterval(function() {
           if (text.length > 0) { return process(searchBar.value)};
           }, 7000);
        }

        recognition.onend = event => {
            if (searchBar.value.length < 1) {
            $('#bi-mic').show();
            $('#bi-mic-listen').hide();
            return alert('Did not listen anything');
            } else {
                return process(searchBar.value);
            }

        }
        // ++
    });




});
