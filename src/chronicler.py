import os
import click
from git import Repo, GitCommandError
from langchain_community.llms import Ollama
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAI

def create_llm(llm: str, llm_model: str) -> OpenAI | Ollama:
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
        return Ollama(model=llm_model)

    raise ValueError(f"Unsupported LLM: {llm}")

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

    docs = [Document(page_content="commits")]

    prompt = PromptTemplate.from_template("""
        Act as a release manager reviewing commits between two branches.
        Write release notes, avoiding hash numbers, developer names, and dates.
        Branches compared: Left branch: {left_branch}, Right branch: {right_branch}.
        Summary of top contributors for these changes.
        Release notes for the current diff branches:\n\n{context}\n
    """)

    llm_instance = create_llm(llm, llm_model)
    chain = create_stuff_documents_chain(llm_instance, prompt)

    release_notes = chain.invoke({
        "left_branch": left_branch,
        "right_branch": right_branch,
        "context": docs
    })

    return release_notes

@click.command()
@click.option('--llm', type=click.Choice(['ollama', 'openai']), default='ollama', help='LLM to use (e.g., ollama, openai)')
@click.option('--llm-model', default='llama2', help='Model to use for ollama (e.g., llama2, mistral)')
@click.argument('left_branch')
@click.argument('right_branch')
@click.argument('path', type=click.Path(exists=True))
def cli(llm, llm_model, left_branch, right_branch, path):
    """
    Command line interface for generating release notes for a Git repository.
    Compares two branches and generates a summary of changes.
    """
    try:
        summary = generate_release_notes(path, left_branch, right_branch, llm, llm_model)
        print(f'{summary}')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    cli()
