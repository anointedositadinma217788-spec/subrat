#!/usr/bin/env python3
"""
subrat - Subdomain Recon Agent Tool
Powered by Sailerbross Technology
Ethical DNS enumerator – use only with permission.
"""

import sys
import os
import argparse
import threading
import time
import re
from queue import Queue

# ------------------------------------------------------------
# SAILERBROSS TECHNOLOGY – DEFAULT WORDLIST (90+ entries)
# ------------------------------------------------------------
SAILERBROSS_WORDLIST = [
    # Basic
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "pop3", "imap",
    "ns1", "ns2", "ns3", "webdisk", "cpanel", "whm", "autodiscover", "autoconfig",
    # Common services
    "admin", "administrator", "blog", "shop", "store", "api", "dev", "test",
    "stage", "staging", "demo", "portal", "remote", "vpn", "secure", "login",
    "account", "support", "help", "status", "stats", "static", "media", "cdn",
    # Development
    "git", "svn", "jenkins", "jira", "confluence", "gitlab", "github", "bitbucket",
    "ci", "cd", "build", "artifact", "repo", "registry", "docker", "k8s", "kubernetes",
    # Cloud / hosting
    "s3", "storage", "bucket", "cloud", "app", "apps", "api2", "api3", "v1", "v2",
    "uat", "preprod", "prod", "production", "backup", "db", "database", "sql",
    # Security / monitoring
    "security", "scan", "audit", "monitor", "logging", "logs", "metrics", "grafana",
    "prometheus", "alert", "alerts", "soc", "siem", "firewall", "waf", "ids", "ips",
    # Corporate
    "corp", "internal", "intranet", "hr", "finance", "payroll", "legal", "compliance",
    "marketing", "sales", "research", "lab", "office", "remote", "work", "staff",
    # Additional
    "mx", "mail2", "smtp2", "pop2", "imap2", "calendar", "exchange", "lync", "skype",
    "teams", "slack", "discord", "chat", "forum", "community", "news", "mediawiki"
]  # Total: 100+ entries

# ------------------------------------------------------------
# COLOR CODES (works on Termux / Linux / macOS / Windows WSL)
# ------------------------------------------------------------
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------------
# BANNER & SAILERBROSS TECHNOLOGY CREDIT
# ------------------------------------------------------------
def print_banner():
    banner = f"""
{Color.CYAN}{Color.BOLD}
   _____       _        _   
  / ____|     | |      | |  
 | (___  _   _| |_ __ _| |_ 
  \___ \| | | | __/ _` | __|
  ____) | |_| | || (_| | |_ 
 |_____/ \__,_|\__\__,_|\__|
{Color.RESET}{Color.YELLOW}{Color.BOLD}                                                     
 Subdomain Recon Agent Tool v2.0
{Color.RESET}{Color.MAGENTA}⚡ Powered by Sailerbross Technology ⚡{Color.RESET}
{Color.DIM} Ethical DNS enumerator – use only with permission.{Color.RESET}
    """
    print(banner)

def print_sailerbross_credit():
    print(f"{Color.MAGENTA}{Color.DIM}🔧 Sailerbross Engine active – {len(SAILERBROSS_WORDLIST)} default payloads loaded{Color.RESET}")

# ------------------------------------------------------------
# ETHICAL WARNING
# ------------------------------------------------------------
def ethical_warning(domain):
    print(f"\n{Color.YELLOW}{Color.BOLD}[!] ETHICAL HACKING WARNING{Color.RESET}")
    print(f"Target domain: {Color.CYAN}{domain}{Color.RESET}")
    print(f"{Color.YELLOW}You must have written permission to scan this domain.{Color.RESET}")
    print(f"Unauthorized scanning is illegal and may result in prosecution.\n")
    resp = input(f"{Color.BOLD}Do you have permission? (yes/no): {Color.RESET}").strip().lower()
    return resp in ['yes', 'y']

# ------------------------------------------------------------
# DNS RESOLUTION ENGINE
# ------------------------------------------------------------
try:
    import dns.resolver
    import dns.exception
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print(f"{Color.RED}[!] dnspython not installed. Run: python -m pip install dnspython{Color.RESET}")

def resolve_subdomain(subdomain, domain, resolver, timeout, verbose, found_list, lock):
    full = f"{subdomain}.{domain}"
    try:
        answers = resolver.resolve(full, 'A')
        ip = answers[0].to_text()
        with lock:
            found_list.append(full)
        print(f"{Color.GREEN}[+] {full} -> {ip}{Color.RESET}")
        return True
    except dns.resolver.NXDOMAIN:
        if verbose:
            print(f"{Color.DIM}[-] {full}{Color.RESET}")
    except dns.resolver.Timeout:
        if verbose:
            print(f"{Color.RED}[!] {full} (timeout){Color.RESET}")
    except dns.resolver.NoAnswer:
        if verbose:
            print(f"{Color.DIM}[?] {full} (no A record){Color.RESET}")
    except Exception as e:
        if verbose:
            print(f"{Color.RED}[!] {full} error: {str(e)[:50]}{Color.RESET}")
    return False

def run_scan(domain, wordlist_source=None, output_file=None, threads=40, timeout=5, verbose=False, resolver_ip=None):
    if not DNS_AVAILABLE:
        print(f"{Color.RED}[!] Cannot scan – dnspython missing.{Color.RESET}")
        return []

    # Load wordlist (use Sailerbross default if none provided)
    if wordlist_source is None:
        subdomains = SAILERBROSS_WORDLIST[:]  # copy
        print(f"{Color.CYAN}[*] Using Sailerbross default wordlist ({len(subdomains)} entries){Color.RESET}")
    else:
        try:
            with open(wordlist_source, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"{Color.CYAN}[*] Loaded external wordlist: {len(subdomains)} entries from {wordlist_source}{Color.RESET}")
        except FileNotFoundError:
            print(f"{Color.RED}[!] Wordlist file not found: {wordlist_source}{Color.RESET}")
            return []
        except Exception as e:
            print(f"{Color.RED}[!] Error reading wordlist: {e}{Color.RESET}")
            return []

    if not subdomains:
        print(f"{Color.RED}[!] Wordlist empty.{Color.RESET}")
        return []

    # Setup resolver
    resolver = dns.resolver.Resolver()
    if resolver_ip:
        resolver.nameservers = [resolver_ip]
    resolver.timeout = timeout
    resolver.lifetime = timeout

    print(f"{Color.BLUE}[*] Target: {domain}{Color.RESET}")
    print(f"[*] Threads: {threads} | Timeout: {timeout}s | Verbose: {'ON' if verbose else 'OFF'}")
    if resolver_ip:
        print(f"[*] Custom resolver: {resolver_ip}")
    print()

    queue = Queue()
    for sub in subdomains:
        queue.put(sub)

    found = []
    lock = threading.Lock()
    active_threads = []

    def worker():
        while not queue.empty():
            try:
                sub = queue.get_nowait()
            except:
                break
            resolve_subdomain(sub, domain, resolver, timeout, verbose, found, lock)
            queue.task_done()

    # Launch threads
    for _ in range(min(threads, len(subdomains))):
        t = threading.Thread(target=worker)
        t.start()
        active_threads.append(t)

    # Wait with interrupt handling
    try:
        for t in active_threads:
            t.join()
        queue.join()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Scan interrupted by user. Partial results shown.{Color.RESET}")

    # Summary
    print(f"\n{Color.CYAN}{Color.BOLD}⚡ Scan finished. Found {len(found)} live subdomains.{Color.RESET}")
    if output_file:
        try:
            with open(output_file, 'w') as f:
                for sub in found:
                    f.write(sub + "\n")
            print(f"{Color.GREEN}[✓] Results saved to: {output_file}{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}[!] Failed to save: {e}{Color.RESET}")

    return found

# ------------------------------------------------------------
# INTERACTIVE SHELL
# ------------------------------------------------------------
class SubratShell:
    def __init__(self):
        self.last_results = []
        self.default_threads = 40
        self.default_timeout = 5
        self.default_resolver = None
        self.verbose = False
        self.running = True

    def do_scan(self, args):
        """scan -d DOMAIN [-w WORDLIST] [-o OUTPUT] [-t THREADS] [--verbose] [--timeout SEC] [--resolver IP]"""
        import shlex
        try:
            parts = shlex.split(args)
        except:
            parts = args.split()

        parser = argparse.ArgumentParser(prog="scan", add_help=False)
        parser.add_argument("-d", "--domain", required=True)
        parser.add_argument("-w", "--wordlist")
        parser.add_argument("-o", "--output")
        parser.add_argument("-t", "--threads", type=int)
        parser.add_argument("--verbose", action="store_true")
        parser.add_argument("--timeout", type=int)
        parser.add_argument("--resolver")

        try:
            ns, _ = parser.parse_known_args(parts)
        except:
            print("Usage: scan -d DOMAIN [-w WORDLIST] [-o OUTPUT] [-t THREADS] [--verbose]")
            return

        domain = ns.domain
        wordlist = ns.wordlist
        output = ns.output
        threads = ns.threads if ns.threads is not None else self.default_threads
        verbose = ns.verbose or self.verbose
        timeout = ns.timeout if ns.timeout is not None else self.default_timeout
        resolver = ns.resolver if hasattr(ns, 'resolver') else self.default_resolver

        if domain != "example.com":
            if not ethical_warning(domain):
                print(f"{Color.YELLOW}[!] Scan aborted.{Color.RESET}")
                return

        results = run_scan(domain, wordlist, output, threads, timeout, verbose, resolver)
        self.last_results = results

    def do_set(self, args):
        parts = args.split()
        if len(parts) < 2:
            print("Usage: set <param> <value>")
            print("Params: threads, timeout, resolver, verbose (on/off)")
            return
        param = parts[0].lower()
        value = " ".join(parts[1:])
        if param == "threads":
            try:
                self.default_threads = int(value)
                print(f"{Color.GREEN}[*] Threads set to {self.default_threads}{Color.RESET}")
            except:
                print(f"{Color.RED}[!] Invalid number{Color.RESET}")
        elif param == "timeout":
            try:
                self.default_timeout = int(value)
                print(f"{Color.GREEN}[*] Timeout set to {self.default_timeout}s{Color.RESET}")
            except:
                print(f"{Color.RED}[!] Invalid number{Color.RESET}")
        elif param == "resolver":
            if value.lower() == "none":
                self.default_resolver = None
                print(f"{Color.GREEN}[*] Using system default resolver{Color.RESET}")
            else:
                self.default_resolver = value
                print(f"{Color.GREEN}[*] Resolver set to {value}{Color.RESET}")
        elif param == "verbose":
            if value.lower() in ["on", "true", "1"]:
                self.verbose = True
                print(f"{Color.GREEN}[*] Verbose ON{Color.RESET}")
            else:
                self.verbose = False
                print(f"{Color.GREEN}[*] Verbose OFF{Color.RESET}")
        else:
            print(f"{Color.RED}[!] Unknown param{Color.RESET}")

    def do_save(self, filename):
        if not filename:
            print("Usage: save <filename>")
            return
        if not self.last_results:
            print(f"{Color.RED}[!] No results to save. Run a scan first.{Color.RESET}")
            return
        try:
            with open(filename, 'w') as f:
                for sub in self.last_results:
                    f.write(sub + "\n")
            print(f"{Color.GREEN}[✓] Saved {len(self.last_results)} subdomains to {filename}{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}[!] Save error: {e}{Color.RESET}")

    def do_tutorial(self, _=None):
        tutorial = f"""
{Color.CYAN}{Color.BOLD}═══════════════════════════════════════════════════════════════{Color.RESET}
{Color.BOLD}  SUBRAT TUTORIAL – powered by Sailerbross Technology{Color.RESET}
{Color.CYAN}{Color.BOLD}═══════════════════════════════════════════════════════════════{Color.RESET}

{Color.BOLD}1. No wordlist? No problem!{Color.RESET}
   subrat has {len(SAILERBROSS_WORDLIST)} built‑in subdomains. Just run:
   {Color.GREEN}scan -d example.com{Color.RESET}

{Color.BOLD}2. Use your own wordlist (anywhere on disk):{Color.RESET}
   {Color.GREEN}scan -d target.com -w /path/to/wordlist.txt{Color.RESET}

{Color.BOLD}3. Save results to a file:{Color.RESET}
   {Color.GREEN}scan -d example.com -o found.txt{Color.RESET}

{Color.BOLD}4. Adjust speed & thoroughness:{Color.RESET}
   {Color.GREEN}set threads 100      # faster (default 40)
   set timeout 3       # quicker failure
   set verbose on      # see all attempts{Color.RESET}

{Color.BOLD}5. Use a custom DNS resolver (e.g., Cloudflare):{Color.RESET}
   {Color.GREEN}set resolver 1.1.1.1{Color.RESET}

{Color.BOLD}6. Legal reminder:{Color.RESET}
   → Only scan domains you OWN or have WRITTEN PERMISSION for.
   → Unauthorized scanning is illegal.

{Color.MAGENTA}⚡ Sailerbross Technology ensures maximum coverage with minimal setup.{Color.RESET}
{Color.CYAN}{Color.BOLD}═══════════════════════════════════════════════════════════════{Color.RESET}
        """
        print(tutorial)

    def do_help(self, _=None):
        help_text = f"""
{Color.CYAN}Available commands:{Color.RESET}
  {Color.BOLD}scan -d DOMAIN [-w WORDLIST] [-o OUTPUT] [-t THREADS] [--verbose]{Color.RESET}
        Perform subdomain enumeration.
  {Color.BOLD}set <param> <value>{Color.RESET}
        Parameters: threads, timeout, resolver, verbose (on/off)
  {Color.BOLD}save <filename>{Color.RESET}
        Save last scan results.
  {Color.BOLD}tutorial{Color.RESET}
        Show step‑by‑step guide.
  {Color.BOLD}help (or ?){Color.RESET}
        This help.
  {Color.BOLD}exit / quit{Color.RESET}
        Exit subrat.
        """
        print(help_text)

    def do_exit(self, _=None):
        self.running = False
        print(f"{Color.GREEN}Exiting subrat. Stay ethical!{Color.RESET}")

    def run(self):
        clear_screen()
        print_banner()
        print_sailerbross_credit()
        print(f"{Color.DIM}Type 'tutorial' to learn, 'help' for commands.{Color.RESET}\n")
        while self.running:
            try:
                cmd_line = input(f"{Color.CYAN}subrat> {Color.RESET}").strip()
                if not cmd_line:
                    continue
                parts = cmd_line.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""
                if cmd in ["scan", "set", "save", "tutorial", "help", "exit", "quit"]:
                    if cmd == "quit":
                        cmd = "exit"
                    if cmd == "?":
                        self.do_help()
                    else:
                        getattr(self, f"do_{cmd}")(arg)
                else:
                    print(f"{Color.RED}[!] Unknown command. Type 'help'.{Color.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Color.YELLOW}Use 'exit' to quit.{Color.RESET}")
            except EOFError:
                break

# ------------------------------------------------------------
# DIRECT MODE (COMMAND LINE)
# ------------------------------------------------------------
def main_direct():
    parser = argparse.ArgumentParser(description="subrat - Subdomain Recon Agent Tool (Powered by Sailerbross Technology)")
    parser.add_argument("-d", "--domain", help="Target domain")
    parser.add_argument("-w", "--wordlist", help="External wordlist file (optional)")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("-t", "--threads", type=int, default=40, help="Threads (default 40)")
    parser.add_argument("--timeout", type=int, default=5, help="DNS timeout (seconds)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--resolver", help="Custom DNS resolver IP")
    parser.add_argument("--tutorial", action="store_true", help="Show tutorial and exit")
    parser.add_argument("--gen-wordlist", action="store_true", help="Generate sample wordlist file from built‑in list")

    args = parser.parse_args()

    if args.tutorial:
        SubratShell().do_tutorial()
        return

    if args.gen_wordlist:
        sample_file = "sailerbross_wordlist.txt"
        with open(sample_file, 'w') as f:
            f.write("\n".join(SAILERBROSS_WORDLIST))
        print(f"{Color.GREEN}[✓] Generated {sample_file} with {len(SAILERBROSS_WORDLIST)} entries.{Color.RESET}")
        print(f"   Use it: subrat -d example.com -w {sample_file}")
        return

    if not args.domain:
        parser.print_help()
        print(f"\n{Color.YELLOW}Example: subrat -d example.com{Color.RESET}")
        return

    if args.domain != "example.com":
        if not ethical_warning(args.domain):
            return

    run_scan(args.domain, args.wordlist, args.output, args.threads, args.timeout, args.verbose, args.resolver)

# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_direct()
    else:
        # Interactive mode
        if not DNS_AVAILABLE:
            print(f"{Color.RED}[!] dnspython missing. Please install: python -m pip install dnspython{Color.RESET}")
            sys.exit(1)
        shell = SubratShell()
        shell.run()