import erniebot
from pydantic import BaseModel
from config import config
erniebot.api_type = config.erniebot_api_type
erniebot.access_token = config.erniebot_access_token


model = 'ernie-3.5'
prompt = """
# Role 格式与排版检测器 - description: 用于检测文章的段落格式和排版结构，确保文档格式的一致性和专业性。 
## Background 你是一个文章格式与排版结构的专家检测器，你的任务是确保文章中的各个元素都遵循特定的格式规范，确保文章的整洁和标准化。
## Goals 1. 检测文章中的各级标题是否遵循特定的格式。 2. 确保所有西文字符和中文字符之间有恰当的空格。 3. 检查特定名词是否首字母大写。 4. 确保特定的简称被正确地大写。 
## Constrains 1. 只检测提供的特定格式和规范，不做其他文本内容的评价。 2. 尽量给出详细的错误位置和建议修正。 
## Skills 1. 文章格式和排版规则知识。 2. 文本扫描和错误定位技能。 3. 中西文字符辨识技能。 4. 名词和简称的标准格式知识。 
## Definition <各级标题格式> - 一级标题：一、二、三、 - 二级标题：一）二）三） - 三级标题：1、2、3、 - 四级标题：1）2）3） 
## Workflows 1. 首先扫描文章的标题部分，确保各级标题格式正确。 - 是否具有<各级标题格式>的各级标题，有没有缺失序号 - 是否符合命名标准 - 是否符合标准格式 1. 检测西文字符和中文字符间的空格，确保它们之间有适当的间隔。如果检测出的错误非常多，请告知用户错误过多，请用户先自行检查。 2. 扫描文章中的英文单词，检查它们是否是特定名词，随后判断首字母是否大写。 3. 检测文章中的英文简写，确认它们是否已大写。 
输出要求：只返回排版后的html源码的body部分
"""

from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import json
styling_router = APIRouter()
content = ''
class RequestModel(BaseModel):
    content: str

@styling_router.post("/styling")
async def styling(request: Request, model:RequestModel):
    try:
        global content
        content = model.content
    except:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # 假设这里的逻辑生成一个SSE URL
    try:
        sse_url = "ai/styling_stream"  # 示例URL
        return JSONResponse({"sseUrl": sse_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@styling_router.get("/styling_stream")
async def styling_stream():
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

