# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.casing import Casing
from openapi_client.model.casing_entity import CasingEntity
from openapi_client.model.casing_input import CasingInput
from openapi_client.model.daily_production import DailyProduction
from openapi_client.model.daily_production_input import DailyProductionInput
from openapi_client.model.deviation_survey import DeviationSurvey
from openapi_client.model.deviation_survey_entity import DeviationSurveyEntity
from openapi_client.model.deviation_survey_input import DeviationSurveyInput
from openapi_client.model.formation_property import FormationProperty
from openapi_client.model.formation_property_entity import FormationPropertyEntity
from openapi_client.model.formation_property_input import FormationPropertyInput
from openapi_client.model.tubing import Tubing
from openapi_client.model.tubing_entity import TubingEntity
from openapi_client.model.tubing_input import TubingInput
from openapi_client.model.well import Well
from openapi_client.model.well_input import WellInput
from openapi_client.model.wellbore import Wellbore
from openapi_client.model.wellbore_input import WellboreInput
