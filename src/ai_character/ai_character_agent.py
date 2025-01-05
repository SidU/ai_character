import argparse, sys, time, yaml, threading
from ai_character import AICharacter

class AICharacterAgent:
    def __init__(self, config_path, debug=False):
        self.config = self._load_config(config_path)
        self.debug = debug
        
        # Add detailed display instructions to system prompt if not present
        if 'system_prompt' in self.config:
            display_instructions = (
                "\nYou can display text on screen by wrapping it in display tags like this: "
                "<display>Text to show on screen</display>. "
                "\nUse display tags in these situations:"
                "\n1. For trivia questions, show the question and options:"
                "\n   <display>"
                "\n   What is the capital of France?"
                "\n   A) London"
                "\n   B) Paris"
                "\n   C) Berlin"
                "\n   D) Madrid"
                "\n   </display>"
                "\n2. For key information or summaries:"
                "\n   <display>"
                "\n   Current Topic: Climate Change"
                "\n   Key Points:"
                "\n   - Global temperatures rising"
                "\n   - Sea levels increasing"
                "\n   - Action needed now"
                "\n   </display>"
                "\n3. For data, statistics, or lists:"
                "\n   <display>"
                "\n   Temperature: 72°F"
                "\n   Humidity: 45%"
                "\n   Wind: 5mph NW"
                "\n   </display>"
                "\nAlways try to provide a concise display summary of your responses when appropriate."
            )
            self.config['system_prompt'] += display_instructions
        
        self.character = AICharacter(config=self.config, debug=debug)
        self.character.add_speaking_callback(self._on_speaking_state_changed)
        self.character.add_speaking_done_callback(self._on_speaking_done)
        self.running = True
        self._speaking_done = threading.Event()
        
        # Add display-related attributes
        self.current_display = None
        self.on_display_callbacks = []

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _on_speaking_state_changed(self, is_speaking):
        if is_speaking:
            if self.debug:
                print("\nCharacter is speaking...", end='', flush=True)
                print(f"\nCurrent response: {self.character.current_response[:50]}..." if self.character.current_response else "None")
            self._speaking_done.clear()

    def _on_speaking_done(self):
        if self.debug:
            print("\nCharacter finished speaking!")
            print(f"Current response cleared: {self.character.current_response is None}")
        self._speaking_done.set()

    def add_display_callback(self, callback):
        """Add a callback to be called when display content changes."""
        self.on_display_callbacks.append(callback)

    def _update_display(self, text):
        """Update current display and notify callbacks."""
        self.current_display = text
        for callback in self.on_display_callbacks:
            callback(text)

    def _extract_display_content(self, response):
        """Extract display content from response and return modified response."""
        import re
        display_pattern = r'<display>(.*?)</display>'
        
        # Find all display tags
        display_matches = re.findall(display_pattern, response, re.DOTALL)
        
        # Remove display tags from response
        clean_response = re.sub(display_pattern, '', response)
        
        # Update display with last display tag content (if any)
        if display_matches:
            self._update_display(display_matches[-1].strip())
        
        return clean_response.strip()

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
                    print(f"Current display: {self.current_display}")

                user_input = self.character.listen()

                if user_input:
                    if self.debug:
                        print("\nThinking...", end='', flush=True)
                    response = self.character.think_response(user_input)
                    if response:
                        # Extract display content before speaking
                        clean_response = self._extract_display_content(response)
                        self.character.speak(clean_response)
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
