const urlLocal = "http://127.0.0.1:5000";
const url = ""

let chat = document.querySelector(".chat");
let input = document.getElementById("input");

// Detect when the Enter key is pressed
input.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("send-question").click();
  }
})

// First I disable the button "Demander"
$("#send-question").prop("disabled", true);

// Disabled the button if input is empty:
$("input").on("input", () => {
  // Select input and if there is an input (change of input) then

  // Below, the disabled attribute of the button has the inverse value
  // of the input content.
  // If the input contains something(true) => disabled = false.
  // If the input is empty(false) => disabled = true.
  $("#send-question").prop("disabled", !$("input").val());
});

let showUnshowCategory = (category) => {
  console.log("category: ", category)
}

let askPapy = async () => {
  let question = $("input").val();

  try {
    // Show the question in the chat
    let userMessage = '<div class="user-message"><div class="txt">';
    userMessage += $("input").val();
    userMessage += "</div></div>";
    chat.innerHTML += userMessage;
    $(".loader").show();
    const res = await fetch(`api?question=${question}`);
    const resAsJson = await res.json();
    $(".loader").hide();
    const papyResponse = resAsJson.message;

    // Show the response in the chat
    let papyMessage = '<div class="papy-message"><div class="txt">';
    papyMessage += papyResponse.replaceAll(
      "<end_of_bubble />",
      "</div></div><div class='papy-message'><div class='txt'>"
    );
    papyMessage += `</div></div>`;
    chat.innerHTML += papyMessage;
    chat.scrollTop = chat.scrollHeight;
    var audio = new Audio("static/sound/bip.mp3");
    audio.play();

    // Clear input value
    $("input").val("");
    // Disable the "Demander" button
    $("#send-question").prop("disabled", true);
  } catch (err) {
    console.error(err);
  }
};
