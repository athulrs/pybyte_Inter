num = 17
if num > 1:
   for i in range(2,num):
       if (num % i) == 0:
           print("prime")
           break
       else:
       	   print("not prime")