#1 ex 
def myf(n):
    return lambda a:a*n
double=myf(2)
print(double(int(input())))
#2 ex 
n=[17,23,5,4,7]
flt=list(filter(lambda x:x%2==0 , n))
print(*flt)
#3 ex
n=[1,2,3,4,5,6]
triple=list(map(lambda x:x*3,n))
print(*triple)
#4 ex
fruits=["banana","apple","orange","mango"]
srt=list(sorted(fruits,key=lambda x :len(x)))
print(*srt)