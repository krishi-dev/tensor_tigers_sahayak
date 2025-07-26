import os
import logging
from google.cloud import vision
from google.cloud import texttospeech
from dotenv import load_dotenv

# ---------- CONFIG ----------
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------- CREDENTIALS UTILITY ----------
def setup_google_credentials():
    """Ensure GOOGLE_APPLICATION_CREDENTIALS is correctly set."""
    try:
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            logger.info(f"Credentials found at {credentials_path}")
            return

        # Try fallback paths
        fallback_paths = [
            './vertex_key.json',
            '../vertex_key.json',
            './ocrmodule/vertex_key.json'
        ]

        for path in fallback_paths:
            if os.path.exists(path):
                abs_path = os.path.abspath(path)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = abs_path
                logger.info(f"Credentials found at fallback: {abs_path}")
                return

        raise FileNotFoundError("No valid Google Cloud credentials found.")
    except Exception as e:
        logger.error(f"Credential setup error: {e}")
        raise


# ---------- OCR MODULE ----------
class GoogleOCR:
    def __init__(self):
        setup_google_credentials()
        self.client = vision.ImageAnnotatorClient()

    def extract_text(self, image_path: str):
        """Extracts text from the given image file using Google Vision API."""
        try:
            with open(image_path, "rb") as f:
                content = f.read()

            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)

            if response.error.message:
                raise Exception(f"Vision API Error: {response.error.message}")

            annotations = response.text_annotations
            extracted_text = annotations[0].description.strip() if annotations else ""
            logger.info(f"Extracted {len(extracted_text)} characters from image.")

            return {
                "text": extracted_text,
                "raw_response": response
            }
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise


# ---------- TEXT TO SPEECH MODULE ----------
class GoogleTTS:
    def __init__(self):
        setup_google_credentials()
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, text: str, language_code: str = "en-US", gender="NEUTRAL") -> bytes:
        """Convert text to audio using Google Cloud TTS."""
        try:
            voice_gender = getattr(texttospeech.SsmlVoiceGender, gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)

            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=voice_gender
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            logger.info("Audio generated successfully.")
            return response.audio_content

        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise
