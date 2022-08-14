Presentation of API Root
===========================

{
    "users": "http://projectether.francecentral.cloudapp.azure.com/auth/users/",
    "users_data": "http://projectether.francecentral.cloudapp.azure.com/api/users_data/",
    "users_skills": "http://projectether.francecentral.cloudapp.azure.com/api/users_skills/",
    "users_inventory": "http://projectether.francecentral.cloudapp.azure.com/api/users_inventory/",
    "users_friends": "http://projectether.francecentral.cloudapp.azure.com/api/users_friends/",
    "game/users_texture": "http://projectether.francecentral.cloudapp.azure.com/api/game/users_texture/",
    "shop/textures": "http://projectether.francecentral.cloudapp.azure.com/api/shop/textures/"
}

"users": "http://projectether.francecentral.cloudapp.azure.com/auth/users/":
--------------------------

Get::

    returns a list of all users

Post::

    takes the arguments
    {
        "email": "",
        "username": "",
        "password": ""
    }
    and create user

"users_data": "http://projectether.francecentral.cloudapp.azure.com/api/users_data/":
--------------------------

Get::

    returns the information of the player thanks to the identification of the user by his token

Post::

    takes the arguments
    {
        "level": null,
        "crystal": null,
        "cash": null,
        "mentoring": null,
        "textureSlot": null,
        "maxTextureSlot": null,
        "hasDoneTutorial": false
    }
    and update data

"users_skills": "http://projectether.francecentral.cloudapp.azure.com/api/users_skills/":
--------------------------

Get::

    returns a list of capabilities accessible by the user thanks to the identification of the user by his token

Post::

    takes the arguments
    {
        "_id": null,
        "_parentId": null,
        "name": "",
        "level": null,
        "equipped": null
    }
    and update data

"users_inventory": "http://projectether.francecentral.cloudapp.azure.com/api/users_inventory/":
--------------------------

Get::

    return a list of items in the inventory thanks to the identification of the user by his token

Post::

    takes the arguments
    {
        "_id": null,
        "name": "",
        "quantity": null,
        "comment": ""
    }
    and update data

"users_friends": "http://projectether.francecentral.cloudapp.azure.com/api/users_friends/":
--------------------------

Get::

    returns a list of friends thanks to the identification of the user by his token

Post::

    ....

"game/users_texture": "http://projectether.francecentral.cloudapp.azure.com/api/game/users_texture/":
--------------------------

Get::

    returns a list of all textures thanks to the identification of the user by his token

Post::

    takes the arguments
    {
        "texture": null
    }
    and update data

"shop/textures": "http://projectether.francecentral.cloudapp.azure.com/api/shop/textures/":
--------------------------

Get::

    returns a list of all the textures on sale

Post::

    takes the arguments
    {
        "texture": null,
        "price": null
    }
    and create a sale