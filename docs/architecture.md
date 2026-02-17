# System Architecture

The Jarvis OS Simulator follows a modular design pattern to separate the assistant's personality and automation from the technical Operating System simulations.

## 🧱 Component Breakdown

### 1. Voice Interaction (`src/voice/`)

Handles the sensory inputs and outputs.

- `speech_input.py`: Listens to user voice via Microphone.
- `speech_output.py`: Speaks back to the user.

### 2. Core Brain (`src/core/`)

- `assistant.py`: Defines the conversational personality.
- `command_router.py`: Paradoxically the "CPU" of the assistant, routing user strings to specific logic.

### 3. OS Simulator (`src/os_simulator/`)

A dedicated sandbox for academic OS concepts.

- `scheduling/`: Multiple algorithms (RR, FCFS, etc.) with visualization.
- `memory_management/`: (Planned) Simulations for paging and segmentation.
- `deadlock/`: (Planned) Resource allocation and detection.

### 4. Integration Layers (`src/automation/`, `src/apis/`)

External world interaction.

- `automation/`: Direct OS interactions (files, apps, messaging).
- `apis/`: Third-party data fetching (WolframAlpha, Wikipedia).
