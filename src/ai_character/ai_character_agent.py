import argparse, sys, time, yaml, threading
from ai_character import AICharacter

class AICharacterAgent:
    def __init__(self, config_path, debug=False):
        self.config = self._load_config(config_path)
        self.debug = debug
        self.character = AICharacter(config=self.config, debug=debug)
        self.character.add_speaking_callback(self._on_speaking_state_changed)
        self.character.add_speaking_done_callback(self._on_speaking_done)
        self.running = True
        self._speaking_done = threading.Event()

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _on_speaking_state_changed(self, is_speaking):
        # If debug, print transitions
        if is_speaking:
            if self.debug:
                print("\nCharacter is speaking...", end='', flush=True)
            self._speaking_done.clear()

    def _on_speaking_done(self):
        # If debug, print completion message
        if self.debug:
            print("\nCharacter finished speaking!")
        self._speaking_done.set()

    def run(self):
        """Run the main interaction loop."""
        try:
            # Say greeting before first listen
            self.character.say_greeting()
            self._speaking_done.wait()  # Wait for greeting to complete

            while self.running:
                self._speaking_done.wait()  # Ensure any previous speech is done

                if self.debug:
                    print("\nListening...", end='', flush=True)
                user_input = self.character.listen()

                if user_input:
                    if self.debug:
                        print("\nThinking...", end='', flush=True)
                    response = self.character.think_response(user_input)
                    if response:
                        self.character.speak(response)
                        self._speaking_done.wait()

                time.sleep(0.1)

        except KeyboardInterrupt:
            if self.debug:
                print("\nStopping character interaction...")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        self.character.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    agent = AICharacterAgent(args.config, args.debug)
    try:
        agent.run()
    except KeyboardInterrupt:
        pass
    agent.stop()
