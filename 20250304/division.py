a=int(input("輸入較大的數字"))
b=int(input("輸入較小的數字"))
x=[]
def division(a,b):
    for i in range (1,a+1):
        if a%i==0 and b%i==0:
            x.append(i)
    print ("最大公因數為",x[-1])

division(a,b)
