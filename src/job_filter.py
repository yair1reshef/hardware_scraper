from typing import Dict, List, Set

class JobFilter:
    """
    Centralized filter for job listings.
    Ensures only relevant jobs (students/interns) are kept and irrelevant ones (HR, Sales, etc.) are excluded.
    """
    
    POSITIVE_KEYWORDS = {
        'student', 'intern', 'internship', 'co-op', 
        'סטודנט', 'התמחות'
    }
    
    NEGATIVE_KEYWORDS = {
        'hr', 'marketing', 'finance', 'legal', 'sales', 'admin',
        'משאבי אנוש', 'שיווק', 'כספים'
    }

    def __init__(self, target_locations: List[str] = None):
        """
        Initialize the filter.
        
        Args:
            target_locations: List of strings that must be present in the location field.
                              If None, location filtering is disabled.
                              Example: ['Israel', 'IL', 'ישראל']
        """
        self.target_locations = [loc.lower() for loc in target_locations] if target_locations else None

    def is_relevant(self, job: Dict[str, str]) -> bool:
        """
        Check if a job is relevant based on title, location, and other attributes.
        
        Args:
            job: Dictionary containing job details (must have 'title', optional 'location').
            
        Returns:
            True if the job is relevant, False otherwise.
        """
        title = job.get('title', '').lower()
        location = job.get('location', '').lower()
        
        # 1. Location Filter (if enabled)
        if self.target_locations:
            has_valid_location = False
            for loc in self.target_locations:
                if loc in location:
                    has_valid_location = True
                    break
            if not has_valid_location:
                return False

        # 2. Negative Keywords (Must NOT include any)
        for keyword in self.NEGATIVE_KEYWORDS:
            if keyword in title:
                return False
                
        # 3. Positive Keywords (Must include at least one)
        has_positive = False
        for keyword in self.POSITIVE_KEYWORDS:
            if keyword in title:
                has_positive = True
                break
        
        if not has_positive:
            return False
            
        return True

    def filter_jobs(self, jobs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Filter a list of jobs.
        
        Args:
            jobs: List of job dictionaries.
            
        Returns:
            List of relevant job dictionaries.
        """
        return [job for job in jobs if self.is_relevant(job)]
