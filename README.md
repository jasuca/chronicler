
# Chronicler ![PyPI - Version](https://img.shields.io/pypi/v/py-chronicler)


## Introduction
Chronicler is an innovative Python tool designed to streamline and automate the documentation process for development projects. By leveraging Git and various language processing technologies, it provides an intuitive interface for tracking changes, generating comprehensive documentation, and ensuring seamless integration with version control workflows.

Chronicler can draft commit descriptions from the current repository status and release notes from the difference between two Git branches. It supports local Ollama models by default and OpenAI models when `OPENAI_API_KEY` is configured.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- uv

### Installation

Install from PyPI:

```bash
uv tool install py-chronicler
```

Clone the repository:

```bash
git clone https://github.com/jasuca/chronicler.git
cd chronicler
```

Install the project and development tools with uv:

```bash
uv sync --group dev
```

Run the CLI from the project checkout:

```bash
uv run chronicler --help
```

`requirements.txt` is retained as a compatibility entry point for tools that still call `pip install -r requirements.txt`; project dependencies and release metadata live in `pyproject.toml`.

### Usage

To use Chronicler, run the following command:

```bash
chronicler release [OPTIONS] LEFT_BRANCH RIGHT_BRANCH [PATH]
chronicler commit [OPTIONS] [PATH]
```

#### Options
* commit   Generate commit description
* release  Generate release notes
* --llm [ollama|openai]: Select the language model provider.
* --llm-model TEXT: Specify the provider model. The default is `llama2`.
* --help: Display the help message.

#### Examples
Comparing two branches: `chronicler release main develop /path/to/repo`

Generate current repo commit: `chronicler commit`

Generate current repo commit using Ollama(mistral): `chronicler commit --llm=ollama --llm-model=mistral  .`

Generate release notes with OpenAI:

```bash
OPENAI_API_KEY=... chronicler release v0.1.1 main . --llm=openai --llm-model=gpt-3.5-turbo-instruct
```

### Development

Run tests:

```bash
uv run pytest
```

Run the CI lint checks locally:

```bash
uv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
uv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

Build release artifacts:

```bash
uv run python -m build
```

If you already synced the dev environment and want to avoid creating an isolated build environment, use:

```bash
uv build --no-build-isolation
```

The package is published to PyPI as `py-chronicler`. The console command installed by the package is `chronicler`.

## Contributing

We welcome contributions to the Chronicler project! If you have suggestions for improvements or want to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
