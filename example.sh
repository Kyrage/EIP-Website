#!/bin/bash

#echo -e 'Récuperation du token (http POST 127.0.0.1:80/api/token-auth/ username=xxx password=xxx)'
http POST 127.0.0.1:80/api/token-auth/ username=admin password=admin

#echo -e 'Création utilisateur (http POST 127.0.0.1:80/api/users/ Authorization: Token xxx username=xxx password=xxx email=xxx@hotmail.fr)'
http POST 127.0.0.1:80/api/users/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' username=test-eip password=Test-eip59 email=test@hotmail.fr
http GET 127.0.0.1:80/api/users/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_data/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' level=25 gold=1243 gem=15
http GET 127.0.0.1:80/api/users_data/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_skills/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' cap_1=Fire cap_2=Lightning cap_3=Earth cap_4=Water
http GET 127.0.0.1:80/api/users_skills/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_position/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' map=Oasis x=34.3 y=78.6 z=-129.4
http GET 127.0.0.1:80/api/users_position/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_inventory/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' item=3 number=42
http GET 127.0.0.1:80/api/users_inventory/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_friends/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' name=Roger
http POST 127.0.0.1:80/api/users_friends/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' name=Mattieu
http GET 127.0.0.1:80/api/users_friends/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'

http POST 127.0.0.1:80/api/users_guild/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18' name=FrenchSoftW3re
http GET 127.0.0.1:80/api/users_guild/ 'Authorization: Token 957f29ce186aef6a89c7e0e585689e7dc20f0f18'


#echo -e 'Unit test avec coverage (pas tres fiable)'
#coverage run --source='.' manage.py test ether && coverage report