echo 'installing virtualenv'
python3 -m pip install virtualenv

echo 'creating virtual environment'
python3 -m virtualenv venv

echo 'installing requirements'
./venv/bin/python3 -m pip install -r requirements_linux.txt

echo 'running command'
nohup ./venv/bin/python3  main.py >nohupLog 2>&1 &
echo 'see details in nohupLog'
