import os
import click
from git import Repo, GitCommandError
from langchain_ollama.llms import OllamaLLM
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAI

# Functions

def create_llm(llm: str, llm_model: str) -> OpenAI | OllamaLLM:
    """
    Creates and returns the language model.
    :param llm: The name of the language model (e.g., 'openai', 'ollama').
    :param llm_model: The specific model of the language model (e.g., 'llama2', 'mistral').
    :return: An instance of the specified language model.
    """
    if llm == 'openai':
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            openai_api_key = click.prompt('Please enter your OpenAI API key', hide_input=True)
        if not openai_api_key:
            raise ValueError("OpenAI API key is required.")
        return OpenAI(openai_api_key=openai_api_key)

    elif llm == 'ollama':
        return OllamaLLM(model=llm_model)

    raise ValueError(f"Unsupported LLM: {llm}")

# Commands

def generate_commit_description(repo_path: str, llm: str, llm_model: str) -> str:
    """
    Generates a detailed description for the most recent commit in a given Git repository.

    This function analyzes the latest commit changes using the repository's `status --v` output and utilizes a specified Language Learning Model (LLM) to generate a clear and comprehensive commit description.

    Parameters:
    - repo_path (str): The file system path to the Git repository.
    - llm (str): The name of the language learning model to use (e.g., 'ollama', 'openai').
    - llm_model (str): The specific model to use for the chosen LLM (e.g., 'llama2', 'mistral').

    Returns:
    - str: A string containing the formatted commit title and detailed notes, encapsulating the essence of the changes made in the commit.

    Raises:
    - RuntimeError: If there is an error in accessing the Git repository or processing the commit data.

    Example:
    >>> generate_commit_description('/path/to/repo', 'ollama', 'llama2')
    'Title: Enhanced Feature X\n-----\nDescription: This commit introduces improvements to Feature X, including...'

    The function first attempts to access the Git repository at the specified path. It then retrieves the status of the latest commit. This data, along with the chosen LLM and its model, is used to construct a detailed narrative of the commit, highlighting key changes, technical advancements, and the overall impact of the commit.
    """
        
    try:
        repo = Repo(repo_path)
        repo_status = repo.git().status('-v')
    except GitCommandError as e:
        raise RuntimeError(f"Git error: {e}")

    docs = [Document(page_content=repo_status)]

    prompt = PromptTemplate.from_template("""

        I need to generate concise and informative commit notes and a commit subject from the following `git status -v` output. The output should be structured to clearly communicate:

        1. **Summary of Changes**: Briefly highlight new features, enhancements, and bug fixes.
        2. **Major Changes**: Provide detailed descriptions of significant updates, focusing on their impact and benefits.
        3. **Technical Details**: Include any relevant code snippets or technical information.

        \n
        {context}
        \n
        Based on this, create a commit subject and notes in a professional format suitable for team members and stakeholders. The format should be:

        Subject
        -------
        [commit subject]

        Description
        -----------
        [commit notes]
                                                
    """)

    llm_instance = create_llm(llm, llm_model)
    chain = create_stuff_documents_chain(llm_instance, prompt)

    commit_description = chain.invoke({
        "context": docs
    })

    return commit_description

def generate_release_notes(repo_path: str, left_branch: str, right_branch: str, llm: str, llm_model: str) -> str:
    """
    Generates release notes by comparing two branches in a Git repository.
    :param repo_path: Path to the Git repository.
    :param left_branch: The name of the left branch for comparison.
    :param right_branch: The name of the right branch for comparison.
    :param llm: The language model to use.
    :param llm_model: The specific model of the language model.
    :return: Generated release notes.
    """

    try:
        repo = Repo(repo_path)
        commits = repo.git.log('--left-right', f'{left_branch}...{right_branch}')
    except GitCommandError as e:
        raise RuntimeError(f"Git error: {e}")

    docs = [Document(page_content=commits)]

    prompt = PromptTemplate.from_template("""

        I require assistance in generating release notes based on the following diff output between two branches (Left branch: {left_branch}, Right branch: {right_branch}) from our Git repository. The release notes should encompass:

        1. A summary of the changes, including new features, enhancements, and bug fixes.
        2. Detailed descriptions of major changes, emphasizing their impact and advantages.
        3. Any pertinent technical details or code snippets that are relevant.
        4. After the release notes, provide statistical data about the contributors, such as the number of commits per contributor, lines of code added or removed, and other relevant metrics.
        \n
        {context}
        \n
        Please format the release notes and the contributor statistics in a clear and professional manner, suitable for distribution to our team and stakeholders.
                                                
    """)

    llm_instance = create_llm(llm, llm_model)
    chain = create_stuff_documents_chain(llm_instance, prompt)

    release_notes = chain.invoke({
        "left_branch": left_branch,
        "right_branch": right_branch,
        "context": docs
    })

    return release_notes

## Prompting

@click.group()
def cli():
    pass

@cli.command('release', help='Generate release notes')
@click.argument('left_branch')
@click.argument('right_branch')
@click.argument('path', nargs=1, type=click.Path(exists=True), default='.')
@click.option('--llm', type=click.Choice(['ollama', 'openai']), default='ollama', help='LLM to use (e.g., ollama, openai)')
@click.option('--llm-model', default='llama2', help='Model to use for ollama (e.g., llama2, mistral)')
def release(llm, llm_model, left_branch, right_branch, path):
    try:
        result = generate_release_notes(path, left_branch, right_branch, llm, llm_model)
        
        print(f'{result}')
    except Exception as e:
        print(f"Error: {e}")

@cli.command('commit', help='Generate commit description')
@click.argument('path', nargs=1, type=click.Path(exists=True), default='.')
@click.option('--llm', type=click.Choice(['ollama', 'openai']), default='ollama', help='LLM to use (e.g., ollama, openai)')
@click.option('--llm-model', default='llama2', help='Model to use for ollama (e.g., llama2, mistral)')
def commit(llm, llm_model, path):

    try:
        result = generate_commit_description(path, llm, llm_model)
        
        print(f'{result}')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    cli()
