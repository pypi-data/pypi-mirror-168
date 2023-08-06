Rastless-CLI
=================

##### A cli for managing data and user access for the cloud application rastless

## Table of Content

- [Installation](#installation)
- [Running the CLI](#running-the-cli)
- [Commands Overview](#commands-overview)
- [Accomplishing a running system](#accomplishing-a-running-system)

## Installation

Requires: Python >=3.8, <4.0

```bash
$ pip install rastless-cli
```

RastLess has to be configured before you can check if everything works. Make sure that your aws account is configured
and has access to DynamoDb and S3.

You can check if everything works correctly by running:

```bash
$ rastless check-aws-connection
```

If it is not working, make sure to configure the aws connection by configuring the aws cli. You need an Access ID and a
Secret ID from aws to configure. Please check
the [official instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for further
help.

##### Developer Installation
```bash
$ pip install poetry
$ git clone https://github.com/EomapCompany/rastless-cli
$ cd rastless-cli
$ poetry install
```

Run tests
```bash
cd tests
poetry run pytest
```

## Running the CLI

After installation you can run the ClI by using:
```bash
$ rastless --help
```

You can decide if you want to upload data to the production or development environment.
By using the "dev" flag you upload it to development, without to production

```bash
# Example development
$ rastless --dev list-layers

# Example production
$ rastless list-layers
```

## Commands Overview

| Commands             |                                                     |
|----------------------|-----------------------------------------------------|
| add-colormap         | Add a SLD file                                      |
| add-permission       | Add a role to one or multiple layers                |
| check-aws-connection | Check if cli can connect to aws                     |
| create-layer         | Create layer                                        |
| create-timestep      | Create timestep entry and upload layer to S3 bucket |
| delete-colormap      | Remove a SLD file                                   |
| delete-layer         | Delete a layer with all timestep entries            |
| delete-permission    | Delete one or multiple permissions                  |
| list-layers          | List all layers                                     |

## Accomplishing a running system

#### 1. Check if you have access to the system
```bash
$ rastless check-aws-connection
```

#### 2. Create a new layer
- All inputs are strings. You have to take care, that the element exists in the database e.g. the colormap name.
- Multiple permissions can be set by using multiple -pe flags
```bash
$ rastless create-layer -cl hypos -pr tur -t Turbidity -cm log75_C2S8_32bit -u FTU -b <rgb uuid> -d "Some description" -r 1 -pe user#marcel -pe role#hypos:full-access
```
It will return a new uuid which you need to store, in order to upload timesteps to the particular layer

#### 3. Upload Timesteps for layer
```bash
$ rastless create-timestep -d 2020-01-01T15:00:00 -s SENT2 -l <layer uuid> -t daily -p deflate
```