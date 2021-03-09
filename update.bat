timeout /t 20 
git pull origin master 
rm output.out
python Main.py > output.out &