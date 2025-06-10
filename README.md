# HIDM (Hallym International Direct Message)

### 데이터 분석과 AI 매칭으로 교환학생-재학생을 연결하는 맞춤형 서비스
본 서비스는 한림대학교 교내 국제 활성화를 위한 프로젝트입니다.

---

## 목차
- [수상](#수상)
- [환경 정보](#환경-정보)
- [시연 영상](#시연-영상)
- [기능 소개](#기능-소개)
- [기술 스택](#기술-스택)
- [설치 및 실행 방법](#설치-및-실행-방법)
- [서버 실행](#서버-실행)
- [접속 방법](#접속-방법)
- [역할 분담](#역할-분담)
- [발표 자료](#발표-자료)


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

## 기능 소개

- **실시간 1:1 채팅 서비스**  
  접속 진입 장벽을 낮추고 자율적이며 유연하게 교환학생과 재학생 간 교류 환경을 구축합니다.  
  - 온라인 특성상 진입 장벽이 낮아 부담 없이 언제든 대화 가능  
  - 영어 스피킹보다 채팅 대화 난이도가 낮아 비영어권 학생들도 쉽게 접근 가능

- **공통 관심사를 기반으로 대화 상대 추천**  
  - 유사도 순으로 대화 상대를 추천하여 자신과 잘 맞는 상대를 쉽게 선택 가능  
  - 대화 기록에서 키워드를 추출해 관심사를 계속 업데이트  
  - AI 추천을 바탕으로 사용자가 직접 친구 요청 가능
  
- **대화 주제 추천**  
  - 기본적인 회화에서 벗어나 심층 토론을 유도하는 대화 주제 제안  
  - 사용자가 직접 주제를 추가하거나 원하는 주제를 저장 가능  
  - 추천받은 순서대로 대화 주제를 정렬

- **고급 프로필 설정 및 친구 관리**  
  - 공개 프로필 설정으로 원하는 항목을 비공개로 설정 가능  
  - 친구 삭제 및 거절 기능으로 원하지 않는 상대를 거부 가능

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

 - **오민우**  
   - HIDM 이름 작명
 
---
## 발표 자료
- [2025 1학기 SW 캡스톤 발표자료](docs/HIDM.pdf)
