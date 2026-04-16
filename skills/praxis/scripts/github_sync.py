import subprocess
import json
import os
import sys


def fetch_github_repos(username):
    try:
        # Use gh cli to fetch repos
        cmd = [
            "gh",
            "repo",
            "list",
            username,
            "--visibility=public",
            "--json",
            "name,description,primaryLanguage,url",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        repos = json.loads(result.stdout)

        projects = []
        for repo in repos:
            lang = repo.get("primaryLanguage")
            projects.append(
                {
                    "name": repo.get("name"),
                    "description": repo.get("description") or "",
                    "url": repo.get("url"),
                    "language": lang.get("name") if lang else None,
                }
            )
        return projects
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch repositories: {e.stderr}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error parsing repositories: {e}", file=sys.stderr)
        return []


def main():
    username = "ksmeltzer"
    print(f"Fetching public repositories for {username}...")
    projects = fetch_github_repos(username)

    if not projects:
        print("No projects found or fetch failed.")
        return

    kb_path = ".praxis/data/knowledge_base.json"
    if not os.path.exists(kb_path):
        print(f"Knowledge base file not found at {kb_path}")
        return

    try:
        with open(kb_path, "r") as f:
            kb = json.load(f)

        kb["Projects"] = projects

        with open(kb_path, "w") as f:
            json.dump(kb, f, indent=2)

        print(f"Successfully updated {kb_path} with {len(projects)} projects.")
    except Exception as e:
        print(f"Failed to update knowledge base: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
