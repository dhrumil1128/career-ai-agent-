"""
jobs.py - LinkedIn Job Search Only
"""

import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import urllib.parse

class LinkedInJobs:
    """Get real jobs from LinkedIn public search"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def get_jobs(self, query: str, limit: int = 5) -> List[Dict]:
        """Get real job listings from LinkedIn"""
        try:
            # LinkedIn jobs search endpoint
            url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            
            params = {
                "keywords": query,
                "location": "Worldwide",
                "f_TPR": "r86400",  # Last 24 hours
                "start": "0"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return self._get_search_link(query)
            
            # Parse HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', class_='base-search-card__info')
            
            jobs = []
            for card in job_cards[:limit]:
                job = self._parse_card(card)
                if job:
                    jobs.append(job)
            
            if jobs:
                return jobs
            else:
                return self._get_search_link(query)
                
        except Exception:
            return self._get_search_link(query)
    
    def _parse_card(self, card) -> Dict:
        """Parse job card from HTML"""
        try:
            # Get job title
            title_elem = card.find('h3', class_='base-search-card__title')
            title = title_elem.text.strip() if title_elem else "Job"
            
            # Get company
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            company = company_elem.text.strip() if company_elem else "Company"
            
            # Get location
            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.text.strip() if location_elem else "Remote"
            
            # NEW:
            # Find the job link properly
            # In _parse_card function, replace the URL extraction part:

            # Get the ACTUAL LinkedIn href
            link_elem = card.find_parent('a', class_='base-card__full-link')
            if link_elem and link_elem.has_attr('href'):
                href = link_elem['href']
                
                # If it's a relative URL (starts with /), make it full URL
                if href.startswith('/'):
                    href = f"https://www.linkedin.com{href}"
                
                # Check if href already has currentJobId
                if 'currentJobId=' in href:
                    url = href  # Use as-is, it's already correct
                else:
                    # Extract job ID from pattern like /jobs/view/123456789/
                    import re
                    job_id_match = re.search(r'/jobs/view/(\d+)', href)
                    if job_id_match:
                        job_id = job_id_match.group(1)
                        # Build proper LinkedIn URL with currentJobId
                        encoded_title = title.replace(' ', '%20')
                        encoded_company = company.replace(' ', '%20')
                        url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}&keywords={encoded_title}%20{encoded_company}"
                    else:
                        # Fallback: use the href as-is
                        url = href
            else:
                # No link found, create search URL
                encoded_query = f"{title} {company}".replace(' ', '%20')
                url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}"
            
            # NEW:
            # Get the job metadata properly
            metadata_elem = card.find('div', class_='base-search-card__metadata')
            if metadata_elem:
                # Clean up the metadata text
                meta_text = metadata_elem.get_text(" ", strip=True)
                # Remove location if it appears twice
                meta_text = meta_text.replace(location, "").strip()
                description = meta_text if meta_text else f"{title} at {company}"
            else:
                description = f"{title} position at {company}"

            # Clean description
            description = " ".join(description.split())  # Remove extra spaces
            description = description[:120] + "..." if len(description) > 120 else description

            return {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": url,
                "source": "LinkedIn"
            }
        except:
            return None
    
    def _get_search_link(self, query: str) -> List[Dict]:
        """Return LinkedIn search link if scraping fails"""
        encoded = urllib.parse.quote(query)
        linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded}"
        
        return [{
            "title": f"Search {query} jobs on LinkedIn",
            "company": "LinkedIn",
            "location": "Worldwide",
            "description": "Click to search real jobs on LinkedIn",
            "url": linkedin_url,
            "source": "LinkedIn Search"
        }]

# Create instance
linkedin = LinkedInJobs()

def format_job(job: Dict) -> str:
    """Format job for display"""
    title = job['title']
    company = job['company']
    location = job['location']
    description = job['description']
    url = job['url']
    
    # NEW:
    if url and url != "#" and "linkedin.com" in url:
        display_url = url
    else:
        # Create a search link as fallback
        search_query = f"{title} {company}".replace(" ", "+")
        display_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
    
    return (
        f"**{title}**\n"
        f"**Company:** {company}\n"
        f"**Location:** {location}\n"
        f"**Description:** {description}\n"
        f"**Apply:** {display_url}\n"
        f"---"
    )



def search_jobs(query: str) -> List[str]:
    """Search for jobs"""
    clean_query = query.replace("jobs", "").replace("for", "").strip()
    
    if not clean_query:
        clean_query = "developer"
    
    jobs = linkedin.get_jobs(clean_query, limit=5)
    
    # Format results
    result = []
    for job in jobs:
        result.append(format_job(job))
    
    return result

def search_jobs_by_skills(resume_text: str, role: str = "Software Engineer") -> List[str]:
    """Search jobs based on resume skills"""
    resume_lower = resume_text.lower()
    
    if 'python' in resume_lower:
        return search_jobs('python developer')
    elif 'java' in resume_lower:
        return search_jobs('java developer')
    elif 'javascript' in resume_lower:
        return search_jobs('javascript developer')
    elif 'data' in resume_lower:
        return search_jobs('data scientist')
    elif 'aws' in resume_lower or 'cloud' in resume_lower:
        return search_jobs('devops engineer')
    else:
        return search_jobs(role)