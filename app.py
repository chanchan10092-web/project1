import random

# 1. 가위바위보 선택지
options = ["가위", "바위", "보"]

# 2. 내가 선택한 항목 (테스트)
user_choice = "바위"

# 3. 컴퓨터의 random.choice() 선택
computer_choice = random.choice(options)

print(f"👤 나: {user_choice} vs 🤖 컴퓨터: {computer_choice}")

# 4. 승패 판정 조건문
if user_choice == computer_choice:
    print("🤝 무승부입니다!")
elif (user_choice == "가위" and computer_choice == "보") or \
     (user_choice == "바위" and computer_choice == "가위") or \
     (user_choice == "보" and computer_choice == "바위"):
    print("🎉 내가 이겼습니다!")
else:
    print("😭 컴퓨터가 이겼습니다!")
