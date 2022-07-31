from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def read_requirements(filename: str):
    with open(filename,'r') as requirements_file:
        import re

        def fix_url_dependencies(req: str) -> str:
            """Pip and setuptools disagree about how URL dependencies should be handled."""
            m = re.match(
                r"^(git\+)?(https|ssh)://(git@)?github\.com/([\w-]+)/(?P<name>[\w-]+)\.git", req
            )
            if m is None:
                return req
            else:
                return f"{m.group('name')} @ {req}"

        requirements = []
        for line in requirements_file:
            line = line.strip()
            if line.startswith("#") or len(line) <= 0:
                continue
            requirements.append(fix_url_dependencies(line))
    print(requirements)
    return requirements
    
setup(
    name='drug_journal',
    version='0.1.0',
    description='data pipeline for drug journal data',
    long_description=long_description,
    author='cyril jacob',
    author_email='xxxx@gmail.com',
    url='https://github.com/cyriljacob/drug_journal',
    packages=find_packages(exclude=('test_de','tests', 'docs')),
    install_requires=read_requirements("requirements.txt"),
    setup_requires=["wheel"],
    python_requires=">=3.9",
)