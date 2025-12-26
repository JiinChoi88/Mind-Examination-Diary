# Mind Examination Diary

## 1. Project Overview
**Mind Examination Diary**는 사용자가 하루 동안의 감정 상태와 일상을 기록하고,  
월별 감정 변화를 확인할 수 있도록 설계된 **콘솔 기반 마음 점검 일기장 프로그램**이다.

본 프로젝트는 *소프트웨어 요구사항 명세서(SRS)*를 바탕으로 구현되었으며,  
사용자의 감정 성찰과 자기 관리에 도움을 주는 것을 목표로 한다.

---

## 2. System Features

### 2.1 Daily Diary Writing
- 날짜별 일기 작성
- 날씨, 감정 점수(1~5), 일기 내용, 다음 날 계획 입력
- 입력 값 검증 및 예외 처리 제공

### 2.2 Diary Search by Date
- 특정 날짜를 입력하여 해당 날짜의 기록 조회 가능
- 기록이 존재하지 않을 경우 안내 메시지 출력

### 2.3 Monthly Emotion Statistics
- 월별 감정 점수 통계 제공
- 평균 감정 점수 계산
- 감정 변화 추이를 텍스트 기반 그래프로 시각화

### 2.4 Data Persistence
- 일기 데이터는 로컬 JSON 파일로 저장
- 프로그램 종료 후 재실행 시에도 기존 데이터 유지

---

## 3. Program Structure

```text
Diary/
 ├─ diary.py
 ├─ mind_journal.json
 └─ README.md
```
Language : Python

---

## 4. Execution Environment
```text
마음 점검 일기장
====================
1) 일기 작성
2) 날짜로 기록 조회
3) 월별 감정 통계
4) 저장 파일 정보
0) 종료

선택:
```
감정 점수는 1~5 범위의 정수만 입력 가능
잘못된 입력 시 오류 메시지 출력 후 재입력 요구

---

## 7. Error Handling

잘못된 날짜 형식 입력 시 예외 처리
감정 점수 범위 초과 입력 방지
데이터 파일 손상 또는 미존재 시 새 데이터로 초기화

---

## 8. Conclusion

본 프로젝트는 요구사항 명세서를 기반으로 설계 및 구현되었으며,
간단한 콘솔 인터페이스를 통해 사용자가 자신의 감정을 꾸준히 기록하고
월별로 감정 변화를 점검할 수 있도록 지원한다.

