#num = 0 선언
num = 0

#  1에서 3사이의 정수를 입력 받는 코드
count = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))

#3단계 
while True:
    try:
        count = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
        if count not in [1, 2, 3]:
            print('1,2,3 중 하나를 입력하세요')
            continue
        break
    except ValueError:
        print('정수를 입력하세요')

#4단계
for i in range(count):
    num += 1
    print(f'playerA : {num}')

#5단계
# playerB 입력 및 출력
while True:
    try:
        count_b = int(input('부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
        if count_b not in [1, 2, 3]:
            print('1,2,3 중 하나를 입력하세요')
            continue
        break
    except ValueError:
        print('정수를 입력하세요')

for i in range(count):
    num += 1
    print(f'playerB : {num}')

#6단계
turn = 'playerA'
while num < 31:
    while True:
        try:
            count = int(input(f'부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : '))
            if count not in [1, 2, 3]:
                print('1,2,3 중 하나를 입력하세요')
                continue
            break
        except ValueError:
            print('정수를 입력하세요')
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

