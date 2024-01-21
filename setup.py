from setuptools import setup, find_packages

setup(
    name="GPT-CLI",  # Replace with your application's name
    version="0.1",  # Your app's version
    packages=find_packages(),
    install_requires=[
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "gptcli=cli-stream:main",  # "yourapp" is the command you'll use to run your script, 
                                          # "yourapp.main" is the python package.module where your script's main function is located
                                          # "main" is the main function within that module
        ],
    },
    python_requires=">=3.6",  # Minimum version requirement of Python
    description="VIOLETNET",  # Optional
)
