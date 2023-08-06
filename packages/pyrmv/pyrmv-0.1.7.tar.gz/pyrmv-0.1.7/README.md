# PythonRMV

Small module that makes your journey with RMV REST API somehow easier. Based fully on official RMV API reference and HAFAS documentation.

# Requirements

* RMV API key (Get it [here](https://opendata.rmv.de/site/start.html))
* Python3 (Tested versions are 3.7.9 and 3.9.13)
* git (Only for installation from source)

# Installation

If you have everything listed in [requirements](#requirements), then let's begin.

### Variant 1:
1. `python -m pip install pyrmv`

### Variant 2:
1. `git clone https://git.end-play.xyz/profitroll/PythonRMV.git`
2. `cd PythonRMV`
3. `python setup.py install`

# Frequently Asked Questions

- [Why are there raw versions and formatted ones?](#why-are-there-raw-versions-and-formatted-ones)
- [Some methods work slightly different](#some-methods-work-slightly-different)
- [Documentation is not perfectly clear](#documentation-is-not-perfectly-clear)

## Why are there raw versions and formatted ones?

For the purposes of my projects I don't really need all the stuff RMV gives (even though it's not much).
I only need some specific things. However I do understand that in some cases other users may find
those methods quite useful so I implemented them as well.


## Some methods work slightly different

Can be. Not all function arguments written may work perfectly because I simply did not test each and
every request. Some of arguments may be irrelevant in my use-case and the others are used quite rare at all.
Just [make an issue](https://git.end-play.xyz/profitroll/PythonRMV/issues/new) and I'll implement it correct when I'll have some free time.

## Documentation is not perfectly clear

Of course docs cannot be perfect as a python docstring, especially if sometimes I don't
know how things should correctly work. That's why you get HAFAS API docs in addition to your
RMV API key. Just use my functions together with those docs, if you want to build something
really sophisticated. However I'm not sure whether RMV supports that many HAFAS features publicly.

# To-Do
- [ ] arrivalBoard (boardArrival)  
- [ ] departureBoard (boardArrival)  
- [x] himsearch (himSearch)  
- [ ] journeyDetail  
- [x] location.nearbystops (stopByCoords)  
- [x] location.name (stopByName)  
- [ ] recon  
- [x] trip (findRoute)  