# Michigan OSINT Background Check Tool

**Personal open-source automation for public records OSINT.**  
Input: name + state (defaults to MI). Opens pre-filled searches across major public sources + optional scraping of people-finder sites.

## ⚠️ LEGAL & ETHICAL DISCLAIMER (Read Carefully)
This tool accesses **publicly available information only**.  
- For **personal/educational OSINT use only**.  
- **NOT** for harassment, stalking, employment screening (FCRA violations), or commercial purposes.  
- You are solely responsible for compliance with CFAA, Michigan laws, site ToS, and all applicable regulations.  
- Data can be incomplete, outdated, or incorrect. This is **NOT** an official background check.  
- ICHAT costs $10 per search. MiCOURT limits some criminal records to 7 years. Bulk downloads prohibited on official sites.

## Features
- One-command launch of 10+ verified public searches (FastPeopleSearch, MiCOURT, MDOC OTIS, PSOR, ICHAT, etc.)
- Rich colored terminal output with rich library
- Optional Selenium scraping → Excel export of addresses/phones
- Timestamped JSON report with notes
- Michigan-optimized with 2026 URLs

## Installation
```bash
git clone https://github.com/Alteration/michigan-osint-bgcheck.git
cd michigan-osint-bgcheck
pip install -r requirements.txt# michigan-osint-bgcheck
