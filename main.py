#!/usr/bin/env python3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import uvicorn

app = FastAPI(title="MAC地址地理位置查询")

# 配置模板目录
templates = Jinja2Templates(directory="templates")

# 天地图 API Key（请替换为你的 Key）
TIANDITU_KEY = "your_api_key_here"

# 外部 WiFi 位置查询 API
LOCATION_API = "http://api.cellocation.com:84/wifi/"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """返回前端页面"""
    return templates.TemplateResponse("index.html", {"request": request, "key": TIANDITU_KEY})

@app.post("/query")
async def query_mac(mac: str = Form(...)):
    """
    接收 MAC 地址，调用外部 API 查询位置，返回 JSON 数据
    """
    try:
        resp = requests.get(LOCATION_API, params={"mac": mac, "output": "json"}, timeout=10)
        data = resp.json()
    except Exception as e:
        return {"error": f"请求外部 API 失败: {str(e)}"}

    if data.get("errcode") == 0:
        return {
            "success": True,
            "lon": data.get("lon"),
            "lat": data.get("lat"),
            "radius": data.get("radius"),
            "address": data.get("address")
        }
    else:
        return {"success": False, "message": "未查询到该 MAC 地址的位置信息"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)