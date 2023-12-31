from typing import Union, Optional
import discord
from Utils.SetaSQLiteClass import SetaSQLiteClass as Seta_sqlite

# Initializing the SQLite database
db = Seta_sqlite('Data/User_DB/user.db')

# Custom exception for a non-existent user in the database
class NotExistUser(Exception):
    def __init__(self):
        super().__init__('데이터 내에 존재하지 않는 유저입니다')

class UserClass:
    # Initialization of user-related attributes
    user: Optional[discord.User] = None
    id: int = 0
    name: str = '알 수 없는 유저'
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
            self.load()  # Loading user data from the database
        except NotExistUser:
            self.name = self.realname if self.realname is not None else self.name
            # Inserting user data into the database if it doesn't exist
            db.insert_sql('users', 'id, name', f"{self.id}, '{self.name}'")
            self.load()  # Loading user data after insertion

        if self.realname is not None:
            if self.realname != self.name:
                db.update_sql('users', f"name='{self.name}'", f"id={self.id}")
            self.name = self.realname  # Updating user name if it's different

    def load(self):
        '''Loads user data from the database'''
        data = self._load_data()
        if data == []:
            raise NotExistUser

        data = data[0]
        self.name = str(data[0])
        self._exp = int(data[1])
        self._permission = int(data[2])
        return data

    def _load_data(self):
        return db.select_sql('users', 'name, exp, permission', f'WHERE id={self.id}')

    # Getter and setter for user experience
    @property
    def exp(self):
        '''User's experience points'''
        return db.select_sql('users', 'exp', f'WHERE id={self.id}')[0][0]

    @exp.setter
    def exp(self, value: int):
        db.update_sql('users', f'exp={int(value)}', f'WHERE id={self.id}')
        self._exp = int(value)

    # Method to add experience points
    def add_exp(self, value: int):
        '''Adds experience points to the user'''
        db.update_sql('users', f'exp=exp+{int(value)}', f'WHERE id={self.id}')
        self._exp += int(value)

    # Getter for user level based on experience points
    @property
    def level(self):
        '''User's level calculated from experience points'''
        if self.exp < 0:
            return 0
        else:
            return int(((self.exp/5)+(1/4))**0.5 + 0.5)

    # Getter and setter for user permission level
    @property
    def permission(self):
        '''User's permission level'''
        return db.select_sql('users', 'permission', f'WHERE id={self.id}')[0][0]

    @permission.setter
    def permission(self, value: int):
        db.update_sql('users', f'permission={int(value)}', f'WHERE id={self.id}')
        self._permission = int(value)
