import unittest
from src.job_filter import JobFilter

class TestJobFilter(unittest.TestCase):
    def setUp(self):
        self.filter = JobFilter()

    def test_positive_keywords(self):
        """Test that jobs with positive keywords are accepted"""
        relevant_titles = [
            "Software Student",
            "Hardware Intern",
            "Summer Internship",
            "Co-op Engineer",
            "סטודנט למדעי המחשב",
            "משרת התמחות"
        ]
        for title in relevant_titles:
            self.assertTrue(self.filter.is_relevant({'title': title}), f"Should accept: {title}")

    def test_negative_keywords(self):
        """Test that jobs with negative keywords are rejected"""
        irrelevant_titles = [
            "HR Manager",
            "Marketing Specialist",
            "Finance Intern",  # Has 'Intern' but also 'Finance' -> Should be rejected
            "Legal Advisor",
            "Sales Representative",
            "Admin Assistant",
            "מנהל משאבי אנוש",
            "איש שיווק",
            "חשב כספים"
        ]
        for title in irrelevant_titles:
            self.assertFalse(self.filter.is_relevant({'title': title}), f"Should reject: {title}")

    def test_mixed_keywords(self):
        """Test edge cases with mixed keywords"""
        # Positive keyword but no negative -> Accept
        self.assertTrue(self.filter.is_relevant({'title': "Engineering Student"}))
        
        # Negative keyword only -> Reject
        self.assertFalse(self.filter.is_relevant({'title': "Senior HR"}))
        
        # Both positive and negative -> Reject (Negative takes precedence in logic: AND NOT negative)
        self.assertFalse(self.filter.is_relevant({'title': "HR Intern"}))
        self.assertFalse(self.filter.is_relevant({'title': "Student Marketing Position"}))

    def test_no_keywords(self):
        """Test jobs with neither positive nor negative keywords"""
        # Should be rejected because it must have at least one positive keyword
        self.assertFalse(self.filter.is_relevant({'title': "Senior Engineer"}))
        self.assertFalse(self.filter.is_relevant({'title': "Software Developer"}))
        self.assertFalse(self.filter.is_relevant({'title': "Team Lead"}))

if __name__ == '__main__':
    unittest.main()
