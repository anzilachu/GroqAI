const chatForm = document.getElementById('chat-form');
const userMessageInput = document.getElementById('user-message');
const chatHistory = document.getElementById('chat-history');

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const userInput = userMessageInput.value.trim();

    if (userInput) {
        // Clear the input field
        userMessageInput.value = '';

        // ... rest of your code to send the request and update chat history
    }
});