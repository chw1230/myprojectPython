from math import *
from datetime import datetime

# 매칭지원금 계산기
# 매개변수 설명 -- year에 복무한 month를 의미 만약 (8,2023)이라면 2023년에 8개월을 복무 했다는 의미!
def calcMatchingMoney(month, year):  
    yearPercent =[0.33,0.71, 1.0, 1.0] # 22년 33%, 23년 71%, 24년 100%, 25년 100%
    if((max == 'Y' or max == 'y') and year == 2025):
        monthlyPayment = 550000 # 2025년 군적금의 월 최대 입금금액 55만원으로 확대
    elif((max == 'Y' or max == 'y') and year < 2025):
        monthlyPayment = 400000# 2024년까지 군적금의 월 최대 임금금액 40만원

    if year == 2022:
        matchingMoney = monthlyPayment * month * yearPercent[0]
    elif year == 2023:
        matchingMoney = monthlyPayment * month * yearPercent[1]
    elif year == 2024:
        matchingMoney = monthlyPayment * month * yearPercent[2]
    elif year == 2025:
        matchingMoney = monthlyPayment * month * yearPercent[3]
    else:
        print("2022년부터 2025년의 값만 처리합니다.")
    return matchingMoney 


# 원금과 이자를 더한 금액을 계산하여 리턴하고
# 매개변수 설명 -- basicMonth  군 종류에 따른 총 복무 개월 수, year와 months는 해당 year에 복무한 months를 의미함, previousMonth 지금까지의 복무한 개월 수
# 만약 (18, 12, 2023, 0)이라면 18개월을 복무해야 하고 2023년에 12개월을 근무 했고 2023년 이전에 근무한 개월 수는 없다는 것을 의미함  
def calcInterest(basicMonth,months,year,previousMonth):
    # 납입액 최대금액 고정
    if(year < 2025):
        monthlyDeposit = 400000
    elif(year == 2025):
        monthlyDeposit = 550000
    # 연 이자율을 월 이자율로 변환 (군적금은 단리 방식이므로 단리 계산식 사용)
    monthlyInterestRate = annual_interest_rate / 12 / 100
    
    totalSavings = 0 # 원금 + 이자
    totalInterest = 0 # 이자
    
    for month in range (months):
        # 각 달의 적금액에 대해 고정된 월수를 곱하여 이자 계산
        interest = monthlyDeposit * monthlyInterestRate * (basicMonth - previousMonth - month)
        month_savings = monthlyDeposit + interest
        totalInterest += interest # 총 이자 구하기
        totalSavings += month_savings # 원금 + 이자 구하기
    return totalSavings


# 입대일과 전역일을 매개변수로 받아 datetime 모듈을 이용하여 복무일수를 구해서 리턴하는 함수
def count_day(startDayList,lastDayList):
    #입대일
    startDay = datetime(startDayList[0],startDayList[1],startDayList[2]) # 복무일수 계산 하기 위한 값 대입
    #전역일
    lastDay = datetime(lastDayList[0],lastDayList[1],lastDayList[2]) # 복무일수 계산 하기 위한 값 대입
    # 복무일수 계산(전역일 - 입대일)
    diffDay = lastDay - startDay
    return diffDay


# 복무 일수를 매개변수로 받아 육군,해군,공군,해병대 구분하고 리턴하는 함수
def categorizeMilitary(diffDate):
    # 윤년을 고려한 최장 복무일을 기준으로 나눔
    if(diffDate<=550):
        return "육군 또는 해병대"
    elif(diffDate<=611):
        return "해군"
    elif(diffDate<=641):
        return "공군"


# 매칭지원금과 이자, 원금을 얻기위해 군대 기간을 연도 별로 잘라주는 함수
def cutAndCalc(startDayList,lastDayList):
    # 북무 연도가 2개 이하일때 (ex> 23입대 24전역, 24입대 25전역)
    if(lastDayList[0]-startDayList[0] == 1) :
        # 2023년 입대, 2024년 전역
        if(startDayList[0]==2023): 
            if(categorizeMilitary(diff_date)=="육군 또는 해병대"):
                basicMonth = 18
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간을 이전에 복무한 기간으로 바꾸기
                partMonth = 18 - partMonth # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="해군"):
                basicMonth = 20
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간을 이전에 복무한 기간으로 바꾸기
                partMonth = 20 - partMonth # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1  # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="공군"):
                basicMonth = 21
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간을 이전에 복무한 기간으로 바꾸기
                partMonth = 21 - partMonth# startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기
            
        # 2024년 입대,2025년 전역
        elif(startDayList[0]==2024): 
            if(categorizeMilitary(diff_date)=="육군 또는 해병대"):
                basicMonth = 18
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간을 이전에 복무한 기간으로 바꾸기
                partMonth = 18 - partMonth # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="해군"):
                basicMonth = 20
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간을 이전에 복무한 기간으로 바꾸기
                partMonth = 20 - partMonth# startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="공군"):
                basicMonth = 21
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMatchingMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간
                partMonth = 21 - partMonth # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                matchingmoney = partMatchingMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

    # 복무 년도가 2개년도를 넘어 갈때 --> (ex. 23년입대 25년전역)
    elif(lastDayList[0]-startDayList[0] == 2): 
        # 2023년 입대, 2025 전역
        if(startDayList[0]==2023): 
            if(categorizeMilitary(diff_date)=="육군 또는 해병대"):
                basicMonth = 18
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간
                partMonth += 12 # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                partMoney = partMoney + calcMatchingMoney(12,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney += calcInterest(basicMonth,partMonth-previousMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기 
                previousMonth = partMonth # 위에서 startDayList[0]+1에 복무한 기간
                partMonth = 18 - partMonth # startDayList[0]+2년에 복무할 개월 수 구하기
                startDayList[0] += 1 # startDayList[0]+2년으로 바꿔주기
                matchingmoney = partMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="해군"):
                basicMonth = 20
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간
                partMonth += 12 # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기 
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                partMoney = partMoney + calcMatchingMoney(12,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney += calcInterest(basicMonth,partMonth-previousMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]+1에 복무한 기간
                partMonth = 20 - partMonth # startDayList[0]+2년에 복무할 개월 수 구하기
                startDayList[0] += 1 # startDayList[0]+2년으로 바꿔주기
                matchingmoney = partMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기

            elif(categorizeMilitary(diff_date)=="공군"):
                basicMonth = 21
                previousMonth = 0
                partMonth = 12 - startDayList[1] + 1 # startDayList[0]년에 복무한 개월 수 구하기 
                partMoney = calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney = calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]에 복무한 기간
                partMonth += 12  # startDayList[0]년에 복무하고 남은 startDayList[0]+1년에 복무할 개월 수 구하기
                startDayList[0] += 1 # startDayList[0]+1년으로 바꿔주기
                partMoney = partMoney + calcMatchingMoney(12,startDayList[0]) # 매칭지원금 구하기
                partSavingMoney += calcInterest(basicMonth,partMonth-previousMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                previousMonth = partMonth # 위에서 startDayList[0]+1에 복무한 기간
                partMonth = 21 - partMonth # startDayList[0]+2년에 복무할 개월 수 구하기
                startDayList[0] += 1 # startDayList[0]+2년으로 바꿔주기
                matchingmoney = partMoney + calcMatchingMoney(partMonth,startDayList[0]) # 매칭지원금 구하기
                savingMoney = partSavingMoney + calcInterest(basicMonth,partMonth,startDayList[0],previousMonth) # 이자와 이자 + 원금 구하기
                return (savingMoney,matchingmoney) # 이자 + 원금과 매칭지원금을 튜플 형태로 리턴하기


def show(total):
    print("원금 + 적금 : {0}원\n매칭지원금 : {1}원".format(int(total[0]),int(total[1])))
    print("총액 : {0}원".format(int(total[0]) + int(total[1])))



#메인 코드
run = True;
total = 0
print("은행 우대 금리 별로 상이할 수 있습니다.\n18회 납입을 기준으로 제작하였으며 23년도의 납부한 군 적금에 대해서 지원되는 정부의 이자 1%는 계산하지 않도록 하겠습니다.\n매월 같은 금액을 입금한 것으로 계산하겠습니다.(추후 업데이트 예정)")
print("또한 무조건 매달 같은 금액을 보무기간 끝까지(만기까지) 지불 하는 경우만을 계산하도록 하겠습니다.(추후 업데이트 예정)")
print("---------------------------------------------------------------------------------------------------------------------------------")
while(run):
    print("1. 군적금+매칭지원금 구하기 | 2. 프로그램 종료하기")
    n = int(input("번호를 선택하시오 : "))

    if(n == 1):
        #복무일 수 계산
        try: # 날짜 입력 오류 예외 처리 해주기
            startday_str = input("입대 날짜를 '.'으로 구분하여 입력(ex> 2023.01.03 or 2023.1.3): ")
            startday_list = [int(day) for day in startday_str.split('.')] # 리스트 컴프리헨션 사용하기
            lastday_str = input("전역 날짜를 '.'으로 구분하여 입력(ex> 2023.01.03 or 2023.1.3): ")
            lastday_list = [int(day) for day in lastday_str.split('.')] # 리스트 컴프리헨션 사용하기
            diff_date = count_day(startday_list,lastday_list) 
            diff_date = int(diff_date.days) + 1 # 복무일 수
        except IndexError:
            print("오류 발생! 예시에 맞는 입대, 전역 날짜를 입력하시오!")
            continue # 처음으로 돌아가기
        except ValueError:
            print("오류 발생! 예시에 맞는 입대, 전역 날짜를 입력하시오!")
            continue # 처음으로 돌아가기
        print("({0}를 복무하였습니다.)군복무 일수 : {1}일".format(categorizeMilitary(diff_date),diff_date)) # 육,해,공 구분과 복무일 수 출력

        # 원금 + 이자 계산
        max = input("매달 입금 할 수 있는 최대금액(23년,24년 -> 400,000원 | 25년 -> 550,000원)을 입금하였나요?(Y or N)")
        if(max=='y' or max =='Y'):
            annual_interest_rate = float(input("(보통의 군 적금은 기본 5% 입니다.) 연 이자율을 입력하세요 (%): "))
        elif(max=='n' or max =='N'):
            print("아직 업데이트 중 입니다.\n")
            continue
        else:
            print("(Y or y), (N or n)이 아닌 다른 문자를 입력하였습니다.\n")
            continue
        total = cutAndCalc(startday_list,lastday_list)
        show(total)

    elif(n == 2):
        print("프로그램이 종료됩니다.")
        run = False
    else:
        print("제공된 번호를 입력하시오.")