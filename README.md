# Koi_Bot_Discord

This is a respository for Koi_Bot running on discord with python. (Koi_Bot#4999)

This project was created out of a personal need.

-   LaptopManagement.py is written assuming that the code runs with the laptop as the server, optimized for specific computers.

If it does not apply, you can remove it.

This respository was created by referring to the following respository.

-   Setabot Framework : https://github.com/Kimu-Nowchira/SetaBot.
-   Used at Logger.py, Permission.py, SetaSQLiteClass.py, UserClass.py at Utils folder.

## How to run

1. Install Chrome to run `Tools.py`
    - Please install according to the execution environment.
2. Install python libraries to execute files.
    - Execute `requirements.bat` to install all libraries for Windows environment.
    - If you needed, you can use `pip install -r requirements.txt` for library installation.
3. Edit `config.py` and `key.py` to suit your environment.
4. If your execution environment is non-display? (Such as docker)
    - Install xvfb to make virtual display (for `pyautogui`)
    - Replace `python Main.py` in run.sh and run.bat to `xvfb-run python Main.py`.
5. Execute `run.sh` or `run.bat` to execute `Main.py`

## To-Do

<details>
<summary> To-Do List </summary>

-   [ ] debug_options() error resolve
-   [ ] Optimize some codes
-   [ ] Add some function related with SQL

</details>
