from db_models import Base
from db_connection import engine

Base.metadata.create_all(bind=engine)
