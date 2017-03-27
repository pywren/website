Title: PyWren 0.2
Date: 2017-03-27
Tags: releases
Category: releases
Slug: release-0.2
Author: Eric Jonas
Summary: Annoucing PyWren 0.2, bugfix release and interactive setup script. 

Today we're excited to release PyWren version 0.2. This release contains
a number of important bug fixes, as well as a new getting started script. 

### Getting Started

We'd like for PyWren to be as easy to use as possible, so we have put together a 
new getting started script for new users. Simply run

```
pywren-setup
```
and follow the prompts! 

See more in [our getting started section]({filename}/pages/gettingstarted.md)

### Notable bug fixes and improvements behind the scenes

* We reorganized the PyWren code internally to make it easier to 
understand and extend. 
* We fixed a number of serialization bugs so that it's easier to use
PyWren from [IPython](https://ipython.org/) and
with [Numba](http://numba.pydata.org/)


### List of issues fixed
* [[98](https://github.com/pywren/pywren/issues/98)] When creating the lambda we indiscriminately upload too much
* [[86](https://github.com/pywren/pywren/issues/86)] Standardize configuration for executors
* [[83](https://github.com/pywren/pywren/issues/83)] pywren not working for numba functions in 0.1 due to module serialization weirdness <span class="label label-default">serialization</span>
* [[82](https://github.com/pywren/pywren/issues/82)] pywren not respecting non UTF-8 encoding (if coding is provided at top of file) <span class="label label-default">serialization</span>
* [[79](https://github.com/pywren/pywren/issues/79)] Only *.py in modules are uploaded <span class="label label-default">serialization</span>
* [[78](https://github.com/pywren/pywren/issues/78)] Handle exception pickling <span class="label label-default">serialization</span>
* [[77](https://github.com/pywren/pywren/issues/77)] Capture exception traceback from remote
* [[75](https://github.com/pywren/pywren/issues/75)] Turn on runtime sharding by default
* [[60](https://github.com/pywren/pywren/issues/60)] Why do we use multiprocess instead of multiprocessing
* [[59](https://github.com/pywren/pywren/issues/59)] Generic refactor / split wren.py / run pyflakes
* [[55](https://github.com/pywren/pywren/issues/55)] Testing for pywrencli.py
* [[44](https://github.com/pywren/pywren/issues/44)] Better synchronization of runtime information with local client <span class="label label-default">serialization</span>
* [[35](https://github.com/pywren/pywren/issues/35)] Create S3 bucket if it doesn't exist
* [[27](https://github.com/pywren/pywren/issues/27)] Add documentation on permissions
* [[18](https://github.com/pywren/pywren/issues/18)] Fix directories so that the conda command-line utils have right path
* [[16](https://github.com/pywren/pywren/issues/16)] Create interactive getting started script
