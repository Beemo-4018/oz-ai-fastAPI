from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# 1. 비동기용 URL (aiomysql 설치 필요: pip install aiomysql)
ASYNC_DATABASE_URL = "mysql+aiomysql://root:1234@db:3306/oz"

# 2. 비동기 엔진 생성
async_engine = create_async_engine(ASYNC_DATABASE_URL)

# 3. 세션 팩토리 연결
AsyncSessionFactory = sessionmaker(
    bind=async_engine,  # 비동기 엔진 연결
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        # 세션을 종료하면서 네트워크를 사용하기 때문에 await
        await session.close()
