#Originated from Kimu-Nowchira's Setabot Framework
#Edited by AKMU_LOVE#4211(KOI#4182)

from typing import Union, Optional

import discord

from Utils.SetaSQLiteClass import SetaSQLiteClass as Seta_sqlite

db = Seta_sqlite('Data/User_DB/user.db') 


class UserClass:
    #Identification information
    user: Optional[discord.User] = None 
    id: int = 0  # User's ID
    name: str = '알 수 없는 유저'  #User's nickname

    #Do not edit variables with '+=', '-=', etc (This approach does not apply to SQL)
    _permission: int = 0
    _exp: int = 0 

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
        self._exp = int(data[1])
        self._permission = int(data[2])
        return data

    def _load_data(self):
        return db.select_sql(
            'users',
            'name, exp, permission',
            f'WHERE id={self.id}'
            )

# --------- Getter/Setter --------- #
    @property
    def exp(self):
        '''int : 유저의 경험치'''
        return db.select_sql('users', 'exp', f'WHERE id={self.id}')[0][0]

    @exp.setter
    def exp(self, value: int):
        db.update_sql('users', f'exp={int(value)}', f'WHERE id={self.id}')
        self._exp = int(value)

    def add_exp(self, value: int):
        '''유저의 경험치를 value 만큼 더합니다. 유저의 경험치를 늘리거나 줄일 때 이 함수의 사용을 권장합니다.'''
        db.update_sql('users', f'exp=exp+{int(value)}', f'WHERE id={self.id}')
        self._exp += int(value)

    @property
    def level(self):
        '''int : 유저의 레벨'''
        if self.exp < 0:
            return 0
        else:
            return int(((self.exp/5)+(1/4))**0.5 + 0.5)

    @property
    def permission(self):
        '''int : 유저의 권한'''
        return db.select_sql('users', 'permission', f'WHERE id={self.id}')[0][0]

    @permission.setter
    def permission(self, value: int):
        db.update_sql('users', f'permission={int(value)}', f'WHERE id={self.id}')
        self._permission = int(value)


class NotExistUser(Exception):
    def __init__(self):
        super().__init__('데이터 내에 존재하지 않는 유저입니다')