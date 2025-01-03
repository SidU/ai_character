import pytest
from ai_character import AICharacter

def test_character_initialization():
    config = {
        # Required parameters
        'sampling_rate': 44100,
        'num_channels': 1,
        'dtype': 'float32',
        'silence_threshold': 0.1,
        'ambient_noise_level_threshold_multiplier': 1.2,
        'max_file_size_bytes': 10485760,  # 10MB
        'enable_squeak': False,
        'system_prompt': 'You are a test assistant.',
        'voice_id': 'test-voice-id',
        'greetings': ['Hello!', 'Hi there!'],
        'enable_vision': False,
        'silence_count_threshold': 30,
        'model': 'gpt-4',
        
        # Optional parameters
        'character_closed_mouth': None,
        'character_open_mouth': None,
        'max_message_history': 20
    }
    
    character = AICharacter(config)
    assert character is not None
    assert character.system_prompt == 'You are a test assistant.'
    assert character.sampling_rate == 44100
    assert character.num_channels == 1

def test_cleanup():
    config = {
        'sampling_rate': 44100,
        'num_channels': 1,
        'dtype': 'float32',
        'silence_threshold': 0.1,
        'ambient_noise_level_threshold_multiplier': 1.2,
        'max_file_size_bytes': 10485760,  # 10MB
        'enable_squeak': False,
        'system_prompt': 'You are a test assistant.',
        'voice_id': 'test-voice-id',
        'greetings': ['Hello!', 'Hi there!'],
        'enable_vision': False,
        'silence_count_threshold': 30,
        'model': 'gpt-4',
        'character_closed_mouth': None,
        'character_open_mouth': None,
        'max_message_history': 20
    }
    character = AICharacter(config)
    
    # Store some messages in the history before cleanup
    character.messages.append({"role": "user", "content": "Hello"})
    character.messages.append({"role": "assistant", "content": "Hi there"})
    
    character.cleanup()
    
    # Assert that cleanup cleared the messages
    assert len(character.messages) == 0
    
    # Additional assertions for other state
    assert not hasattr(character, 'audio_stream') or character.audio_stream is None
    assert not hasattr(character, 'recording') or not character.recording