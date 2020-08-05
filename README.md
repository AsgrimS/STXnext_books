# STXnext_books
Recruitment task for STXnext

Application downloads books to the local PostgreSQL database, and creates api based on it. Each time `python manage.py update_database` is used or POST with required body is sent, database is reviewed and updated.

To update database run `python manage.py update_database`

List of books is under `http://127.0.0.1:8000/books`<br>

You can sort them with query params like: 
  `http://127.0.0.1:8000/books?published_date=2020`<br>
  `http://127.0.0.1:8000/books?sort=published_date`<br>
  `http://127.0.0.1:8000/books?sort=-published_date`<br>
  `http://127.0.0.1:8000/books?author=J. R. R. Tolkien`<br>
  You can also combine params with '&' e.g. `?published_date=2020&sort=published_date`<br>
  
To add new books make a POST to `http://127.0.0.1:8000/db` with body `{"q":"<e.g. war>"}`<br>
To see progress bars in the console during POST, you have to change `loggin` value in `views.py` to `True`


In case of local dev don't forget to start database with `docker-compose up -d` and comment out: <br>
`DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)`<br>

To run tests simply enter `pytest` in the terminal
