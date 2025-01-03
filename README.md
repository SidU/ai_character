# AI Character Framework

A powerful Python framework for creating interactive AI characters with voice capabilities. Create engaging, personality-driven AI agents that can listen, think, and speak in real-time conversations.

## Features

- 🎙️ **Real-time Voice Interaction** - Seamless audio input processing with noise detection
- 🤖 **AI-Powered Conversations** - Leverages advanced language models for natural dialogue
- 🗣️ **Text-to-Speech** - High-quality voice synthesis with customizable voices
- 👀 **Vision Capabilities** - Optional image understanding and processing
- ⚙️ **Flexible Configuration** - Easy YAML-based character customization
- 🎭 **Personality Engine** - Create unique character personalities through system prompts
- 🔊 **Advanced Audio Processing** - Intelligent silence detection and ambient noise handling
- 📦 **Modular Design** - Easy to extend and customize for different use cases

## Prerequisites

Before installing the AI Character Framework, ensure you have:

- Python 3.10 or higher
- A virtual environment tool (like `venv` or `conda`)
- An API key for your chosen language model (e.g., OpenAI)
- A voice provider API key (e.g., ElevenLabs)
- PyAudio dependencies (for audio processing)
  - On Ubuntu/Debian: `sudo apt-get install python3-pyaudio`
  - On macOS: `brew install portaudio`
  - On Windows: No additional installation needed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sidu/ai_character.git
   cd ai_character
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # On Unix/macOS:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   # On Unix/macOS:
   export OPENAI_API_KEY="your-api-key"
   export ELEVEN_API_KEY="your-api-key"

   # On Windows:
   set OPENAI_API_KEY=your-api-key
   set ELEVEN_API_KEY=your-api-key
   ```

## Quick Start with `AICharacterAgent`

To quickly get up and running, use the **`AICharacterAgent`** class, which provides a simple, batteries-included experience (listen → think → speak loop, greeting support, and callbacks).

1. **Create a config file** (e.g., `config.yaml`):
   ```yaml
   system_prompt: "You are Skullton, a playful skeleton with a mischievous streak."
   voice_id: "your-elevenlabs-voice-id"
   greetings:
     - "Boo! Did I scare you?"
     - "Welcome to my spooky corner!"
   enable_vision: false
   model: "gpt-4o-mini"
   sampling_rate: 16000
   silence_threshold: 10.0
   silence_count_threshold: 10

2. Run the agent script to start interacting with your character:
   ```bash
   python run_agent.py --config ghost.yaml --debug 
   ```

* The agent will speak a greeting, then listen for your voice input.
* It will generate a response using your chosen language model and speak it aloud.

## Configuration

### Basic Configuration
The framework uses YAML configuration files to define character behavior. Here's what each core setting does:

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `system_prompt` | Defines the character's personality and behavior | None | Yes |
| `voice_id` | ElevenLabs voice ID for speech synthesis | None | Yes |
| `greetings` | List of possible greeting messages | [] | No |
| `enable_vision` | Enable image processing capabilities | false | No |
| `model` | Language model to use (e.g., gpt-4-vision-preview) | "gpt-4" | No |

### Advanced Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `duration` | Recording duration in seconds | 1 |
| `sampling_rate` | Audio sampling rate | 16000 |
| `num_channels` | Number of audio channels | 1 |
| `silence_threshold` | Threshold for silence detection | 10 |
| `silence_count_threshold` | Required silent frames to stop recording | 10 |
| `ambient_noise_level_threshold_multiplier` | Noise detection sensitivity | 3.0 |
| `max_file_size_bytes` | Maximum audio file size | 26214400 |
| `enable_lonely_sounds` | Enable ambient character sounds | false |
| `enable_squeak` | Enable interaction sounds | false |

## Usage Examples

### Basic Usage
```python
from ai_character import AICharacterAgent

# Initialize agent with config file
agent = AICharacterAgent("config.yaml", debug=False)

# Run the agent (this handles the listen → think → speak loop)
try:
    agent.run()
except KeyboardInterrupt:
    agent.stop()
```

### Advanced Usage
This advanced example demonstrates how to extend the `AICharacterAgent` class to control physical hardware (like a robot). Key features shown:

- **Hardware Integration**: Shows how to coordinate AI responses with physical movements
- **State Management**: Demonstrates proper handling of robot positions and states
- **Event Handling**: Uses the speaking callbacks to synchronize mouth movements with speech
- **Resource Management**: Proper initialization and cleanup of hardware resources
- **Custom Behaviors**: Adds gesture system that responds to specific keywords in conversation

You can use this pattern to create your own specialized agents, such as:
- Robot characters with servo motors
- Virtual avatars with animated expressions
- Smart home characters that control IoT devices
- Game characters with in-game actions

```python
from ai_character import AICharacterAgent
import time

class RobotCharacterAgent(AICharacterAgent):
    def __init__(self, config_path, debug=False):
        super().__init__(config_path, debug)
        self.motor_enabled = True
        # Initialize your robot's hardware here
        
    def _on_speaking_state_changed(self, is_speaking):
        super()._on_speaking_state_changed(is_speaking)
        if is_speaking:
            # Move robot's mouth when speaking
            self._move_mouth(True)
        else:
            self._move_mouth(False)
    
    def _move_mouth(self, open):
        if self.motor_enabled:
            if self.debug:
                print(f"\nMoving mouth {'open' if open else 'closed'}")
            # Add your motor control code here
            
    def run(self):
        """Custom run loop with additional robot behaviors"""
        try:
            # Initialize robot position
            self._move_to_ready_position()
            
            # Say greeting with gesture
            self._wave_hand()
            self.character.say_greeting()
            self._speaking_done.wait()

            while self.running:
                self._speaking_done.wait()

                if self.debug:
                    print("\nListening and watching...", end='', flush=True)
                user_input = self.character.listen()

                if user_input:
                    # Add gesture based on user input
                    if "happy" in user_input.lower():
                        self._do_happy_dance()
                    
                    if self.debug:
                        print("\nProcessing and planning movement...", end='', flush=True)
                    response = self.character.think_response(user_input)
                    
                    if response:
                        # Coordinate speech with movement
                        self._prepare_gesture(response)
                        self.character.speak(response)
                        self._speaking_done.wait()

                time.sleep(0.1)

        except KeyboardInterrupt:
            if self.debug:
                print("\nStopping robot character...")
        finally:
            self._move_to_rest_position()
            self.stop()
    
    def stop(self):
        # Cleanup robot hardware
        if self.motor_enabled:
            self._move_to_rest_position()
        super().stop()
    
    # Robot-specific methods
    def _move_to_ready_position(self):
        if self.debug:
            print("Moving to ready position")
        # Add motor control code
        
    def _move_to_rest_position(self):
        if self.debug:
            print("Moving to rest position")
        # Add motor control code
        
    def _wave_hand(self):
        if self.debug:
            print("Waving hand")
        # Add motor control code
        
    def _do_happy_dance(self):
        if self.debug:
            print("Performing happy dance")
        # Add motor control code
        
    def _prepare_gesture(self, response):
        if self.debug:
            print("Preparing gesture based on response")
        # Add gesture planning code

# Usage example
if __name__ == "__main__":
    robot = RobotCharacterAgent("robot_config.yaml", debug=True)
    try:
        robot.run()
    except KeyboardInterrupt:
        robot.stop()
```

## API Reference

### AICharacter Class

The main class for creating and managing AI characters.

#### Constructor
```python
AICharacter(config: dict, debug: bool = False)
```

#### Core Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `listen()` | Records and transcribes user audio | None | str or None |
| `think_response(user_input: str)` | Generates AI response with rate limiting | user_input: str | str or None |
| `speak(text: str, callback: callable = None)` | Converts text to speech asynchronously | text, optional callback | None |
| `say_greeting()` | Speaks a random greeting from config | None | None |
| `cleanup()` | Cleans up resources | None | None |

#### State Management Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `set_state(new_state: str)` | Updates character's state | new_state |
| `get_speaking_state()` | Returns current speaking status | None |
| `add_speaking_callback(callback: callable)` | Adds speaking state callback | callback |
| `set_volume(volume: float)` | Sets audio volume (0.0 to 1.0) | volume |
| `get_metrics()` | Returns performance metrics | None |

#### States (AICharacterState)
- `IDLE`
- `LISTENING`
- `THINKING`
- `SPEAKING`
- `ERROR`

## Contributing

We welcome contributions to the AI Character Framework! Here's how you can help:

1. **Fork the Repository**
   - Create your feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit your changes (`git commit -m 'Add some AmazingFeature'`)
   - Push to the branch (`git push origin feature/AmazingFeature`)
   - Open a Pull Request

2. **Report Bugs**
   - Open an issue with a clear title and description
   - Include steps to reproduce the bug
   - Add any relevant screenshots or error messages

3. **Suggest Enhancements**
   - Open an issue to discuss new features
   - Explain the use case and benefits
   - Provide examples if possible

### Development Setup

```bash
# Clone your fork
git clone https://github.com/sidu/ai_character.git

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Code Style
- Include docstrings for all functions and classes
- Add type hints where possible
- Write unit tests for new features

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Thanks to OpenAI for their GPT models
- Thanks to ElevenLabs for their text-to-speech technology
- Special thanks to the open-source community for their invaluable tools and libraries:
  - PyAudio for audio processing
  - PyYAML for configuration handling
  - Pygame for sound playback
- Thanks to my wife for letting me test this at night 🙏