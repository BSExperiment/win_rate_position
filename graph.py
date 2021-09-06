# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import seaborn as sns
import BS_Experiment_main as bem
import numpy as np

fontFile = 'C:/Windows/Fonts/malgun.ttf'
fontName = fm.FontProperties(fname=fontFile, size=50).get_name()
plt.rc('font', family=fontName)

file_name = '20210906-170220.txt'
file_name = '20210906-170250.txt'
# file_name = '20210906-170259.txt'
# file_name = '20210906-170310.txt'

player1 = bem._Player(18, 'player1', bem._Character(), [[bem._Item(), 10], None, None, None, None, None], bem.dict_equipment_state, [], 'SS')#, 'Dodging')
player2 = bem._Player(18, 'player2', bem._Character(), [[bem._Item(), 10], None, None, None, None, None], bem.dict_equipment_state, [], 'SS')#, 'Dodging')
player3 = bem._Player(18, 'player3', bem._Character(), [[bem._Item(), 10], None, None, None, None, None], bem.dict_equipment_state, [], 'SS', 'Dodging')
    

win_count_df = pd.read_csv(file_name, encoding='utf-8',
                               names=['fixed_damage', 'player1(%s)' % player1.stance, 'player2(%s)' % player2.stance, 'player3(%s)' % player3.stance])
print(win_count_df)
win_count_df = win_count_df.sort_values(by=['fixed_damage'], ascending=True)
print(win_count_df)
print((win_count_df['fixed_damage'].astype(str)).tolist())
# print(win_count_df[['player1', 'player2', 'player3']])

sns.lineplot(data=win_count_df[['player1(%s)' % player1.stance, 'player2(%s)' % player2.stance, 'player3(%s)' % player3.stance]])
#ax=plt.axes()
#ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
# plt.xticks(win_count_df['player3'], ['5d', '10d', '15d', '20d', '25d', '30d', '35d', '40d', '45d', '50d', '55d', '60d', '65d', '70d', '75d', '80d', '85d', '90d', '95d', '100d', '105d', '110d', '115d', '120d', '125d', '130d', '135d', '140d', '145d', '150d', '155d', '160d', '165d', '170d', '175d', '180d', '185d', '190d', '195d', '200d', '205d', '210d', '215d', '220d', '225d', '230d'])
# plt.xticks(win_count_df['player1'], (win_count_df['fixed_damage'].astype(str) + 'd').tolist(), rotation=90)

plt.xticks(np.arange(200, 1, -10))
plt.yticks(np.arange(0, 10000, 1000))

plt.xlabel('200 - max_hp / damage')
plt.ylabel('victory')
plt.show()