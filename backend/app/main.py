import logging
import json
import asyncio
import ast
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import redis.asyncio as redis

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='websocket_server.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis接続設定
REDIS_URL = "redis://redis:6379"  # Redisサーバーのアドレスを適切に設定してください
REDIS_CHANNEL = "chat_messages"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis_client = redis.from_url(REDIS_URL)
        self.pubsub = self.redis_client.pubsub()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        await self.redis_client.publish(REDIS_CHANNEL, message)
        logger.info(f"Published message to Redis: {message}")

    async def redis_listener(self):
        await self.pubsub.subscribe(REDIS_CHANNEL)
        try:
            while True:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    data = message["data"].decode("utf-8")
                    print(data, type(data))
                    message = ast.literal_eval(data).get("message")
                    await self.send_to_all_connections(message)
        finally:
            await self.pubsub.unsubscribe(REDIS_CHANNEL)

    async def send_to_all_connections(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(f"Message received: {message}")
        logger.info(f"Sent message to all connections: {message}")

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manager.redis_listener())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            await manager.broadcast(json.dumps({"message": data}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("message: A client disconnected")
        # await manager.broadcast(json.dumps({"message": "A client disconnected"}))
    except Exception as e:
        logger.error(f"UnexpectedError: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting WebSocket server")
    uvicorn.run(app, host="0.0.0.0", port=8080)