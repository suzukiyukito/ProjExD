import random,time

num_taisho = 9
num_hyoji = 7
num_charenge = 2

def taisho():
    global num_taisho, num_hyoji,num_charenge
    
    num_list = [chr(random.randint(65,90)) for i in range(num_taisho)]
    num_list2 = num_list.copy()
    for i in range(int(num_taisho)-int(num_hyoji)):
        del num_list2[random.randint(0,len(num_list2)-1)]
    num_list3 = [i for i in num_list if i not in num_list2]

    #ここから表示
    print("対象文字：")
    for i in num_list:
        print(i,end=" ")
    print("\n表示文字：",)
    for i in num_list2:
        print(i,end=" ")

    print(num_list3,len(num_list3))
    a = input("欠損文字はいくつあるでしょうか？:")

    if int(len(num_list3)) == int(a):
        print("正解です。それでは具体的に欠損文字を１つずつ入れてください")
        for i in range(len(num_list3)):
            a = input(f"{i+1}番目の文字を入力して下さい:")
            if a in num_list3:
                num_list3.remove(a)
            else:
                print("不正解です。またチャレンジして下さい")
                num_charenge -= 1
            if num_list3 == []:
                print("おめ～～！！！！")
                return False
                break
            
                
    else:
        print("不正解です。またチャレンジして下さい")
        num_charenge -= 1

if __name__ == "__main__":
    while num_charenge > 0:
        a = taisho()
        if a == False:
            break