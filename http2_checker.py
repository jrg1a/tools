import requests

def check_http2_support(url):
    try:
        # Make a request to the provided URL
        response = requests.get(url, stream=True)
        
        # Check if the response used HTTP/2
        if response.raw.version == 11:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Ask the user for the website URL
    url = input("Enter the website URL (e.g., https://example.com): ")
    
    # Check if the website supports HTTP/2
    if check_http2_support(url):
        print(f"{url} supports HTTP/2!")
    else:
        print(f"{url} does not support HTTP/2.")

