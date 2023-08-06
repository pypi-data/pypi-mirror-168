import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="get_rankings",
    version="0.4",
    author="Georges Da Costa",
    author_email="georges.da-costa@irit.fr",
    description="DBLP ranking using CORE Rank and SJR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.irit.fr/sepia-pub/dacosta/get-rankings",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'BeautifulSoup4', 'datetime', 'parsedate', 'pandas', 'nunmpy', 'json', 'argparse'],
    entry_points={
        'console_scripts': [
            'get_rankings = get_rankings.get_rankings:main',
        ]
    }
)
