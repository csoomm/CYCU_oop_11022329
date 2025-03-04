def absolute_value_wrong(w):
    if w < 0:
        print(-w)
    if w > 0:
        print(w)
    
def absolute_value_extra_return(x):
    if x < 0:
        print(-x)
    else:
        print(x)
    
    return 'This is dead code.'

def is_divisible(y, z):
    if y % z == 0:
        print("True")
    else:
        print("False")
    
w=int(input("輸入W:"))
absolute_value_wrong(w)
x=int(input("輸入X:"))
absolute_value_extra_return(x)
y=int(input("輸入Y:"))
z=int(input("輸入Z:"))
print(is_divisible(y, z))

