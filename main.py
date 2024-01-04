"""
This script is the main executable, calling the main_module_function which does
the rest of the work.
"""

# Import the main package
import csvfilter


def run():
    csvfilter.main_module_function()


# Run the function if this is the main file executed
if __name__ == "__main__":
    run()
