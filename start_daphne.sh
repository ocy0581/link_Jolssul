
cd django/mysite
daphne -e ssl:8001:privateKey=private.key:certKey=private.crt mysite.asgi:application