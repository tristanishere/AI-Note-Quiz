import sys
import whisper

def transcribe(audio_path: str) -> str:
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py path/to/audio.wav")
        sys.exit(1)
    print("Transcription:\n", transcribe(sys.argv[1]))

