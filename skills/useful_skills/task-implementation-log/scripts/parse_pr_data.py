#!/usr/bin/env python3
"""
Parse Pull Request data and extract relevant information for task logs.

Usage:
    python scripts/parse_pr_data.py <pr_data_json>

Input: JSON string containing PR data from GitHub API
Output: Structured data for task log generation
"""

import sys
import json
import re


def extract_ticket_id(text):
    """Extract Jira ticket ID from text (e.g., PROJ-123)"""
    match = re.search(r'([A-Z]+-\d+)', text)
    return match.group(1) if match else None


def determine_task_type(labels, title, description):
    """Determine task type from labels and content"""
    label_names = [label.lower() for label in labels]

    if 'bug' in label_names or 'bugfix' in label_names:
        return "Bug Fix"
    elif 'feature' in label_names or 'enhancement' in label_names:
        return "Feature"
    elif 'refactor' in label_names or 'refactoring' in label_names:
        return "Refactor"
    elif 'chore' in label_names or 'maintenance' in label_names:
        return "Chore"

    # Fallback: check title/description
    text = (title + description).lower()
    if 'fix' in text or 'bug' in text:
        return "Bug Fix"
    elif 'add' in text or 'feature' in text:
        return "Feature"
    elif 'refactor' in text or 'improve' in text:
        return "Refactor"

    return "Change"


def rank_file_significance(files):
    """
    Rank files by significance.

    Priority:
    1. Core source files (src/, lib/, app/)
    2. New files
    3. Files with substantial changes (>50 lines)
    4. Configuration files
    5. Tests
    6. Documentation
    """
    ranked = []

    for file in files:
        filename = file.get('filename', '')
        additions = file.get('additions', 0)
        deletions = file.get('deletions', 0)
        status = file.get('status', '')

        score = 0

        # Core source files
        if any(filename.startswith(prefix) for prefix in ['src/', 'lib/', 'app/', 'core/']):
            score += 100

        # New files
        if status == 'added':
            score += 50

        # Substantial changes
        total_changes = additions + deletions
        if total_changes > 100:
            score += 30
        elif total_changes > 50:
            score += 20

        # Configuration files
        if filename.endswith(('.json', '.yml', '.yaml', '.toml', '.ini', '.config')):
            score += 10

        # Tests (lower priority)
        if 'test' in filename.lower() or filename.startswith('tests/'):
            score -= 20

        # Documentation (lowest priority)
        if filename.endswith(('.md', '.rst', '.txt')) or 'docs/' in filename:
            score -= 30

        ranked.append((score, filename, total_changes, status))

    # Sort by score descending
    ranked.sort(key=lambda x: x[0], reverse=True)

    return ranked


def parse_pr_data(pr_data):
    """Parse PR data and extract structured information"""
    result = {
        'title': pr_data.get('title', ''),
        'description': pr_data.get('body', ''),
        'labels': [label.get('name', '') for label in pr_data.get('labels', [])],
        'files': pr_data.get('files', []),
        'commits': pr_data.get('commits', []),
        'url': pr_data.get('html_url', '')
    }

    # Extract ticket ID
    ticket_id = extract_ticket_id(result['title'])
    if not ticket_id:
        ticket_id = extract_ticket_id(result['description'])
    result['ticket_id'] = ticket_id

    # Determine task type
    result['task_type'] = determine_task_type(
        result['labels'],
        result['title'],
        result['description']
    )

    # Rank files by significance
    result['significant_files'] = rank_file_significance(result['files'])[:10]

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_pr_data.py <pr_data_json>")
        sys.exit(1)

    pr_data = json.loads(sys.argv[1])
    result = parse_pr_data(pr_data)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
