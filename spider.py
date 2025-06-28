#!/usr/bin/env python3
"""
Spider - Web Image Downloader
by abderrafie
"""
import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def is_valid_image(url):
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if any(url.lower().endswith(ext) for ext in extensions):
        return True
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    if any(path.endswith(ext) for ext in extensions):
        return True
    return False

def download_file(url, path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
        
            if not filename or not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
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
            print(f"{Fore.GREEN}   ✓ {Style.BRIGHT}{filename}")
        else:
            print(f"{Fore.RED}   ✗ Failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}   ✗ Error: {e}")

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
            if parsed_url.netloc == base_domain.netloc:
                links.add(absolute_url)
                
        return links
    except Exception as e:
        print(f"{Fore.RED}✗ Failed to get links: {e}")
        return set()

def spider(url, recursive, max_depth, path, current_depth=1):
    if current_depth > max_depth:
        return
        
    # Nice scraping indicator
    if current_depth == 1:
        print(f"{Fore.CYAN}🕷️  {Style.BRIGHT}Scraping images... {Fore.YELLOW}{url}")
    else:
        print(f"{Fore.CYAN}   └─ {Style.DIM}Depth {current_depth}: {url}")
    
    if is_valid_image(url):
        print(f"{Fore.MAGENTA}🖼️  Direct image URL detected")
        download_file(url, path)
        return
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images_found = 0
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            if is_valid_image(img_url):
                download_file(img_url, path)
                images_found += 1
        
        if images_found > 0:
            print(f"   {Fore.GREEN}🖼️  Found {images_found} images")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
    
    if recursive and current_depth < max_depth:
        base_domain = urlparse(url)
        links = get_links(url, base_domain)
        
        for link in links:
            spider(link, recursive, max_depth, path, current_depth + 1)

def main():
    parser = argparse.ArgumentParser(description='Spider by abderrafie - website image downloader')
    parser.add_argument('url', help='URL to process')
    parser.add_argument('-r', action='store_true', help='Recursive download')
    parser.add_argument('-l', type=int, default=5, help='Maximum depth level for recursive download')
    parser.add_argument('-p', default='./data/', help='Path to save downloaded files')
    
    args = parser.parse_args()
    os.makedirs(args.p, exist_ok=True)
    
    spider(args.url, args.r, args.l, args.p)
    print(f"{Fore.GREEN}🎉 {Style.BRIGHT}Download completed! Images saved to: {Fore.YELLOW}{args.p}")

if __name__ == '__main__':
    main()