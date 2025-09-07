import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def hash_content(content):
    return hashlib.sha256(content).hexdigest()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("Mindfully collecting images from the web\n")

    # Accept multiple URLs (comma-separated)
    urls = input("Enter image URLs (separate multiple URLs with commas): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]

    # Create folder if not exists
    os.makedirs("Fetched_Images", exist_ok=True)

    # Track seen files by their hash to prevent duplicates
    seen_hashes = set()

    for url in urls:
        try:
            # Validate URL format (must start with http/https)
            if not url.startswith(("http://", "https://")):
                print(f"✗ Skipped invalid URL: {url}")
                continue
                
# Request the image (stream=True avoids preloading large files into memory)
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Check headers
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length")

        # Ensure content is an image
            if not content_type.startswith("image/"):
                print(f"✗ Skipped (not an image): {url}")
                continue
         # Enforce a maximum size limit (10 MB in this example)
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10 MB limit
                print(f"✗ Skipped (file too large): {url}")
                continue
                
        # Download full content into memory
            content = response.content

            # Generate a hash to detect duplicates
            content_hash = hash_content(content)

            if content_hash in seen_hashes:
                print(f"✗ Skipped duplicate: {url}")
                continue

            seen_hashes.add(content_hash)
            
          # Extract filename or assign default
            filename = get_filename_from_url(url)
            filepath = os.path.join("Fetched_Images", filename)

            # Save image locally
            with open(filepath, "wb") as f:
                f.write(content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
        except Exception as e:
            print(f"✗ Error for {url}: {e}")

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()

