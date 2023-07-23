from .api import routes
from .database import services

app = routes.app
services.add_tables()
