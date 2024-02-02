import pytest
from unittest.mock import patch
from chronicler import create_llm, generate_release_notes, generate_commit_description

# Using pytest's fixture for environment variables
@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key')

@pytest.fixture
def mock_chain():
    with patch('chronicler.create_stuff_documents_chain') as mock_chain:
        mock_chain.return_value.invoke.return_value = 'llm result'
        yield mock_chain

# Tests
def test_create_llm_openai_without_env():
    with patch('chronicler.click.prompt') as mock_prompt:
        mock_prompt.return_value = 'test_key'
        llm_instance = create_llm('openai', 'test_model')
        mock_prompt.assert_called_once_with('Please enter your OpenAI API key', hide_input=True)
        # Add more assertions here as needed

def test_create_llm_openai_with_env(mock_env: None):
    with patch('chronicler.click.prompt') as mock_prompt:
        llm_instance = create_llm('openai', 'test_model')
        mock_prompt.assert_not_called()
        # Add more assertions here as needed

def test_create_llm_ollama():
    with patch('chronicler.Ollama') as mock_ollama:
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
    mock_repo.return_value.git.return_value.status.return_value = 'status'
    result = generate_commit_description('path', 'ollama', 'llama2')
    assert result == 'llm result'
   