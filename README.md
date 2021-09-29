# Tailslide

Median and percentile for Django models

Supports:

- PostgreSQL
- SQLite
- MariaDB
- MySQL (with an extension)
- SQL Server

:fire: Uses native functions when possible for blazing performance

[![Build Status](https://github.com/ankane/tailslide/workflows/build/badge.svg?branch=master)](https://github.com/ankane/tailslide/actions)

## Installation

Run:

```sh
pip install tailslide
```

For MySQL, also follow [these instructions](#additional-instructions).

## Getting Started

Median

```python
from tailslide import Median

Item.objects.aggregate(Median('price'))
```

Percentile

```python
from tailslide import Percentile

Request.objects.aggregate(Percentile('response_time', .95))
```

Works with grouping, too, with PostgreSQL, MySQL, and SQLite

```python
Order.objects.values('store').annotate(total=Median('total')).order_by('store')
```

## Additional Instructions

### MySQL

MySQL requires the `PERCENTILE_CONT` function from [udf_infusion](https://github.com/infusion/udf_infusion). To install it, do:

```sh
git clone https://github.com/infusion/udf_infusion.git
cd udf_infusion
./configure --enable-functions="percentile_cont"
make
sudo make install
mysql <options> < load.sql
```

## Contributing

Everyone is encouraged to help improve this project. Here are a few ways you can help:

- [Report bugs](https://github.com/ankane/tailslide/issues)
- Fix bugs and [submit pull requests](https://github.com/ankane/tailslide/pulls)
- Write, clarify, or fix documentation
- Suggest or add new features

To get started with development:

```sh
git clone https://github.com/ankane/tailslide.git
cd tailslide
pip install -r requirements.txt

# Postgres
createdb tailslide_test
ADAPTER=postgresql pytest

# SQLite
ADAPTER=sqlite pytest

# MariaDB
mysqladmin create tailslide_test
ADAPTER=mariadb pytest

# MySQL (install the extension first)
mysqladmin create tailslide_test
ADAPTER=mysql pytest

# SQL Server
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourStrong!Passw0rd' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest
docker exec -it <container-id> /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YourStrong\!Passw0rd -Q "CREATE DATABASE tailslide_test"
ADAPTER=sqlserver pytest
```
