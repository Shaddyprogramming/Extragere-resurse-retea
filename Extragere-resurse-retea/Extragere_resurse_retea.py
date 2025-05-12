import urllib.request  # Importing urllib for HTTP requests
from itertools import islice # Importing islice for efficient slicing
from xmlrpc.client import boolean  # Importing islice for efficient slicing
from selectolax.parser import HTMLParser  # Importing selectolax for HTML parsing
from concurrent.futures import ThreadPoolExecutor  # Added for parallel processing

# I compared this with lxml and BeautifulSoup, and selectolax is faster for this use case
# Benchmark suggests that selectolax is faster than BeautifulSoup with around 35% in crawling and parsing time
# Benchmark suggests that selectolax is faster than lxml with around 55% in crawling and parsing time

PAGE:str="https://en.wikipedia.org/wiki/Main_Page" # Global variable for the main page URL
SUB_PAGE:str="https://en.wikipedia.org" # Global variable for the sub-page URL
COUNT:int=100 # Global variable for the maximum number of links to extract
WRITING:boolean=True # Global variable for printing the results
WORKERS:int=10  # Number of parallel workers for crawling (OPTIMAL IS 10)


def get_page(max_links: int = 100) -> tuple[list, list]:
    """
    Get the necessary links and images from a page.

    :param max_links: Maximum number of links to extract
    :return: Tuple containing a list of links and a list of images
    """
    html_content = crawl_page("https://en.wikipedia.org/wiki/Main_Page")  # crawls the main page

    links = parse_pages(html_content, max_links)  # parse the links from the main page

    images = images_page(html_content)  # parse the images from the main page
    
    def fetch_images(link): # Fetch images from a given link
        try:
            return images_page(crawl_page(link)) # crawl the link and parse images
        except Exception:
            return []

    with ThreadPoolExecutor(max_workers=WORKERS) as executor: # Create a thread pool for parallel processing
        all_images_lists = list(executor.map(fetch_images, links)) # Map the fetch_images function to the links
    
    all_images = [img for img_list in all_images_lists for img in img_list if img] # Flatten the list of lists and filter out empty images

    images.extend(all_images)  # extend the images list with all_images

    return links, images  # return the links and images


def crawl_page(page:str=PAGE)->str:
    """
    Download HTML content from the page using optimized settings

    :param page: URL of the page to crawl
    :return: HTML content of the page
    """
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml"} # Set headers to mimic a browser request
    request = urllib.request.Request(page, headers=headers) # Create a request with headers

    try:
        with urllib.request.urlopen(request, timeout=10) as response: # Open the URL with a timeout
            return response.read() # Read the response content
    except Exception as e: # Handle exceptions
        print(f"Error fetching {page}: {str(e)}") # Print the error message
        return ""


def parse_pages(html_content:str, max_links:int=100) ->list:
    """
    Parse the PAGE pages and extract links up to max_links

    :param html_content: HTML content of the page
    :param max_links: Maximum number of links to extract
    :return: List of links
    """
    parser = HTMLParser(html_content) # Parse the HTML content

    limited_nodes = islice((node for node in parser.css('a[href^="/wiki/"]') 
                           if not node.attributes.get("href", "").startswith(("/wiki/File:", "/wiki/Special:", "/wiki/Help:", "/wiki/Talk:"))), 
                          max_links) # limit the number of nodes to max_links and filter out unwanted links

    # Create the links list with full URLs
    links = [
        SUB_PAGE + node.attributes["href"] for node in limited_nodes # Extract href attributes
    ]

    return links # Return the list of links


def images_page(html_content:str) ->str:
    """
    Extract all image URLs from an HTML page

    :param html_content: HTML content of the page
    :return: List of image URLs
    """
    if not html_content:  # Skip processing empty content
        return []
        
    parser = HTMLParser(html_content) # Parse the HTML content
    nodes = parser.css("img[src]") # Extract image nodes with src attributes

    image_urls = [] # Initialize an empty list for image URLs
    for node in nodes:
        src = node.attributes.get("src", "")
        if src.startswith("//"): # Check if the src starts with "//"
            image_urls.append(f"https:{src}") # Add "https:" to the src
        elif src.startswith("/"): # Check if the src starts with "/"
            # Fixed the string literal issue
            image_urls.append(f"{SUB_PAGE}{src}") # Add SUB_PAGE to the src
        elif src: # Check if the src is not empty
            image_urls.append(src) # Add src

    return image_urls


def write_file(file, items)->None:
    """
    Write the extracted items to a file

    :param file: File name to write the items
    :param items: List of items to write to the file
    :return: None
    """
    with open(file, "w", encoding="utf-8") as f: # Open the file in write mode with UTF-8 encoding
        if items: # Check if items is not empty
            for item in items:
                f.write(item)
                f.write("\n")

if __name__ == "__main__": # Main function to execute the script
    
    file_links = "wikipedia_links.txt" # File name for links
    file_images = "wikipedia_images.txt"  # File name for images

    links, images = get_page(COUNT) # Get the links and images from the main page

    write_file(file_links, links) # Write the links to the file
    write_file(file_images, images) # Write the images to the file

    if WRITING: # Check if writing is enabled
        for image in images:
            if image:
                print(image)

########################################################################################################################################
#
# Documentation:
#
# En:
# The code was written to extract network resources from Wikipedia, using selectolax for parsing and urllib to access web pages.
# This implementation is optimized to extract links and images from Wikipedia's main page. The project is configured to extract
# a maximum of 100 links and all images from the page. It is also set up to use 10 execution threads to speed up the image
# extraction process, and these are written to a text file or displayed on screen. All properties are set as global variables
# to be easily modified according to user requirements. The code is structured to be easy to understand and use, with separate
# functions for crawling, parsing, and writing results to files. Parallel execution is used to accelerate the image extraction process.
#
# Bibliography:
# https://www.reddit.com/r/webscraping/comments/znweub/advice_for_scraping_massive_number_of_items_faster/
# https://pypi.org/project/selectolax/
# https://www.youtube.com/watch?v=D4xCGnwjMZQ
# https://www.youtube.com/watch?v=SAueUTQNup8
#
########################################################################################################################################           
               