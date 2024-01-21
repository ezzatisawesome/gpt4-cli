from setuptools import setup, find_packages

setup(
    name="GPT-CLI",  # Replace with your application's name
    version="0.1",  # Your app's version
    py_modules=['src.cli_stream'],  # Directly specify the module
    install_requires=[
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "gptcli=src.cli_stream:main"
        ],
    },
    python_requires=">=3.6",  # Minimum version requirement of Python
)
