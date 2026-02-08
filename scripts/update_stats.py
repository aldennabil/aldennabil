#!/usr/bin/env python3
"""
Script to update GitHub README with profile statistics
"""

import os
import requests
from datetime import datetime

GITHUB_USERNAME = "aldennabil"
README_PATH = "README.md"

def get_github_stats(username):
    """Fetch GitHub user statistics"""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.json()

def get_github_repos(username):
    """Fetch GitHub repositories"""
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
    response = requests.get(url)
    return response.json()

def get_language_stats(repos):
    """Calculate programming language statistics"""
    languages = {}
    for repo in repos:
        if repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    return languages

def generate_stats_section(username):
    """Generate statistics section for README"""
    stats = get_github_stats(username)
    repos = get_github_repos(username)
    languages = get_language_stats(repos)
    
    # Sort repos by stars
    top_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:5]
    
    # Create stats markdown
    stats_md = f"""
## 📊 GitHub Statistics

| Metric | Value |
|--------|-------|
| Public Repos | {stats['public_repos']} |
| Followers | {stats['followers']} |
| Following | {stats['following']} |
| Public Gists | {stats['public_gists']} |

## 🔤 Top Languages

"""
    
    # Add language stats
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_md += f"- **{lang}**: {count} repos\n"
    
    # Add top repositories
    stats_md += "\n## ⭐ Top Repositories\n\n"
    
    for repo in top_repos:
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        desc = repo['description'] or 'No description'
        url = repo['html_url']
        lang = repo['language'] or 'N/A'
        
        stats_md += f"""
### [{repo['name']}]({url})
{desc}
- ⭐ Stars: {stars}
- 🔀 Forks: {forks}
- 🔤 Language: {lang}

"""
    
    # Add timestamp
    stats_md += f"\n---\n**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    
    return stats_md

def update_readme(stats_section):
    """Update README with new statistics"""
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace stats section
    start_marker = "<!-- STATS-START -->"
    end_marker = "<!-- STATS-END -->"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        
        updated_content = (
            content[:start_idx] + 
            "\n" + stats_section + "\n" + 
            content[end_idx:]
        )
    else:
        # If markers don't exist, append to end
        updated_content = content + "\n\n" + stats_section
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ README updated successfully!")

if __name__ == "__main__":
    print(f"🔄 Fetching stats for {GITHUB_USERNAME}...")
    stats = generate_stats_section(GITHUB_USERNAME)
    update_readme(stats)
    print("✨ Done!")
