# HIDM (Hallym International Direct Message)

### 데이터 분석과 AI 매칭으로 교환학생-재학생을 연결하는 맞춤형 서비스


---

## 목차
- [소개](#소개)
- [수상](#수상)
- [환경 정보](#환경-정보)
- [시연 영상](#시연-영상)
- [기술 스택](#기술-스택)
- [주요 기능](#주요-기능)
- [설치 및 실행 방법](#설치-및-실행-방법)
- [서버 실행](#서버-실행)
- [접속 방법](#접속-방법)
- [역할 분담](#역할-분담)
- [발표 자료](#발표-자료)


---

## 소개

HIDM 프로젝트는 한림대학교 국제 기숙사(HID)에서 생활하는 교환학생과 재학생 간 원활한 문화 교류와 글로벌 커뮤니케이션 능력 향상을 목표로 합니다.  
사용자 프로필과 실시간 대화 내용을 분석해 맞춤형 대화 주제를 추천하고, WebSocket 기반 실시간 채팅을 제공합니다.

---

## 수상

### 🎉 2025-1 SW 캡스톤디자인 경진대회 2위 금상
![수상 인증 이미지](images/award.jpg)

## 환경 정보

> 이 프로젝트는 Ubuntu 24.04.2 LTS (코드네임: noble) 기반 리눅스 환경에서 개발 및 테스트되었습니다.  
> Windows, MacOS에서도 실행 가능하지만, 일부 명령어는 다를 수 있으니 참고해 주세요.

---

## 시연 영상

[![HIDM 시연 영상](https://img.youtube.com/vi/IL4jb1mR-r0/0.jpg)](https://youtu.be/IL4jb1mR-r0?si=_2exdRLn_pb90kia)

**[Hallym University Software Capstone 2025 - HIDM (Seohee Han) ](https://youtu.be/IL4jb1mR-r0?si=_2exdRLn_pb90kia)**

---

## 기술 스택
- Python 3.12.7  
- Django 5.2.1  
- Django Channels (WebSocket)  
- Redis (메시지 브로커)  
- SQLite (기본 데이터베이스)  
- 자연어 처리: SBERT (Sentence-BERT)  
- 프론트엔드: HTML, CSS, JavaScript

---

## 주요 기능

- 사용자 프로필 기반 대화 상대 및 주제 매칭  
- 관심사와 대화 이력 반영한 대화 주제 추천  
- WebSocket 실시간 채팅 지원  
- 채팅방 비밀번호 설정 및 자동 삭제 기능  
- 관리자용 대화 데이터 모니터링 및 분석 도구

---

## 설치 및 실행 방법

```bash
# Python 버전 확인 (3.12.7 권장)
python --version

# 프로젝트 폴더 생성 및 이동
mkdir django_chat
cd django_chat

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# pip 최신 버전으로 업그레이드
pip install --upgrade pip

# Django 5.2.1 설치
pip install Django==5.2.1

# Redis 서버 시작 (Ubuntu 리눅스 기준)
sudo service redis-server start

# Django 버전 확인
django-admin --version
````
---
## 서버 실행
```bash
# Django 개발 서버 실행 (로컬 테스트용)
python manage.py runserver

# 실제 WebSocket 서비스용 ASGI 서버 실행 (Daphne)
daphne config.asgi:application
````
---
## 접속 방법
```bash
# 웹 브라우저에서 아래 주소로 접속하세요
echo "http://127.0.0.1:8000"
````
---
## 역할 분담
- **이민호 (팀장)**  
  - AI 모델 개발 총괄  
  - 결과 보고서 작성  
  - 포스터 제작  
  - 발표 진행

- **한서희**  
  - 전체 프로젝트 기획  
  - AI 모델 개발  
  - 프론트엔드 및 백엔드 개발  
  - UI/UX 설계 및 구현  
  - 시연 영상 촬영 및 편집  
  - PPT 제작
 
---
## 발표 자료
- [2025 1학기 SW캡스톤 발표자료 (최종본)](docs/HIDMpresentation.ppt)
