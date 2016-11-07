cd Table
python develop_table.py

cd ../Web
nohup gunicorn -c gunicorn.conf msg_web:msg_web 1>>msg_web.log 2>>msg_web.log &
