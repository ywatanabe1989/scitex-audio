SciTeX Audio
============

.. raw:: html

   <p align="center"><b>Text-to-Speech with multiple backends for scientific workflows</b></p>
   <br>

**SciTeX Audio** provides a unified interface for text-to-speech synthesis with support
for multiple backends, allowing you to choose the best balance of quality, latency,
and cost for your scientific applications.

Supported Backends
------------------

- **ElevenLabs** - High-quality commercial TTS with natural voices (paid)
- **LuxTTS** - Open-source offline TTS with voice cloning support
- **Google TTS (gTTS)** - Free cloud-based TTS (requires internet)
- **System TTS (pyttsx3)** - Offline TTS using system espeak or SAPI5

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/scitex_audio

Quick Example
-------------

.. code-block:: python

   from scitex_audio import speak, get_tts

   # Simple usage
   speak("Hello, this is a test of text-to-speech!")

   # Advanced usage with specific backend
   tts = get_tts("luxtts")
   tts.speak("Custom voice synthesis")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
