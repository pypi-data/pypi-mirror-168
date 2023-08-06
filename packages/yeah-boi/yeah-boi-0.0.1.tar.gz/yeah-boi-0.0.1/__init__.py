import asyncio

def function():
        print('lol')

def radar():
        radar = input(str('what '))
        if radar == 'idk ':
                print('me too')
        else:
                print('i see youre a man of culture as well')
class IDK():
        idk = 'idk'
        idk_yall = input('yes idk ')
        if idk_yall == 'idk':
                while True:
                        input1 = input('do you want to go on (y/n)')
                        if input1 == 'y':
                                print('aaaaa')
                        elif input1 == 'n':
                                print('stopped.')
                                break


class nope_on_your_marks():
        yoyo = 'nope'
        nope = input('what is this? ')
        if nope == 'nope':
                while True:
                        yes = input("nope. you're not going anywhere.")
                        if yes == 'quit':
                                break


def calculate():
        calculate = input('whats up ')
        if calculate == str('5 + 3'):
                answer = 8
                print(f'{answer} idk')
        elif calculate == str('2 + 2'):
                print('22 boom! nailed it.')
        else:
                print('what')

def again(loop):
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        print('o o o o o o o o  o o o o  o o o o o ')
        loop.stop()

loop = asyncio.get_event_loop()

loop.call_soon(again, loop)

loop.run_forever()
loop.close()

class OMG_WHAT_U_DOIN():
        omg = "smooth like butter"
        print('smooth like butter like a criminal undercover')

class Ravioli():
        def __init__(self, food):
                self.food = food
        print('ravioli')

def add_numbers(num1, num2):
        return num1 + num2
