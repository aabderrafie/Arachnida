#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_image(url):
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # Check if URL ends with image extension
    if any(url.lower().endswith(ext) for ext in extensions):
        return True
    
    # For URLs with query parameters, check the path part
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    if any(path.endswith(ext) for ext in extensions):
        return True
    
    # Special case for common image hosting services
    image_hosts = ['images.unsplash.com', 'i.imgur.com', 'upload.wikimedia.org']
    if any(host in url.lower() for host in image_hosts):
        return True
    
    return False

def download_file(url, path):
    """Download a file from URL to specified path"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Extract filename from URL, handling query parameters
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # If no filename or extension, generate one
            if not filename or not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                # Try to get extension from content-type header
                content_type = response.headers.get('content-type', '')
                ext = '.jpg'  # default
                if 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'bmp' in content_type:
                    ext = '.bmp'
                
                filename = f"image_{hash(url) % 100000}{ext}"
            
            filepath = os.path.join(path, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def get_links(url, base_domain):
    """Extract all links from a webpage that belong to the same domain"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            parsed_url = urlparse(absolute_url)
            
            # Only include links from the same domain
            if parsed_url.netloc == base_domain.netloc:
                links.add(absolute_url)
                
        return links
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return set()

def spider(url, recursive, max_depth, path, current_depth=1):
    if current_depth > max_depth:
        return
        
    print(f"Processing: {url} (depth: {current_depth})")
    
    # Check if the URL is a direct image link
    if is_valid_image(url):
        print(f"Direct image URL detected: {url}")
        download_file(url, path)
        return
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            if is_valid_image(img_url):
                download_file(img_url, path)
    except Exception as e:
        print(f"Error processing images at {url}: {e}")
    
    if recursive and current_depth < max_depth:
        base_domain = urlparse(url)
        links = get_links(url, base_domain)
        
        for link in links:
            spider(link, recursive, max_depth, path, current_depth + 1)

def main():
    parser = argparse.ArgumentParser(description='Spider - website image downloader')
    parser.add_argument('url', help='URL to process')
    parser.add_argument('-r', action='store_true', help='Recursive download')
    parser.add_argument('-l', type=int, default=5, help='Maximum depth level for recursive download')
    parser.add_argument('-p', default='./data/', help='Path to save downloaded files')
    
    args = parser.parse_args()
    os.makedirs(args.p, exist_ok=True)
    
    spider(args.url, args.r, args.l, args.p)
    print(f"Download completed. Images saved to: {args.p}")

if __name__ == '__main__':
    main()