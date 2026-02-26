# SQLAlchemy 사용에 팔요한 기본 설정
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DB 접속 정보(DB 종류, 주소, 포트번호, 사용자, 비밀번호)

# sqlite:// sqlite를 사용하겠다.
# /./test.db -> 현재 프로젝트 경로에 test.db라는 이름의 파일을 만들어라
DATABASE_URL = "sqlite:///./test.db"  # SQLite 데이터베이스 URL

# Engine : 데이터베이스와의 연결을 관리하는 객체
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session : DB 작업단위
# SessionFactory : 세션을 생성하는 클래스
SessionFactory = sessionmaker(
    bind=engine,  # 엔진을 연결
    # 기본 옵션
    autoflush=False,  # 자동으로 flush()
    autocommit=False,  # 자동으로 commit()
    expire_on_commit=False,  # commit() 후에 자동으로 데이터 만료
)

# return => 호출부로 값 반환 및 실행 함수 종료
# yield => 호출부로 값 반환 및 실행 함수 일시 정지


def getSession():
    with SessionFactory() as session:
        yield session
