Backends
========

SciTeX Audio supports four TTS backends with automatic fallback. When no backend
is specified, the system tries each in order until one succeeds.

Fallback Order
--------------

1. **ElevenLabs** → 2. **LuxTTS** → 3. **Google TTS** → 4. **System TTS**

ElevenLabs
----------

High-quality commercial TTS with natural-sounding voices.

- **Quality:** Best
- **Cost:** Paid (API key required)
- **Internet:** Required
- **Default speed:** 1.2x

.. code-block:: python

   speak("Hello", backend="elevenlabs", speed=1.2)

.. code-block:: bash

   export SCITEX_AUDIO_ELEVENLABS_API_KEY="your-api-key"

LuxTTS
------

Open-source TTS with voice cloning support. Based on
`LuxTTS <https://github.com/ysharma3501/LuxTTS>`_ (Apache 2.0).

- **Quality:** High (48kHz output)
- **Cost:** Free
- **Internet:** First model download only
- **Default speed:** 2.0x
- **CPU performance:** ~1.27x realtime factor (near-realtime)

.. code-block:: python

   speak("Hello", backend="luxtts", speed=2.0)

   # Control CPU threads
   speak("Hello", backend="luxtts", num_threads=4)

Features:

- Voice cloning from reference audio samples
- Singleton model caching (7.5s init, then instant)
- Encoded prompt caching per reference audio
- Automatic device detection (CUDA/MPS/CPU)

Place reference audio files in ``~/.scitex/audio/reference/`` for voice cloning.
Without reference audio, a generic voice is used.

Google TTS (gTTS)
-----------------

Free cloud-based TTS via Google Translate's speech synthesis.

- **Quality:** Good
- **Cost:** Free
- **Internet:** Required
- **Default speed:** 1.5x

.. code-block:: python

   speak("Bonjour", backend="gtts", voice="fr", speed=1.5)

Supports many languages via the ``voice`` parameter (ISO language codes).

System TTS (pyttsx3)
--------------------

Offline TTS using the system's speech synthesis engine (espeak on Linux, SAPI5 on Windows).

- **Quality:** Basic
- **Cost:** Free
- **Internet:** Not required
- **Default speed:** 150 words per minute

.. code-block:: python

   speak("Hello", backend="pyttsx3", rate=200)

.. code-block:: bash

   # Linux: install espeak
   apt install espeak-ng

Checking Available Backends
---------------------------

.. code-block:: python

   from scitex_audio import available_backends, FALLBACK_ORDER

   # List installed backends
   print(available_backends())  # ['gtts', 'pyttsx3']

   # See the fallback order
   print(FALLBACK_ORDER)  # ['elevenlabs', 'luxtts', 'gtts', 'pyttsx3']

.. code-block:: bash

   scitex-audio backends
