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

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 15 15 15

   * - Backend
     - Quality
     - Cost
     - Internet
     - Offline
     - Default Speed
   * - **ElevenLabs**
     - High
     - Paid
     - Required
     - No
     - 1.2x
   * - **LuxTTS**
     - High
     - Free
     - First download
     - Yes
     - 2.0x
   * - **Google TTS**
     - Good
     - Free
     - Required
     - No
     - 1.5x
   * - **System TTS**
     - Basic
     - Free
     - No
     - Yes
     - 150 wpm

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   quickstart
   backends
   relay
   env_vars

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/scitex_audio
   api/engines
   api/mcp

Quick Example
-------------

.. code-block:: python

   from scitex_audio import speak, available_backends

   # Check what's available
   print(available_backends())  # e.g., ['gtts', 'pyttsx3']

   # Simple usage
   speak("Hello, this is a test of text-to-speech!")

   # Specific backend with speed control
   speak("Fast speech", backend="gtts", speed=1.5)

   # Save to file without playing
   speak("Save this", output_path="output.mp3", play=False)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
