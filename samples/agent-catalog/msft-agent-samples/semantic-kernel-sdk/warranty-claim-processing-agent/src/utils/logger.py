# Helper class to log the steps of the pipeline execution
class Logger:
    @staticmethod
    def log_step_start(step_name):
        print("\n\n--------------------------------------------------------------\n")
        print(f"Starting step: {step_name}")
    
    @staticmethod
    def log_step_completion(step_name):
        print(f"\nCompleted step: {step_name}")

    def log_step_result(result):
        print(f"\nStep result:\n{result}")