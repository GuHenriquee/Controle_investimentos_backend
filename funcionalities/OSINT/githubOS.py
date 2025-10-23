from github import Github
from ignore import Gitignore
from github import Auth
from objects.gitOB import Git
from urllib.parse import urlparse



def githubAnalise(cripto_id: str, url: str)->Git | None :

    auth = Auth.Token(Gitignore.GITHUB_TOKEN)
    g = Github(auth=auth)
    
    try:
        path = urlparse(url).path 
        repo_name = path.strip("/")
        repo = g.get_repo(repo_name)

        git_on_db = Git(
            id = cripto_id,
            last_commit = repo.pushed_at,
            stars_number = repo.stargazers_count,
            issues_count = repo.open_issues_count,
            forks = repo.forks_count,
            created_at = repo.created_at
        )
        return git_on_db
        
    except Exception as e:
        print(e)
        return None    


urls = "https://github.com/ethereum/go-ethereum"
githubAnalise(urls)
        