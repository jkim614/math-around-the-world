from random import *
import time
import decimal
from decimal import Decimal as D

class QuestionGenerator:
    '''
        This class generates the questions that are displayed in the
            Question Boxes
    '''
    def __init__(self):
        # Dictionary of operators
        self.dict = {
            1: '+',
            2: '-',
            3: '*',
            4: '/',
            5: '**'
        }

        # References for operations
        self.easy_divisions = [1, 2, 4, 5, 8, 9, 10, 20, 25, 40, 50, 80, -1, -2, -4, -5, -8, -9, -10, -20, -25, -40, -50, -80]
        self.easy_exponential = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]
        self.trigonometry = {
            0:['tan(0°)', 'sin(180°)', 'sin(0°)', 'cos(90°)'], 
            10:['tan(45°)', 'sin(90°)', 'cos(0°)', '1'], 
            -10:['tan(135°)', 'cos(180°)', '-1', '-1'], 
            5: ['sin(30°)', 'sin(150°)', 'cos(60°)', '0.5'],
            -5: ['cos(120°)', '-0.5', '-0.5', '-0.5']
        }

    def level_1(self):
        '''
            Uses random processes to produce questions for Level 1
                (Basic math operations between two numbers ranging 
                from 0 to 9)
            args: none
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        # Randomly selects two numbers and an operator
        exp = '{num1}{operation}{num2}'.format(num1=randint(0, 9), operation=self.dict[randint(1, 4)], num2=randint(0, 9))
        
        # Avoids dividing by zero
        if exp[1] == '/' and exp[-1] == '0':
            exp = exp.replace(exp[-1], str(randint(1, 9)))

        ans = D(str(eval(exp))).quantize(D('0.1')**2, rounding=decimal.ROUND_HALF_UP) # a decent way to round result to 2 numbers after the point. thanks to 'unutbu' from https://stackoverflow.com/questions/48887515/sympy-rounding-behaviour?rq=1
        ans = str(int(ans)) if ans == int(ans) else str(ans) # e.g. ans should be 3 instead of 3.00
        while ans[-1] == '0' and ans.find('.') != -1: # e.g. ans should be 1.2 instead of 1.20 but 0 and 10 should still be itself
            ans = ans[:-1]

        # Replaces Pythonic operators with more reader-friendly symbols
        try: exp = exp.replace('*', '×')
        except: pass
        try: exp = exp.replace('/', '÷')
        except: pass
        
        return exp, ans

    def level_2(self):
        '''
            Uses random processes to produce questions for Level 2
                (Basic math operations between two numbers ranging
                from 0 to 99)
            args: none
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        # Randomly selects two numbers and an operator
        exp = '{num1}{operation}{num2}'.format(num1=randint(0, 99), operation=self.dict[randint(1, 4)], num2=randint(0, 99))

        # Avoids divisions that are too hard
        if exp[1] == '/' or exp[2] == '/':
            exp = exp.replace(exp[exp.index('/')+1:], str(self.easy_divisions[randint(0,11)]))

        ans = D(str(eval(exp))).quantize(D('0.1')**2, rounding=decimal.ROUND_HALF_UP) # a decent way to round result to 2 numbers after the point. thanks to 'unutbu' from https://stackoverflow.com/questions/48887515/sympy-rounding-behaviour?rq=1
        ans = str(int(ans)) if ans == int(ans) else str(ans) # e.g. ans should be 3 instead of 3.00
        while ans[-1] == '0' and ans.find('.') != -1: # e.g. ans should be 1.2 instead of 1.20 but 0 and 10 should still be itself
            ans = ans[:-1]

        # Replaces Pythonic operators with more reader-friendly symbols
        try: exp = exp.replace('*', '×')
        except: pass
        try: exp = exp.replace('/', '÷')
        except: pass
        
        return exp, ans

    def level_3(self):
        '''
            Uses random processes to produce questions for Level 3
                (Math operations between 3 numbers, which may include 
                some basic trigonometry calculations. Range of numbers 
                are narrowed in order to keep the problem not too difficult)
            args: none
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        ans = 120001
        while ans > 120000 or ans < -120000: # upper and lower limit of result
            exp = str(randint(-100, 100))
            temp = exp # use an additional variable 'temp' in order to add 

            for i in range(2):
                temp_op = self.dict[randint(1,4)]
                if temp_op == '/':
                    temp_num = str(self.easy_divisions[randint(0,23)])
                else:
                    temp_num = str(randint(-100,100))
                # add some trigonometry staff
                if int(temp_num) in self.trigonometry.keys():
                    temp += temp_op
                    temp_temp = self.trigonometry[int(temp_num)][randint(0,3)]
                    temp += temp_temp if temp_temp[0] != '-' else '(' + temp_temp + ')'

                    exp += temp_op
                    exp += str(int(temp_num)/10) if str(int(temp_num)/10)[0] != '-' else '(' + str(int(temp_num)/10) + ')' # notice that in self.trigonometry, the key is actually 10 times the values in value list
                else:
                    if temp_num[0] == '-':
                        temp_num = '(' + temp_num + ')'
                    temp += temp_op
                    temp += temp_num
                    exp += temp_op
                    exp += temp_num
            
            ans = eval(exp)
        
        ans = D(str(eval(exp))).quantize(D('0.1')**2, rounding=decimal.ROUND_HALF_UP) # a decent way to round result to 2 numbers after the point. thanks to 'unutbu' from https://stackoverflow.com/questions/48887515/sympy-rounding-behaviour?rq=1
        ans = str(int(ans)) if ans == int(ans) else str(ans) # e.g. ans should be 3 instead of 3.00
        while ans[-1] == '0' and ans.find('.') != -1: # e.g. ans should be 1.2 instead of 1.20 but 0 and 10 should still be itself
            ans = ans[:-1]

        # Replaces Pythonic operators with more reader-friendly symbols
        try: temp = temp.replace('*', '×')
        except: pass
        try: temp = temp.replace('/', '÷')
        except: pass
        
        return temp, str(ans)

    def level_4(self):
        '''
            Uses random processes to produce questions for Level 4
                (Similar to level_3 but with a wider number range and 
                more mathematical operations)
            args: none
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        ans = 200001
        while ans > 200000 or ans < -200000: # upper and lower limit of result
            exp = str(randint(-100, 100))
            temp = exp # use an additional variable 'temp' in order to add 

            for i in range(2):
                temp_op = self.dict[randint(1,5)] # this randomly select an operation method
                if temp_op == '/':
                    temp_num = str(self.easy_divisions[randint(0,23)])
                elif temp_op == '**':
                    temp_num = str(self.easy_exponential[randint(0,3)])
                else:
                    temp_num = str(randint(-100,100))
                # add some trigonometry staff
                if int(temp_num) in self.trigonometry.keys():
                    temp += temp_op
                    temp_temp = self.trigonometry[int(temp_num)][randint(0,3)]
                    temp += temp_temp if temp_temp[0] != '-' else '(' + temp_temp + ')'

                    exp += temp_op
                    exp += str(int(temp_num)/10) if str(int(temp_num)/10)[0] != '-' else '(' + str(int(temp_num)/10) + ')' # notice that in self.trigonometry, the key is actually 10 times the values in value list
                else:
                    if temp_num[0] == '-':
                        temp_num = '(' + temp_num + ')'
                    temp += temp_op
                    temp += temp_num
                    exp += temp_op
                    exp += temp_num

            ans = eval(exp)
        
        ans = D(str(ans)).quantize(D('0.1')**2, rounding=decimal.ROUND_HALF_UP) # a decent way to round result to 2 numbers after the point. thanks to 'unutbu' from https://stackoverflow.com/questions/48887515/sympy-rounding-behaviour?rq=1
        ans = str(int(ans)) if ans == int(ans) else str(ans) # e.g. ans should be 3 instead of 3.00
        while ans[-1] == '0' and ans.find('.') != -1: # e.g. ans should be 1.2 instead of 1.20 but 0 and 10 should still be itself
            ans = ans[:-1]

        # Replaces Pythonic operators with more reader-friendly symbols
        try: temp = temp.replace('**', '^')
        except: pass
        try: temp = temp.replace('*', '×')
        except: pass
        try: temp = temp.replace('/', '÷')
        except: pass

        return temp, str(ans)

    def level_5(self):
        '''
            Uses random processes to produce questions for Level 5
                (Do not bother reading codes in this method. Questions 
                produced here are probably for computers, not humans.)
            args: none
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        flag = True
        while flag:
            exp = str(randint(-100, 100))
            temp = exp # use an additional variable 'temp' in order to add 

            for i in range(3):
                temp_op = self.dict[randint(1,5)]
                if temp_op == '/':
                    temp_num = str(self.easy_divisions[randint(0,23)])
                elif temp_op == '**':
                    temp_num = str(self.easy_exponential[randint(0,3)])
                else:
                    temp_num = str(randint(-100,100))
                # add some trigonometry staff
                if int(temp_num) in self.trigonometry.keys():
                    temp += temp_op
                    temp_temp = self.trigonometry[int(temp_num)][randint(0,3)]
                    temp += temp_temp if temp_temp[0] != '-' else '(' + temp_temp + ')'

                    exp += temp_op
                    exp += str(int(temp_num)/10) if str(int(temp_num)/10)[0] != '-' else '(' + str(int(temp_num)/10) + ')' # notice that in self.trigonometry, the key is actually 10 times the values in value list
                else:
                    if temp_num[0] == '-':
                        temp_num = '(' + temp_num + ')'
                    temp += temp_op
                    temp += temp_num
                    exp += temp_op
                    exp += temp_num
            if exp.count('**') < 2: flag = False
        
        #print(exp) # sometimes it may take a long long time to compute, even for computers
        ans = eval(exp)
        ans = D(str(ans)).quantize(D('0.1')**2, rounding=decimal.ROUND_HALF_UP) # a decent way to round result to 2 numbers after the point. thanks to 'unutbu' from https://stackoverflow.com/questions/48887515/sympy-rounding-behaviour?rq=1
        ans = str(int(ans)) if ans == int(ans) else str(ans) # e.g. ans should be 3 instead of 3.00
        while ans[-1] == '0' and ans.find('.') != -1: # e.g. ans should be 1.2 instead of 1.20 but 0 and 10 should still be itself
            ans = ans[:-1]
        
        # Replaces Pythonic operators with more reader-friendly symbols
        try: temp = temp.replace('**', '^')
        except: pass
        try: temp = temp.replace('*', '×')
        except: pass
        try: temp = temp.replace('/', '÷')
        except: pass

        return temp, str(ans)

    def level_6(self):
        '''
            Uses random processes to produce questions for Level 6;
                you are either too lucky or an extremely intelligent 
                math genius if you are solving questions produced here :)
            return: ('tuple') two strings: the first contains
                    the question, the second contains the answer
        '''
        exp = str(randint(-500, 500))
        temp = exp # use an additional variable 'temp' in order to add 

        for i in range(3):
            temp_op = self.dict[randint(1,5)]
            if temp_op == '/':
                temp_num = str(randint(1,500))
            elif temp_op == '**':
                temp_num = str(self.easy_exponential[randint(0,9)])
            else:
                temp_num = str(randint(-500,500))
            # add some trigonometry staff
            if int(temp_num) in self.trigonometry.keys():
                temp += temp_op
                temp_temp = self.trigonometry[int(temp_num)][randint(0,3)]
                temp += temp_temp if temp_temp[0] != '-' else '(' + temp_temp + ')'

                exp += temp_op
                exp += str(int(temp_num)/10) if str(int(temp_num)/10)[0] != '-' else '(' + str(int(temp_num)/10) + ')' # notice that in self.trigonometry, the key is actually 10 times the values in value list
            else:
                if temp_num[0] == '-':
                    temp_num = '(' + temp_num + ')'
                temp += temp_op
                temp += temp_num
                exp += temp_op
                exp += temp_num
        
        print(exp)
        ans = round(eval(exp), 2)
        if ans == int(ans): ans = int(ans)

        # Replaces Pythonic operators with more reader-friendly symbols
        try: temp = temp.replace('**', '^')
        except: pass
        try: temp = temp.replace('*', '×')
        except: pass
        try: temp = temp.replace('/', '÷')
        except: pass

        return temp, str(ans)


def test():

    test = QuestionGenerator()
    while True:
        print(test.level_1(),1)
        print(test.level_2(),2)
        print(test.level_3(),3)
        print(test.level_4(),4)
        print(test.level_5(),5)
        #print(test.level_6(),6) # You can try this one but it's not necessary. My conputer crushed here :) - Yuqiao
        #time.sleep(0.01)

if __name__ == '__main__':
    test()

