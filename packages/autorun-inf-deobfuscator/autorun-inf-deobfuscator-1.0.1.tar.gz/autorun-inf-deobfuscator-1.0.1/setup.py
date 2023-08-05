import setuptools

with open('README.md', mode='r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="autorun-inf-deobfuscator",
    version="1.0.1",
    author="Florian Wahl",
    author_email="florian.wahl.developer@gmail.com",
    description="A cli script to deobfuscate obfuscated autorun.inf files as used by the Conficker / Downadup malware for example.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahlflo/AurorunInfDeobfuscator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'cli-formatter>=1.2.0'
    ],
    entry_points={
        "console_scripts": [
            "deobfuscate-autorun-inf=autorun_inf_deobfuscator.cli_script:main"
        ],
    }
)