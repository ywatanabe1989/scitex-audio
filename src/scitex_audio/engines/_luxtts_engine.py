#!/usr/bin/env python3
# Timestamp: "2026-03-14 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-python/src/scitex/audio/engines/_luxtts_engine.py
# ----------------------------------------

"""
LuxTTS backend - Open-source, offline, voice-cloning TTS.

Uses the ZipVoice/LuxTTS model from HuggingFace.
Supports CPU, CUDA, and MPS devices.
48kHz output, near-realtime on CPU, 150x+ on GPU.

Install:
    pip install git+https://github.com/ysharma3501/LuxTTS.git
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import List, Optional

from ._base import BaseTTS

__all__ = ["LuxTTS"]

_lock = threading.Lock()
_cached_model = None
_cached_prompt = None
_cached_ref_path = None


def _get_model(device: str = "cpu", model_id: str = "YatharthS/LuxTTS"):
    """Get or create cached LuxTTS model (singleton)."""
    global _cached_model
    with _lock:
        if _cached_model is None:
            from zipvoice.luxvoice import LuxTTS as _LuxTTSModel

            _cached_model = _LuxTTSModel(model_id, device=device)
        return _cached_model


def _get_encoded_prompt(model, ref_path: str, duration: float = 5.0):
    """Get or create cached encoded prompt for a reference audio."""
    global _cached_prompt, _cached_ref_path
    with _lock:
        if _cached_prompt is None or _cached_ref_path != ref_path:
            _cached_prompt = model.encode_prompt(ref_path, duration=duration)
            _cached_ref_path = ref_path
        return _cached_prompt


class LuxTTS(BaseTTS):
    """LuxTTS backend - open-source voice-cloning TTS.

    High-quality 48kHz output. Near-realtime on CPU, 150x+ on GPU.
    Requires a reference audio file for voice cloning.

    Install: pip install git+https://github.com/ysharma3501/LuxTTS.git
    """

    # Default reference audio search paths
    _DEFAULT_REF_DIRS = [
        "~/.config/scitex/audio/reference",
        "~/.scitex/audio/reference",
    ]

    def __init__(
        self,
        device: Optional[str] = None,
        model_id: str = "YatharthS/LuxTTS",
        reference_audio: Optional[str] = None,
        num_steps: int = 4,
        speed: float = 2.0,
        guidance_scale: float = 3.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._device = device or self._detect_device()
        self._model_id = model_id
        self._reference_audio = reference_audio
        self.num_steps = num_steps
        self.speed = speed
        self.guidance_scale = guidance_scale

    @staticmethod
    def _detect_device() -> str:
        """Auto-detect best available device."""
        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
        except ImportError:
            pass
        return "cpu"

    @property
    def name(self) -> str:
        return "luxtts"

    @property
    def requires_internet(self) -> bool:
        # Only for initial model download from HuggingFace
        return False

    def _find_reference_audio(self) -> Optional[str]:
        """Find a reference audio file from configured paths."""
        # Explicit config
        if self._reference_audio:
            path = Path(self._reference_audio).expanduser()
            if path.exists():
                return str(path)

        # Environment variable
        env_ref = os.environ.get("SCITEX_AUDIO_LUXTTS_REFERENCE")
        if env_ref:
            path = Path(env_ref).expanduser()
            if path.exists():
                return str(path)

        # Search default directories
        for dir_path in self._DEFAULT_REF_DIRS:
            d = Path(dir_path).expanduser()
            if d.is_dir():
                for ext in ("*.wav", "*.mp3", "*.flac", "*.ogg"):
                    files = sorted(d.glob(ext))
                    if files:
                        return str(files[0])

        return None

    def _create_default_reference(self) -> str:
        """Create a minimal reference audio when none is provided."""
        import numpy as np
        import soundfile as sf

        ref_dir = Path("~/.config/scitex/audio/reference").expanduser()
        ref_dir.mkdir(parents=True, exist_ok=True)
        ref_path = ref_dir / "default_ref.wav"

        if not ref_path.exists():
            sr = 16000
            duration = 3
            audio = np.random.randn(sr * duration).astype(np.float32) * 0.01
            sf.write(str(ref_path), audio, sr)

        return str(ref_path)

    def synthesize(self, text: str, output_path: str) -> Path:
        """Synthesize text using LuxTTS."""
        try:
            from zipvoice.luxvoice import LuxTTS as _LuxTTSModel  # noqa: F401
        except ImportError:
            raise ImportError(
                "LuxTTS (zipvoice) not installed. Install with:\n"
                "  pip install git+https://github.com/ysharma3501/LuxTTS.git"
            )

        import soundfile as sf

        # Get model (cached singleton)
        model = _get_model(device=self._device, model_id=self._model_id)

        # Find or create reference audio
        ref_path = self._find_reference_audio()
        if ref_path is None:
            ref_path = self._create_default_reference()

        # Encode prompt (cached per reference audio)
        encoded = _get_encoded_prompt(model, ref_path)

        # Generate speech
        speed = self.config.get("speed", self.speed)
        audio = model.generate_speech(
            text,
            encoded,
            num_steps=self.num_steps,
            guidance_scale=self.guidance_scale,
            speed=speed,
        )

        # Save as WAV (48kHz)
        out_path = Path(output_path)
        wav = audio.cpu().numpy()
        if wav.ndim == 2:
            wav = wav[0]

        # LuxTTS outputs WAV at 48kHz
        if out_path.suffix.lower() in (".mp3", ".ogg"):
            # Save as WAV first, then convert
            wav_tmp = out_path.with_suffix(".wav")
            sf.write(str(wav_tmp), wav, 48000)
            try:
                from pydub import AudioSegment

                sound = AudioSegment.from_wav(str(wav_tmp))
                sound.export(str(out_path), format=out_path.suffix.lstrip("."))
                wav_tmp.unlink()
            except ImportError:
                # No pydub — save as WAV instead
                out_path = wav_tmp
        else:
            sf.write(str(out_path), wav, 48000)

        return out_path

    def speak(
        self,
        text: str,
        output_path: Optional[str] = None,
        play: bool = True,
        voice: Optional[str] = None,
    ) -> dict:
        """Synthesize and optionally play. Uses .wav temp files (not .mp3)."""
        import tempfile

        if output_path:
            out_path = Path(output_path)
        else:
            fd, tmp_path = tempfile.mkstemp(suffix=".wav", prefix="scitex_tts_")
            os.close(fd)
            out_path = Path(tmp_path)

        if voice:
            self.config["voice"] = voice

        result_path = self.synthesize(text, str(out_path))

        played = False
        if play:
            played = self._play_audio(result_path)

        result = {"success": True, "played": played, "play_requested": play}
        if output_path:
            result["path"] = result_path
        return result

    def get_voices(self) -> List[dict]:
        """Get available voices (reference audio files)."""
        voices = []
        for dir_path in self._DEFAULT_REF_DIRS:
            d = Path(dir_path).expanduser()
            if d.is_dir():
                for f in sorted(d.iterdir()):
                    if f.suffix.lower() in (".wav", ".mp3", ".flac", ".ogg"):
                        voices.append(
                            {
                                "name": f.stem,
                                "id": str(f),
                                "type": "reference_audio",
                            }
                        )
        if not voices:
            voices.append(
                {
                    "name": "default",
                    "id": "default",
                    "type": "generated",
                }
            )
        return voices


# EOF
