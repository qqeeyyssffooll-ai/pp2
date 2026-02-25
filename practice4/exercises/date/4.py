from datetime import datetime

now = datetime.now().replace(microsecond=0)

user_input = input("YYYY-MM-DD HH:MM:SS: ")
users_date = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")

difference = now - users_date
print(int(abs(difference.total_seconds())))