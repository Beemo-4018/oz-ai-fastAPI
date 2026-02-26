from db_models import User
from db_connection import SessionFactory
from sqlalchemy import select

session = SessionFactory()
stmt = select(User)

result = session.execute(stmt)
mappings = result.mappings().all()

print(mappings)


scalars = result.scalar()
