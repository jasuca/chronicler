
# ![Chronicler Logo](http://graphene-python.org/favicon.png) Chronicler ![PyPI - Version](https://img.shields.io/pypi/v/py-chronicler)


## Introduction
Chronicler is an innovative Python tool designed to streamline and automate the documentation process for development projects. By leveraging Git and various language processing technologies, it provides an intuitive interface for tracking changes, generating comprehensive documentation, and ensuring seamless integration with version control workflows.

## Inspiration Behind the Name
The name 'Chronicler' is inspired by the Resident Evil: The Umbrella Chronicles movie. Much like the movie chronicles key events in a thrilling narrative, our tool chronicles the development journey of your projects, ensuring every change and update is meticulously documented and easy to follow.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/jasuca/chronicler.git
cd chronicler
```

Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
```

Install the package in editable mode:

```bash
pip install --editable .
```

This command will install the package and its dependencies, allowing you to make changes to the code and see them reflected immediately.

### Usage

To use Chronicler, run the following command:

```bash
chronicler release [OPTIONS] LEFT_BRANCH RIGHT_BRANCH [PATH]
chronicler commit [OPTIONS] [PATH]
```

#### Options
* commit   Generate commit description
* release  Generate release notes
* --llm [ollama|openai]: Select the Language Learning Model to use (e.g., ollama, openai).
* --llm-model TEXT: Specify the model for ollama (e.g., llama2, mistral).
* --help: Display the help message.

#### Examples
Comparing two branches: `chronicler release main develop /path/to/repo`

Generate current repo commit: `chronicler commit`

## Contributing

We welcome contributions to the Chronicler project! If you have suggestions for improvements or want to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
