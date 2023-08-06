# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.daily_production import DailyProduction
from openapi_client.model.daily_production_input import DailyProductionInput
from openapi_client.model.well_header import WellHeader
from openapi_client.model.well_header_input import WellHeaderInput
