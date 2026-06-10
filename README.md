subrat – Subdomain Recon Agent Tool
Powered by Sailerbross Technology
Ethical DNS enumerator – use only with permission.

subrat is a fast, beginner‑friendly subdomain discovery tool. It comes with a built‑in wordlist of 100+ common subdomains, so you can start scanning immediately – no external files required. You can also use your own wordlist from anywhere.

✨ Features
🚀 Zero setup – Built‑in wordlist (100+ entries)

📁 External wordlist support – Use any custom list

🎨 Beautiful CLI – Colored output, banners, interactive shell

⚡ Multi‑threaded – Fast DNS resolution

📱 Termux ready – Works on Android

🛡️ Ethical warning – Prompts for permission

💾 Save results – Export found subdomains to a file

📖 Built‑in tutorial – Type tutorial inside the shell

📦 Installation
1. Install Python 3.8+
Download Python (check “Add to PATH” on Windows)

2. Install dnspython
bash
python -m pip install dnspython
3. Download subrat.py
Save the script as subrat.py in your preferred folder.

🚀 Usage
Interactive shell (recommended for beginners)
bash
python subrat.py
Then type commands:

text
subrat> tutorial          # shows step‑by‑step guide
subrat> scan -d example.com
subrat> save results.txt
subrat> exit
Direct command line
bash
# Use built‑in wordlist
python subrat.py -d example.com

# Use your own wordlist
python subrat.py -d target.com -w /path/to/wordlist.txt -o found.txt

# Generate a copy of the built‑in wordlist
python subrat.py --gen-wordlist
Options
Flag	Description
-d, --domain	Target domain (required in direct mode)
-w, --wordlist	Path to external wordlist (optional)
-o, --output	Save results to file
-t, --threads	Number of threads (default 40)
--timeout	DNS timeout in seconds (default 5)
-v, --verbose	Show failed attempts
--resolver	Custom DNS resolver IP (e.g., 1.1.1.1)
--tutorial	Show tutorial and exit
--gen-wordlist	Save built‑in wordlist to a file
📝 Example Output
text
[+] www.example.com -> 93.184.216.34
[+] mail.example.com -> 192.0.2.10
[*] Scan finished. Found 2 live subdomains.
⚠️ Ethical & Legal Warning
This tool performs only DNS queries.
You must have explicit written permission to scan any domain you do not own. Unauthorized scanning may violate laws (CFAA, Computer Misuse Act, etc.) and terms of service. The author assumes no liability for misuse.

🧪 Test Safely
Always test on example.com or your own domain:

bash
python subrat.py -d example.com
🤝 Credit
subrat is powered by Sailerbross Technology – built for ethical hackers, bug bounty hunters, and cybersecurity learners.

📄 License
Free for educational and ethical security testing. Redistribution with credit is allowed.
