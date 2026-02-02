import requests
from bs4 import BeautifulSoup


URL = "https://in.indeed.com/viewjob?jk=5ddd43ad65fb0ac7"

def fetch_job_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://in.indeed.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def extract_text(soup, selector_config):
    """
    Helper to extract text using various selector strategies.
    selector_config is a list of (tag, attrs) tuples to try in order.
    """
    for tag, attrs in selector_config:
        element = soup.find(tag, attrs)
        if element:
            return element.get_text(strip=True)
    return "N/A"

def parse_job(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Job Title (prefer h1)
    title = extract_text(soup, [
        ("h1", {}),
        ("div", {"class": "jobsearch-JobInfoHeader-title"}),
        ("h2", {"class": "jobsearch-JobInfoHeader-title"})
    ])

    # 2. Company Name
    company = extract_text(soup, [
        ("div", {"data-testid": "inlineHeader-companyName"}),
        ("a", {"data-testid": "inlineHeader-companyName"}),
        ("div", {"class": "jobsearch-CompanyInfoContainer"}) # Fallback, might be messy
    ])

    # 3. Job Location
    location = extract_text(soup, [
        ("div", {"data-testid": "inlineHeader-companyLocation"}),
        ("div", {"class": "jobsearch-JobInfoHeader-subtitle"}) # Fallback, might include company
    ])

    # 4. Job Description
    description = extract_text(soup, [
        ("div", {"id": "jobDescriptionText"}),
        ("div", {"class": "jobsearch-jobDescriptionText"})
    ])

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description
    }

def main():
    html = fetch_job_page(URL)
    if not html:
        return

    print("Page fetched successfully")
    print(f"HTML Length: {len(html)}")

    job_data = parse_job(html)

    print("\n--- JOB DATA ---")
    print(f"Title: {job_data['title']}")
    print(f"Company: {job_data['company']}")
    print(f"Location: {job_data['location']}")
    
    print("\nDescription preview:")
    if job_data['description'] != "N/A":
        print(job_data['description'][:500])
    else:
        print("N/A")

if __name__ == "__main__":
    main()
