# schaermu-ch [![Build Status](https://travis-ci.org/schaermu/schaermu-ch.svg?branch=master)](https://travis-ci.org/schaermu/schaermu-ch) [![Coverage Status](https://coveralls.io/repos/github/schaermu/schaermu-ch/badge.svg?branch=master)](https://coveralls.io/github/schaermu/schaermu-ch?branch=master)
My wagtail-based personal website. Awesome.
## Setup
1. Clone repository
2. Create new virtualenv (make sure it's running python 3.x)
3. brew install postgres
4. brew services start postgres
5. pip install -r requirements.txt
6. createuser -s postgres
7. createdb schaermu_ch
8. ./manage.py migrate
9. ./manage.py loaddata export.json
10. ./manage.py runserver
11. Browse http://localhost:8000/
