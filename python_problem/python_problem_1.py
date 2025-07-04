#1단계
num = 0

#8단계 brGame 함수 정의 - 중복되는 입력 검증 코드를 함수로 만들기
def brGame():
    while True:
        try:
            count = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
            if count not in [1, 2, 3]:
                print('1,2,3 중 하나를 입력하세요')
                continue
            break
        except ValueError:
            print('정수를 입력하세요')
    return count

#  1에서 3사이의 정수를 입력 받는 코드
count = brGame()

#3단계 
count = brGame()

#4단계
for i in range(count):
    num += 1
    print(f'playerA : {num}')

#5단계
# playerB 입력 및 출력
count_b = brGame()

for i in range(count):
    num += 1
    print(f'playerB : {num}')

#6단계
turn = 'playerA'
while num < 31:
    count = brGame()
    for i in range(1, count + 1):
        num += 1
        print(f'{turn} : {num}')
        if num == 31:
            break
    if num == 31:
        break
    turn = 'playerB' if turn == 'playerA' else 'playerA'

#7단계
# 31을 부른 사람이 지므로, turn이 마지막에 31을 부른 사람임
winner = 'playerB' if turn == 'playerA' else 'playerA'
print(f'{winner} win!')

