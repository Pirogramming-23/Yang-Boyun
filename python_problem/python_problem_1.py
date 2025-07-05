import random
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

#6단계 - 게임 시작
turn = 'computer'  
while num < 31:
    if turn == 'computer':
        # computer는 임의로 1~3개의 수를 부름
        count = random.randint(1, 3)
    else:
        # player는 입력받음
        count = brGame()
    
    # 31을 넘지 않도록 조정
    remaining = 31 - num
    if count > remaining:
        count = remaining
    
    for i in range(1, count + 1):
        num += 1
        print(f'{turn} : {num}')
        if num == 31:
            break
    if num == 31:
        break
    turn = 'player' if turn == 'computer' else 'computer'

#7단계
# 31을 부른 사람이 지므로, turn이 마지막에 31을 부른 사람임
winner = 'player' if turn == 'computer' else 'computer'
print(f'{winner} win!')

