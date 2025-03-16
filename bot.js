const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (message) {
        appendMessage("You", message);
        userInput.value = "";
        fetchBotResponse(message);
    }
});

function fetchBotResponse(userMessage) {
    fetch("https://api.together.xyz/v1/completions", {
        method: "POST",
        headers: {
            "Authorization": "b003e3943f0d2e4dbcc7a1c50b6525491d467b2f175651e454718cd7b1804e14",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            prompt: `Question: ${userMessage}\nAnswer:`,
            temperature: 0.7,
            max_tokens: 100
        })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = data.choices?.[0]?.text?.trim() || "Sorry, I couldn't process that.";
        appendMessage("Bot", botMessage);
    })
    .catch(error => appendMessage("Bot", "Error fetching response."));
}
