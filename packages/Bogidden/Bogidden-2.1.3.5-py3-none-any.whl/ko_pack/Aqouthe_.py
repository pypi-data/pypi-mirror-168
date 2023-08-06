
import math

class math_fuction() :
    def inch_change_cm(inch) :
        '''인치를 cm로 바꾸는 함수'''
        cm = inch * 2.54
        return cm

    def cir_area(radius) :
        '''원 넓이를 구하는 함수'''
        return radius * radius * math.pi()

    def cir_circum(radius) :
        '''원 둘레?를 구하는 함수(뭔지 모르겠음)'''
        return 2 * math.pi() * radius

    def gcd(x, y) :
        '''최대공약수를 구하는 함수'''
        if x > y :
            small = y
        else : 
            small = x
        for i in range(1, small + 1) :
            if((x % i == 0) and (y % i == 0)) :
                result = i
        return result

    def factorial(n) :
        '''팩토리얼을 계산하는 함수'''
        return math.factorial(n)

    def plus(a, b) :
        '''더하기를 해주는 함수'''
        return a + b

    def minus(a, b) :
        '''두 수를 빼는 함수'''
        return a - b

    def multiply(a, b) :
        '''a와 b값을 곱하는 함수'''
        return a * b

    def divide(a, b) :
        '''a와 b를 나누어주는 함수이다.'''
        return a / b

    def wa_sans() :
        print('''언더테일 아시는구나! 혹시 모르시는분들에 대해
설명해드립니다 샌즈랑 언더테일의 세가지 엔딩루트중 몰살엔딩의 최종보스로 진.짜.겁.나.어.렵.습.니.다 공격은 전부다 회피하고 만피가 92인데 
샌즈의 공격은 1초당 60이 다는데다가 독뎀까지 추가로 붙어있습니다.. 
하지만 이러면 절대로 게임을 깰 수 가없으니 제작진이 치명적인 약점을 만들었죠. 샌즈의 치명적인 약점이 바로 지친다는것입니다.
 패턴들을 다 견디고나면 지쳐서 자신의 턴을 유지한채로 잠에듭니다.
하지만 잠이들었을때 창을옮겨서 공격을 시도하고 샌즈는 1차공격은 피하지만 
그 후에 바로날아오는 2차 공격을 맞고 죽습니다.''')
