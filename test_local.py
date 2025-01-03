from ai_character import AICharacter
import os
import yaml

def load_config(file_path='config.yaml'):
    """Load configuration from YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Load configuration from YAML
    config = {
        'duration': 1,
        'sampling_rate': 16000,
        'num_channels': 1,
        'dtype': 'int16',
        'silence_threshold': 10,
        'silence_count_threshold': 10,
        'ambient_noise_level_threshold_multiplier': 3.0,
        'max_file_size_bytes': 26214400,
        'enable_lonely_sounds': False,
        'enable_squeak': False,
        'system_prompt': "You're Skullton, a playful and spooky toy skeleton with a mischievous streak. "
                        "Engage with users in a way that's fun, a little eerie, but always friendly and "
                        "kid-appropriate. Add a dash of skeletal humor and keep the mood lighthearted and silly.",
        'voice_id': "FL5NzwE3soEvgUUAktfG",
        'greetings': [
            "Boo! Did I scare you? Just kidding—Skullton here to make you laugh!",
            "Welcome to my spooky corner! I promise not to rattle your bones… too much.",
            "Ah, a new friend! Let's shake things up… or just shake, since I'm all bones.",
            "Who's ready for some bone-chilling fun? Don't worry, I'm more goofy than scary.",
            "Step right up! Skullton's here to bring you some laughs from beyond the grave!",
            "Looking for a spooky friend? I'm your guy—just don't lose your head!",
            "Skeletons like me don't have hearts, but I'm all about the laughs!",
            "Ready to rattle and roll? Let's have some fun, bone-buddy!",
            "You seem brave! Let's see if you can keep up with my spooky jokes.",
            "Knock, knock! Who's there? Just me, your friendly neighborhood skeleton!"
        ],
        'enable_vision': True,
        'model': 'gpt-4o-mini'
    }

    # Create character instance
    character = AICharacter(config, debug=True)

    try:
        # Test greeting
        print("\n=== Testing Skullton's Greeting ===")
        character.say_greeting()
        input("\nPress Enter after greeting completes...")

        # Test conversation
        print("\n=== Starting Conversation with Skullton ===")
        print("Speak something (or press Ctrl+C to exit)")
        while True:
            # Listen for input
            user_input = character.listen()
            if user_input:
                print(f"\nYou said: {user_input}")
                
                # Generate response
                response = character.think_response(user_input)
                if response:
                    print(f"Skullton's response: {response}")
                    character.speak(response)

    except KeyboardInterrupt:
        print("\n\nExiting... Thanks for chatting with Skullton!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        character.cleanup()

if __name__ == "__main__":
    main()