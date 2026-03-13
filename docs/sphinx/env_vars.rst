Environment Variables
=====================

All environment variables are optional. The defaults provide sensible behavior
for local usage.

Audio Routing
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Variable
     - Default
     - Description
   * - ``SCITEX_AUDIO_MODE``
     - ``auto``
     - Audio mode: ``local``, ``remote``, or ``auto``
   * - ``SCITEX_AUDIO_RELAY_URL``
     - *(auto)*
     - Full relay URL (e.g., ``http://localhost:31293``)
   * - ``SCITEX_AUDIO_RELAY_HOST``
     - *(none)*
     - Relay host (combined with port to build URL)
   * - ``SCITEX_AUDIO_RELAY_PORT``
     - ``31293``
     - Relay server port
   * - ``SCITEX_AUDIO_HOST``
     - ``0.0.0.0``
     - Relay server bind host

Backend Configuration
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Variable
     - Default
     - Description
   * - ``SCITEX_AUDIO_ELEVENLABS_API_KEY``
     - *(none)*
     - ElevenLabs API key for premium TTS
   * - ``ELEVENLABS_API_KEY``
     - *(none)*
     - Alternative ElevenLabs API key variable

General
-------

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Variable
     - Default
     - Description
   * - ``SCITEX_DIR``
     - ``~/.scitex``
     - Base directory for audio cache and reference files
   * - ``SCITEX_CLOUD``
     - *(none)*
     - Set to ``true`` for browser relay mode (OSC escape)

Port Convention
---------------

The default port **31293** encodes "sa-i-te-ku-su" (サイテクス) in Japanese
phone keypad mapping. Other SciTeX ports follow the same scheme:

.. list-table::
   :header-rows: 1
   :widths: 15 50

   * - Port
     - Service
   * - 31291
     - crossref-local API
   * - 31292
     - openalex-local API
   * - 31293
     - Audio relay
   * - 31294
     - scitex-cloud staging

Example Shell Configuration
----------------------------

.. code-block:: bash

   # Local machine (has speakers)
   export SCITEX_AUDIO_MODE=local
   export SCITEX_AUDIO_RELAY_PORT=31293

   # Remote server (no speakers, uses SSH tunnel)
   export SCITEX_AUDIO_MODE=remote
   export SCITEX_AUDIO_RELAY_PORT=31293

   # ElevenLabs (optional, for premium quality)
   export SCITEX_AUDIO_ELEVENLABS_API_KEY="your-key-here"
