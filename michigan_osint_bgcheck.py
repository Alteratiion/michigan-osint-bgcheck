import argparse
import webbrowser
import json
from datetime import datetime
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

console = Console()

def open_url(name: str, url: str):
    if url:
        console.print(f"[bold green]📌 Opening:[/bold green] {name}")
        webbrowser.open(url)
        return url
    return None

def scrape_fastpeoplesearch(first: str, last: str, state: str = "MI"):
    console.print("[yellow]Attempting to scrape FastPeopleSearch (may take 10-30s, respects protections)...[/yellow]")
    try:
        driver = uc.Chrome(headless=True, use_subprocess=False)
        url = f"https://www.fastpeoplesearch.com/name/{first.lower()}-{last.lower()}_{state.lower()}"
        driver.get(url)
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []
        for card in soup.select(".search-result"):
            name_tag = card.select_one(".name")
            age_tag = card.select_one(".age")
            addr_tag = card.select_one(".address")
            phones = [p.get_text(strip=True) for p in card.select(".phone")]
            name = name_tag.get_text(strip=True) if name_tag else ""
            age = age_tag.get_text(strip=True) if age_tag else ""
            address = addr_tag.get_text(strip=True) if addr_tag else ""
            results.append({"name": name, "age": age, "address": address, "phones": phones})
        driver.quit()
        if results:
            df = pd.DataFrame(results)
            df.to_excel("fastpeoplesearch_results.xlsx", index=False)
            console.print(f"[green]✅ Scraped {len(results)} results → fastpeoplesearch_results.xlsx[/green]")
        return results
    except Exception as e:
        console.print(f"[red]Scraping failed (common with protections): {e}[/red]")
        return []

def main():
    parser = argparse.ArgumentParser(description="Michigan-Focused Personal OSINT Background Check Tool (Open Source)")
    parser.add_argument("first_name", help="First name")
    parser.add_argument("last_name", help="Last name")
    parser.add_argument("--state", default="MI", help="Two-letter state (default: MI)")
    parser.add_argument("--city", default="", help="Optional city (e.g., Detroit)")
    parser.add_argument("--dob", default="", help="Optional DOB (YYYY-MM-DD) — improves accuracy")
    parser.add_argument("--scrape", action="store_true", help="Enable FastPeopleSearch scraping")
    parser.add_argument("--output", default="bgcheck_report.json", help="Output JSON file")
    args = parser.parse_args()

    full_name = f"{args.first_name} {args.last_name}".strip()
    query = f"{full_name} {args.city} {args.state}".strip()

    console.print(Panel(f"[bold cyan]🚀 Shepherd OSINT Flock — Michigan Background Check for {full_name} in {args.state}[/bold cyan]", expand=False))

    # 2026 Verified Michigan URLs
    searches = {
        "FastPeopleSearch": f"https://www.fastpeoplesearch.com/name/{full_name.lower().replace(' ', '-')}_{args.state.lower()}",
        "TruePeopleSearch": f"https://www.truepeoplesearch.com/results?name={full_name.replace(' ', '%20')}&state={args.state}",
        "JudyRecords (Court Cases)": f"https://www.judyrecords.com/?q={query.replace(' ', '+')}",
        "Google Advanced OSINT": f"https://www.google.com/search?q=%22{full_name}%22+{args.state}+(arrest+OR+court+OR+record+OR+news+OR+obituary)",
        "MiCOURT Case Search (Statewide — note 7-year limit on some criminal sentences)": "https://micourt.courts.michigan.gov/case-search/",
        "MDOC OTIS (Incarceration/Parole/Probation)": "https://mdocweb.state.mi.us/otis2/otis2.aspx",
        "Michigan Public Sex Offender Registry (PSOR)": "https://mspsor.com/Home/Search",
        "ICHAT (Michigan Criminal History — $10 fee per search)": "https://apps.michigan.gov/ICHAT/",
        "LARA License Lookup (Professional/Business)": "https://aca-prod.accela.com/MILARA/GeneralProperty/PropertyLookUp.aspx?isLicensee=Y",
        "NSOPW National Sex Offender": f"https://www.nsopw.gov/search?firstName={args.first_name}&lastName={args.last_name}&state={args.state}",
    }

    report = {
        "timestamp": datetime.now().isoformat(),
        "query": {"name": full_name, "state": args.state.upper(), "city": args.city, "dob": args.dob},
        "searches_performed": {},
        "notes": "Public records only. ICHAT requires payment. MiCOURT has 7-year limits on some criminal sentences. Bulk scraping prohibited on official sites. Data can be incomplete/outdated/wrong. Personal OSINT use only — respect all laws and ToS.",
        "scraped_data": None
    }

    table = Table(title="Launched Public Searches")
    table.add_column("Source", style="cyan")
    table.add_column("Status", style="green")

    for name, url in searches.items():
        if "ICHAT" in name or "MiCOURT" in name:
            console.print(f"[yellow]⚠️ Note:[/yellow] {name} may require manual DOB or payment.")
        performed = open_url(name, url)
        if performed:
            report["searches_performed"][name] = performed
            table.add_row(name, "✅ Opened")

    console.print(table)

    if args.scrape and args.state.upper() == "MI":
        scraped = scrape_fastpeoplesearch(args.first_name, args.last_name, args.state)
        report["scraped_data"] = scraped

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    console.print(f"\n[bold green]✅ Structured report saved → {args.output}[/bold green]")
    console.print("[bold yellow]Review every tab. For county-specific courts (Wayne uses Odyssey, Oakland has Court Explorer, etc.), visit local clerk sites.[/bold yellow]")
    console.print("[dim]Personal OSINT only. Respect ToS, rate limits, and Michigan/Federal laws.[/dim]")

if __name__ == "__main__":
    main()
