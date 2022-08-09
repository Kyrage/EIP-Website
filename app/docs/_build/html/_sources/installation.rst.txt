Presentation of the project
===========================

Project Ether is a mobile video game of dungeon management and exploration.
You play as a character with supernatural abilities and you must create dungeons
as well as explore those of other players or those created by the developers.
All this in a fantasy world.

Technology
**********

The technology used are docker-composer to virtualize the project and
framework python django with azure for hosting.


Installating
************

Requirements:
--------------------------

You need for this project to have docker-composer installed on your machine::

    install docker-compose

.. note:: install depends of your package manager.


Project Execution
-----------------

At the root of the repository to launch the project::

    docker-compose build && docker-compose up

    Or

    docker-compose up --build

In the dashboard folder to launch the units tests::

    ./manage.py test

Enjoy yourself!