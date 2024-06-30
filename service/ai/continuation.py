import erniebot
from erniebot import ChatCompletionResponse
from config import config

erniebot.api_type = config.erniebot_api_type
erniebot.access_token = config.erniebot_access_token

model = 'ernie-3.5'
prompt = """
# Role 续写专家 - description: 用于文档内容续写，确保文档内容的一致性和专业性。 
## Background 你是一个文章续写的专家，你的任务是确保你续写的内容与前文风格保持一致。
输出要求：只返回续写后的html源码的body部分，
"""

from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import asyncio
import json
continuation_router = APIRouter()
content = ''
class RequestModel(BaseModel):
    content: str

@continuation_router.post("/continuation")
async def continuation(request: Request, model: RequestModel):
    try:
        global content
        content = model.content
    except:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # 假设这里的逻辑生成一个SSE URL
    try:
        sse_url = "ai/continuation_stream"  # 示例URL
        return JSONResponse({"sseUrl": sse_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@continuation_router.get("/continuation_stream")
async def continuation_stream():
    global content
    messages = [{'role': 'user', 'content': prompt + content}]
    response = erniebot.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True
    )
    async def event_generator(response):
        try:
            for _ in response:
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'response': _.get_result()})}\n\n"
            #  for i in range(10):
            #     yield f"data: {json.dumps({'response': f'续写内容 {i}'})}\n\n"
                
                 
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return StreamingResponse(event_generator(response), media_type="text/event-stream")

