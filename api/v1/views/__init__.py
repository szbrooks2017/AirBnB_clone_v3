#!/usr/bin/python3
from flask import Blueprint

# need to finish blueprint template
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1') 

from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places_reviews import *
from api.v1.views.reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
