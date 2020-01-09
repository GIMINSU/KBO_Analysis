# # daum_stock_price = 89000
# # naver_stock_price = 751000
# # daum_stock = 100
# # naver_stock = 20
#
# def calculation_stock(daum_stock, daum_stock_price, daum_price_rate, naver_stock, naver_stock_price, naver_price_rate):
#     if daum_price_rate == 0 and naver_price_rate == 0:
#         daum_amount = (daum_stock * daum_stock_price)
#         naver_amount = (naver_stock * naver_stock_price)
#         total_amount = daum_amount + naver_amount
#         return total_amount
#     elif daum_price_rate != 0 or daum_price_rate != 0:
#         apply_daum_price = daum_stock_price + (daum_stock_price * daum_price_rate)
#         apply_naver_price = naver_stock_price + (naver_stock_price * naver_price_rate)
#         apply_daum_amount = daum_stock * apply_daum_price
#         apply_naver_amount = naver_stock * apply_naver_price
#         apply_total_amount = apply_daum_amount + apply_naver_amount
#         return apply_total_amount
#
#
# def trans_temperature(fahrenheit):
#     celsius = (float(fahrenheit-32))/1.8
#     return celsius
# print(trans_temperature(50))
#
# def enumerater_print(some_string, num_try):
#     for i in range(0, num_try):
#         print(some_string)
#
# # enumerater_print('pizza', 10)
#
#
#
# print(calculation_stock(daum_stock=100, daum_stock_price=89000, daum_price_rate=-0.05, naver_stock=20, naver_stock_price=751000, naver_price_rate=-0.1))

# # class, instance, inheritance
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def setx(self, x):
#         self.x = x
#
#     def sety(self, y):
#         self.y = y
#
#     def get(self):
#         return (self.x, self.y)
#
#     def move(self, dx, dy):
#         self.x += dx
#         self.y += dy
#
# a = Point(3,3)
# a.setx(4)
# a.sety(3)
# print(a.get())
# a.move(2, 3)
# print(a.get())

# oop inheritance and subclass

class Unit(object):
    def __init__(self, rank, size, life):
        self.name = self.__class__.__name__
        self.rank = rank
        self.size = size
        self.life = life

    def show_status(self):
        print('이름: {}'.format(self.name))
        print('등급: {}'.format(self.rank))
        print('사이즈: {}'.format(self.size))
        print('라이프: {}'.format(self.life))

class Goblin(Unit):
    # method override and damage 속성 추가
    def __init__(self, rank, size, life, attack_type, damage):
        super(Goblin, self).__init__(rank, size, life)
        self.attack_type = attack_type
        self.damage = damage
    def show_status(self):
        super(Goblin, self).show_status()
        print('공격 타입: {}'.format(self.attack_type))
        print('데미지: {}'.format(self.damage))

    # attack method 추가
    def attack(self):
        print('[{}]이 공격합니다! 상대방 데미지({})'.format(self.name, self.damage))

class SpearGoblin(Goblin):
    def __init__(self, rank, size, life, attack_type, damage, spear_type):
        super(SpearGoblin, self).__init__(rank, size, life, attack_type, damage)
        self.spear_type = spear_type

    def show_status(self):
        super(SpearGoblin, self).show_status()
        print('창 타입: {}'.format(self.spear_type))

class Hero(Unit):
    def __init__(self, rank, size, life, goblins=None):

        super(Hero, self).__init__(rank, size, life)

        if goblins is None:
            self.goblins = []
        else:
            self.goblins = goblins

    def show_own_goblins(self):
        num_of_goblins = len([x for x in self.goblins if isinstance(x, Goblin)])
        num_of_spear_goblins = len([x for x in self.goblins if isinstance(x, SpearGoblin)])
        print('현재 영웅이 소유한 고블린은 {}명, 창 고블린은 {}명 입니다.'.format(num_of_goblins, num_of_spear_goblins))

    def make_goblin_attack(self):
        for goblin in self.goblins:
            goblin.attack()

    def add_goblins(self, new_goblins):
        for goblin in new_goblins:
            if goblin not in self.goblins:
                self.goblins.append(goblin)
            else:
                print('이미 추가된 고블린입니다.')

    def remove_goblins(self, old_goblins):
        for goblin in old_goblins:
            try:
                self.goblins.remove(goblin)
            except:
                print('소유하고 있지 않은 고블린입니다.')

# goblin_1 = Goblin('병사', 'Small', 100, '근접 공격')
#
# goblin_1.show_status()
# print(Goblin.__dict__)
# print(help(Goblin))
# print(dir(Goblin))

# spear_goblin_1 = SpearGoblin('병사', 'Small', 100, '레인지 공격', 10, '긴 창')
#
# spear_goblin_1.show_status()

# create goblin object
goblin_1 = Goblin('병사', 'Small', 100, '근접 공격', 15)
goblin_2 = Goblin('병사', 'Small', 100, '근접 공격', 15)
spear_goblin_1 = SpearGoblin('병사', 'Small', 100, '레인지 공격', 10, '긴 창')

# create hero object than assign goblin object
hero_1 = Hero('영웅', 'Big', 300, [goblin_1, goblin_2, spear_goblin_1])

# create new goblin
goblin_3 = Goblin('병사', 'Small', 100, '근접 공격', 20)
spear_goblin_2 = SpearGoblin('병사', 'Small', 100, '레인지 공격', 5, '긴 창')

print('# 새로운 고블린 추가 전')
hero_1.show_own_goblins()
hero_1.make_goblin_attack()

# 새로운 고블린 추가
hero_1.add_goblins([goblin_3, spear_goblin_2])

print('\n# 새로운 고블린 추가 후')
hero_1.show_own_goblins()
hero_1.make_goblin_attack()

# 추가한 고블린 삭제
hero_1.remove_goblins([goblin_3, spear_goblin_2])

print('\n# 추가한 고블린 삭제 후')
hero_1.show_own_goblins()
hero_1.make_goblin_attack()

# 영웅에게 소유되지 않은 고블린 생성
goblin_4 = Goblin('병사', 'Small', 100, '근접 공격', 20)

# 이미 소유한 고블린 추가
print('\n# 에러 메세지 발생')
hero_1.add_goblins([goblin_1])
hero_1.remove_goblins([goblin_4])
