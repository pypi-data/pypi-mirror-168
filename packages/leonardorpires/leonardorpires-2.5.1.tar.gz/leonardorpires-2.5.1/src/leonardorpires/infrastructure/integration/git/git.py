import git


class Git(object):
    @staticmethod
    def get_last_commit():
        repo = git.Repo(search_parent_directories=True)
        last_commit = repo.head.object.hexsha
        return last_commit

    @staticmethod
    def get_last_commit_of_a_file(file_path: str):
        commits = list(git.Repo().iter_commits())
        file_commits = list()
        for commit in commits:
            files = git.Repo().git.show("--pretty=", "--name-only", commit.hexsha)
            if file_path in files:
                file_commits.append(commit)

        return file_commits[0].hexsha
