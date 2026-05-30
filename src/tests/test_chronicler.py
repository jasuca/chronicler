from unittest.mock import patch

import pytest
from click.testing import CliRunner

from chronicler import cli, create_llm, generate_commit_description, generate_release_notes


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key')


@pytest.fixture
def mock_chain():
    with patch('chronicler.create_stuff_documents_chain') as mock_chain:
        mock_chain.return_value.invoke.return_value = 'llm result'
        yield mock_chain


def test_create_llm_openai_without_env():
    with patch('chronicler.click.prompt') as mock_prompt, patch('chronicler.OpenAI') as mock_openai:
        mock_prompt.return_value = 'test_key'
        create_llm('openai', 'test_model')
        mock_prompt.assert_called_once_with('Please enter your OpenAI API key', hide_input=True)
        mock_openai.assert_called_once_with(openai_api_key='test_key', model_name='test_model')


def test_create_llm_openai_with_env(mock_env: None):
    with patch('chronicler.click.prompt') as mock_prompt, patch('chronicler.OpenAI') as mock_openai:
        create_llm('openai', 'test_model')
        mock_prompt.assert_not_called()
        mock_openai.assert_called_once_with(openai_api_key='test_key', model_name='test_model')


def test_create_llm_ollama():
    with patch('chronicler.OllamaLLM') as mock_ollama:
        create_llm('ollama', 'llama2')
        mock_ollama.assert_called_once()


def test_create_llm_invalid():
    with pytest.raises(ValueError):
        create_llm('invalid_llm', 'test_model')


@patch('chronicler.Repo')
def test_generate_release_notes(mock_repo, mock_chain):
    mock_repo.return_value.git.log.return_value = 'commit_log'
    result = generate_release_notes('path', 'branch1', 'branch2', 'ollama', 'llama2')
    assert result == 'llm result'


@patch('chronicler.Repo')
def test_generate_commit_description(mock_repo, mock_chain):
    mock_repo.return_value.git.status.return_value = 'status'
    result = generate_commit_description('path', 'ollama', 'llama2')
    assert result == 'llm result'


def test_release_cli_exits_nonzero_on_error():
    runner = CliRunner()
    with patch('chronicler.generate_release_notes', side_effect=RuntimeError('boom')):
        result = runner.invoke(cli, ['release', 'main', 'develop', '.'])

    assert result.exit_code != 0
    assert 'boom' in result.output


def test_commit_cli_exits_nonzero_on_error():
    runner = CliRunner()
    with patch('chronicler.generate_commit_description', side_effect=RuntimeError('boom')):
        result = runner.invoke(cli, ['commit', '.'])

    assert result.exit_code != 0
    assert 'boom' in result.output
