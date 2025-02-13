from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_cors import CORS
from rev_ai import apiclient
from deep_translator import GoogleTranslator, exceptions
import os
import time
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'

# Rev AI API Client
REV_AI_API_KEY = "Replace with your actual Rev AI API key"  # Replace with your actual Rev AI API key
rev_client = apiclient.RevAiAPIClient(REV_AI_API_KEY)

# Ensure uploads folder exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In-memory user storage (for demonstration purposes)
users = {}

# Root route serves the speech translation page directly
@app.route('/')
def home():
    if 'email' in session:
        return render_template('speech_translation.html')
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Wrong Password")
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users:
            return render_template('register.html', error="Email already registered")
        else:
            users[email] = password
            return redirect(url_for('login'))
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

# Upload and process audio file
@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files or "input_lang" not in request.form:
        return jsonify({"error": "Missing audio file or language input"}), 400

    audio_file = request.files["audio"]
    input_lang = request.form["input_lang"]

    audio_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file.filename)
    audio_file.save(audio_path)

    try:
        job = rev_client.submit_job_local_file(audio_path, language=input_lang)

        while True:
            job_details = rev_client.get_job_details(job.id)
            if job_details.status in ["transcribed", "failed"]:
                break
            time.sleep(5)

        if job_details.status == "transcribed":
            transcript = rev_client.get_transcript_text(job.id)
            return jsonify({"text": transcript})
        else:
            return jsonify({"error": "Transcription failed"}), 500
    except Exception as e:
        logger.error(f"Error in transcription: {e}")
        return jsonify({"error": str(e)}), 500

# Audio to Text with Translation
@app.route("/translate_audio", methods=["POST"])
def translate_audio():
    if "audio" not in request.files or "input_lang" not in request.form or "target_lang" not in request.form:
        return jsonify({"error": "Missing required inputs"}), 400

    input_lang = request.form["input_lang"]
    target_lang = request.form["target_lang"]
    audio_file = request.files["audio"]

    audio_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file.filename)
    audio_file.save(audio_path)

    try:
        job = rev_client.submit_job_local_file(audio_path, language=input_lang)

        while True:
            job_details = rev_client.get_job_details(job.id)
            if job_details.status in ["transcribed", "failed"]:
                break
            time.sleep(5)

        if job_details.status == "transcribed":
            transcript = rev_client.get_transcript_text(job.id)
            translated_text = translate_text_with_fallback(transcript, input_lang, target_lang)
            return jsonify({"text": transcript, "translated_text": translated_text})
        else:
            return jsonify({"error": "Transcription failed"}), 500
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        return jsonify({"error": str(e)}), 500

# Translate text with fallback mechanism
def translate_text_with_fallback(text, source_lang, target_lang):
    try:
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated_text
    except exceptions.TranslationNotFound:
        logger.warning(f"Translation not found for text: {text}. Trying alternative translation method.")
        return "Translation not available"
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        return "Translation not available"

# Translate text
@app.route("/translate_text", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text", "")
    target_lang = data.get("target_lang", "hi")

    try:
        translated_text = translate_text_with_fallback(text, "auto", target_lang)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
