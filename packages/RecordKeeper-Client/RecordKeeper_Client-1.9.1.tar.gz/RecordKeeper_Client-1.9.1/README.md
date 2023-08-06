
# Context

RecordKeeper (abbreviated to RK) is aimed at two broad goals:

1. Explaining why something happened in your platform.
   Common example that we want to support is: why event X happened at time T?
   What Models were used? Who trained them, using training data ingested from which
   datasources? It achieves it by creating graph of events.

2. Recreating platform state at that time.

# Basics

RKClient library is used to create events (PEMS) and inform RK about them.

You will need a running RecordKeeper Event Receiver to be able to work with it.

Recommended usage:

```
emitter_id = uuid.UUID('..some static uuid..')
rk_host = os.environ.get('RK_HOST')

rk_client = RKClientFactory.get(rk_host, emitter_id)
```

By using factory, automatically when `RK_MOCK=true` env variable will be defined, 
the returned client will fake the connections and return only success codes. 

# Details

The Receiver will be configured with max PEM payload size. If your PEM exceeds 
this limit, it will be rejected (with explanation).

You can query for the PEM limit size in `get_info()`, in `pem_size_limit` field.

# API

RKClient:
- prepare_pem
- prepare_artifact
- send_pem
- ping
- get_info
- get_tag
- set_tag

RKAdmin:
- get_pems
- get_pems_count
- get_artifact
- get_artifacts
- get_artifacts_count
- get_taxonomy_file
- get_tags
- get_tags_count
- query_graph
- clean_dbs


# Authenticating

If you want to do anything more than sending a PEM, you will need to pass a
RK authentication credential when creating RKClient or RKAdmin.

There are two types:
1. User auth
2. PUC auth

First is available in RecordKeeper Dashboard, in your user profile. It's intended 
to be used in tests.

Machine code on production should rather use PUC-auth, since it's user agnostic. 
However, you will need to ask RK admin to create the PUC and send you its auth code.

## RKClient from Python console

```
cd rkclient/
python3
>>> from rkclient import RKAdmin
>>> rk = RKAdmin('http://127.0.0.1:8082')
>>> pems, msg, ok = rk.get_pems()
>>> assert ok, msg
>>> for pem in pems:
>>>   print(pem)
```

## Changelog

### [1.9.1] - 20.9.2022
Version updated to match other components

### [1.9.0] - 13.9.2022
Added async test.

### [1.8.0] - 23.2.2022
Support for PUC auth type. New function get_tags_count.

### [1.7.0] - 23.2.2022
RKClient catches timeout exception. Artifact instances in python can be compared using equal operator.

### [1.6.1] - 26.01.2022
PEM deduplicates uses artifacts. Fix for function behaviour in mocked RKClient.

### [1.6.0] - 17.01.2022
Removed PEM User field, bumped PEM version to 1.0.1

### [1.5.0] - 21.12.2021
Version updated to match other components

### [1.4.0] - 16.11.2021
Version updated to match other components

### [1.3.0] - 6.9.2021
Remove the requests dependency

### [1.2.3] - 26.8.2021
Bump the requests version to 2.26.*

### [1.2.2] - 17.6.2021
Option to disable SSL cert verification

### [1.2.1] - 8.6.2021
Official release on Pypi, added license


---
RKClient is part of ERST Recordkeeper repository.

RKClient is licensed with GNU General Public License version 3 or later,
see LICENSE file for details.

Recordkeeper is ERST's implementation of the Context Cartographer specification.

