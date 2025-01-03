import argparse, sys, time, yaml, threading
from ai_character import AICharacter

class AICharacterAgent:
    def __init__(self, config_path, debug=False):
        self.config = self._load_config(config_path)
        self.character = AICharacter(config=self.config, debug=debug)
        self.character.add_speaking_callback(self._on_speaking_state_changed)
        self.character.add_speaking_done_callback(self._on_speaking_done)
        self.running = True
        self._speaking_done = threading.Event()  # Add this for synchronization

    def _load_config(self, config_path):
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _on_speaking_state_changed(self, is_speaking):
        """Handle character speaking state changes."""
        if is_speaking:
            print("\nCharacter is speaking...", end='', flush=True)
            self._speaking_done.clear()

    def _on_speaking_done(self):
        """Handle when character completely finishes speaking."""
        print("\nCharacter finished speaking!")
        self._speaking_done.set()

    def run(self):
        """Run the main interaction loop."""
        try:
            # Say greeting before first listen
            self.character.say_greeting()
            self._speaking_done.wait()  # Wait for greeting to complete

            while self.running:
                # Make sure any previous speaking is done before listening again
                self._speaking_done.wait()
                
                # Listen for user input
                print("\nListening...", end='', flush=True)
                user_input = self.character.listen()
                
                if user_input:
                    # Process and respond
                    print("\nThinking...", end='', flush=True)
                    response = self.character.think_response(user_input)
                    
                    if response:
                        self.character.speak(response)
                        self._speaking_done.wait()
                
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                
        except KeyboardInterrupt:
            print("\nStopping character interaction...")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        self.character.cleanup()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()
    agent = AICharacterAgent(args.config, args.debug)
    try:
        agent.run()
    except KeyboardInterrupt:
        pass
    agent.stop()
