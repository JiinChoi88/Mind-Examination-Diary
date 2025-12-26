import json
import os
import sys
from datetime import datetime

DATA_FILE = "mind_journal.json"
MOOD_MIN = 1
MOOD_MAX = 5

def clear():
    print("\n" * 2)

def pause():
    input("\n(Enter) 계속... ")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return {}
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("Invalid data format")
            return data
    except (OSError, json.JSONDecodeError, ValueError):
        print("오류: 저장 파일이 없거나 손상되었습니다. 새로 시작합니다.")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print("오류: 파일 저장에 실패했습니다.")
        return False

def input_non_empty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("오류: 빈 입력은 허용되지 않습니다. 다시 입력하세요.")

def input_date(prompt="날짜 입력 (YYYY-MM-DD): "):
    while True:
        s = input_non_empty(prompt)
        try:
            dt = datetime.strptime(s, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("오류: 날짜 형식이 올바르지 않습니다. 예) 2025-12-27")

def input_mood(prompt="감정 점수 입력 (1~5): "):
    while True:
        s = input_non_empty(prompt)
        if not s.isdigit():
            print("오류: 감정 점수는 정수로 입력해야 합니다.")
            continue
        v = int(s)
        if MOOD_MIN <= v <= MOOD_MAX:
            return v
        print("오류: 감정 점수는 1~5 범위여야 합니다.")

def write_entry(data):
    clear()
    print("=== 일기 작성 ===")
    date_str = input_date()
    weather = input_non_empty("날씨 입력(문자열): ")
    print("오늘의 일기 내용 입력 (한 줄): ")
    diary = input_non_empty("> ")
    mood = input_mood()
    plan = input_non_empty("내일의 계획 입력: ")

    data[date_str] = {
        "date": date_str,
        "weather": weather,
        "diary": diary,
        "mood": mood,
        "plan": plan
    }

    if save_data(data):
        print("\n저장 완료.")
    pause()

def view_entry(data):
    clear()
    print("=== 날짜로 기록 조회 ===")
    date_str = input_date()
    entry = data.get(date_str)
    if not entry:
        print("\n해당 날짜의 기록이 없습니다.")
        pause()
        return

    print("\n--- 기록 ---")
    print(f"날짜: {entry.get('date','')}")
    print(f"날씨: {entry.get('weather','')}")
    print(f"감정 점수: {entry.get('mood','')}")
    print(f"일기: {entry.get('diary','')}")
    print(f"내일의 계획: {entry.get('plan','')}")
    pause()

def month_key_from_date(date_str):
    return date_str[:7]

def get_month_moods(data, month_yyyy_mm):
    moods = []
    for d, entry in data.items():
        if isinstance(d, str) and d.startswith(month_yyyy_mm):
            m = entry.get("mood")
            if isinstance(m, int) and MOOD_MIN <= m <= MOOD_MAX:
                moods.append((d, m))
    moods.sort(key=lambda x: x[0])
    return moods

def sparkline_for_moods(moods):
    blocks = {1: "▁", 2: "▂", 3: "▃", 4: "▄", 5: "▅"}
    return "".join(blocks.get(m, "·") for _, m in moods)

def monthly_stats(data):
    clear()
    print("=== 월별 감정 통계 ===")
    month = input_non_empty("월 입력 (YYYY-MM): ")
    try:
        datetime.strptime(month + "-01", "%Y-%m-%d")
    except ValueError:
        print("오류: 월 형식이 올바르지 않습니다. 예) 2025-12")
        pause()
        return

    moods = get_month_moods(data, month)
    if not moods:
        print("\n해당 월의 기록이 없습니다.")
        pause()
        return

    count = len(moods)
    avg = sum(m for _, m in moods) / count

    print("\n--- 통계 ---")
    print(f"월: {month}")
    print(f"기록 개수: {count}")
    print(f"평균 감정 점수: {avg:.2f}")
    print("\n감정 변화 추이(날짜 순):")
    print(sparkline_for_moods(moods))
    print("\n(참고) 날짜:점수")
    for d, m in moods:
        print(f"- {d}: {m}")
    pause()

def list_months(data):
    months = set()
    for d in data.keys():
        if isinstance(d, str) and len(d) >= 7 and d[4] == "-" and d[7-1] != "":
            months.add(d[:7])
    return sorted(months)

def menu():
    data = load_data()
    while True:
        clear()
        print("마음 점검 일기장")
        print("=" * 20)
        print("1) 일기 작성")
        print("2) 날짜로 기록 조회")
        print("3) 월별 감정 통계")
        print("4) 저장 파일 정보")
        print("0) 종료")
        choice = input("\n선택: ").strip()

        if choice == "1":
            write_entry(data)
            data = load_data()
        elif choice == "2":
            view_entry(data)
        elif choice == "3":
            monthly_stats(data)
        elif choice == "4":
            clear()
            print("=== 저장 파일 정보 ===")
            print(f"파일명: {DATA_FILE}")
            print(f"기록 수: {len(data)}")
            ms = list_months(data)
            if ms:
                print("저장된 월:")
                for m in ms:
                    print(f"- {m}")
            else:
                print("저장된 기록이 없습니다.")
            pause()
        elif choice == "0":
            print("종료합니다.")
            return
        else:
            print("오류: 메뉴 번호를 다시 선택하세요.")
            pause()

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n종료합니다.")
        sys.exit(0)
