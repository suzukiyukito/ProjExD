import random
def shutudai():
    qst =[["勤労感謝の日は何月何日？",("11月23日","１１月２３日","11がつ23にち","11月２３日","１１月23日")],
    ["海の日は何月何日？",("7月18日","７月１８日","7がつ18にち","7月１８日","７月18日")],
    ["憲法記念日は何月何日？",("5月7日","５月７日","5がつ7にち","5月７日","５月7日")]]
    num = random.randint(0,len(qst)-1)
    print(qst[num][0])
    return qst[num][1]
    
def kaito(n):
    ans = input()
    if ans in n:
        print("正解！")
    else:
        print("はずれ～～～～")

if __name__ == "__main__":
    n = shutudai()
    kaito(n)
