from setuptools import setup

setup(
    name="pyrmv",
    version="0.1.7",
    author="Profitroll",
    description="Small module that makes your journey with RMV REST API somehow easier.",
    long_description="Small module that makes your journey with RMV REST API somehow easier. Based fully on official RMV API reference and HAFAS documentation.\n\n# Frequently Asked Questions\n\n- [Why are there raw versions and formatted ones?](#why-are-there-raw-versions-and-formatted-ones)\n- [Some methods work slightly different](#some-methods-work-slightly-different)\n- [Documentation is not perfectly clear](#documentation-is-not-perfectly-clear)\n\n## Why are there raw versions and formatted ones?\n\nFor the purposes of my projects I don't really need all the stuff RMV gives (even though it's not much).\nI only need some specific things. However I do understand that in some cases other users may find\nthose methods quite useful so I implemented them as well.\n\n\n## Some methods work slightly different\n\nCan be. Not all function arguments written may work perfectly because I simply did not test each and\nevery request. Some of arguments may be irrelevant in my use-case and the others are used quite rare at all.\nJust [make an issue](https://git.end-play.xyz/profitroll/PythonRMV/issues/new) and I'll implement it correct when I'll have some free time.\n\n## Documentation is not perfectly clear\n\nOf course docs cannot be perfect as a python docstring, especially if sometimes I don't\nknow how things should correctly work. That's why you get HAFAS API docs in addition to your\nRMV API key. Just use my functions together with those docs, if you want to build something\nreally sophisticated. However I'm not sure whether RMV supports that many HAFAS features publicly.\n\n# To-Do\n- [ ] arrivalBoard (boardArrival)  \n- [ ] departureBoard (boardArrival)  \n- [x] himsearch (himSearch)  \n- [ ] journeyDetail  \n- [x] location.nearbystops (stopByCoords)  \n- [x] location.name (stopByName)  \n- [ ] recon  \n- [x] trip (findRoute)",
    long_description_content_type="text/markdown",
    author_email="profitroll@end-play.xyz",
    url="https://git.end-play.xyz/profitroll/PythonRMV",
    project_urls={
        "Bug Tracker": "https://git.end-play.xyz/profitroll/PythonRMV/issues",
        "Documentation": "https://git.end-play.xyz/profitroll/PythonRMV/wiki",
        "Source Code": "https://git.end-play.xyz/profitroll/PythonRMV.git",
    },
    packages=[
        "pyrmv",
        "pyrmv.raw"
    ],
    install_requires=[
        "requests",
        "xmltodict"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)