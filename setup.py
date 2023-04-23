from setuptools import setup

setup(
    name = 'montecarlo',
    version = '0.1.0',
    author = 'zeitgeistf',
    author_email = 'shawnsfeng@gmail.com',
    url = 'https://github.com/zeitgeistf/montecarlo',
    packages = ['montecarlo'],
    description = 'A package creates and analyzes games with configurable dice',
    install_requires = [
        "pandas"
    ],
    python_requires='>3.10'
)
