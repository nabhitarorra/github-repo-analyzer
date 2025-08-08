import base64
import spacy
import pandas as pd
from github import Github, RateLimitExceededException, UnknownObjectException
from collections import Counter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Pre-defined list of common tech keywords for better tagging
TECH_KEYWORDS = [
    'react', 'angular', 'vue', 'python', 'javascript', 'typescript', 'java',
    'c++', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala',
    'fastapi', 'flask', 'django', 'node.js', 'express', 'spring', 'docker',
    'kubernetes', 'aws', 'azure', 'gcp', 'terraform', 'ansible', 'jenkins',
    'ci/cd', 'postgresql', 'mysql', 'mongodb', 'redis', 'kafka', 'graphql',
    'rest', 'api', 'html', 'css', 'd3.js', 'pytorch', 'tensorflow', 'scikit-learn'
]


class RepoAnalyzer:
    def __init__(self, github_token):
        if not github_token:
            raise ValueError("GitHub API token is required.")
        self.github_client = Github(github_token)

    def analyze(self, repo_url):
        try:
            repo_name = repo_url.replace("https://github.com/", "")
            repo = self.github_client.get_repo(repo_name)
        except UnknownObjectException:
            return {"error": f"Repository not found: {repo_name}"}
        except RateLimitExceededException:
            return {"error": "GitHub API rate limit exceeded. Please wait and try again."}
        except Exception:
            return {"error": f"Invalid repository URL: {repo_url}"}

        readme_content = self._get_readme_content(repo)
        commit_freq = self._get_commit_frequency(repo)

        analysis_result = {
            "stats": {
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.subscribers_count,
                "open_issues": repo.open_issues_count,
                "language": repo.language,
            },
            "commit_frequency": commit_freq,
            "readme_tags": self._analyze_readme_tags(readme_content) if readme_content else [],
            "error": None
        }
        return analysis_result

    def _get_readme_content(self, repo):
        try:
            readme = repo.get_readme()
            return base64.b64decode(readme.content).decode('utf-8')
        except Exception:
            return None

    def _get_commit_frequency(self, repo):
        try:
            commits = repo.get_commits()
            dates = [commit.commit.author.date.strftime('%Y-%U') for commit in
                     commits[:200]]  # Analyze last 200 commits
            freq = Counter(dates)

            # Create a full date range for the last 52 weeks for a complete graph
            end_date = pd.to_datetime('today')
            start_date = end_date - pd.DateOffset(weeks=52)
            all_weeks = pd.date_range(start=start_date, end=end_date, freq='W-SUN').strftime('%Y-%U')

            commit_data = {week: freq.get(week, 0) for week in all_weeks}
            return commit_data
        except Exception:
            return {}

    def _analyze_readme_tags(self, text):
        # Convert text to lowercase for case-insensitive matching
        lower_text = text.lower()
        tags = set()

        # Find matches from our pre-defined tech list
        for keyword in TECH_KEYWORDS:
            if keyword in lower_text:
                tags.add(keyword)

        # Use spaCy for more advanced entity recognition
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                # If a recognized entity is in our tech list, add it for consistency
                if ent.text.lower() in TECH_KEYWORDS:
                    tags.add(ent.text.lower())

        return sorted(list(tags))[:15]  # Return top 15 tags