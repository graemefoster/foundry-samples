# Helper class to log the program execution status
class Logger:
    @staticmethod
    def log_start(name: str):
        print("\n\n--------------------------------------------------------------\n")
        print(f"Starting: {name}")
    
    @staticmethod
    def log_completion(name: str):
        print(f"\nCompleted: {name}")

    def log_result(result):
        print(f"\nResult:\n{result}")