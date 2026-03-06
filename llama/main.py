from llama_cpp import Llama
from fastapi import FastAPI, Request, Body
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
import asyncio


# lifespan 시작과 종료시 실행
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 실행 전
    app.state.llm = Llama(
        model_path="../models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,  # 컨텍스트 사이즈
        n_threads=2,  # CPU 스레드
        verbose=False,  # 로그 출력을 간단하게
        chat_format="llama-3",  # 응답 생성 포켓
    )
    yield
    # 서버 종료 후


app = FastAPI(lifespan=lifespan)


# LLM
# 입력: 프롬프트 -> LLM -> 출력: 문장

# role
# system: 모델의 규칙, 행동방식, 성격
# user: 사용자들이 질문, 요청
# assistant: 이전에 모델이 생성한 답변

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


@app.post("/chats")
def genrate_chat_handler(request: Request, user_input: str = Body(..., embed=True)):
    # embeb=False => "이건 뭐야?"
    # embeb=True => {"user_input":"이건 뭐야"}

    async def event_generator():
        llm = request.app.state.llm
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True,
        )
        print(response)
        for chunk in response:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token
                await asyncio.sleep(0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
