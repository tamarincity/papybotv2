// Recognition API
const SpeechRecognition = window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

let userInput = $('#input');  // Where the user enter his question

// Info about the speech (is listening, ...)
let infoOnSpeech = document.getElementById('infoOnSpeech');

let content = '';

recognition.continuous = true;

recognition.onresult = function (event) {

    let current = event.resultIndex;

    let transcript = event.results[current][0].transcript;

    content = transcript;
    // Replace with correct words
    content = (content.replace('papy bottes', 'PapyBot')
        .replace('papy botte', 'PapyBot')
        .replace('papi bottes', 'PapyBot')
        .replace('papi botte', 'PapyBot')
        .replace('de peine classrooms', 'd\'OpenClassrooms')
        .replace('de peine classroom', 'd\'OpenClassrooms')
        .replace('de open classroom', 'd\'OpenClassrooms')
        .replace('de open classrooms', 'd\'OpenClassrooms')
        .replace('peine classrooms', 'OpenClassrooms')
        .replace('peine classroom', 'OpenClassrooms')
        .replace('openclassrooms', 'OpenClassrooms')
        .replace('openclassroom', 'OpenClassrooms')
        .replace('open classrooms', 'OpenClassrooms')
        .replace('open classroom', 'OpenClassrooms')
    )
    console.log(content)
    userInput.val(content);
    recognition.stop();
    askPapy()  // This is a function from logic.js

};

info = (message) => {
    infoOnSpeech.innerHTML = message
}

recognition.onstart = function () {
    infoOnSpeech.val ='Je t\'écoute ...';
    console.log(infoOnSpeech.val)
    info(infoOnSpeech.val)
}

recognition.onspeechend = function () {
    infoOnSpeech.val = 'Clique à nouveau sur "parler" pour parler.';
    info(infoOnSpeech.val)
}

recognition.onerror = function (event) {
    if (event.error == 'no-speech') {
        infoOnSpeech.val = 'Essaie encore.';
        info(infoOnSpeech.val)
    }
}

$('#speak-btn').on('click', function (e) {
    recognition.start();
});

userInput.on('input', function () {
    content = $(this).val();    
})
