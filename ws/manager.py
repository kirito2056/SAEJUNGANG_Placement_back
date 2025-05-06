from fastapi import WebSocket
from typing import List, Dict, Set
import json
from schemas import WebSocketMessage

class ConnectionManager:
    def __init__(self):
        # 활성 연결 관리 (구역별로 관리할 수도 있음)
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"WebSocket connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        print(f"WebSocket disconnected: {websocket.client}")

    async def broadcast(self, message: WebSocketMessage):
        """모든 활성 연결에 메시지 전송"""
        disconnected_sockets = set()
        message_str = message.model_dump_json() # Pydantic V2
        # message_str = message.json() # Pydantic V1
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception: # 예: WebSocketDisconnect, RuntimeError 등
                # 전송 실패 시 연결 목록에서 제거 대상 추가
                disconnected_sockets.add(connection)
                print(f"Error sending to {connection.client}, marking for removal.")

        # 연결이 끊어진 소켓 정리
        for socket in disconnected_sockets:
            self.disconnect(socket)

# 싱글톤 인스턴스 생성
manager = ConnectionManager()
