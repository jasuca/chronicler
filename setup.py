from setuptools import setup, find_packages
import pathlib

# read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8') if (here / 'README.md').exists() else ''

setup(
    name='chronicler',
    version='0.1.0',
    description='Chronicler is an innovative Python tool designed to streamline and automate the documentation process for development projects. Leveraging the power of Git and various language processing technologies, it provides an intuitive interface for tracking changes, generating comprehensive documentation, and ensuring seamless integration with existing version control workflows. Ideal for developers and teams looking to enhance their productivity and maintain clear, up-to-date documentation, Chronicler simplifies the complexities of project management and documentation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jasuca/chronicler',
    author='Jacob Sunol',
    author_email='contact@jasuca.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='development, automation',
    package_dir={'': 'src'}, 
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=(here / 'requirements.txt').read_text().splitlines(),
    entry_points={ 
        'console_scripts': [
            'chronicler = chronicler:cli',
        ],
    },
)
