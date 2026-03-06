from pydantic import BaseModel


# 회원가입 요청 본문의 데이터 형태
class UserSignUpRequest(BaseModel):
    name: str  # 필수 필드
    age: int = 0  # 기본값 0
    # email: str | None = None  # 선택적 필드, None 허용
    # grade: str | None = None  # 선택적 필드, None 허용


# 회원가입 응답 본문의 데이터 형태
class UserResponse(BaseModel):
    id: int
    name: str
    age: int | None
    # email: str | None


# 사용자 정보 수정 요청 본문
class UserUpdateRequest(BaseModel):
    name: str | None = None
    age: int | None = None
