let mediaRecorder;
let recordedChunks = [];
let isRecording = false;

// Function to toggle recording
async function toggleRecording() {
    const recordButton = document.getElementById("recordButton");

    if (!isRecording) {
        // Start Recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(recordedChunks, { type: "audio/wav" });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audioFile = new File([audioBlob], "recording.wav", { type: "audio/wav" });

                // Update the file input
                const fileInput = document.getElementById("audioFile");
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(audioFile);
                fileInput.files = dataTransfer.files;

                // Update the file label
                updateFileLabel();

                // Reset recorded chunks
                recordedChunks = [];
            };

            mediaRecorder.start();
            isRecording = true;
            recordButton.textContent = "⏹ Stop Recording";
            recordButton.style.backgroundColor = "#ff4444"; // Change button color to red
        } catch (error) {
            console.error("Error accessing microphone:", error);
            alert("Microphone access denied. Please allow microphone access to record audio.");
        }
    } else {
        // Stop Recording
        mediaRecorder.stop();
        isRecording = false;
        recordButton.textContent = "⏺ Start Recording";
        recordButton.style.backgroundColor = "#004080"; // Reset button color
    }
}

// Update the file label to show the uploaded file name
function updateFileLabel() {
    const fileInput = document.getElementById("audioFile");
    const fileLabel = document.getElementById("audioFileLabel");
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name; // Get the file name
        fileLabel.textContent = fileName; // Display the file name
    }
}

// Upload audio file and process it
async function uploadAudio(endpoint) {
    const fileInput = document.getElementById("audioFile");
    const inputLang = document.getElementById("inputLangAudio").value;
    const targetLang = document.getElementById("targetLangAudio");

    if (fileInput.files.length === 0) {
        alert("Please upload or record an audio file");
        return;
    }

    const formData = new FormData();
    formData.append("audio", fileInput.files[0]);
    formData.append("input_lang", inputLang);

    if (endpoint === "translate_audio") {
        formData.append("target_lang", targetLang.value);
    }

    showLoading(); // Show "Processing..." message
    try {
        const response = await fetch(`/${endpoint}`, { method: "POST", body: formData });
        const result = await response.json();
        displayResult(result); // Display the result in the table
    } catch (error) {
        console.error("Error uploading audio:", error);
        alert("An error occurred while uploading the audio.");
    } finally {
        hideLoading(); // Hide "Processing..." message
    }
}

// Translate text input
async function translateText() {
    const text = document.getElementById("textInput").value;
    const targetLang = document.getElementById("targetLangText").value;

    if (!text) {
        alert("Please enter text to translate");
        return;
    }

    showLoading(); // Show "Processing..." message
    try {
        const response = await fetch("/translate_text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, target_lang: targetLang }),
        });
        const result = await response.json();
        displayResult(result); // Display the result in the table
    } catch (error) {
        console.error("Error translating text:", error);
        alert("An error occurred while translating the text.");
    } finally {
        hideLoading(); // Hide "Processing..." message
    }
}

// Display the result in the table
function displayResult(result) {
    const table = document.getElementById("resultTable").getElementsByTagName("tbody")[0];
    table.innerHTML = ""; // Clear previous results

    for (let key in result) {
        const row = table.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        cell1.textContent = key;
        cell2.textContent = result[key];
    }
}

// Show a loading message
function showLoading() {
    const processingMessage = document.getElementById("processingMessage");
    processingMessage.style.display = "block";
}

// Hide the loading message
function hideLoading() {
    const processingMessage = document.getElementById("processingMessage");
    processingMessage.style.display = "none";
}

// Logout function
function logout() {
    alert("You have been logged out.");
    window.location.href = "/logout"; // Redirect to logout endpoint or login page
}