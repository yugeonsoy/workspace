import random

def 강화_확률(단계):
    return max(0.1, 1.0 - 단계 * 0.1)  # 단계가 올라갈수록 성공 확률이 감소

def 강화_검(검이름, 현재단계):
    if 현재단계 >= 5:
        return f"{검이름}의 강화 단계는 이미 최대입니다."
    
    성공확률 = 강화_확률(현재단계)
    if random.random() <= 성공확률:
        새로운단계 = 현재단계 + 1
        return f"검 강화 성공! (현재 검 등급: {검이름} {새로운단계}단계)"
    else:
        return "검이 깨졌다 (강화실패)"

def main():
    검이름 = input("검의 이름을 입력하세요: ")
    현재단계 = 0
    
    while 현재단계 < 5:
        print(f"현재 단계: {현재단계}단계")
        input("강화 하려면 Enter를 누르세요...")
        결과 = 강화_검(검이름, 현재단계)
        print(결과)
        
        if "강화 성공" in 결과:
            현재단계 += 1
        else:
            break

    if 현재단계 == 5:
        print(f"{검이름}은 이미 최대 단계입니다.")

if __name__ == "__main__":
    main()
