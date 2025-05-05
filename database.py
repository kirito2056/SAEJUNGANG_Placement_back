from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os # 환경 변수 사용을 위해 추가

# --- MySQL 연결 설정 ---
# 실제 운영 환경에서는 환경 변수나 설정 파일에서 로드하는 것이 안전합니다.
MYSQL_USER = os.getenv("MYSQL_USER", "root") # 시스템 환경 변수 MYSQL_USER 또는 기본값 'root'
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password") # 시스템 환경 변수 MYSQL_PASSWORD 또는 기본값 'password'
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost") # 시스템 환경 변수 MYSQL_HOST 또는 기본값 'localhost'
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306") # 시스템 환경 변수 MYSQL_PORT 또는 기본값 '3306'
MYSQL_DB = os.getenv("MYSQL_DB", "reservation_db") # 시스템 환경 변수 MYSQL_DB 또는 기본값 'reservation_db'

# SQLAlchemy 데이터베이스 URL 형식 (MySQL + PyMySQL)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 의존성 주입을 위한 데이터베이스 세션 가져오기 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 테이블 생성 함수 (앱 시작 시 호출)
def create_db_tables():
    # 주의: 실제 운영 환경에서는 Alembic 같은 마이그레이션 도구 사용을 권장합니다.
    print(f"Attempting to connect to database: {MYSQL_DB}@{MYSQL_HOST}")
    try:
        # 테이블 생성 전에 DB 연결 확인 (선택 사항)
        with engine.connect() as connection:
            print("Database connection successful.")
        Base.metadata.create_all(bind=engine)
        print("Database tables created or already exist.")
    except Exception as e:
        print(f"Error connecting to database or creating tables: {e}")
        # 필요한 경우 여기서 애플리케이션 실행을 중단하거나 다른 처리를 할 수 있습니다.
