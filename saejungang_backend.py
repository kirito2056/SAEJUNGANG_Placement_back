import fastapi
from fastapi.middleware.cors import CORSMiddleware

# 모듈 임포트
import database
import models # models 임포트는 필요 없을 수 있으나, 명시적으로 포함
from api import reservations # API 라우터
from ws import router as ws_router # WebSocket 라우터

# FastAPI 앱 인스턴스 생성
app = fastapi.FastAPI(
    title="새중앙 좌석 예약 시스템 API",
    description="FastAPI와 WebSocket을 이용한 좌석 예약 백엔드",
    version="0.1.0"
)

# --- CORS 미들웨어 설정 (필요 시) ---
# origins = [
#     "http://localhost",
#     "http://localhost:3000", # 예: 프론트엔드 개발 서버 주소
#     # 실제 배포 환경의 프론트엔드 주소 추가
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# --- 이벤트 핸들러: 애플리케이션 시작 시 DB 테이블 생성 ---
@app.on_event("startup")
def on_startup():
    print("Application startup: Creating database tables...")
    database.create_db_tables()
    print("Database tables check/creation complete.")

# --- 라우터 포함 ---
app.include_router(reservations.router) # API 엔드포인트
app.include_router(ws_router.router)   # WebSocket 엔드포인트

# --- 기본 경로 ---
@app.get("/")
def read_root():
    return {"message": "Saejungang Reservation Backend is running!"}

# --- 서버 실행 (uvicorn 사용 시) ---
# 터미널에서: uvicorn saejungang_backend:app --reload --host 0.0.0.0 --port 8000
# (또는 main:app, 파일 이름에 따라)

