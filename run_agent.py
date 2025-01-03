import argparse, sys
from ai_character import AICharacterAgent

def main():
    parser = argparse.ArgumentParser(description="Runner for AICharacterAgent")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--debug", action="store_true", help="Enable debug")
    args = parser.parse_args()

    agent = AICharacterAgent(args.config, debug=args.debug)
    try:
        agent.run()
    except KeyboardInterrupt:
        agent.stop()
        print("\nStopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
