# cli.py

from core.database import DatabaseManager


def main():
    print("Fantasy RAG CLI")
    print("Type 'exit', 'quit', or press Ctrl+C to stop")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            question = input("\nYour question: ")
            
            # Check for exit commands
            if question.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            # Skip empty input
            if not question.strip():
                continue
            
            # Process the question (placeholder for now)
            print(f"You asked: {question}")
            database = DatabaseManager()
            content = database.search(question)
            
            print(f"Search results: {content}")
            
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\n\nGoodbye!")
            break
        except EOFError:
            # Handle Ctrl+D
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()