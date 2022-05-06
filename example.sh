#!/bin/bash

# echo -e 'Récuperation du token (http POST 127.0.0.1:80/api/token-auth/ username=xxx password=xxx)'
# http POST 127.0.0.1:80/api/token-auth/ username=test password=Test-eip59

# echo -e 'Création utilisateur (http POST 127.0.0.1:80/api/users/ Authorization: Token xxx username=xxx password=xxx email=xxx@hotmail.fr)'
# http POST 127.0.0.1:80/api/users/ 'Authorization: Token 7669979ed6df9c64805d3c3755b3d079f4a745e9' username=test password=Test-eip59 email=test@hotmail.fr
# http GET 127.0.0.1:80/api/users/ 'Authorization: Token 7669979ed6df9c64805d3c3755b3d079f4a745e9'

http POST 127.0.0.1:80/api/users_data/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' level=25000 gold=12 gem=16
http GET 127.0.0.1:80/api/users_data/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'

http POST 127.0.0.1:80/api/users_skills/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' cap_1=Fire cap_2=Lightning cap_3=Earth cap_4=Water
http GET 127.0.0.1:80/api/users_skills/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'

http POST 127.0.0.1:80/api/users_position/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' map=Oasis x=34.3 y=78.6 z=-129.4
http GET 127.0.0.1:80/api/users_position/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'

http POST 127.0.0.1:80/api/users_inventory/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' item=3 number=42
http GET 127.0.0.1:80/api/users_inventory/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'

http POST 127.0.0.1:80/api/users_friends/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' name=Roger
http POST 127.0.0.1:80/api/users_friends/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' name=Mattieu
http GET 127.0.0.1:80/api/users_friends/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'

http POST 127.0.0.1:80/api/users_guild/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857' name=FrenchSoftW3re
http GET 127.0.0.1:80/api/users_guild/ 'Authorization: Token e991f3680da04cdfe1951892bdb3a02d0baee857'


# echo -e 'Unit test avec coverage (pas tres fiable)'
# coverage run --source='.' manage.py test ether && coverage report