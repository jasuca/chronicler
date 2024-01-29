import unittest
from unittest.mock import patch, MagicMock
from chronicler import create_llm, generate_release_notes

class TestChronicler(unittest.TestCase):

    @patch('chronicler.click.prompt')
    def test_create_llm_openai_without_env(self, mock_prompt):
        mock_prompt.return_value = 'test_key'
        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}, clear=True):
            llm_instance = create_llm('openai', 'test_model')
            mock_prompt.assert_called_once_with('Please enter your OpenAI API key', hide_input=True)
            # Add more assertions here as needed

    @patch('chronicler.click.prompt')
    def test_create_llm_openai_with_env(self, mock_prompt):
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            llm_instance = create_llm('openai', 'test_model')
            mock_prompt.assert_not_called()
            # Add more assertions here as needed

    def test_create_llm_ollama(self):
        with patch('chronicler.Ollama') as mock_ollama:
            create_llm('ollama', 'llama2')
            mock_ollama.assert_called_once()

    def test_create_llm_invalid(self):
        with self.assertRaises(ValueError):
            create_llm('invalid_llm', 'test_model')

    @patch('chronicler.Repo')
    @patch('chronicler.create_stuff_documents_chain')
    def test_generate_release_notes(self, mock_chain, mock_repo):
        mock_repo.return_value.git.log.return_value = 'commit_log'
        mock_chain.return_value.invoke.return_value = 'release_notes'

        result = generate_release_notes('path', 'branch1', 'branch2', 'ollama', 'llama2')
        self.assertEqual(result, 'release_notes')

if __name__ == '__main__':
    unittest.main()
