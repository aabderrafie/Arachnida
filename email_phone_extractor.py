#!/usr/bin/env python3
"""
Email & Phone Extractor - Contact Information Extractor
by abderrafie
"""
import os
import sys
import argparse
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style
import time

# Initialize colorama
init(autoreset=True)

class EmailPhoneExtractor:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Phone number regex patterns (various formats)
        self.phone_patterns = [
            re.compile(r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'),  # International
            re.compile(r'\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}'),  # (XXX) XXX-XXXX
            re.compile(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'),      # XXX-XXX-XXXX
            re.compile(r'\d{3}\.\d{3}\.\d{4}'),                # XXX.XXX.XXXX
            re.compile(r'\d{10}'),                             # XXXXXXXXXX
        ]

    def extract_emails_and_phones(self, text):
        emails = set(self.email_pattern.findall(text))
        phones = set()
        
        for pattern in self.phone_patterns:
            phones.update(pattern.findall(text))
        
        return emails, phones

    def save_to_file(self, data, filename, data_type):
        """Save extracted data to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"=== {data_type.upper()} EXTRACTION RESULTS ===\n\n")
                if data:
                    for item in sorted(data):
                        f.write(f"{item}\n")
                    f.write(f"\nTotal {data_type} found: {len(data)}\n")
                else:
                    f.write(f"No {data_type} found.\n")
            print(f"{Fore.GREEN}✓ {Style.BRIGHT}{data_type.capitalize()} saved successfully!")
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving {data_type}: {e}")

    def get_links(self, url, base_domain):
        """Extract all links from a webpage that belong to the same domain"""
        try:
            response = requests.get(url, timeout=10)
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

    def extract_from_url(self, url, recursive=False, max_depth=5, save_path='./data/', current_depth=1):
        """Extract emails and phone numbers from URL"""
        if current_depth > max_depth:
            return set(), set()
            
        # Nice scraping indicator
        if current_depth == 1:
            print(f"{Fore.CYAN}🕷️  {Style.BRIGHT}Scraping... {Fore.YELLOW}{url}")
        else:
            print(f"{Fore.CYAN}   └─ {Style.DIM}Depth {current_depth}: {url}")
        
        all_emails = set()
        all_phones = set()
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from the page
            text_content = soup.get_text()
            
            # Also check specific elements that might contain contact info
            contact_elements = soup.find_all(['div', 'span', 'p', 'li'], 
                                           class_=re.compile('contact|email|phone|footer', re.I))
            for element in contact_elements:
                text_content += " " + element.get_text()
            
            # Extract emails and phones
            emails, phones = self.extract_emails_and_phones(text_content)
            all_emails.update(emails)
            all_phones.update(phones)
            
            # Show results with icons
            if emails or phones:
                print(f"   {Fore.GREEN}📧 {len(emails)} emails  📞 {len(phones)} phones")
            
            # Recursive processing
            if recursive and current_depth < max_depth:
                base_domain = urlparse(url)
                links = self.get_links(url, base_domain)
                
                for link in list(links)[:10]:  # Limit to avoid overwhelming
                    try:
                        sub_emails, sub_phones = self.extract_from_url(
                            link, recursive, max_depth, save_path, current_depth + 1
                        )
                        all_emails.update(sub_emails)
                        all_phones.update(sub_phones)
                    except Exception as e:
                        print(f"{Fore.RED}   ✗ Failed: {e}")
                        continue
                        
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}")
        
        return all_emails, all_phones

def main():
    parser = argparse.ArgumentParser(description='Email & Phone Extractor by abderrafie - extract contact information from websites')
    parser.add_argument('url', help='URL to process')
    parser.add_argument('-r', action='store_true', help='Recursive extraction')
    parser.add_argument('-l', type=int, default=5, help='Maximum depth level for recursive extraction')
    parser.add_argument('-p', default='./data/', help='Path to save extracted files')
    parser.add_argument('--emails-only', action='store_true', help='Extract only emails')
    parser.add_argument('--phones-only', action='store_true', help='Extract only phone numbers')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.p, exist_ok=True)
    
    # Initialize extractor
    extractor = EmailPhoneExtractor()
    
    # Extract data
    print(f"{Fore.CYAN}🚀 {Style.BRIGHT}Starting extraction from: {Fore.YELLOW}{args.url}")
    emails, phones = extractor.extract_from_url(args.url, args.r, args.l, args.p)
    
    # Save results based on arguments
    if not args.phones_only:
        email_file = os.path.join(args.p, 'emails.txt')
        extractor.save_to_file(emails, email_file, 'emails')
    
    if not args.emails_only:
        phone_file = os.path.join(args.p, 'phones.txt')
        extractor.save_to_file(phones, phone_file, 'phone numbers')
    
    print(f"\n{Fore.GREEN}🎉 {Style.BRIGHT}Extraction completed!")
    print(f"{Fore.BLUE}📧 Total emails found: {Fore.YELLOW}{len(emails)}")
    print(f"{Fore.BLUE}📞 Total phone numbers found: {Fore.YELLOW}{len(phones)}")
    print(f"{Fore.BLUE}📁 Files saved to: {Fore.YELLOW}{args.p}")

if __name__ == '__main__':
    main()
