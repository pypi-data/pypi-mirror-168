from setuptools import setup

setup(
    name="pyrmv",
    version="0.2.0",
    author="Profitroll",
    description="Small module that makes your journey with RMV REST API somehow easier.",
    long_description="## PythonRMV\n\nSmall module that makes your journey with RMV REST API somehow easier. Based fully on official RMV API reference and HAFAS documentation.\n\n## Usage\n\n```py\nimport pyrmv\n\n# Set API key\naccessId = \"Something\"\n\n# Get origin's and destination's location\norigin = pyrmv.raw.stop_by_name(accessid, \"Frankfurt Hauptbahnhof\", maxNo=3)[0][\"StopLocation\"]\ndestination = pyrmv.raw.stop_by_coords(accessid, 50.099613, 8.685449, maxNo=3)[0][\"StopLocation\"]\n\n## Find a trip by locations got\ntrip = pyrmv.raw.trip_find(accessId, originId=origin[\"id\"], destExtId=destination[\"id\"])\n```\n\n## Frequently Asked Questions\n\n- Why are there raw versions and formatted ones?\n- Some methods work slightly different\n- Documentation is not perfectly clear\n\n### Why are there raw versions and formatted ones?\n\nFor the purposes of my projects I don't really need all the stuff RMV gives (even though it's not much).\nI only need some specific things. However I do understand that in some cases other users may find\nthose methods quite useful so I implemented them as well.\n\n\n### Some methods work slightly different\n\nCan be. Not all function arguments written may work perfectly because I simply did not test each and\nevery request. Some of arguments may be irrelevant in my use-case and the others are used quite rare at all.\nJust [make an issue](https://git.end-play.xyz/profitroll/PythonRMV/issues/new) and I'll implement it correct when I'll have some free time.\n\n### Documentation is not perfectly clear\n\nOf course docs cannot be perfect as a python docstring, especially if sometimes I don't\nknow how things should correctly work. That's why you get HAFAS API docs in addition to your\nRMV API key. Just use my functions together with those docs, if you want to build something\nreally sophisticated. However I'm not sure whether RMV supports that many HAFAS features publicly.\n\n## To-Do\n- [ ] arrivalBoard (board_arrival)  \n- [ ] departureBoard (board_departure)  \n- [x] himsearch (him_search)  \n- [ ] journeyDetail (journey_detail)\n- [x] location.nearbystops (stop_by_coords)  \n- [x] location.name (stop_by_name)  \n- [x] trip (trip_find)  \n- [ ] recon (trip_recon)",
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
        "pyrmv.raw",
        "pyrmv.errors",
        "pyrmv.methods",
        "pyrmv.utility",
        "pyrmv.classes"
    ],
    install_requires=[
        "requests",
        "xmltodict",
        "isodate"
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