import requests

def get_external_ip():
    try:
        # Google Cloud metadata server URL for external IP
        metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip"
        headers = {"Metadata-Flavor": "Google"}

        # Make a request to the metadata server
        response = requests.get(metadata_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error fetching external IP: {e}")
        return None

def get_internal_ip():
    try:
        # Google Cloud metadata server URL for internal IP
        metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip"
        headers = {"Metadata-Flavor": "Google"}

        # Make a request to the metadata server
        response = requests.get(metadata_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error fetching internal IP: {e}")
        return None
    