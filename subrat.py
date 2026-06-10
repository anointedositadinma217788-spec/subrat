#!/usr/bin/env python3
"""
███████╗██╗   ██╗██████╗ ██████╗  █████╗ ████████╗
██╔════╝██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
███████╗██║   ██║██████╔╝██████╔╝███████║   ██║   
╚════██║██║   ██║██╔══██╗██╔══██╗██╔══██║   ██║   
███████║╚██████╔╝██████╔╝██║  ██║██║  ██║   ██║   
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝   

subrat v3.0 - Ultra-Powered Subdomain Recon Agent Tool
Powered by Sailerbross Technology
Ethical DNS enumerator – use only with permission.

Features:
- 500+ built-in high-value wordlist entries
- Multi-threaded DNS resolution (up to 500 threads)
- CNAME / MX / TXT / NS / AAAA record support
- Wildcard detection & filtering
- Rate limiting & retry logic
- Zone transfer attempt
- Output: TXT, JSON, CSV formats
- Color-coded live output
- Banner grabbing (HTTP/HTTPS)
- Subdomain takeover detection
- Progress bar
- Resume / checkpoint support
"""

import sys
import os
import argparse
import threading
import time
import re
import json
import csv
import socket
import random
import string
import hashlib
import ipaddress
from queue import Queue, Empty
from datetime import datetime
from collections import defaultdict

# ============================================================
# SAILERBROSS TECHNOLOGY – ULTRA WORDLIST (500+ entries)
# ============================================================
SAILERBROSS_WORDLIST = [
    # ── Web / HTTP ──────────────────────────────────────────
    "www", "www1", "www2", "www3", "www4", "www5",
    "web", "web1", "web2", "web3", "website", "websites",
    "webserver", "webmail", "webmin", "webdisk", "webadmin",
    "webcam", "webftp", "webapi", "webdb", "webhook",
    "webalizer", "webdav", "webstats", "websocket",

    # ── Mail ────────────────────────────────────────────────
    "mail", "mail1", "mail2", "mail3", "mail4", "mail5",
    "email", "emails", "smtp", "smtp1", "smtp2", "smtp3",
    "smtps", "pop", "pop2", "pop3", "imap", "imap2",
    "imaps", "mx", "mx1", "mx2", "mx3", "mx4", "mx5",
    "relay", "outbound", "inbound", "mta", "mx-in",
    "mailhost", "mailserver", "mailrelay", "mailin",
    "mailout", "autodiscover", "autoconfig", "exchange",
    "owa", "ews", "lync", "skype", "teams", "groupwise",
    "mimecast", "proofpoint", "mailgun", "sendgrid",
    "postfix", "exim", "dovecot", "roundcube",

    # ── FTP / File Transfer ─────────────────────────────────
    "ftp", "ftp1", "ftp2", "ftp3", "ftps", "sftp",
    "files", "file", "fileserver", "filetransfer",
    "download", "downloads", "upload", "uploads",
    "transfer", "share", "shares", "shared", "nas",
    "storage", "store", "stores", "backup", "backups",
    "bak", "archive", "archives", "data", "dataset",

    # ── DNS / NS ────────────────────────────────────────────
    "ns", "ns1", "ns2", "ns3", "ns4", "ns5",
    "dns", "dns1", "dns2", "dns3", "dns4",
    "nameserver", "resolver", "rdns", "axfr",

    # ── Admin / Control Panel ───────────────────────────────
    "admin", "admin1", "admin2", "administrator",
    "administration", "administrador", "admins",
    "cpanel", "whm", "plesk", "directadmin",
    "panel", "control", "controlpanel", "cp",
    "manage", "management", "manager",
    "dashboard", "console", "cPanel",

    # ── Authentication / SSO ────────────────────────────────
    "login", "logout", "auth", "authenticate",
    "authentication", "sso", "oauth", "oauth2",
    "saml", "ldap", "iam", "idp", "sp",
    "account", "accounts", "myaccount", "profile",
    "user", "users", "password", "passwd",
    "register", "signup", "signin", "signout",
    "reset", "forgot", "verify", "verification",

    # ── API ─────────────────────────────────────────────────
    "api", "api1", "api2", "api3", "api4", "api5",
    "apis", "apiv1", "apiv2", "apiv3",
    "api-v1", "api-v2", "api-v3",
    "v1", "v2", "v3", "v4", "rest", "restapi",
    "graphql", "grpc", "soap", "wsdl",
    "gateway", "gw", "proxy", "rproxy",
    "backend", "frontend", "endpoint",
    "microservice", "service", "services",
    "webhook", "webhooks", "callback",
    "internal-api", "external-api", "public-api",
    "private-api",

    # ── Development / Staging ───────────────────────────────
    "dev", "dev1", "dev2", "dev3", "developer",
    "develop", "development",
    "test", "test1", "test2", "test3", "testing",
    "stage", "stage1", "stage2", "staging",
    "uat", "qa", "qas", "qa1", "qa2",
    "sandbox", "sandbox1", "sandbox2",
    "demo", "demo1", "demo2", "demos",
    "lab", "labs", "lab1", "lab2",
    "preview", "beta", "alpha", "canary",
    "experimental", "experiment",
    "preprod", "pre-prod", "pre",
    "prod", "production", "prod1", "prod2",
    "live", "release",

    # ── CI/CD / DevOps ──────────────────────────────────────
    "git", "gitlab", "github", "gitea",
    "bitbucket", "svn", "cvs", "mercurial", "hg",
    "jenkins", "jenkins1", "ci", "cd", "cicd",
    "travis", "circleci", "teamcity",
    "bamboo", "drone", "gocd", "spinnaker",
    "build", "builder", "builds",
    "artifact", "artifacts", "artifactory",
    "nexus", "registry", "harbor",
    "pipeline", "deploy", "deployer", "deployment",
    "ansible", "chef", "puppet", "saltstack",
    "terraform", "packer", "vagrant",

    # ── Container / Cloud ───────────────────────────────────
    "docker", "k8s", "kubernetes",
    "rancher", "openshift", "swarm",
    "container", "containers", "pod", "pods",
    "cluster", "clusters", "node", "nodes",
    "aws", "azure", "gcp", "cloud",
    "s3", "ec2", "lambda", "rds",
    "bucket", "buckets", "blob", "blobs",
    "compute", "functions", "serverless",
    "heroku", "digitalocean", "linode",
    "vultr", "cloudflare", "fastly", "akamai",

    # ── Database ─────────────────────────────────────────────
    "db", "db1", "db2", "db3", "db4",
    "database", "databases",
    "sql", "mysql", "psql", "postgres",
    "postgresql", "mariadb", "oracle",
    "mssql", "sqlserver",
    "mongo", "mongodb", "redis",
    "elasticsearch", "elastic", "es",
    "solr", "cassandra", "couchdb",
    "neo4j", "influxdb", "graphdb",
    "memcache", "memcached", "cache", "caches",

    # ── Monitoring / Logging ────────────────────────────────
    "monitor", "monitoring", "mon",
    "grafana", "prometheus", "alertmanager",
    "kibana", "logstash", "fluentd",
    "splunk", "datadog", "newrelic",
    "zabbix", "nagios", "icinga",
    "prtg", "solarwinds", "cacti",
    "logs", "log", "logging",
    "metrics", "metric",
    "stats", "statistics", "stat",
    "trace", "tracing", "jaeger",
    "apm", "sentry", "airbrake",
    "uptime", "health", "healthcheck",
    "ping", "alive", "status",
    "alerts", "alert", "pagerduty",

    # ── Security ─────────────────────────────────────────────
    "security", "secure", "sec",
    "firewall", "waf", "ids", "ips",
    "vpn", "vpn1", "vpn2", "vpn3",
    "remote", "remote1", "remote2",
    "soc", "siem", "scan", "scanner",
    "audit", "auditor", "compliance",
    "pentest", "bounty", "bugbounty",
    "vault", "secrets", "secret",
    "pki", "cert", "certs", "certificate",
    "ca", "ocsp", "crl", "acme",
    "2fa", "mfa", "otp", "totp",
    "proxy", "squid", "tor", "onion",

    # ── CDN / Static ─────────────────────────────────────────
    "cdn", "cdn1", "cdn2", "cdn3",
    "static", "static1", "static2",
    "assets", "asset",
    "media", "media1", "media2",
    "img", "images", "image",
    "video", "videos", "stream",
    "audio", "fonts", "font",
    "js", "css", "res", "resources",

    # ── CMS / Portal ─────────────────────────────────────────
    "cms", "wordpress", "wp", "wp-admin",
    "drupal", "joomla", "magento",
    "typo3", "contao", "craft",
    "shopify", "woocommerce",
    "portal", "portals", "client",
    "clients", "customer", "customers",
    "partner", "partners", "vendor", "vendors",
    "shop", "store1", "store2", "ecommerce",
    "cart", "checkout", "payment", "payments",
    "billing", "invoice", "invoices",
    "order", "orders", "catalog",

    # ── Communication / Collaboration ───────────────────────
    "chat", "chat1", "chat2",
    "slack", "discord", "teams", "zoom",
    "meet", "meeting", "meetings",
    "conference", "webinar",
    "calendar", "cal",
    "wiki", "confluence", "notion",
    "docs", "doc", "documentation",
    "kb", "knowledgebase", "faq",
    "forum", "forums", "board", "boards",
    "community", "discuss",
    "ticket", "tickets", "helpdesk",
    "support", "support1", "support2",
    "desk", "service",

    # ── Corporate / HR ───────────────────────────────────────
    "corp", "corporate",
    "intranet", "internal", "inside",
    "hr", "human-resources", "people",
    "payroll", "salary", "benefits",
    "finance", "financial", "accounting",
    "erp", "sap", "oracle-erp",
    "crm", "salesforce", "hubspot",
    "legal", "law", "compliance",
    "marketing", "market",
    "sales", "sale",
    "research", "r-and-d", "rd",
    "office", "offices",
    "staff", "employees", "employee",
    "directory", "phonebook",

    # ── Hosting / Infrastructure ────────────────────────────
    "host", "hosting",
    "server", "server1", "server2",
    "server3", "server4", "server5",
    "node1", "node2", "node3",
    "host1", "host2", "host3",
    "vm", "vm1", "vm2",
    "vps", "dedicated", "bare",
    "load", "lb", "loadbalancer",
    "haproxy", "nginx", "apache",
    "iis", "tomcat", "jboss",
    "wildfly", "glassfish",

    # ── GeoIP / Regional ────────────────────────────────────
    "us", "usa", "us-east", "us-west",
    "eu", "europe", "eu-west", "eu-central",
    "uk", "gb", "de", "fr", "nl",
    "au", "ap", "asia", "sg", "jp",
    "ca", "br", "mx", "in",
    "nyc", "lon", "ams", "fra", "syd",
    "tok", "sin", "sfo", "lax",

    # ── Misc / Extras ────────────────────────────────────────
    "localhost", "local",
    "private", "public",
    "test-api", "dev-api", "staging-api",
    "uat-api", "prod-api",
    "old", "new", "legacy", "deprecated",
    "classic", "next", "nextgen",
    "mobile", "m", "app", "apps",
    "ios", "android",
    "desktop", "agent",
    "router", "switch", "gateway",
    "modem", "ap", "access-point",
    "idm", "iga", "pam", "bastion",
    "jump", "jumpbox", "jumphost",
    "terminal", "ssh", "rdp", "telnet",
    "vnc", "guacamole", "citrix",
    "print", "printer", "scan", "scanner",
    "erp", "mes", "scada", "iot",
    "ota", "update", "updates",
    "license", "activation",
    "social", "feed", "rss", "atom",
    "sitemap", "robots",
    "404", "403", "500",
    "test-new", "new-test", "newdev",
    "uat2", "uat3", "pre-uat",
    "mirror", "clone", "replica",
    "master", "slave", "primary", "secondary",
    "active", "passive", "standby",
    "dr", "disaster-recovery",
    "failover", "ha", "cluster",
]

# Deduplicate while preserving order
seen = set()
_DEDUPED = []
for _w in SAILERBROSS_WORDLIST:
    if _w not in seen:
        seen.add(_w)
        _DEDUPED.append(_w)
SAILERBROSS_WORDLIST = _DEDUPED

# ============================================================
# SUBDOMAIN TAKEOVER FINGERPRINTS
# ============================================================
TAKEOVER_SIGNATURES = {
    "github.io":           "There isn't a GitHub Pages site here",
    "s3.amazonaws.com":    "NoSuchBucket",
    "cloudfront.net":      "ERROR: The request could not be satisfied",
    "herokuapp.com":       "No such app",
    "shopify.com":         "Sorry, this shop is currently unavailable",
    "fastly.net":          "Fastly error: unknown domain",
    "pantheon.io":         "404 error unknown site",
    "wordpress.com":       "Do you want to register",
    "smugmug.com":         "Page Not Found",
    "ghost.io":            "The thing you were looking for is no longer here",
    "surge.sh":            "project not found",
    "tumblr.com":          "There's nothing here",
    "unbounce.com":        "The requested URL was not found",
    "helpscout.net":       "No settings were found for this company",
    "zendesk.com":         "Help Center Closed",
    "freshdesk.com":       "There is no helpdesk here",
    "intercom.com":        "This page is reserved for artistic dogs",
    "statuspage.io":       "Better Uptime",
}

# ============================================================
# COLOR CODES
# ============================================================
class Color:
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    YELLOW  = '\033[93m'
    CYAN    = '\033[96m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE   = '\033[97m'
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    ORANGE  = '\033[38;5;208m'

def c(text, *colors):
    return "".join(colors) + str(text) + Color.RESET

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================
# PROGRESS BAR
# ============================================================
class ProgressBar:
    def __init__(self, total, width=50):
        self.total   = total
        self.width   = width
        self.done    = 0
        self.lock    = threading.Lock()
        self.start   = time.time()
        self._active = True

    def increment(self):
        with self.lock:
            self.done += 1

    def render(self):
        with self.lock:
            pct      = self.done / max(self.total, 1)
            filled   = int(self.width * pct)
            bar      = '█' * filled + '░' * (self.width - filled)
            elapsed  = time.time() - self.start
            rate     = self.done / max(elapsed, 0.001)
            eta      = (self.total - self.done) / max(rate, 0.001)
            print(
                f"\r{Color.CYAN}[{bar}]{Color.RESET} "
                f"{Color.BOLD}{pct*100:.1f}%{Color.RESET} "
                f"({self.done}/{self.total}) "
                f"{Color.DIM}{rate:.0f}/s ETA:{eta:.0f}s{Color.RESET}",
                end='', flush=True
            )

    def stop(self):
        self._active = False
        print()  # newline after bar

    def loop(self, interval=0.25):
        while self._active:
            self.render()
            time.sleep(interval)

# ============================================================
# BANNER
# ============================================================
def print_banner():
    banner = f"""
{Color.CYAN}{Color.BOLD}
███████╗██╗   ██╗██████╗ ██████╗  █████╗ ████████╗
██╔════╝██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
███████╗██║   ██║██████╔╝██████╔╝███████║   ██║   
╚════██║██║   ██║██╔══██╗██╔══██╗██╔══██║   ██║   
███████║╚██████╔╝██████╔╝██║  ██║██║  ██║   ██║   
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝   
{Color.RESET}
{Color.YELLOW}{Color.BOLD}      Subdomain Recon Agent Tool  v3.0{Color.RESET}
{Color.MAGENTA}{Color.BOLD}      ⚡ Powered by Sailerbross Technology ⚡{Color.RESET}
{Color.DIM}      Ethical DNS enumerator – use only with permission.{Color.RESET}
{Color.CYAN}      {len(SAILERBROSS_WORDLIST)} built-in wordlist entries | Multi-record | Takeover-detect{Color.RESET}
"""
    print(banner)

# ============================================================
# ETHICAL WARNING
# ============================================================
def ethical_warning(domain):
    print(f"\n{c('[!] ETHICAL HACKING WARNING', Color.YELLOW, Color.BOLD)}")
    print(f"  Target : {c(domain, Color.CYAN, Color.BOLD)}")
    print(f"  {c('You must have WRITTEN permission to scan this domain.', Color.YELLOW)}")
    print(f"  {c('Unauthorized scanning is ILLEGAL.', Color.RED, Color.BOLD)}\n")
    resp = input(f"{Color.BOLD}Do you have permission? (yes/no): {Color.RESET}").strip().lower()
    return resp in ['yes', 'y']

# ============================================================
# DNS LIBRARY CHECK
# ============================================================
try:
    import dns.resolver
    import dns.exception
    import dns.zone
    import dns.query
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print(f"{c('[!] dnspython not installed.', Color.RED)} "
          f"Run: {c('pip install dnspython', Color.GREEN)}")

# HTTP for banner grab / takeover (optional)
try:
    import urllib.request
    import urllib.error
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

# ============================================================
# WILDCARD DETECTION
# ============================================================
def detect_wildcard(domain, resolver, timeout=5):
    """
    Resolve a random subdomain. If it resolves, wildcards are active.
    Returns (is_wildcard: bool, wildcard_ips: set)
    """
    rand = ''.join(random.choices(string.ascii_lowercase, k=16))
    test = f"{rand}.{domain}"
    wc_ips = set()
    try:
        answers = resolver.resolve(test, 'A')
        for a in answers:
            wc_ips.add(a.to_text())
        return True, wc_ips
    except Exception:
        return False, wc_ips

# ============================================================
# ZONE TRANSFER ATTEMPT
# ============================================================
def attempt_zone_transfer(domain, resolver):
    results = []
    print(f"\n{c('[*] Attempting zone transfer (AXFR)...', Color.YELLOW)}")
    try:
        ns_answers = resolver.resolve(domain, 'NS')
        for ns_rr in ns_answers:
            ns_host = ns_rr.to_text().rstrip('.')
            try:
                ns_ip = socket.gethostbyname(ns_host)
                z = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=10))
                print(f"{c('[+] Zone transfer SUCCESS on ' + ns_host, Color.GREEN, Color.BOLD)}")
                for name in z.nodes:
                    results.append(f"{name}.{domain}")
                    print(f"  {c(str(name) + '.' + domain, Color.GREEN)}")
            except Exception as e:
                print(f"  {c('[-] ' + ns_host + ' refused: ' + str(e)[:60], Color.DIM)}")
    except Exception as e:
        print(f"  {c('[!] NS lookup failed: ' + str(e)[:60], Color.RED)}")
    if not results:
        print(f"  {c('[-] Zone transfer not available (expected).', Color.DIM)}")
    return results

# ============================================================
# HTTP BANNER GRAB & TAKEOVER CHECK
# ============================================================
def http_probe(fqdn, timeout=5):
    """
    Returns dict with status_code, server, title, takeover_hint
    """
    info = {"status": None, "server": "", "title": "", "takeover": ""}
    if not HTTP_AVAILABLE:
        return info
    for scheme in ("https", "http"):
        url = f"{scheme}://{fqdn}"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "subrat/3.0 (Sailerbross Technology)"}
            )
            resp = urllib.request.urlopen(req, timeout=timeout)
            body = resp.read(4096).decode('utf-8', errors='ignore')
            info["status"] = resp.getcode()
            info["server"] = resp.headers.get("Server", "")
            # extract title
            m = re.search(r'<title>(.*?)</title>', body, re.I | re.S)
            if m:
                info["title"] = m.group(1).strip()[:60]
            # takeover check
            for sig, pattern in TAKEOVER_SIGNATURES.items():
                if pattern.lower() in body.lower():
                    info["takeover"] = f"POSSIBLE TAKEOVER ({sig})"
            return info
        except urllib.error.HTTPError as e:
            info["status"] = e.code
            try:
                body = e.read(2048).decode('utf-8', errors='ignore')
                for sig, pattern in TAKEOVER_SIGNATURES.items():
                    if pattern.lower() in body.lower():
                        info["takeover"] = f"POSSIBLE TAKEOVER ({sig})"
            except Exception:
                pass
            return info
        except Exception:
            continue
    return info

# ============================================================
# CORE RESOLVE FUNCTION
# ============================================================
RECORD_TYPES = ['A', 'AAAA', 'CNAME', 'MX', 'TXT']

def resolve_subdomain(
    subdomain, domain, resolver, timeout,
    verbose, found_list, lock,
    wildcard_ips, probe_http, record_types
):
    fqdn = f"{subdomain}.{domain}"
    result = {
        "fqdn": fqdn,
        "records": defaultdict(list),
        "ips": [],
        "cname": "",
        "http": {},
        "takeover": "",
    }
    resolved = False

    for rtype in record_types:
        try:
            answers = resolver.resolve(fqdn, rtype)
            for rr in answers:
                val = rr.to_text()
                result["records"][rtype].append(val)
                if rtype == 'A':
                    # wildcard filter
                    if val not in wildcard_ips:
                        result["ips"].append(val)
                        resolved = True
                elif rtype == 'AAAA':
                    result["ips"].append(f"[{val}]")
                    resolved = True
                elif rtype == 'CNAME':
                    result["cname"] = val
                    resolved = True
                elif rtype in ('MX', 'TXT'):
                    resolved = True
        except dns.resolver.NXDOMAIN:
            break  # no point checking other records
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.Timeout:
            if verbose:
                print(f"  {c('[T] ' + fqdn + ' timeout', Color.DIM)}")
            continue
        except Exception:
            continue

    if resolved:
        # optional HTTP probe
        if probe_http and result["ips"]:
            result["http"] = http_probe(fqdn, timeout)
            result["takeover"] = result["http"].get("takeover", "")

        with lock:
            found_list.append(result)

        # ── pretty print ──────────────────────────────────
        ips_str = ", ".join(result["ips"][:4]) if result["ips"] else ""
        cname_str = f" → {c(result['cname'], Color.YELLOW)}" if result["cname"] else ""
        http_str = ""
        if result["http"].get("status"):
            code = result["http"]["status"]
            clr = Color.GREEN if code < 400 else Color.RED
            http_str = (
                f" [{c(str(code), clr)} "
                f"{c(result['http'].get('title','')[:30], Color.DIM)}]"
            )
        takeover_str = (
            f" {c('⚠ ' + result['takeover'], Color.RED, Color.BOLD)}"
            if result["takeover"] else ""
        )

        line = (
            f"{c('[+]', Color.GREEN, Color.BOLD)} "
            f"{c(fqdn, Color.CYAN, Color.BOLD)}"
        )
        if ips_str:
            line += f" → {c(ips_str, Color.GREEN)}"
        line += cname_str + http_str + takeover_str
        print(line)
        return True

    elif verbose:
        print(f"  {c('[-] ' + fqdn, Color.DIM)}")

    return False

# ============================================================
# RETRY WRAPPER
# ============================================================
def resolve_with_retry(retries=2, **kwargs):
    for attempt in range(retries + 1):
        try:
            return resolve_subdomain(**kwargs)
        except Exception:
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
    return False

# ============================================================
# MAIN SCAN ENGINE
# ============================================================
def run_scan(
    domain,
    wordlist_source=None,
    output_file=None,
    output_format="txt",
    threads=100,
    timeout=5,
    verbose=False,
    resolver_ip=None,
    probe_http=False,
    record_types=None,
    do_zone_transfer=False,
    retries=1,
    rate_limit=0,
    checkpoint_file=None,
):
    if not DNS_AVAILABLE:
        print(c("[!] dnspython missing – cannot scan.", Color.RED))
        return []

    if record_types is None:
        record_types = ['A', 'CNAME']

    # ── Load wordlist ──────────────────────────────────────
    if wordlist_source is None:
        subdomains = SAILERBROSS_WORDLIST[:]
        print(c(
            f"[*] Sailerbross default wordlist → {len(subdomains)} entries",
            Color.MAGENTA, Color.BOLD
        ))
    else:
        try:
            with open(wordlist_source, 'r', errors='ignore') as f:
                subdomains = [
                    l.strip() for l in f
                    if l.strip() and not l.startswith('#')
                ]
            print(c(
                f"[*] External wordlist: {len(subdomains)} entries from {wordlist_source}",
                Color.CYAN
            ))
        except FileNotFoundError:
            print(c(f"[!] Wordlist not found: {wordlist_source}", Color.RED))
            return []

    if not subdomains:
        print(c("[!] Wordlist is empty.", Color.RED))
        return []

    # ── Resume / checkpoint ───────────────────────────────
    already_done = set()
    if checkpoint_file and os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as cf:
            already_done = {l.strip() for l in cf if l.strip()}
        before = len(subdomains)
        subdomains = [s for s in subdomains if s not in already_done]
        print(c(
            f"[*] Checkpoint: skipping {before - len(subdomains)} already-checked entries",
            Color.YELLOW
        ))

    # ── Setup resolver ────────────────────────────────────
    try:
        resolver = dns.resolver.Resolver()
    except dns.resolver.NoResolverConfiguration:
        # Fallback for systems without /etc/resolv.conf (e.g., Termux/Android)
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google DNS
        print(c(
            "[*] Using fallback resolver (Google DNS) – /etc/resolv.conf not found",
            Color.YELLOW
        ))
    
    if resolver_ip:
        # Support multiple resolvers
        ips = [ip.strip() for ip in resolver_ip.split(',')]
        resolver.nameservers = ips
        print(c(f"[*] Custom resolver(s): {', '.join(ips)}", Color.CYAN))
    resolver.timeout  = timeout
    resolver.lifetime = timeout * 2

    # ── Wildcard detection ────────────────────────────────
    print(c("[*] Checking for DNS wildcard...", Color.YELLOW))
    is_wc, wc_ips = detect_wildcard(domain, resolver, timeout)
    if is_wc:
        print(c(
            f"[!] Wildcard detected! IPs {wc_ips} will be filtered.",
            Color.RED, Color.BOLD
        ))
    else:
        print(c("[✓] No wildcard detected.", Color.GREEN))

    # ── Zone transfer ─────────────────────────────────────
    zt_results = []
    if do_zone_transfer:
        zt_results = attempt_zone_transfer(domain, resolver)

    # ── Scan info ─────────────────────────────────────────
    print(f"\n{c('[*] Target:', Color.BLUE)} {c(domain, Color.CYAN, Color.BOLD)}")
    print(
        f"[*] Threads: {c(threads, Color.BOLD)} | "
        f"Timeout: {c(str(timeout) + 's', Color.BOLD)} | "
        f"Records: {c(','.join(record_types), Color.BOLD)} | "
        f"HTTP probe: {c('ON' if probe_http else 'OFF', Color.BOLD)} | "
        f"Verbose: {c('ON' if verbose else 'OFF', Color.BOLD)}"
    )
    print(f"[*] Scan started: {c(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Color.DIM)}\n")

    # ── Thread setup ──────────────────────────────────────
    q        = Queue()
    found    = []                 # list of result dicts
    lock     = threading.Lock()
    cp_lock  = threading.Lock()

    for sub in subdomains:
        q.put(sub)

    # Progress bar
    pb = ProgressBar(len(subdomains))
    pb_thread = threading.Thread(target=pb.loop, daemon=True)
    pb_thread.start()

    def worker():
        while True:
            try:
                sub = q.get_nowait()
            except Empty:
                break
            resolve_with_retry(
                retries    = retries,
                subdomain  = sub,
                domain     = domain,
                resolver   = resolver,
                timeout    = timeout,
                verbose    = verbose,
                found_list = found,
                lock       = lock,
                wildcard_ips     = wc_ips,
                probe_http       = probe_http,
                record_types     = record_types,
            )
            pb.increment()
            if rate_limit > 0:
                time.sleep(rate_limit)
            # checkpoint write
            if checkpoint_file:
                with cp_lock:
                    with open(checkpoint_file, 'a') as cf:
                        cf.write(sub + "\n")
            q.task_done()

    # Launch workers
    active = []
    for _ in range(min(threads, len(subdomains))):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        active.append(t)

    try:
        q.join()
    except KeyboardInterrupt:
        print(f"\n{c('[!] Interrupted. Saving partial results...', Color.YELLOW)}")

    pb.stop()

    # ── Merge zone transfer results ───────────────────────
    zt_structs = [{"fqdn": f, "records": {}, "ips": [], "cname": "",
                   "http": {}, "takeover": ""} for f in zt_results]

    all_results = found + zt_structs

    # ── Summary ───────────────────────────────────────────
    elapsed = time.time() - pb.start
    print(f"\n{c('═'*60, Color.CYAN)}")
    print(f"{c('⚡ SCAN COMPLETE', Color.MAGENTA, Color.BOLD)}")
    print(f"   Live subdomains : {c(len(all_results), Color.GREEN, Color.BOLD)}")
    print(f"   Total checked   : {c(len(subdomains), Color.BOLD)}")
    print(f"   Elapsed         : {c(f'{elapsed:.1f}s', Color.BOLD)}")
    print(f"   Rate            : {c(f'{len(subdomains)/max(elapsed,1):.0f}/s', Color.BOLD)}")

    # Takeover summary
    takeovers = [r for r in all_results if r.get("takeover")]
    if takeovers:
        print(f"\n{c('⚠ POSSIBLE SUBDOMAIN TAKEOVERS:', Color.RED, Color.BOLD)}")
        for t in takeovers:
            print(f"   {c(t['fqdn'], Color.RED)} — {t['takeover']}")

    print(c('═'*60, Color.CYAN))

    # ── Save output ───────────────────────────────────────
    if output_file:
        _save_results(all_results, output_file, output_format, domain)

    return all_results

# ============================================================
# OUTPUT WRITERS
# ============================================================
def _save_results(results, output_file, fmt, domain):
    fmt = fmt.lower()
    # auto-append extension
    if not output_file.endswith(f".{fmt}"):
        output_file = f"{output_file}.{fmt}"

    try:
        if fmt == "json":
            with open(output_file, 'w') as f:
                json.dump({
                    "domain": domain,
                    "scan_time": datetime.now().isoformat(),
                    "count": len(results),
                    "results": [
                        {
                            "fqdn": r["fqdn"],
                            "ips": r["ips"],
                            "cname": r["cname"],
                            "records": dict(r["records"]),
                            "http_status": r["http"].get("status"),
                            "http_title": r["http"].get("title",""),
                            "takeover": r["takeover"],
                        } for r in results
                    ]
                }, f, indent=2)

        elif fmt == "csv":
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "fqdn","ips","cname",
                    "http_status","http_title","server","takeover"
                ])
                for r in results:
                    writer.writerow([
                        r["fqdn"],
                        "|".join(r["ips"]),
                        r["cname"],
                        r["http"].get("status",""),
                        r["http"].get("title",""),
                        r["http"].get("server",""),
                        r["takeover"],
                    ])

        else:  # txt (default)
            with open(output_file, 'w') as f:
                f.write(f"# subrat v3.0 – Sailerbross Technology\n")
                f.write(f"# Domain: {domain}\n")
                f.write(f"# Date: {datetime.now().isoformat()}\n")
                f.write(f"# Count: {len(results)}\n\n")
                for r in results:
                    ips = ", ".join(r["ips"])
                    line = r["fqdn"]
                    if ips:
                        line += f"\t{ips}"
                    if r["cname"]:
                        line += f"\tCNAME:{r['cname']}"
                    if r["takeover"]:
                        line += f"\t⚠ {r['takeover']}"
                    f.write(line + "\n")

        print(f"{c('[✓] Results saved → ' + output_file, Color.GREEN, Color.BOLD)}")
    except Exception as e:
        print(c(f"[!] Save error: {e}", Color.RED))

# ============================================================
# INTERACTIVE SHELL
# ============================================================
class SubratShell:
    def __init__(self):
        self.last_results    = []
        self.default_threads = 100
        self.default_timeout = 5
        self.default_resolver= None
        self.verbose         = False
        self.probe_http      = False
        self.record_types    = ['A', 'CNAME']
        self.output_format   = "txt"
        self.retries         = 1
        self.rate_limit      = 0
        self.running         = True

    # ── scan ──────────────────────────────────────────────
    def do_scan(self, args):
        import shlex
        try:
            parts = shlex.split(args)
        except Exception:
            parts = args.split()

        p = argparse.ArgumentParser(prog="scan", add_help=False)
        p.add_argument("-d", "--domain",   required=True)
        p.add_argument("-w", "--wordlist")
        p.add_argument("-o", "--output")
        p.add_argument("-f", "--format",   default=self.output_format,
                       choices=["txt","json","csv"])
        p.add_argument("-t", "--threads",  type=int)
        p.add_argument("--verbose",        action="store_true")
        p.add_argument("--timeout",        type=int)
        p.add_argument("--resolver")
        p.add_argument("--http",           action="store_true")
        p.add_argument("--records",        default=",".join(self.record_types))
        p.add_argument("--axfr",           action="store_true")
        p.add_argument("--retries",        type=int)
        p.add_argument("--rate",           type=float)
        p.add_argument("--checkpoint")

        try:
            ns, _ = p.parse_known_args(parts)
        except Exception:
            print("Usage: scan -d DOMAIN [options]  — type 'help' for details")
            return

        domain   = ns.domain
        wordlist = ns.wordlist
        output   = ns.output
        fmt      = ns.format
        threads  = ns.threads   if ns.threads  is not None else self.default_threads
        verbose  = ns.verbose   or self.verbose
        timeout  = ns.timeout   if ns.timeout  is not None else self.default_timeout
        resolver = ns.resolver  or self.default_resolver
        http     = ns.http      or self.probe_http
        records  = [r.strip().upper() for r in ns.records.split(',')]
        axfr     = ns.axfr
        retries  = ns.retries   if ns.retries  is not None else self.retries
        rate     = ns.rate      if ns.rate     is not None else self.rate_limit
        checkpoint = ns.checkpoint

        if domain != "example.com":
            if not ethical_warning(domain):
                print(c("[!] Scan aborted.", Color.YELLOW))
                return

        self.last_results = run_scan(
            domain           = domain,
            wordlist_source  = wordlist,
            output_file      = output,
            output_format    = fmt,
            threads          = threads,
            timeout          = timeout,
            verbose          = verbose,
            resolver_ip      = resolver,
            probe_http       = http,
            record_types     = records,
            do_zone_transfer = axfr,
            retries          = retries,
            rate_limit       = rate,
            checkpoint_file  = checkpoint,
        )

    # ── set ───────────────────────────────────────────────
    def do_set(self, args):
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            print("Usage: set <param> <value>")
            print("Params: threads, timeout, resolver, verbose, http, "
                  "records, format, retries, rate")
            return
        param, value = parts[0].lower(), parts[1].strip()

        def _int(v):
            try:
                return int(v)
            except Exception:
                print(c("[!] Must be an integer.", Color.RED))
                return None

        if param == "threads":
            v = _int(value)
            if v:
                self.default_threads = v
                print(c(f"[*] Threads = {v}", Color.GREEN))
        elif param == "timeout":
            v = _int(value)
            if v:
                self.default_timeout = v
                print(c(f"[*] Timeout = {v}s", Color.GREEN))
        elif param == "resolver":
            if value.lower() == "none":
                self.default_resolver = None
                print(c("[*] Using system resolver.", Color.GREEN))
            else:
                self.default_resolver = value
                print(c(f"[*] Resolver = {value}", Color.GREEN))
        elif param == "verbose":
            self.verbose = value.lower() in ("on","true","1","yes")
            print(c(f"[*] Verbose = {'ON' if self.verbose else 'OFF'}", Color.GREEN))
        elif param == "http":
            self.probe_http = value.lower() in ("on","true","1","yes")
            print(c(f"[*] HTTP probe = {'ON' if self.probe_http else 'OFF'}", Color.GREEN))
        elif param == "records":
            self.record_types = [r.strip().upper() for r in value.split(',')]
            print(c(f"[*] Record types = {self.record_types}", Color.GREEN))
        elif param == "format":
            if value.lower() in ("txt","json","csv"):
                self.output_format = value.lower()
                print(c(f"[*] Output format = {self.output_format}", Color.GREEN))
            else:
                print(c("[!] Format must be txt, json, or csv.", Color.RED))
        elif param == "retries":
            v = _int(value)
            if v is not None:
                self.retries = v
                print(c(f"[*] Retries = {v}", Color.GREEN))
        elif param == "rate":
            try:
                self.rate_limit = float(value)
                print(c(f"[*] Rate limit = {self.rate_limit}s/query", Color.GREEN))
            except Exception:
                print(c("[!] Must be a float (e.g. 0.05).", Color.RED))
        else:
            print(c(f"[!] Unknown param: {param}", Color.RED))

    # ── save ──────────────────────────────────────────────
    def do_save(self, args):
        parts = args.split()
        if not parts:
            print("Usage: save <filename> [txt|json|csv]")
            return
        filename = parts[0]
        fmt = parts[1].lower() if len(parts) > 1 else self.output_format
        if not self.last_results:
            print(c("[!] No results. Run a scan first.", Color.RED))
            return
        _save_results(self.last_results, filename, fmt, "last_scan")

    # ── show ──────────────────────────────────────────────
    def do_show(self, _=None):
        if not self.last_results:
            print(c("[!] No results.", Color.RED))
            return
        print(f"\n{c('Found subdomains:', Color.CYAN, Color.BOLD)}")
        for i, r in enumerate(self.last_results, 1):
            ips   = ", ".join(r["ips"][:4])
            extra = f" [{c(ips, Color.GREEN)}]" if ips else ""
            extra += f" {c('⚠ ' + r['takeover'], Color.RED)}" if r["takeover"] else ""
            print(f"  {c(str(i).rjust(3), Color.DIM)}. {c(r['fqdn'], Color.CYAN)}{extra}")
        print()

    # ── wordlist ──────────────────────────────────────────
    def do_wordlist(self, _=None):
        print(f"\n{c('Sailerbross built-in wordlist:', Color.MAGENTA, Color.BOLD)}")
        cols = 5
        for i, w in enumerate(SAILERBROSS_WORDLIST):
            end = '\n' if (i + 1) % cols == 0 else ' '
            print(f"  {c(w, Color.CYAN)}", end=end)
        print(f"\n\n{c(f'Total: {len(SAILERBROSS_WORDLIST)} entries', Color.BOLD)}\n")

    # ── tutorial ──────────────────────────────────────────
    def do_tutorial(self, _=None):
        tut = f"""
{c('═'*65, Color.CYAN)}
{c('  SUBRAT v3.0 TUTORIAL — Sailerbross Technology', Color.BOLD)}
{c('═'*65, Color.CYAN)}

{c('QUICK SCAN (built-in wordlist):', Color.BOLD)}
  {c('scan -d example.com', Color.GREEN)}

{c('CUSTOM WORDLIST:', Color.BOLD)}
  {c('scan -d target.com -w /path/to/wordlist.txt', Color.GREEN)}

{c('SAVE RESULTS (txt / json / csv):', Color.BOLD)}
  {c('scan -d example.com -o results -f json', Color.GREEN)}
  {c('save results.csv csv', Color.GREEN)}

{c('FULL POWER SCAN:', Color.BOLD)}
  {c('scan -d example.com --http --axfr --records A,AAAA,CNAME,MX,TXT', Color.GREEN)}

{c('CONFIGURE ENGINE:', Color.BOLD)}
  {c('set threads 200      # up to 500', Color.GREEN)}
  {c('set timeout 3', Color.GREEN)}
  {c('set resolver 1.1.1.1,8.8.8.8   # multiple resolvers', Color.GREEN)}
  {c('set http on          # HTTP banner grab + takeover detect', Color.GREEN)}
  {c('set verbose on       # see all attempts', Color.GREEN)}
  {c('set format json      # default save format', Color.GREEN)}

{c('RESUME A SCAN:', Color.BOLD)}
  {c('scan -d example.com --checkpoint .chk_example', Color.GREEN)}
  # Restart and it skips already-checked subdomains.

{c('VIEW / WORDLIST:', Color.BOLD)}
  {c('show      # list last results', Color.GREEN)}
  {c('wordlist  # display built-in wordlist', Color.GREEN)}

{c('⚠ LEGAL REMINDER:', Color.RED, Color.BOLD)}
  Only scan domains you OWN or have WRITTEN PERMISSION for.
  Unauthorized scanning is illegal and unethical.

{c('═'*65, Color.CYAN)}
"""
        print(tut)

    # ── help ──────────────────────────────────────────────
    def do_help(self, _=None):
        h = f"""
{c('═'*60, Color.CYAN)}
{c(' SUBRAT v3.0 COMMANDS', Color.BOLD)}
{c('═'*60, Color.CYAN)}

{c('scan', Color.GREEN)} -d DOMAIN [options]
    -w  --wordlist FILE      external wordlist
    -o  --output   FILE      output file (auto-extension)
    -f  --format   txt|json|csv
    -t  --threads  N         parallel threads (default 100)
    --timeout  N             DNS timeout seconds (default 5)
    --resolver IP[,IP]       custom DNS server(s)
    --http                   HTTP probe + takeover check
    --records  A,AAAA,...    record types to query
    --axfr                   attempt zone transfer
    --retries  N             retry failed queries
    --rate     FLOAT         delay between queries (stealth)
    --checkpoint FILE        save/resume progress
    --verbose                show all attempts

{c('set', Color.GREEN)} <param> <value>
    threads, timeout, resolver, verbose, http,
    records, format, retries, rate

{c('show', Color.GREEN)}       — list last scan results
{c('save', Color.GREEN)} <file> [fmt]  — save last results
{c('wordlist', Color.GREEN)}   — display built-in wordlist
{c('tutorial', Color.GREEN)}   — step-by-step guide
{c('help / ?', Color.GREEN)}   — this screen
{c('exit / quit', Color.GREEN)} — exit subrat
{c('═'*60, Color.CYAN)}
"""
        print(h)

    # ── exit ──────────────────────────────────────────────
    def do_exit(self, _=None):
        self.running = False
        print(c("\nExiting subrat. Stay ethical! — Sailerbross Technology", Color.MAGENTA, Color.BOLD))

    # ── shell loop ────────────────────────────────────────
    def run(self):
        clear_screen()
        print_banner()
        print(c(
            f"🔧 Sailerbross Engine — {len(SAILERBROSS_WORDLIST)} wordlist entries loaded\n",
            Color.MAGENTA, Color.DIM
        ))
        print(c("  Type 'tutorial' to learn | 'help' for all commands\n", Color.DIM))

        CMDS = {
            "scan": self.do_scan,
            "set":  self.do_set,
            "save": self.do_save,
            "show": self.do_show,
            "wordlist":  self.do_wordlist,
            "tutorial":  self.do_tutorial,
            "help":      self.do_help,
            "?":         self.do_help,
            "exit":      self.do_exit,
            "quit":      self.do_exit,
        }

        while self.running:
            try:
                raw = input(f"{c('subrat', Color.CYAN, Color.BOLD)}"
                            f"{c('>', Color.MAGENTA)} ").strip()
                if not raw:
                    continue
                parts = raw.split(maxsplit=1)
                cmd   = parts[0].lower()
                arg   = parts[1] if len(parts) > 1 else ""
                if cmd in CMDS:
                    CMDS[cmd](arg)
                else:
                    print(c(f"[!] Unknown command '{cmd}'. Type 'help'.", Color.RED))
            except KeyboardInterrupt:
                print(c("\n  Use 'exit' to quit.", Color.YELLOW))
            except EOFError:
                break

# ============================================================
# DIRECT CLI MODE
# ============================================================
def main_direct():
    p = argparse.ArgumentParser(
        description="subrat v3.0 — Subdomain Recon Agent Tool (Sailerbross Technology)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    p.add_argument("-d", "--domain",    help="Target domain")
    p.add_argument("-w", "--wordlist",  help="External wordlist file")
    p.add_argument("-o", "--output",    help="Output file")
    p.add_argument("-f", "--format",    default="txt",
                   choices=["txt","json","csv"], help="Output format (default: txt)")
    p.add_argument("-t", "--threads",   type=int, default=100)
    p.add_argument("--timeout",         type=int, default=5)
    p.add_argument("-v", "--verbose",   action="store_true")
    p.add_argument("--resolver",        help="Custom DNS resolver IP(s), comma-separated")
    p.add_argument("--http",            action="store_true", help="HTTP probe + takeover check")
    p.add_argument("--records",         default="A,CNAME",
                   help="Record types to query (default: A,CNAME)")
    p.add_argument("--axfr",            action="store_true", help="Attempt zone transfer")
    p.add_argument("--retries",         type=int, default=1)
    p.add_argument("--rate",            type=float, default=0,
                   help="Rate limit: delay (sec) between queries")
    p.add_argument("--checkpoint",      help="Checkpoint file for resume")
    p.add_argument("--tutorial",        action="store_true")
    p.add_argument("--gen-wordlist",    action="store_true",
                   help="Export built-in wordlist to file")

    args = p.parse_args()

    print_banner()

    if args.tutorial:
        SubratShell().do_tutorial()
        return

    if args.gen_wordlist:
        out = "sailerbross_wordlist.txt"
        with open(out, 'w') as f:
            f.write("\n".join(SAILERBROSS_WORDLIST))
        print(c(f"[✓] Exported {len(SAILERBROSS_WORDLIST)} entries → {out}", Color.GREEN, Color.BOLD))
        print(f"    Use: {c(f'subrat -d example.com -w {out}', Color.CYAN)}")
        return

    if not args.domain:
        p.print_help()
        print(f"\n{c('Example:', Color.YELLOW)} subrat -d example.com --http --axfr")
        return

    if args.domain != "example.com":
        if not ethical_warning(args.domain):
            return

    records = [r.strip().upper() for r in args.records.split(',')]

    run_scan(
        domain           = args.domain,
        wordlist_source  = args.wordlist,
        output_file      = args.output,
        output_format    = args.format,
        threads          = args.threads,
        timeout          = args.timeout,
        verbose          = args.verbose,
        resolver_ip      = args.resolver,
        probe_http       = args.http,
        record_types     = records,
        do_zone_transfer = args.axfr,
        retries          = args.retries,
        rate_limit       = args.rate,
        checkpoint_file  = args.checkpoint,
    )

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_direct()
    else:
        if not DNS_AVAILABLE:
            print(c("[!] Install dnspython: pip install dnspython", Color.RED))
            sys.exit(1)
        SubratShell().run()
