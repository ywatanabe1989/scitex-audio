Remote Audio Relay
==================

When agents run on remote servers (NAS, cloud, HPC), they have no speakers.
The **relay server** solves this: the local machine (with speakers) runs a
lightweight HTTP server, and the remote agent sends speech requests over an
SSH tunnel.

Architecture
------------

.. code-block:: text

   Remote Server (NAS/Cloud)          Local Machine (has speakers)
   ┌─────────────────────┐            ┌──────────────────────┐
   │ AI Agent            │            │ Relay Server         │
   │   speak("Hello")    │            │   scitex-audio relay │
   │     ↓               │            │     ↓                │
   │ POST /speak ────────┼── SSH ─────┼→ TTS engine          │
   │   (port 31293)      │  tunnel    │     ↓                │
   │                     │            │   🔊 Speakers        │
   └─────────────────────┘            └──────────────────────┘

The relay uses port **31293** by default, encoding "sa-i-te-ku-su" (サイテクス)
in Japanese phone keypad mapping.

Setup Guide
-----------

Step 1: Start Relay (Local Machine)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the machine with speakers:

.. code-block:: bash

   scitex-audio relay --port 31293

   # Or with force restart (kills existing process on port)
   scitex-audio relay --port 31293 --force

Step 2: SSH Tunnel
~~~~~~~~~~~~~~~~~~

Add ``RemoteForward`` to your ``~/.ssh/config`` on the local machine:

.. code-block:: text

   Host my-server
     HostName 192.168.0.69
     User myuser
     RemoteForward 31293 127.0.0.1:31293   # Audio relay

Then connect normally: ``ssh my-server``. The tunnel maps the remote server's
port 31293 back to your local relay server.

Step 3: Configure Remote Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the remote server, set:

.. code-block:: bash

   export SCITEX_AUDIO_MODE=remote
   export SCITEX_AUDIO_RELAY_PORT=31293

Now ``speak("Hello")`` on the remote server plays audio on your local speakers.

Relay Endpoints
---------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - ``/speak``
     - POST
     - Play TTS (``{"text": "...", "backend": "gtts"}``)
   * - ``/health``
     - GET
     - Health check (returns ``{"status": "ok"}``)
   * - ``/list_backends``
     - GET
     - List available backends on the relay host

Mode Resolution
---------------

The ``SCITEX_AUDIO_MODE`` variable controls routing:

- **``auto``** (default): Checks local audio availability. If audio sink is
  suspended/unavailable and a relay URL is detected, routes to relay.
  Otherwise uses local.
- **``local``**: Always use local TTS engine and speakers. Fails if no audio.
- **``remote``**: Always send speech to relay server. Fails if relay unreachable.

Auto-Start Relay (Shell Profile)
---------------------------------

Add to ``~/.bashrc`` on your local machine (the one with speakers):

.. code-block:: bash

   _start_audio_relay() {
       local port="${SCITEX_AUDIO_RELAY_PORT:-31293}"
       # Skip if already healthy
       curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && return
       # Kill stale process if port is bound but not responding
       if timeout 1 bash -c "echo >/dev/tcp/127.0.0.1/$port" 2>/dev/null; then
           pkill -f "scitex audio relay" 2>/dev/null || true
           sleep 1
       fi
       # Start relay in background
       scitex-audio relay --port "$port" --force &>/dev/null &
       disown
   }
   _start_audio_relay

Tunnel Validation (Remote Side)
-------------------------------

On the remote server, you can validate the SSH tunnel is active:

.. code-block:: bash

   # Quick TCP check
   timeout 1 bash -c "echo >/dev/tcp/127.0.0.1/31293" 2>/dev/null \
       && echo "Tunnel active" \
       || echo "Tunnel down (reconnect SSH)"

   # Full health check
   curl -sf http://localhost:31293/health && echo "Relay OK"

Cloud Relay (Browser)
---------------------

When running inside a SciTeX Cloud Apptainer container, audio is relayed
to the browser via OSC escape sequences:

.. code-block:: bash

   export SCITEX_CLOUD=true

The speech flows through: PTY → WebSocket → browser xterm.js → ``speakText()``.
This mode is automatic when ``SCITEX_CLOUD=true`` is set.
