from . import base
from db import engine
from .books import *
from .users import *


base.Base.metadata.create_all(bind=engine)
