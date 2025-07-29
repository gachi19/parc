#1
total = 0
num = int(input("과목 개수는? "))
for i in range(num):
    total += int(input(f"{i+1}번 과목 점수: "))
avg = total / num
print(f"평균점수는 {avg} 입니다.")

#2
f = open("새파일.txt" , "w")
data = input("rf")
f.write(data + "\n")
f.close()

f = open("새파일.txt", "a")
data_1 = input("남자")
f.write(data_1 + "\n")
data_2 = input("010-5555-4444")
f.write(data_2 + "\n")
while True:
    line = f.readline()
    if not line:
        break
    print(line)
f.close()

#3
a = input("첫번째 숫자 : ")
b = input("두번째 숫자 : ")

def holsu(a, b):
    holsu_list = []
    for i in range(a,b+1):
        if i % 3 == 0:
            holsu_list.append(i)
    return holsu_list
result = holsu(int(a), int(b))
print(f"{a}~{b} 사이의 홀수는 {result} 입니다.")

#5
import random
random.randrange(1,51)

answer = random.randint(1,51)
count = 5
while True:
    count -= 1
    guess = int(input("1~50 사이의 숫자를 맞춰보세요: "))
    if guess == answer:
        print("정답입니다!")
        break
    elif count == 0:
        print(f"정답은 {answer} 입니다. 기회를 모두 사용하셨습니다.")
        break