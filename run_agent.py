import argparse, sys
from ai_character import AICharacterAgent

class ConsoleDisplayAgent(AICharacterAgent):
    def __init__(self, config_path, debug=False):
        super().__init__(config_path, debug)
        self.add_display_callback(self._show_display)
        
    def _show_display(self, text):
        if text:
            print("\n┌─────────── Display ───────────┐")
            for line in text.split('\n'):
                print("│ " + line.ljust(28) + " │")
            print("└────────────────────────────┘\n")

def main():
    parser = argparse.ArgumentParser(description="Runner for AICharacterAgent")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--debug", action="store_true", help="Enable debug")
    args = parser.parse_args()

    agent = ConsoleDisplayAgent(args.config, debug=args.debug)
    try:
        agent.run()
    except KeyboardInterrupt:
        agent.stop()
        print("\nStopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
