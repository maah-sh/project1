import time
import os

def log_function_run_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        run_time = time.time() - start_time

        file_path = "log/function_runtime_log.txt"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "a") as f:
            f.write("function_name: " + func.__name__  + " runtime: " + str(run_time) + " seconds \n")

        return result
    
    return wrapper