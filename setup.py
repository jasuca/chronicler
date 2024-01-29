from setuptools import setup, find_packages
import pathlib

# read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8') if (here / 'README.md').exists() else ''

setup(
    name='chronicler',
    version='0.1.0',
    description='Chronicler is a Python tool that automates documentation in development projects. Utilizing Git and language processing technologies, it offers an intuitive interface for tracking changes and generating detailed documentation, seamlessly integrating with version control workflows. It\'s perfect for developers and teams aiming to boost productivity and maintain clear, current project documentation, thereby simplifying project management.',
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
