import erniebot
from pydantic import BaseModel
from config import config
erniebot.api_type = config.erniebot_api_type
erniebot.access_token = config.erniebot_access_token

model = 'ernie-3.5'
prompt = """
如果后面是中文，翻译成英文，否则英语翻译中文
"""

from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import json
trans_router = APIRouter()
content = ''
class RequestModel(BaseModel):
    content: str

@trans_router.post("/translate")
async def trans(request: Request, model:RequestModel):
    try:
        global content
        content = model.content
    except:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # 假设这里的逻辑生成一个SSE URL
    try:
        sse_url = "ai/translate_stream"  # 示例URL
        return JSONResponse({"sseUrl": sse_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@trans_router.get("/translate_stream")
async def trans_stream():
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

