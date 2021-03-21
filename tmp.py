
# class Human(object):
#     def __init__(self):
#         super().__init__()
#         self.age = 20
#     def newYear(self):
#         self.age +=1
    
#     def sleep(self)  : 
#         # print("zzz")
#         return "zzz"
    
#     def eat(self):
#         # print("yummy")
#         return "yummy"


# class Student(Human):
#     def __init__(self, *args):
#         super(Student, self).__init__(*args)
#         self.grade = 0;

# import os

# if __name__ == '__main__':
#     student1 = Student()
#     student2 = Student()

#     print(student1.age)
#     print(student2.age)
#     student1.newYear()

#     print(student1.age)
#     print(student2.age)    
    
#     print(student1.sleep())
#     print(student2.sleep())

#     print(student1.eat())
#     print(student2.eat())

#     print(student1.grade)
#     print(student2.grade)
    
import random
if __name__ == '__main__':
    nums = list(range(0,10))
    answer = random.sample(nums,3)
    print(answer)
    check = True
    answer[0] = str(answer[0])
    answer[1] = str(answer[1])
    answer[2] = str(answer[2])
    while(check):
        user = input("숫자")
        ball = 0
        strike = 0
        for x in range(3):
            print(user[x],answer[x])
            if user[x] == answer[x]:
                strike+=1
            elif user[x] in answer:
                ball += 1
        print(ball,strike)
        if(strike == 3):
            check = False
    print("end")
    
    
    
