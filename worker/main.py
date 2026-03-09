import redis
import json
from llama_cpp import Llama

#

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

llm = Llama(
    model_path="../models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,  # 컨텍스트 사이즈
    n_threads=2,  # CPU 스레드
    verbose=False,  # 로그 출력을 간단하게
    chat_format="llama-3",  # 응답 생성 포켓
)
SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


def create_response(question: str):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=256,
        temperature=0.7,
        stream=False,
    )
    return response["choices"][0]["message"].get("content")


def run():
    print("Worker is running...")
    while True:
        try:
            # 1. Queue에서 Job을 deque
            result = redis_client.brpop("inference_queue", timeout=0)
            if result:
                _, job_data = result
                job = json.loads(job_data)

                # 2. 추론 로직 수행
                question = job.get("question")
                job_id = job.get("id")
                print(f"[{job_id}] 처리 중: {question}")
                answer = create_response(question=question)
                print(f"{answer}")

                # 3. API 서버로 반환
                channel = f"result:{job["id"]}"
                redis_client.publish(channel, answer)

        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    run()
