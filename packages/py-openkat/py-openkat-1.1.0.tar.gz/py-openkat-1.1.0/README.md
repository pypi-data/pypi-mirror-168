# Openkat

An experimental sandbox environment to easily experiment with (some) functionality of [openkat](https://openkat.nl/).
This version of openkat runs all services in a single process and replaces services such as
[Bytes](https://github.com/minvws/nl-kat-bytes), Rabbitmq and Celery with an in-memory implementation.
As a consequence, the current version does not guarantee persistence beyond the lifetime of the process.
It speaks for itself that this library **should not be used in a production environment**.
To properly deploy an openkat instance,
please refer to the [official documentation](https://github.com/minvws/nl-kat-coordination) on Github.


## Features

These features of openkat are currently present in this package:
- The Rocky interface: UI around reporting on Findings
- The Octopoes models: for modelling the Objects Of Interest (OOIs)
- The Boefjes/Normalizers: the python scripts that find OOIs (excluding the containerized versions)
- The Scheduler: dispatching Boefjes and Normalizers automatically

The benefits and extra features of this package are:
- Lightweight: a single process for the app, reducing overhead of the official services and installation times
- A default superuser and development organization
- OTP disabled to optimize for restarting the service even after an update
- Docker not a dependency
- Adding plugins by creating plugins in a custom `plugins` folder

However, some features are excluded from this version:
- Bytes: the raw data store, which has been replaced by an in-memory variant
- Bits
- Dockerized boefjes
- Deletion Propagation: you have to manually delete every single OOI
- ScanProfile inheritance: you have to manually add scan profiles to observed OOIs
- Valid times: you cannot browse the OOI history through time
- Multiple organizations
- Some miscellaneous functionality, such as filtering in the UI


## Installation

```shell
$ pip install openkat
```

### Running the server

To start the instance, run

```shell
$ python -m openkat
```

and navigate to http://localhost:8000.



## Contributing

Dependencies:
- `poetry`
- `yarn`


To setup a development environment, run
```shell
$ make init
```

To build, run
```shell
$ make build
```
