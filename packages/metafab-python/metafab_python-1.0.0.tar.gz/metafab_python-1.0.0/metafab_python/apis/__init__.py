
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from metafab_python.api.contracts_api import ContractsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from metafab_python.api.contracts_api import ContractsApi
from metafab_python.api.currencies_api import CurrenciesApi
from metafab_python.api.games_api import GamesApi
from metafab_python.api.players_api import PlayersApi
from metafab_python.api.transactions_api import TransactionsApi
from metafab_python.api.wallets_api import WalletsApi
