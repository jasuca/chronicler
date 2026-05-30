import os

import click
from git import Repo, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_openai import OpenAI


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
        return OpenAI(openai_api_key=openai_api_key, model_name=llm_model)

    elif llm == 'ollama':
        return OllamaLLM(model=llm_model)

    raise ValueError(f"Unsupported LLM: {llm}")


def generate_commit_description(repo_path: str, llm: str, llm_model: str) -> str:
    """
    Generates a detailed description for the most recent commit in a given Git repository.

    This function opens the Git repository at ``repo_path``, reads
    ``git status -v`` output, wraps that output in a LangChain ``Document``,
    and asks the selected language model to draft a professional commit
    subject and description. ``git status -v`` is used because it includes the
    staged diff in addition to the normal status summary, giving the model
    enough context to describe the commit that is about to be created.

    Parameters:
        repo_path: File-system path to the Git repository to inspect.
        llm: Language model provider to use. Supported values are ``openai``
            and ``ollama``.
        llm_model: Provider-specific model name. For Ollama this is typically
            a local model such as ``llama2`` or ``mistral``; for OpenAI it is
            passed as the OpenAI completion model name.

    Returns:
        A formatted string containing a commit subject and detailed notes.

    Raises:
        RuntimeError: If the path cannot be opened as a Git repository or Git
            cannot produce the status output.
        ValueError: If ``llm`` is not a supported provider, or if the selected
            provider is missing required credentials.

    Example:
        >>> generate_commit_description('/path/to/repo', 'ollama', 'llama2')
        'Subject\\n-------\\nImprove release notes\\n\\nDescription\\n-----------\\n...'
    """

    try:
        repo = Repo(repo_path)
        repo_status = repo.git.status('-v')
    except (GitCommandError, InvalidGitRepositoryError, NoSuchPathError) as e:
        raise RuntimeError(f"Git error: {e}")

    docs = [Document(page_content=repo_status)]

    prompt = PromptTemplate.from_template("""
        I need to generate concise and informative commit notes and a commit
        subject from the following `git status -v` output.

        1. **Summary of Changes**: Briefly highlight new features, enhancements, and bug fixes.
        2. **Major Changes**: Provide detailed descriptions of significant updates, focusing on their impact and benefits.
        3. **Technical Details**: Include any relevant code snippets or technical information.

        \n
        {context}
        \n
        Based on this, create a commit subject and notes in a professional
        format suitable for team members and stakeholders. The format should be:

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
    except (GitCommandError, InvalidGitRepositoryError, NoSuchPathError) as e:
        raise RuntimeError(f"Git error: {e}")

    docs = [Document(page_content=commits)]

    prompt = PromptTemplate.from_template("""
        I require assistance in generating release notes based on the following
        diff output between two branches (Left branch: {left_branch}, Right
        branch: {right_branch}) from our Git repository.

        1. A summary of the changes, including new features, enhancements, and bug fixes.
        2. Detailed descriptions of major changes, emphasizing their impact and advantages.
        3. Any pertinent technical details or code snippets that are relevant.
        4. After the release notes, provide statistical data about contributors,
        such as commits per contributor, lines added or removed, and other
        relevant metrics.
        \n
        {context}
        \n
        Please format the release notes and contributor statistics clearly for
        distribution to our team and stakeholders.
    """)

    llm_instance = create_llm(llm, llm_model)
    chain = create_stuff_documents_chain(llm_instance, prompt)

    release_notes = chain.invoke({
        "left_branch": left_branch,
        "right_branch": right_branch,
        "context": docs
    })

    return release_notes


@click.group()
def cli():
    pass


@cli.command('release', help='Generate release notes')
@click.argument('left_branch')
@click.argument('right_branch')
@click.argument('path', nargs=1, type=click.Path(exists=True), default='.')
@click.option(
    '--llm',
    type=click.Choice(['ollama', 'openai']),
    default='ollama',
    help='LLM to use (e.g., ollama, openai)',
)
@click.option('--llm-model', default='llama2', help='Model to use for ollama (e.g., llama2, mistral)')
def release(llm, llm_model, left_branch, right_branch, path):
    try:
        result = generate_release_notes(path, left_branch, right_branch, llm, llm_model)

        print(f'{result}')
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command('commit', help='Generate commit description')
@click.argument('path', nargs=1, type=click.Path(exists=True), default='.')
@click.option(
    '--llm',
    type=click.Choice(['ollama', 'openai']),
    default='ollama',
    help='LLM to use (e.g., ollama, openai)',
)
@click.option('--llm-model', default='llama2', help='Model to use for ollama (e.g., llama2, mistral)')
def commit(llm, llm_model, path):
    try:
        result = generate_commit_description(path, llm, llm_model)

        print(f'{result}')
    except Exception as e:
        raise click.ClickException(str(e))


if __name__ == '__main__':
    cli()
