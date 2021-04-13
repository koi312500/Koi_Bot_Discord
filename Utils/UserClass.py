'''
<User 클래스>
- user를 통해 객체를 생성합니다.
- user = User(author)처럼 사용합니다.
- user = User(id)로도 쓸 수 있지만 기능이 제한됩니다.
'''
from typing import Union, Optional

import discord

from Utils.SetaSQLiteClass import SetaSQLiteClass as Seta_sqlite
from Utils import LevelDesign

db = Seta_sqlite('Data/User_DB/user.db') 


class UserClass:
    # 기본 정보 #
    user: Optional[discord.User] = None  # 디스코드의 유저 객체
    id: int = 0  # 유저 아이디
    name: str = '알 수 없는 유저'  # 유저 이름

    # 게임용 변수 # (user.money += 4 같이 값을 직접 바꾸는 사용은 절대 금지! 함수를 쓰세요!)
    _money: int = 0  # 보유한 돈
    _exp: int = 0  # 경험치 (레벨은 경험치에 따라 자동 조정되며, 공격, 방어 등의 스탯은 레벨에 따라 자동 조정 됩니다.)
    items: list = []  # 아이템 목록

    realname: Optional[str] = None

    def __init__(self, user: Union[discord.User, int]):
        if isinstance(user, int):
            self.id = user
        else:
            self.user = user
            self.id = user.id
            self.realname = user.name.replace("'", '').replace("\"", '')

        try:
            self.load()
        except NotExistUser:
            self.name = self.realname if self.realname is not None else self.name
            db.insert_sql(
                'users', 'id, name',
                f"{self.id}, '{self.name}'"
                )
            self.load()

        if self.realname is not None:
            if self.realname != self.name:
                db.update_sql('users', f"name='{self.name}'", f"id={self.id}")
            self.name = self.realname

    def load(self):
        '''데이터에서 값을 다시 불러옵니다'''
        data = self._load_data()
        if data == []:
            raise NotExistUser

        data = data[0]
        self.name = str(data[0])
        self._money = int(data[1])
        self._exp = int(data[2])
        return data

    def _load_data(self):
        return db.select_sql(
            'users',
            'name, money, exp',
            f'WHERE id={self.id}'
            )

# --------- Getter/Setter --------- #

    @property
    def money(self):
        '''int: 유저의 돈'''
        return db.select_sql('users', 'money', f'WHERE id={self.id}')[0][0]

    @money.setter
    def money(self, value: int):
        db.update_sql('users', f'money={int(value)}', f'WHERE id={self.id}')
        self._money = int(value)

    def add_money(self, value: int):
        '''유저의 돈을 value 만큼 더합니다. 유저의 돈을 늘리거나 줄일 때 add_money의 사용을 권장합니다.'''
        db.update_sql('users', f'money=money+{int(value)}', f'WHERE id={self.id}')
        self._money += int(value)

    @property
    def exp(self):
        '''int: 유저의 경험치'''
        return db.select_sql('users', 'exp', f'WHERE id={self.id}')[0][0]

    @exp.setter
    def exp(self, value: int):
        db.update_sql('users', f'exp={int(value)}', f'WHERE id={self.id}')
        self._exp = int(value)

    def add_exp(self, value: int):
        '''유저의 경험치를 value 만큼 더합니다. 유저의 경험치를 늘리거나 줄일 때 이 함수의 사용을 권장합니다.'''
        db.update_sql('users', f'exp=exp+{int(value)}', f'WHERE id={self.id}')
        self._exp += int(value)

# --------- 스테이터스 관련 --------- #

    @property
    def level(self):
        '''int: 유저의 레벨'''
        return LevelDesign.exp_to_level(self.exp)

class NotExistUser(Exception):
    def __init__(self):
        super().__init__('데이터 내에 존재하지 않는 유저입니다')