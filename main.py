from autinfo import AutInfo

user = AutInfo(
    username="<__USERNAME__>", 
    password="<__PASSWORD__>"
)

print("GET SPECIAL USER OR SMALL RANGE:".center(50, "*"))
print(user.get(9913004))


print("GET A RANGE".center(50, "*"))
print(user.get_range(40013004, 40013008))
