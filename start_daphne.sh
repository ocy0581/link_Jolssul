conda deactivate
source ~/link_venv/15th_venv/bin/activate
cd django/mysite
daphne -e ssl:8001:privateKey=private.key:certKey=private.crt mysite.asgi:application