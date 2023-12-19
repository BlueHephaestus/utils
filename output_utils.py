from contextlib import contextmanager
import sys, os

@contextmanager
def silent():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        except:
            pass
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

if __name__ == "__main__":
    # Example usage:
    print("heyo")
    with silent():
        # Code inside this block will not produce any visible output
        print("This will not be displayed")
        # Any exceptions raised will not be displayed either
        1 / 0

    # Output is restored outside the context manager
    print("Output is back to normal")
