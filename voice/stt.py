from faster_whisper import WhisperModel


_model = None


def _get_model():
    global _model

    if _model is None:
        # Small local model suitable for the laptop.
        _model = WhisperModel(
            "tiny",
            device="auto",
            compute_type="int8",
        )

    return _model


def listen():
    """
    Record one short utterance and return its transcription.

    Requires sounddevice. If STT cannot initialize or no speech is detected,
    return an empty string so terminal.py can fall back to typed input.
    """
    try:
        import sounddevice as sd
        import numpy as np

        sample_rate = 16000
        seconds = 5

        audio = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        audio = np.squeeze(audio)

        if float(np.max(np.abs(audio))) < 0.01:
            return ""

        segments, _ = _get_model().transcribe(
            audio,
            beam_size=1,
            vad_filter=True,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        return text.strip()

    except Exception:
        return ""
