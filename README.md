# Koi_Bot_Discord
This is a respository for Koi_Bot running on discord with python. (Koi_Bot#4999)

This project uses `Pycord` python module.
* This project is using Pycord's Development Version. Try to install pycord's Development version by using this command.

```sh
$ git clone https://github.com/Pycord-Development/pycord
$ cd pycord
$ python3 -m pip install -U .[voice]
```

This project was created out of a personal need.
* LaptopManagement.py is written assuming that the code runs with the laptop as the server.
* Tools.py, Utils/login_utils.py are written assuming that the user attends a specific school in Korea.

If it does not apply, you can remove it.
* Python module `psutil` is only used at LaptopManagement.py.
* Python module `pytz`, `python-dateutil`, `selenium`, `pyautogui` are only used at Tools.py and login_utils.py.


This respository was created by referring to the following respository.
* Setabot Framework : https://github.com/Kimu-Nowchira/SetaBot.
* Used at Logger.py, Permission.py, SetaSQLiteClass.py, UserClass.py at Utils folder.
