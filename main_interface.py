#!/usr/bin/env python3
"""
Arachnida - Advanced Web Data Extraction Tool Suite
by abderrafie
"""
import os
import sys
import argparse
import time
import subprocess
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class ArachnidaInterface:
    def __init__(self):
        self.title = f"""
{Fore.CYAN}{'═' * 80}
{Fore.CYAN}█████╗ ██████╗  █████╗  ██████╗██╗  ██╗███╗   ██╗██╗██████╗  █████╗ 
{Fore.CYAN}██╔══██╗██╔══██╗██╔══██╗██╔════╝██║  ██║████╗  ██║██║██╔══██╗██╔══██╗
{Fore.BLUE}███████║██████╔╝███████║██║     ███████║██╔██╗ ██║██║██║  ██║███████║
{Fore.BLUE}██╔══██║██╔══██╗██╔══██║██║     ██╔══██║██║╚██╗██║██║██║  ██║██╔══██║
{Fore.MAGENTA}██║  ██║██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████║██║██████╔╝██║  ██║
{Fore.MAGENTA}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═════╝ ╚═╝  ╚═╝
{Fore.YELLOW}                                                     by abderrafie
{Fore.CYAN}{'═' * 80}
        """
        
    def print_header(self):
        """Print the application header with animation"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.title)
        print(f"{Fore.GREEN}{Style.BRIGHT}🕷️  Advanced Web Data Extraction Tool Suite 🕷️")
        print(f"{Fore.YELLOW}{'─' * 80}")
        print(f"{Fore.WHITE}Extract images, emails, and phone numbers from websites")
        print(f"{Fore.CYAN}Support for recursive crawling and custom configurations")
        print(f"{Fore.YELLOW}{'─' * 80}")
        
    def print_menu(self):
        """Print the main menu with beautiful design"""
        print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} 🎯 EXTRACTION OPTIONS {Style.RESET_ALL}")
        print(f"{Fore.CYAN}╭─────────────────────────────────────────────────────────╮")
        print(f"{Fore.CYAN}│ {Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] {Fore.GREEN}📸 Images Only        {Fore.CYAN}│ {Fore.WHITE}[{Fore.BLUE}2{Fore.WHITE}] {Fore.BLUE}📧 Emails Only        {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────┤")
        print(f"{Fore.CYAN}│ {Fore.WHITE}[{Fore.MAGENTA}3{Fore.WHITE}] {Fore.MAGENTA}📞 Phone Numbers Only {Fore.CYAN}│ {Fore.WHITE}[{Fore.YELLOW}4{Fore.WHITE}] {Fore.YELLOW}📧📞 Emails + Phones   {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────┤")
        print(f"{Fore.CYAN}│ {Fore.WHITE}[{Fore.RED}5{Fore.WHITE}] {Fore.RED}🎯 Everything         {Fore.CYAN}│ {Fore.WHITE}[{Fore.CYAN}6{Fore.WHITE}] {Fore.CYAN}⚙️  Custom Options    {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────┤")
        print(f"{Fore.CYAN}│                   {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}] {Fore.RED}❌ Exit                      {Fore.CYAN}│")
        print(f"{Fore.CYAN}╰─────────────────────────────────────────────────────────╯")
        
    def get_common_params(self):
        """Get common parameters from user with improved UI"""
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} ⚙️  CONFIGURATION {Style.RESET_ALL}")
        print(f"{Fore.CYAN}╭─────────────────────────────────────────────────────────╮")
        
        # URL input with validation
        while True:
            url = input(f"{Fore.CYAN}│ {Fore.WHITE}🌐 Enter URL: {Fore.GREEN}")
            if url.strip():
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                break
            print(f"{Fore.RED}│ ❌ Please enter a valid URL!")
            
        # Recursive option
        recursive_input = input(f"{Fore.CYAN}│ {Fore.WHITE}🔄 Recursive extraction? ({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}N{Fore.WHITE}): {Fore.GREEN}").lower()
        recursive = recursive_input in ['y', 'yes']
        
        # Depth level if recursive
        depth = 5
        if recursive:
            depth_input = input(f"{Fore.CYAN}│ {Fore.WHITE}📊 Maximum depth level (default {Fore.YELLOW}5{Fore.WHITE}): {Fore.GREEN}")
            try:
                depth = int(depth_input) if depth_input else 5
                depth = max(1, min(depth, 10))  # Limit between 1-10
            except ValueError:
                depth = 5
                
        # Output path
        path_input = input(f"{Fore.CYAN}│ {Fore.WHITE}📁 Output directory (default {Fore.YELLOW}./data/{Fore.WHITE}): {Fore.GREEN}")
        path = path_input.strip() if path_input.strip() else './data/'
        
        print(f"{Fore.CYAN}╰─────────────────────────────────────────────────────────╯")
        
        # Show configuration summary
        print(f"\n{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} 📋 SUMMARY {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}┌─────────────────────────────────────────────────────────┐")
        print(f"{Fore.YELLOW}│ {Fore.WHITE}URL: {Fore.CYAN}{url}")
        print(f"{Fore.YELLOW}│ {Fore.WHITE}Recursive: {Fore.GREEN if recursive else Fore.RED}{'Yes' if recursive else 'No'}")
        if recursive:
            print(f"{Fore.YELLOW}│ {Fore.WHITE}Max Depth: {Fore.CYAN}{depth}")
        print(f"{Fore.YELLOW}│ {Fore.WHITE}Output: {Fore.CYAN}{path}")
        print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────┘")
        
        return url, recursive, depth, path
        
    def run_spider(self, url, recursive, depth, path):
        """Run the spider script for images with beautiful output"""
        cmd = ['python3', 'spider.py', url]
        if recursive:
            cmd.append('-r')
        cmd.extend(['-l', str(depth), '-p', path])
        
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} 🚀 LAUNCHING SPIDER {Style.RESET_ALL}")
        print(f"{Fore.GREEN}🕷️  Starting image extraction...")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} ✅ SUCCESS {Style.RESET_ALL}")
            print(f"{Fore.GREEN}🎉 Image extraction completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ❌ ERROR {Style.RESET_ALL}")
            print(f"{Fore.RED}💥 Error running spider: {e}")
            
    def run_email_phone_extractor(self, url, recursive, depth, path, emails_only=False, phones_only=False):
        """Run the email/phone extractor script with beautiful output"""
        cmd = ['python3', 'email_phone_extractor.py', url]
        if recursive:
            cmd.append('-r')
        cmd.extend(['-l', str(depth), '-p', path])
        if emails_only:
            cmd.append('--emails-only')
        if phones_only:
            cmd.append('--phones-only')
            
        print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} 🚀 LAUNCHING EXTRACTOR {Style.RESET_ALL}")
        
        if emails_only:
            print(f"{Fore.BLUE}📧 Starting email extraction...")
        elif phones_only:
            print(f"{Fore.MAGENTA}📞 Starting phone number extraction...")
        else:
            print(f"{Fore.YELLOW}📧📞 Starting email and phone extraction...")
            
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} ✅ SUCCESS {Style.RESET_ALL}")
            print(f"{Fore.BLUE}🎉 Contact extraction completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ❌ ERROR {Style.RESET_ALL}")
            print(f"{Fore.RED}💥 Error running extractor: {e}")
            
    def custom_options_menu(self):
        """Show custom options menu with improved design"""
        print(f"\n{Back.CYAN}{Fore.BLACK}{Style.BRIGHT} ⚙️  CUSTOM OPTIONS {Style.RESET_ALL}")
        print(f"{Fore.CYAN}╭─────────────────────────────────────────────────────────╮")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Select what to extract (multiple choices allowed)       {Fore.CYAN}│")
        print(f"{Fore.CYAN}╰─────────────────────────────────────────────────────────╯")
        
        choices = {}
        choices['images'] = input(f"{Fore.GREEN}📸 Extract Images? ({Fore.WHITE}y{Fore.GREEN}/{Fore.RED}N{Fore.GREEN}): {Fore.WHITE}").lower() in ['y', 'yes']
        choices['emails'] = input(f"{Fore.BLUE}📧 Extract Emails? ({Fore.WHITE}y{Fore.BLUE}/{Fore.RED}N{Fore.BLUE}): {Fore.WHITE}").lower() in ['y', 'yes']
        choices['phones'] = input(f"{Fore.MAGENTA}📞 Extract Phone Numbers? ({Fore.WHITE}y{Fore.MAGENTA}/{Fore.RED}N{Fore.MAGENTA}): {Fore.WHITE}").lower() in ['y', 'yes']
        
        if not any(choices.values()):
            print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ❌ ERROR {Style.RESET_ALL}")
            print(f"{Fore.RED}No extraction type selected!")
            input(f"{Fore.YELLOW}Press Enter to continue...")
            return
            
        url, recursive, depth, path = self.get_common_params()
        
        # Run selected extractors
        if choices['images']:
            self.run_spider(url, recursive, depth, path)
            
        if choices['emails'] or choices['phones']:
            emails_only = choices['emails'] and not choices['phones']
            phones_only = choices['phones'] and not choices['emails']
            self.run_email_phone_extractor(url, recursive, depth, path, emails_only, phones_only)
            
    def show_loading_animation(self, text="Processing", duration=2):
        """Show a loading animation"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        for i in range(duration * 10):
            char = chars[i % len(chars)]
            print(f"\r{Fore.CYAN}{char} {text}...", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{Fore.GREEN}✓ {text} complete!   ")
            
    def run(self):
        """Main application loop with enhanced UI"""
        while True:
            self.print_header()
            self.print_menu()
            
            try:
                choice = input(f"\n{Fore.WHITE}🎯 Select option ({Fore.GREEN}0-6{Fore.WHITE}): {Fore.GREEN}")
                
                if choice == '0':
                    print(f"\n{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} 👋 GOODBYE {Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Thank you for using Arachnida! 🕷️")
                    print(f"{Fore.CYAN}Created by abderrafie with ❤️")
                    break
                    
                elif choice == '1':  # Images Only
                    url, recursive, depth, path = self.get_common_params()
                    self.run_spider(url, recursive, depth, path)
                    
                elif choice == '2':  # Emails Only
                    url, recursive, depth, path = self.get_common_params()
                    self.run_email_phone_extractor(url, recursive, depth, path, emails_only=True)
                    
                elif choice == '3':  # Phone Numbers Only
                    url, recursive, depth, path = self.get_common_params()
                    self.run_email_phone_extractor(url, recursive, depth, path, phones_only=True)
                    
                elif choice == '4':  # Emails + Phone Numbers
                    url, recursive, depth, path = self.get_common_params()
                    self.run_email_phone_extractor(url, recursive, depth, path)
                    
                elif choice == '5':  # Everything
                    url, recursive, depth, path = self.get_common_params()
                    self.run_spider(url, recursive, depth, path)
                    self.run_email_phone_extractor(url, recursive, depth, path)
                    
                elif choice == '6':  # Custom Options
                    self.custom_options_menu()
                    
                else:
                    print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ❌ INVALID CHOICE {Style.RESET_ALL}")
                    print(f"{Fore.RED}Please select a number between 0-6!")
                    time.sleep(1.5)
                    continue
                    
            except KeyboardInterrupt:
                print(f"\n\n{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} ⚠️  INTERRUPTED {Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Operation cancelled by user.")
                break
            except Exception as e:
                print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ❌ ERROR {Style.RESET_ALL}")
                print(f"{Fore.RED}An error occurred: {e}")
                time.sleep(2)
                
            # Ask if user wants to continue
            if choice != '0':
                print(f"\n{Fore.CYAN}{'─' * 60}")
                continue_choice = input(f"{Fore.CYAN}🔄 Perform another extraction? ({Fore.GREEN}Y{Fore.CYAN}/{Fore.RED}n{Fore.CYAN}): {Fore.GREEN}").lower()
                if continue_choice in ['n', 'no']:
                    print(f"\n{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} 👋 GOODBYE {Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Thank you for using Arachnida! 🕷️")
                    print(f"{Fore.CYAN}Created by abderrafie with ❤️")
                    break

def main():
    """Main function with argument parsing support"""
    parser = argparse.ArgumentParser(
        description='🕷️  Arachnida - Advanced Web Data Extraction Tool Suite by abderrafie',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main_interface.py                    # Interactive mode
  python3 main_interface.py --cli --url example.com --type all -r
        """
    )
    
    parser.add_argument('--cli', action='store_true', 
                       help='Run in CLI mode without interactive menu')
    parser.add_argument('--url', 
                       help='URL to process (CLI mode only)')
    parser.add_argument('--type', choices=['images', 'emails', 'phones', 'all'], 
                       help='Extraction type (CLI mode only)')
    parser.add_argument('-r', action='store_true', 
                       help='Recursive extraction (CLI mode only)')
    parser.add_argument('-l', type=int, default=5, 
                       help='Maximum depth level (CLI mode only)')
    parser.add_argument('-p', default='./data/', 
                       help='Output path (CLI mode only)')
    
    args = parser.parse_args()
    
    if args.cli and args.url and args.type:
        # CLI mode
        print(f"{Fore.CYAN}🕷️  Arachnida CLI Mode by abderrafie")
        print(f"{Fore.YELLOW}{'─' * 50}")
        interface = ArachnidaInterface()
        
        if args.type in ['images', 'all']:
            interface.run_spider(args.url, args.r, args.l, args.p)
            
        if args.type in ['emails', 'phones', 'all']:
            emails_only = args.type == 'emails'
            phones_only = args.type == 'phones'
            interface.run_email_phone_extractor(args.url, args.r, args.l, args.p, emails_only, phones_only)
    else:
        # Interactive mode
        try:
            app = ArachnidaInterface()
            app.run()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Goodbye! 👋")

if __name__ == '__main__':
    main()
