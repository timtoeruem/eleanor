from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ellie",  # You can change this to your desired package name
    version="0.1.0",  # Update version as needed
    packages=find_packages(where="ellie"),  # Find packages inside 'ellie' folder
    package_dir={"": "ellie"},
    install_requires=requirements,  # Install dependencies from requirements.txt
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    entry_points={
        "console_scripts": [
            # Example: "ellie-cli=ellie.cli:main"  # Modify as needed
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Adjust based on your compatibility
)