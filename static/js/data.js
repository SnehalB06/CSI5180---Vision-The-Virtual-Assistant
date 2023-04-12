const searchForm = document.querySelector("#search-form");
const searchFormInput = searchForm.querySelector("input"); // <=> document.querySelector("#search-form input");
const info = document.querySelector(".info");
var transcribe = [];

// The speech recognition interface lives on the browser’s window object
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition; // if none exists -> undefined

if(SpeechRecognition) {
  console.log("Your Browser supports speech Recognition");

  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  // recognition.lang = "en-US";

  searchForm.insertAdjacentHTML("beforeend", '<button type="button"><i class="fas fa-microphone"></i></button>');
  searchFormInput.style.paddingRight = "50px";

  const micBtn = searchForm.querySelector("button");
  const micIcon = micBtn.firstElementChild;

  micBtn.addEventListener("click", micBtnClick);

  function micBtnClick() {
    if(micIcon.classList.contains("fa-microphone")) { // Start Voice Recognition
      recognition.start(); // First time you have to allow access to mic!
    }
    else {
      recognition.stop();
    }
  }

  recognition.addEventListener("start", startSpeechRecognition); // <=> recognition.onstart = function() {...}
  function startSpeechRecognition() {
    micIcon.classList.remove("fa-microphone");
    micIcon.classList.add("fa-microphone-slash");
    searchFormInput.focus();
    console.log("Voice activated, SPEAK");
  }

  recognition.addEventListener("end", endSpeechRecognition); // <=> recognition.onend = function() {...}
  function endSpeechRecognition() {
    micIcon.classList.remove("fa-microphone-slash");
    micIcon.classList.add("fa-microphone");
    searchFormInput.focus();
    console.log("Speech recognition service disconnected");
  }

  recognition.addEventListener("result", resultOfSpeechRecognition); // <=> recognition.onresult = function(event) {...} - Fires when you stop talking


  function resultOfSpeechRecognition(event) {

    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    console.log(transcript);
    transcribe.push(transcript);
    console.log("results ",transcribe);

    if(transcript.toLowerCase().trim()==="stop recording") {
      recognition.stop();
    }
    else if(!searchFormInput.value) {
      searchFormInput.value = transcript;
    }
    else {
      if(transcript.toLowerCase().trim()==="go") {
        searchForm.submit();
      }
      else if(transcript.toLowerCase().trim()==="call flask") {
        searchFormInput.value = transcript;
        callFlask(transcribe);
      }
      else if(transcript.toLowerCase().trim()==="reset input") {
        searchFormInput.value = "";
      }
      else {
        searchFormInput.value = transcript;
      }
    }
    // searchFormInput.value = transcript;
    // searchFormInput.focus();
    // setTimeout(() => {
    //   searchForm.submit();
    // }, 500);
  }

  info.textContent = 'Voice Commands: "stop recording","call flask", "reset input", "go"';

}
else {
  console.log("Your Browser does not support speech Recognition");
  info.textContent = "Your Browser does not support Speech Recognition";
}


const uploadURL = "{{ url_for('about')}}";
function callFlask(x)
    {
        let content = document.getElementById("content");
        const transcript = searchFormInput.value; // <=> document.querySelector("#search-form input");
        console.log("transcribe",x);
        console.log("transcript in cal flask ",transcript);
        command = x[x.length - 2]
        console.log("command",command);
        fetch(uploadURL, {
              method: "POST",
              body: JSON.stringify(command)
              })
        .then(response => response.json())
        .then(result => {
        console.log(result['weather']) })
             .catch(error => {
              console.log('Error:', error);
             })

