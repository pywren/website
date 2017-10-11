Title: PyWren 0.3
Date: 2017-10-11
Tags: releases
Category: releases
Slug: release-0.3
Author: Eric Jonas
Summary: Annoucing PyWren 0.3, with region-specific runtimes, better error handling, and a storage API

Today we're excited to release PyWren version 0.3. This release contains
a number of important bug fixes, as we move towards some exciting
new capabilities in 0.4. 

The latest version is installable via:
```
pip install --upgrade pywren
```

And remember to redeploy your pywren function to AWS with 
```
pywren deploy_lambda
```

## Major Changes
- switched to using region-specific runtimes with sharding
- refactored storage API for future support of other cloud providers
- support for python 3.4
- better error handling
- Developer stuff: APL2 license, using pylint on commit. 

**Closed issues:**

- Test Function doesn't parse command-line config [\#166](https://github.com/pywren/pywren/issues/166)
- Error with None result [\#183](https://github.com/pywren/pywren/issues/183)
- Create max list seatbelt [\#176](https://github.com/pywren/pywren/issues/176)
- Make ALL\_COMPLETED, ANY\_COMPLETED, and ALWAYS available without having to specifically import [\#174](https://github.com/pywren/pywren/issues/174)
- Generic Release clean-up [\#171](https://github.com/pywren/pywren/issues/171)
- Change default runtime URLS to be region-specific [\#164](https://github.com/pywren/pywren/issues/164)
- config files manually loaded must be patched with storage config [\#162](https://github.com/pywren/pywren/issues/162)
- Straggler due to list-after-write consistency [\#160](https://github.com/pywren/pywren/issues/160)
- Do not proceed with travis build if pylint fails. [\#157](https://github.com/pywren/pywren/issues/157)
- I can't run test function [\#156](https://github.com/pywren/pywren/issues/156)
- Describe .pywren\_config in "getting started" [\#134](https://github.com/pywren/pywren/issues/134)
- Mapping over an empty list should return an empty list [\#129](https://github.com/pywren/pywren/issues/129)
- Create License File [\#116](https://github.com/pywren/pywren/issues/116)
- Refactor storage APIs [\#108](https://github.com/pywren/pywren/issues/108)
- Too big of runtime [\#105](https://github.com/pywren/pywren/issues/105)
- Update `getting started` webpage on the interactive script [\#103](https://github.com/pywren/pywren/issues/103)
- Have setup.py check for supported python versions [\#101](https://github.com/pywren/pywren/issues/101)
- Support 3.4 runtime \(and others\) [\#95](https://github.com/pywren/pywren/issues/95)
- Migrate travis script to using sec-since-epoch as GUID [\#91](https://github.com/pywren/pywren/issues/91)
- Consider using boto3 s3 transfer interface [\#23](https://github.com/pywren/pywren/issues/23)
- ImportError: No module named 'wren' [\#19](https://github.com/pywren/pywren/issues/19)

**Merged pull requests:**

- \[Issue\#183\] removing none result check [\#184](https://github.com/pywren/pywren/pull/184) ([ooq](https://github.com/ooq))
- Fix issue 91 [\#182](https://github.com/pywren/pywren/pull/182) ([ericmjonas](https://github.com/ericmjonas))
- Release 0.3 [\#178](https://github.com/pywren/pywren/pull/178) ([ericmjonas](https://github.com/ericmjonas))
- New max-limit seatbelt [\#177](https://github.com/pywren/pywren/pull/177) ([ericmjonas](https://github.com/ericmjonas))
- Fix setup py version [\#173](https://github.com/pywren/pywren/pull/173) ([ericmjonas](https://github.com/ericmjonas))
- Lambda toobig seatbelts [\#172](https://github.com/pywren/pywren/pull/172) ([ericmjonas](https://github.com/ericmjonas))
- Issue\#160 Straggler due to list-after-write consistency [\#170](https://github.com/pywren/pywren/pull/170) ([ooq](https://github.com/ooq))
- Switch to region specific runtimes [\#169](https://github.com/pywren/pywren/pull/169) ([ericmjonas](https://github.com/ericmjonas))
- Fix patching of storage handler config, then fix commandline [\#167](https://github.com/pywren/pywren/pull/167) ([ericmjonas](https://github.com/ericmjonas))
- change docstring [\#147](https://github.com/pywren/pywren/pull/147) ([apengwin](https://github.com/apengwin))
- Enable Pylint checks for PyWren [\#144](https://github.com/pywren/pywren/pull/144) ([shivaram](https://github.com/shivaram))
- Pylint cleanup [\#143](https://github.com/pywren/pywren/pull/143) ([shivaram](https://github.com/shivaram))
- Remove cloudpickle dependency and use local cloudpickle. [\#142](https://github.com/pywren/pywren/pull/142) ([ooq](https://github.com/ooq))
- add exclude modules argument to map [\#140](https://github.com/pywren/pywren/pull/140) ([Vaishaal](https://github.com/Vaishaal))
- Handle empty input list in map [\#133](https://github.com/pywren/pywren/pull/133) ([shivaram](https://github.com/shivaram))
- Add Apache v2 License [\#132](https://github.com/pywren/pywren/pull/132) ([shivaram](https://github.com/shivaram))
- \[Issue\#108\] Refactor Storage API [\#119](https://github.com/pywren/pywren/pull/119) ([ooq](https://github.com/ooq))
- fixed minor spelling mistake [\#118](https://github.com/pywren/pywren/pull/118) ([sean-smith](https://github.com/sean-smith))
- Added validation for s3 bucket names and made username portion of def… [\#117](https://github.com/pywren/pywren/pull/117) ([sean-smith](https://github.com/sean-smith))
- Fix issue with bucket creation in us-east-1 [\#113](https://github.com/pywren/pywren/pull/113) ([Donohue](https://github.com/Donohue))


