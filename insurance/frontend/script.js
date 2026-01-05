// ===== DOM REFERENCES =====
const messagesDiv = document.getElementById("messages");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const micBtn = document.getElementById("mic");

// ===== STATE =====
let isProcessing = false; // prevents double send / erase

// ===== HELPER: ADD MESSAGE (NO RE-RENDER, NO CLEAR) =====
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender; // "user" or "bot"
  div.textContent = text;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  return div; // return element if we want to update it
}

// ===== SEND BUTTON =====
sendBtn.addEventListener("click", sendMessage);

// ===== ENTER KEY (SAFE: NO REPEAT) =====
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.repeat) {
    sendMessage();
  }
});

// ===== VOICE INPUT (STT) =====
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;

  micBtn.addEventListener("click", () => {
    if (isProcessing) return;
    micBtn.textContent = "🎙️";
    recognition.start();
  });

  recognition.onresult = (event) => {
    if (isProcessing) return;
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    sendMessage();
  };

  recognition.onend = () => {
    micBtn.textContent = "🎤";
  };
} else {
  micBtn.disabled = true;
  micBtn.textContent = "❌";
}

// ===== MAIN SEND FUNCTION =====
async function sendMessage() {
  if (isProcessing) return;

  const text = input.value.trim();
  if (!text) return;

  isProcessing = true;
  input.value = "";

  // Show user message
  addMessage(text, "user");

  // Show placeholder bot message (we will replace this)
  const placeholder = addMessage("Checking policy details…", "bot");

  try {
    const response = await fetch("http://127.0.0.1:8000/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_input: text })
    });

    const data = await response.json();

    const reply =
      data.conversation[data.conversation.length - 1]
        .voice_response_text;

    // Replace placeholder text (NO CLEAR, NO RE-RENDER)
    placeholder.textContent = reply;

    // Speak response
    speak(reply);

  } catch (error) {
    placeholder.textContent =
      "⚠️ Unable to reach the service. Please try again.";
  } finally {
    isProcessing = false;
  }
}

// ===== TEXT TO SPEECH (TTS) =====
function speak(text) {
  if (!window.speechSynthesis) return;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;
  utterance.pitch = 1;

  window.speechSynthesis.cancel(); // stop previous speech
  window.speechSynthesis.speak(utterance);
}
