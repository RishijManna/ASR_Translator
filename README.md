# Speech Translation Application

This is a Flask-based web application that allows users to upload audio files, transcribe them into text, and translate the transcribed text into a target language. The application uses the Rev AI API for speech-to-text transcription and the `deep_translator` library for text translation.

## Features

1. **User Authentication**:
   - Users can register, log in, and log out.
   - Session management ensures secure access to the application.

2. **Audio Transcription**:
   - Upload audio files (e.g., `.wav`, `.mp3`) and transcribe them into text using the Rev AI API.
   - Supports multiple input languages for transcription.

3. **Text Translation**:
   - Translate transcribed text into a target language using Google Translate via the `deep_translator` library.
   - Fallback mechanism for handling translation errors.

4. **Real-Time Processing**:
   - Asynchronous processing of audio files with periodic status checks.
   - Returns transcribed and translated text in JSON format.

5. **File Management**:
   - Uploaded audio files are saved in a dedicated `uploads` folder.

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.7 or higher
- A Rev AI API key (sign up at [Rev AI](https://www.rev.ai/))
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/speech-translation-app.git
   cd speech-translation-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your Rev AI API key:
     ```
     REV_AI_API_KEY=your_rev_ai_api_key_here
     ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application in your browser at `http://localhost:5000`.

## Usage

1. **Register or Log In**:
   - Navigate to the registration page to create an account.
   - Log in with your credentials to access the speech translation features.

2. **Upload Audio**:
   - On the home page, upload an audio file and select the input language.
   - Click "Submit" to transcribe the audio.

3. **Translate Text**:
   - After transcription, the application will display the transcribed text.
   - Optionally, translate the text into a target language by selecting the target language and clicking "Translate".

4. **Log Out**:
   - Use the logout button to securely end your session.

## API Endpoints

- **POST /upload**: Upload an audio file for transcription.
- **POST /translate_audio**: Upload an audio file for transcription and translation.
- **POST /translate_text**: Translate a given text into a target language.

## Project Structure

```
speech-translation-app/
│
├── app.py                # Main Flask application
├── requirements.txt      # List of dependencies
├── .env                  # Environment variables
├── uploads/              # Directory for uploaded audio files
├── static/
    ├── css/
       ├── styles.css
       ├── styleslog.css
       ├── stylesreg.css
    ├── js/
       ├── script.js     
├── templates/            # HTML templates
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── speech_translation.html  # Main application page
└── README.md             # Project documentation
```

## Dependencies

- Flask: Web framework
- Flask-CORS: Cross-Origin Resource Sharing support
- Rev AI Python SDK: Speech-to-text transcription
- Deep Translator: Text translation
- Python-dotenv: Environment variable management

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to the branch.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This `README.md` provides a comprehensive overview of your project, making it easier for users and contributors to understand and use your application. Adjust the content as needed to fit your specific requirements.
