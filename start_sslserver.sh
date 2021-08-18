conda deactivate
source ~/link_venv/15th_venv/bin/activate
cd django/mysite
python3 manage.py runsslserver 192.168.0.15:8000  --certificate private.crt --key private.key
