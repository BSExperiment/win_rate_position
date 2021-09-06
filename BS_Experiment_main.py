# -*- coding:utf-8 -*-
from time import perf_counter as clock, sleep
from copy import deepcopy
from random import random, shuffle
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import seaborn as sns

fontFile = 'C:/Windows/Fonts/malgun.ttf'
fontName = fm.FontProperties(fname=fontFile, size=50).get_name()
plt.rc('font', family=fontName)

class _Item: # 아이템
    def __init__(self, name='Crimson Flower', main_category='FOOD', sub_category='Health', item_class='Legendary', item_value=220, 
                 item_per_set=1, effect_dict={}):
        # main_category : 아이템 대분류(무기, 방어구, 음식, 기타)
        # sub_category : 아이템 소분류( (무기:권법,둔기,베기,찌르기,총,활,던,트랩),(방어구:머리,몸통,팔,다리,장신구)... )
        # item_class : 아이템의 등급
        # item_value : 아이템의 수치(예:붕대의 item_value는 30임)
        # item_per_set : 1세트당 아이템 개수
        # effect_dict : 아이템이 가지고 있는 효과들
        self.name = name
        self.main_category = main_category # 아이템 대분류(무기, 방어구, 음식, 기타)
        self.sub_category = sub_category # 아이템 소분류( (무기:권법,둔기,베기,찌르기,총,활,던),(방어구:머리,몸통,팔,다리,장신구)... )
        self.item_class = item_class # 아이템의 등급
        self.item_value = item_value # 아이템의 수치(예:붕대의 item_value는 30임)
        self.item_per_set = item_per_set # 1세트당 아이템 개수
        self.effect_dict = effect_dict # 아이템이 가지고 있는 효과들
        
        
        if self.main_category=='Gear': # 아이템 대분류가 방어구면
            if self.item_class=='Epic': self.damage_decrease = -3# 영웅등급 방어구 데미지 감소 : -3
        
    def item_info(self):
        print('----------')
        print('이름\t', self.name)
        print('대분류\t', self.main_category)
        print('소분류 \t', self.sub_category)
        print('등급\t', self.item_class)
        print('수치\t', self.item_value)
        print('세트당 개수\t', self.item_per_set)
        print('효과\t', self.effect_dict)
        
class _Character: # 캐릭터
    def __init__(self, name='HyunWoo', li_stat=[12,14,120,100,46,58.2,222,168], combat=None, field=None, li_passive=[], 
                 dict_mastery={'Hand':'D', 'Blunt':'F', 'Blade':'F', 'Stab':'F', 'Gun':'F', 'Bow':'F', 'Thrown':'F'}):
        # li_stat : [1레벨 공격력,방어력,체력,스테미너, 18레벨 공격력,방어력,체력,스테미너]
        self.name = name
        self.lv1_attack = li_stat[0]
        self.lv1_armor = li_stat[1]
        self.lv1_health = li_stat[2]
        self.lv1_stamina = li_stat[3]
        self.lv18_attack = li_stat[4]
        self.lv18_armor = li_stat[5]
        self.lv18_health = li_stat[6]
        self.lv18_stamina = li_stat[7]
        self.growth_attack = (self.lv18_attack-self.lv1_attack)/17 # 성장 체력
        self.growth_armor = (self.lv18_armor-self.lv1_armor)/17 # 성장 방어력
        self.growth_health = (self.lv18_health-self.lv1_health)/17 # 성장 체력
        self.growth_stamina = (self.lv18_stamina-self.lv1_stamina)/17 # 성장 스테미너
        self.combat = combat
        self.field = field
        self.li_passive = li_passive
        self.dict_mastery = dict_mastery
    def character_info(self):
        print('----------')
        print(self.name)
        for i in self.dict_mastery.keys():
            print('%s\t' % i, end='')
        print()
        for i in self.dict_mastery.values():
            print('%s\t' % i, end='')
        
        print('\n\n\t공격력\t방어력\t체력\t스테미너')
        for i in range(0, 18):
            atk = self.growth_attack*i+self.lv1_attack
            arm = self.growth_armor*i+self.lv1_armor
            health = self.growth_health*i+self.lv1_health
            stamina = self.growth_stamina*i+self.lv1_stamina
            print('%d레벨\t%.1f\t%.1f\t%.1f\t%.1f' % (i+1, atk, arm, health, stamina) )
        print('성장\t%.1f\t%.1f\t%.1f\t%.1f\n' % (self.growth_attack, self.growth_armor, self.growth_health, self.growth_stamina) )
        
        print('컴뱃 스킬\t%s' % self.combat)
        print('필드 스킬\t%s' % self.field)
        print('패시브 스킬\t%s' % self.li_passive)
    def level_stat(self, i): # 특정 레벨에서의 스탯(공방체스)을 계산해서 반환함
        # i : 레벨
        i = i-1
        return (self.growth_attack*i+self.lv1_attack, self.growth_armor*i+self.lv1_armor, 
    self.growth_health*i+self.lv1_health, self.growth_stamina*i+self.lv1_stamina)

class _Player: # 플레이어
    category = 'player'
    modifiers = {
        'F':{'atk':0.55, 'hit':0.7, 'armor_penetration':0},
        'E':{'atk':0.6, 'hit':0.74, 'armor_penetration':0},
        'E+':{'atk':0.7, 'hit':0.77, 'armor_penetration':0},
        'D':{'atk':0.8, 'hit':0.8, 'armor_penetration':0},
        'D+':{'atk':0.9, 'hit':0.82, 'armor_penetration':0},
        'C':{'atk':1.1, 'hit':0.85, 'armor_penetration':0},
        'C+':{'atk':1.3, 'hit':0.87, 'armor_penetration':0},
        'B':{'atk':1.5, 'hit':0.9, 'armor_penetration':0},
        'B+':{'atk':1.7, 'hit':0.92, 'armor_penetration':0},
        'A':{'atk':1.9, 'hit':0.95, 'armor_penetration':0},
        'A+':{'atk':2.15, 'hit':0.97, 'armor_penetration':0},
        'S':{'atk':2.4, 'hit':0.99, 'armor_penetration':0.07},
        'SS':{'atk':2.65, 'hit':1, 'armor_penetration':0.15}
        }
    def __init__(self, level=1, name=None, character=_Character(), li_bag_state=[None, None, None, None, None, None], 
                 dict_equipment_state={'Weapon':None , 'Head':None, 'Clothes':None, 'Arm':None, 'Leg':None, 'Accessory':None}, 
                 li_effects=[], mastery = 'D', stance = 'Offensive'):
        self.name = name
        self.level = level
        self.character = character
        self.dict_character_stat = {}
        (self.dict_character_stat['attack'], self.dict_character_stat['armor'], 
         self.dict_character_stat['health'], self.dict_character_stat['stamina']) = self.character.level_stat(self.level)
        
        self.is_live = True # 살아있나?
        
        self.li_bag_state = li_bag_state
        self.dict_equipment_state = dict_equipment_state
        self.effect_dict = li_effects
        self.mastery = mastery # 숙련도
        self.stance = stance # 태세
        
        if self.stance=='Offensive': # 공격 태세
            self.find_enemy = 0.3 # 발견률 보정치
            self.found = 0 # 피발견률 보정치
        else: # 은신 태세
            self.find_enemy = -0.3 # 발견률 보정치
            self.found = -0.2 # 피발견률 보정치
        
        # self.armor_penetration = 0 # 방어구 관통력
        # if self.mastery=='S': self.armor_penetration = 0.07
        # elif self.mastery=='SS': self.armor_penetration = 0.15
        self.modifiers = _Player.modifiers[self.mastery]
        # print(self.modifiers)
        
        self.dict_total_stat = {} # 최종 스탯(장비, 효과, 연구 성과 등을 모두 반영함)
        # 전체 공격력( (캐릭터 공격력+무기 공격력) * 보정효과 )
        self.dict_total_stat['attack'] = (self.dict_character_stat['attack']+
                                          self.dict_equipment_state['Weapon'].item_value) * self.modifiers['atk']
                                          
        # 전체 방어력( 캐릭터 방어력 + 전체 방어력 )
        self.dict_total_stat['armor'] = (self.dict_character_stat['armor'] + dict_equipment_state['Head'].item_value +
                                         dict_equipment_state['Clothes'].item_value + dict_equipment_state['Arm'].item_value+
                                         dict_equipment_state['Leg'].item_value + dict_equipment_state['Accessory'].item_value)
        self.dict_total_stat['health'] = self.dict_character_stat['health']
        self.dict_total_stat['stamina'] = self.dict_character_stat['stamina']
        # print(self.dict_total_stat)
        # 데미지 감소 총합
        self.dict_total_stat['damage_decrease'] = (dict_equipment_state['Head'].damage_decrease + 
                                                   dict_equipment_state['Clothes'].damage_decrease +
                                                   dict_equipment_state['Arm'].damage_decrease +
                                                   dict_equipment_state['Leg'].damage_decrease +
                                                   dict_equipment_state['Accessory'].damage_decrease)
        
        self.dict_current_stat = {} # 현재 공방체스
        for k, v in self.dict_total_stat.items():
            self.dict_current_stat[k] = v
    
    def change_stance(self, stance=None):
        if stance == None:
            if self.stance == 'Offensive':
                self.stance = 'Dodging'
            else:
                self.stance = 'Offensive'
        else:
            self.stance = stance
        
        if self.stance=='Offensive':
            self.find_enemy = 0.3 # 발견률 보정치
            self.found = 0 # 피발견률 보정치
        else:
            self.find_enemy = -0.3 # 발견률 보정치
            self.found = -0.2 # 피발견률 보정치
    
    def player_info(self):
        print('----------')
        print('이름\t%s' % self.name)
        print('캐릭터\t%s' % self.character.name)
        print('현재 레벨\t%d' % self.level)
        print('현재 숙련도\t%s' % self.mastery)
        print('현재 태세\t%s' % self.stance)
        
        print('\n현재 캐릭터 스탯')
        for k in self.dict_character_stat.keys():
            print('%s\t' % k, end='')
        print()
        for v in self.dict_character_stat.values():
            print('%.2f\t' % v, end='')
            
        print('\n\n최종 캐릭터 스탯')
        for k in self.dict_total_stat.keys():
            print('%s\t' % k, end='')
        print()
        for v in self.dict_total_stat.values():
            print('%.2f\t' % v, end='')
            
        print('\n\n현재 캐릭터 스탯')
        for k in self.dict_current_stat.keys():
            print('%s\t' % k, end='')
        print()
        for v in self.dict_current_stat.values():
            print('%.2f\t' % v, end='')
            
        print('\n\n현재 가지고 있는 아이템 목록')#, self.li_bag_state)
        for i in self.li_bag_state:
            if i==None: break
            print([i[0].name, i[1]])
        
        print('\n현재 장비 상태')
        for k, v in self.dict_equipment_state.items():
            print('%s\t%s' % (k[:7], v.name))
        
        print('\n부여되어있는 효과 목록 :', self.effect_dict)
        # for i in self.effect_dict:
            # print(i)
        
        
class _Area: # 지역
    def __init__(self, name='지하통로', li_players=[], li_items=[]):
        # li_players : 이 지역에 있는 플레이어 리스트
        # li_items : 이 지역에 있는 아이템 리스트
        self.name = name
        self.li_players = li_players
        self.player_cnt = len(self.li_players)
        self.li_items = li_items
        
        self.dead_body_li = []
    
    def live_player(self): # 현재 지역에 살아있는 플레이어 수
        cnt = 0
        for i in self.li_players:
            if i.is_live: cnt += 1
        return cnt
    
    def area_info(self):
        print('%s에 있는 플레이어 목록' % self.name)
        for i in self.li_players:
            print(i.name)
        
        print('\n%s에 있는 아이템 목록' % self.name)
        for i in self.li_items:
            print(i.name)
    
class _None:
    category = None
    name = None

class _Battle_state:
    def __init__(self, action_time, player, action, find_li=[_None()],
                is_fixed_damage = False,
                fixed_damage = 1):
        self.action_time = action_time
        self.player = player
        self.action = action
        self.find_li = find_li
        self.is_fixed_damage = is_fixed_damage
        self.fixed_damage = fixed_damage
        
        # print(self.is_fixed_damage)
        
    def search_start(self, area):
        found_object_li = []
        battle_state_li = []
        #3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
        # 3순위 : 플레이어 발견(70%)
        li_find_enemies = [] # 각각의 적들이 발견당할 확률
        li_find_enemies2= [] # 각각의 적들이 발견당할 누적 확률 (예시 : A의 피발견률이 80%고, B의 피발견률이 100%면 li_find_enemies의 값은 [0.8, 1.8]이 됨)
        find_enemies = 0.0 # 적들이 발견당할 누적 확률 (예시 : A의 피발견률이 80%고, B의 피발견률이 100%면 find_enemise의 값은 1.8이 됨)
        find_enemy = 0 # 특정 적이 발견될 확률
        for i, v in enumerate(area.li_players):
            if v.name==self.player.name or (not v.is_live):
                find_enemy = 0
            else:
                find_enemy = 0.7 + v.found + self.player.find_enemy # 특정 적의 피발견률 = 0.7(기본 발견률) + 적의 피발견률 보정 + 나의 발견률 보정
                find_enemies += find_enemy
            li_find_enemies.append(find_enemy)
            li_find_enemies2.append(find_enemies)
            
        if len(li_find_enemies)==0:
            enemy_test_subject_find = 0
        else:
            enemy_test_subject_find = max(li_find_enemies) # 적 플레이어 발견 확률
            
        found = random() # 0이상 1미만의 실수
        if enemy_test_subject_find > found: # 적 플레이어를 발견함
            # print('플레이어 발견')
            found = random() * max(li_find_enemies2) # 어떤 플레이어가 발견되었을까를 정해주는 값
            start_value = 0
            # print(found)
            for i, v in enumerate(li_find_enemies2):
                if v > found >= start_value:
                    found_object_li = [area.li_players[i]]
                start_value = v
                    
            battle_state_li.append(_Battle_state(self.action_time+1.5, self.player, 'search_completion', found_object_li, is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
            # battle_state_li.append(_Battle_state(self.action_time+1.5, self.player, 'attack', found_object_li))
            return battle_state_li
        #3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
        
        battle_state_li.append(_Battle_state(self.action_time+1.5, self.player, 'search_completion', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
        battle_state_li.append(_Battle_state(self.action_time+1.5, self.player, 'search_start', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
        return battle_state_li
    
    def enemy_player_found(self):
        return [_Battle_state(self.action_time, self.player, 'attack', self.find_li, is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage)]
    
    def attack(self):
        battle_state_li = []
        if self.find_li[0].is_live: # 살아있으면 공격
            if self.is_fixed_damage:
                self.find_li[0].dict_character_stat['health'] -= self.fixed_damage
            else:
                self.find_li[0].dict_character_stat['health'] = _Attack(self.player, self.find_li[0])
            # print(self.find_li[0].dict_character_stat['health'])
            
            if self.find_li[0].dict_character_stat['health'] <= 0: # 적 처치
                self.find_li[0].is_live = False
                    
                battle_state_li.append(_Battle_state(self.action_time, self.find_li[0], 'dead', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
                battle_state_li.append(_Battle_state(self.action_time+1.5, self.player, 'search_start', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
            else:
                battle_state_li.append(_Battle_state(self.action_time+1, self.player, 'search_start', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
                    
        else: # 죽어있음
            battle_state_li.append(_Battle_state(self.action_time, self.player, 'already_dead', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage))
            # battle_state_li.append(_Battle_state(self.action_time+0.5, self.player, 'search_start'))
        
        return battle_state_li
    
    def already_dead(self):
        # return [_Battle_state(self.action_time, self.player, 'search_start')]
        return [_Battle_state(self.action_time+0.5, self.player, 'search_start', is_fixed_damage=self.is_fixed_damage, fixed_damage=self.fixed_damage)]
        
def _Attack(attacker, enemy):
    # 데미지 = (attacker의 합계 공격력 * 100) / (enemy의 합계 방어력 + 100)
    damage = int( (attacker.dict_total_stat['attack'] * 100) / 
                  (enemy.dict_total_stat['armor'] * (1-attacker.modifiers['armor_penetration']) + 100) +
                  enemy.dict_total_stat['damage_decrease'] )
    if damage <= 0: damage = 1
    # print(damage)
    # print(enemy.dict_current_stat['health'])
    enemy.dict_current_stat['health'] -= damage
    # print(enemy.dict_current_stat['health'])
    # print(damage)
    return enemy.dict_current_stat['health']

def _Print(player_cnt, n, munjayeol, t):
    print('%9.3f ' % t, end='')
    for i in range(player_cnt):
        if i==n:
            print('%20s' % (munjayeol))
            break
        else:
            print('%20s ' % (''), end='')


def _Area_Battle(area, print_sw=True,
                   is_fixed_damage = False,
                   fixed_damage = 1):
    name_li = [] # 순위
    # print(is_fixed_damage)
    
    name_no_dict = {}
    for i, v in enumerate(area.li_players):
        name_no_dict[v.name] = i+1
    
    battle_state_li = [] # 전투 상황
    # battle_state_li.append(_Battle_state(0, area.li_players[0], 'search_start')) # 0초에 0번 플레이어의 탐색 시작
    # battle_state_li.append([0.3, 2, 'search_start']) # 0.3초에 2번 플레이어의 탐색 시작
    # battle_state_li.append([0.9, 1, 'search_start']) # 0.9초에 1번 플레이어의 탐색 시작
    for i in area.li_players:
        battle_state_li.append(_Battle_state(random(), i, 'search_start', is_fixed_damage=is_fixed_damage, fixed_damage=fixed_damage))
    battle_state_li = sorted(battle_state_li, key=lambda x: x.action_time)
    
    battle_state = []
    player_cnt = len(area.li_players)
    player_name = None
    while area.live_player() > 1 or len(battle_state) > 1:# or True:
        battle_state = []
        player_name = battle_state_li[0].player.name
        
        if not battle_state_li[0].player.is_live and battle_state_li[0].action!='dead':
            if print_sw: _Print(player_cnt, name_no_dict[player_name]-1, 'already dead', battle_state_li[0].action_time)
            del battle_state_li[0]
            continue
        
        if battle_state_li[0].action == 'search_start':
            # print(area.live_player(), battle_state_li[0].player.stance)
            if area.live_player() <= 2: # 1대1 상황이 되면 무조건 공격태세
                battle_state_li[0].player.change_stance('Offensive')
            # print(area.live_player(), battle_state_li[0].player.stance)
                
            battle_state = battle_state_li[0].search_start(area)
            if print_sw: _Print(player_cnt, name_no_dict[player_name]-1, battle_state_li[0].action, battle_state_li[0].action_time)
        elif battle_state_li[0].action == 'search_completion':
            if battle_state_li[0].find_li[0].category == 'player':
                battle_state = battle_state_li[0].enemy_player_found()
                if print_sw:
                    _Print(player_cnt,
                           name_no_dict[player_name]-1,
                           battle_state_li[0].find_li[0].name + ' found',
                           battle_state_li[0].action_time)
            if battle_state_li[0].find_li[0].category == None:
                if print_sw: _Print(player_cnt, name_no_dict[player_name]-1, battle_state_li[0].action, battle_state_li[0].action_time)
                
        elif battle_state_li[0].action == 'attack':
            battle_state = battle_state_li[0].attack()
            if print_sw:
                _Print(player_cnt,
                       name_no_dict[player_name]-1,
                       battle_state_li[0].action + ' ' + str(battle_state_li[0].find_li[0].name),
                       battle_state_li[0].action_time)
        elif battle_state_li[0].action == 'dead':
            name_li.append(player_name)
            if print_sw: _Print(player_cnt, name_no_dict[player_name]-1, battle_state_li[0].action, battle_state_li[0].action_time)
        elif battle_state_li[0].action == 'already_dead':
            battle_state = battle_state_li[0].already_dead()
            if print_sw: _Print(player_cnt, name_no_dict[player_name]-1, battle_state_li[0].action, battle_state_li[0].action_time)
        
        # if len(battle_state) < 1 and print_sw: print(battle_state_li[0].action)
        del battle_state_li[0]
        for v in battle_state:
            battle_state_li.append(v)
        
        battle_state_li = sorted(battle_state_li, key=lambda x: x.action_time)
        if print_sw: sleep(1)
    
    for i in area.li_players:
        if i.is_live:
            name_li.append(i.name)
            break
    
    name_li.reverse()
    return name_li
    
def _win_rate_test(area, loop_cnt,
                   is_fixed_damage = False,
                   fixed_damage = 1):
    # is_fixed_damage : 피해량을 지정해 줄 것인지 확인
    # fixed_damage : 피해량을 지정해 줄 경우 fixed_damage의 값을 고정 피해량으로 지정함 (추가 피해와는 다름)
    copy_area = None
    name_li = []
    name_dict = {}
    for i in area.li_players:
        name_dict[i.name] = 0
    
    for i in range(loop_cnt):
        copy_area = deepcopy(area)
        name_li = _Area_Battle(copy_area, False, is_fixed_damage=is_fixed_damage, fixed_damage=fixed_damage)
        
        name_dict[name_li[0]] += 1
    
    # print('%-16s\t%-10s\t%10s\t%9s' % ('player name', 'position', 'victory', 'win rate'))
    # for i in area.li_players:
        # print('%-16s\t%-10s\t%10d\t%9.5f%%' % (i.name, i.stance, name_dict[i.name], name_dict[i.name]/loop_cnt*100))
    
    print('%s,%s,%s,%s' % ('player name', 'position', 'victory', 'win rate'))
    for i in area.li_players:
        print('%s,%s,%d,%f%%' % (i.name, i.stance, name_dict[i.name], name_dict[i.name]/loop_cnt*100))
    
    return name_dict

dict_items = {}
dict_items['Brasil Gauntlet'] = _Item('Brasil Gauntlet', 'Weapon', 'Hand', 'Epic', 47, 1, [])
dict_items['Mithril Helm'] = _Item('Mithril Helm', 'Gear', 'Head', 'Epic', 45, 1, [])
dict_items["Clergy's Cassock"] = _Item("Clergy's Cassock", 'Gear', 'Clothes', 'Epic', 55, 1, [])
dict_items['Mithril Shield'] = _Item('Mithril Shield', 'Gear', 'Arm', 'Epic', 35, 1, [])
dict_items['Mithril Boots'] = _Item('Mithril Boots', 'Gear', 'Leg', 'Epic', 35, 1, [])
dict_items["Schrodinger's Box"] = _Item("Schrodinger's Box", 'Gear', 'Accessory', 'Epic', 22, 1, [])

item0 = _Item('Brasil Gauntlet', 'Weapon', 'Hand', 'Epic', 47, 1, {})
item1 = _Item('Mithril Helm', 'Gear', 'Head', 'Epic', 45, 1, {})
item2 = _Item("Clergy's Cassock", 'Gear', 'Clothes', 'Epic', 55, 1, {})
item3 = _Item('Mithril Shield', 'Gear', 'Arm', 'Epic', 35, 1, {})
item4 = _Item('Mithril Boots', 'Gear', 'Leg', 'Epic', 35, 1, {})
item5 = _Item("Schrodinger's Box", 'Gear', 'Accessory', 'Epic', 22, 1, {})
dict_equipment_state={'Weapon':item0, 'Head':item1, 'Clothes':item2, 'Arm':item3, 'Leg':item4, 'Accessory':item5}


if __name__=="__main__":
    player1 = _Player(18, 'player1', _Character(), [[_Item(), 10], None, None, None, None, None], dict_equipment_state, [], 'SS', 'Dodging')
    player2 = _Player(18, 'player2', _Character(), [[_Item(), 10], None, None, None, None, None], dict_equipment_state, [], 'SS', 'Dodging')
    player3 = _Player(18, 'player3', _Character(), [[_Item(), 10], None, None, None, None, None], dict_equipment_state, [], 'SS', 'Dodging')
    player4 = _Player(18, 'player4', _Character(), [[_Item(), 10], None, None, None, None, None], dict_equipment_state, [], 'SS', 'Dodging')
    player5 = _Player(18, 'player5', _Character(), [[_Item(), 10], None, None, None, None, None], dict_equipment_state, [], 'SS', 'Dodging')
    li_players = [player1, player2, player3]#, player4, player5]
    
    area = _Area('지하 통로', li_players, [])
    loop_cnt = 10000
        
    file_name = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S') + '.txt'
    #print(file_name)
    
    for i in li_players:
        print(i.name, i.stance)
    print('loop_cnt :', loop_cnt)
    
    # for i in range(200, 0, -1):#(1, 101):
        # fixed_damage = 222.01 / i
        # print('------------------------------------------------------')
        # print('고정 피해량 :', fixed_damage)
        # print(222/fixed_damage, i)
        #
        # if not 0 < i - 222/fixed_damage < 1: break
    # exit()
    
    loop_strat_clock = clock()
    # for i in range(5, 231, 5):
    for i in range(200, 0, -1):#(1, 101):
        fixed_damage = 222.01 / i
        print('------------------------------------------------------')
        print('고정 피해량 :', fixed_damage)
        print(222/fixed_damage, i)
        t1 = clock()
        name_dict = _win_rate_test(area, loop_cnt, is_fixed_damage=True, fixed_damage=fixed_damage)
        print(name_dict, clock()-t1)
        
        f = open(file_name, 'a', encoding='utf-8')
        f.write('%d' % i)
        for k, v in name_dict.items():
            print(k, v)
            f.write(',%d' % v)
        f.write('\n')
        f.close()
    
    print(clock()-loop_strat_clock)
    win_count_df = pd.read_csv(file_name, encoding='utf-8',
                               names=['fixed_damage', 'player1(%s)' % player1.stance, 'player2(%s)' % player2.stance, 'player3(%s)' % player3.stance])
    print(win_count_df)
    print((win_count_df['fixed_damage'].astype(str)).tolist())
    # print(win_count_df[['player1', 'player2', 'player3']])
    
    sns.lineplot(data=win_count_df[['player1(%s)' % player1.stance, 'player2(%s)' % player2.stance, 'player3(%s)' % player3.stance]])
    #ax=plt.axes()
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # plt.xticks(win_count_df['player3'], ['5d', '10d', '15d', '20d', '25d', '30d', '35d', '40d', '45d', '50d', '55d', '60d', '65d', '70d', '75d', '80d', '85d', '90d', '95d', '100d', '105d', '110d', '115d', '120d', '125d', '130d', '135d', '140d', '145d', '150d', '155d', '160d', '165d', '170d', '175d', '180d', '185d', '190d', '195d', '200d', '205d', '210d', '215d', '220d', '225d', '230d'])
    # plt.xticks(win_count_df['player1'], (win_count_df['fixed_damage'].astype(str) + 'd').tolist(), rotation=90)
    plt.xlabel('x+1대 맞으면 사망')
    plt.ylabel('승리 횟수')
    plt.show()
    
    # name_dict = _win_rate_test(area, loop_cnt)
    # player1.player_info()
    # player2.player_info()
    # player3.player_info()
    # player4.player_info()
