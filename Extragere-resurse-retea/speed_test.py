import timeit # Import timeit for measuring execution time
from Extragere_resurse_retea import get_page # Import the get_page function from the main module

def measure_get_page_time(num_runs:int=3, max_links:int=100)->None:
    """Measure the execution time of the get_page function"""
    setup = """
from Extragere_resurse_retea import get_page
"""

    stmt = f"get_page({max_links})" # Statement to be executed
    
    total_time = timeit.timeit(stmt=stmt, setup=setup, number=num_runs) # Measure the execution time
    avg_time = total_time / num_runs # Calculate average time per run
    
    print(f"Getting {max_links} Wikipedia links' images:") # Print the number of links
    print(f"Total time for {num_runs} runs: {total_time:.5f} seconds") # Print total time
    print(f"Average time per run: {avg_time:.5f} seconds") # Print average time per run

if __name__ == "__main__": # Main function to run the script
    measure_get_page_time(num_runs=3, max_links=100) # Measure the execution time of get_page function
