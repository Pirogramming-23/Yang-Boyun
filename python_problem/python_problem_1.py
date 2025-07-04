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
for i in range(1, count + 1):
    num += 1
    print(f'playerA : {num}')