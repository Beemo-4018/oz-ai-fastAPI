import os
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.responses import StreamingResponse
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openapi_client = AsyncOpenAI(api_key=settings.open_api_key)
    yield
    await app.state.openapi_client.close()


app = FastAPI(lifespan=lifespan)


class ResultSchema(BaseModel):
    result: str = Field(..., description="질문에 대한 답변")
    confidence: float = Field(..., description="답변에 대한 신뢰도")


@app.post("/gpt")
async def call_gpt_handler(
    request: Request, user_input: str = Body(..., embed=True)  # 요청에 대한 메타 정보
):
    client = request.app.state.openapi_client

    # responses = await client.responses.parse(
    #     model="gpt-4.1-mini",
    #     input=user_input,
    #     text_format=ResultSchema
    # )
    async def event_generator():
        # 1) OpenAI 서버로 스트리밍 요청을 보낸다.
        async with client.responses.stream(
            model="gpt-4.1-mini", input=user_input, text_format=ResultSchema
        ) as stream:
            # 2) 스트리밍 데이터를 하나씩 event 라는 형태로 응답 받는다.
            async for event in stream:
                # 3-1) event 값이 delta 면, 그 안의 값(token)을 꺼낸다
                if event.type == "response.output_text.delta":
                    yield event.delta
                # 3-2) event가 completed 면, 스트리밍을 종료한다.
                elif event.type == "response.completed":
                    break

    return StreamingResponse(
        # generator
        event_generator(),
        media_type="text/event-stream",
    )
