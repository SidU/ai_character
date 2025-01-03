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
   git clone https://github.com/yourusername/ai_character.git
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
   export ELEVENLABS_API_KEY="your-api-key"

   # On Windows:
   set OPENAI_API_KEY=your-api-key
   set ELEVENLABS_API_KEY=your-api-key
   ```

## Quick Start

1. Create a configuration file `config.yaml` for your character:
   ```yaml
   system_prompt: "You're Skullton, a playful and spooky toy skeleton with a mischievous streak. 
                  Engage with users in a way that's fun, a little eerie, but always friendly."
   voice_id: "your-elevenlabs-voice-id"
   greetings:
     - "Boo! Did I scare you? Just kidding!"
     - "Welcome to my spooky corner!"
   enable_vision: true
   model: "gpt-4-vision-preview"
   ```

2. Run the test script to start interacting with your character:
   ```bash
   python test_local.py
   ```

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
from ai_character import AICharacter

# Initialize with basic configuration
config = {
    'system_prompt': 'You are a helpful assistant.',
    'voice_id': 'your-voice-id',
    'model': 'gpt-4o-mini'
}

character = AICharacter(config)

# Basic conversation loop
try:
    # Get user input
    user_input = character.listen()
    
    # Generate and speak response
    response = character.think_response(user_input)
    character.speak(response)
finally:
    character.cleanup()
```

### Advanced Usage
```python
from ai_character import AICharacter

# Initialize with advanced configuration
config = {
    'system_prompt': 'You are a storytelling assistant.',
    'voice_id': 'your-voice-id',
    'model': 'gpt-4-vision-preview',
    'enable_vision': True,
    'sampling_rate': 44100,
    'silence_threshold': 15,
    'enable_lonely_sounds': True
}

character = AICharacter(config, debug=True)

try:
    # Custom greeting
    character.speak("Let me tell you a story...")
    
    # Process image and voice input
    image_path = "example.jpg"
    user_input = character.listen()
    response = character.think_response(user_input, image=image_path)
    character.speak(response)
finally:
    character.cleanup()
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
git clone https://github.com/yourusername/ai_character.git

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
flake8
```

### Code Style
- Follow PEP 8 guidelines
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