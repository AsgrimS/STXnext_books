# STXnext_books
Recruitment task for STXnext

Application downloads books to the local PostgreSQL database, and creates api based on it. Each time `python manage.py update_database` is used or POST with required body is sent, database is reviewed and updated.

To update database run `python manage.py update_database`

List of books is under `http://127.0.0.1:8000/api/books/`<br>

You can sort them with query params like: 
  `http://127.0.0.1:8000/api/books/?published_date=2020`<br>
  `http://127.0.0.1:8000/api/books/?sort=published_date`<br>
  `http://127.0.0.1:8000/api/books/?sort=-published_date`<br>
  `http://127.0.0.1:8000/api/books/?author=J. R. R. Tolkien`<br>
  You can also combine params with '&' e.g. `?published_date=2020&sort=published_date`<br>
  
To add new books make a POST to `http://127.0.0.1:8000/api/db` with body `{"q":"<e.g. war>"}`<br>
To see progress bars in the console during POST, you have to change `loggin` value in `views.py` to `True`

To run tests simply enter `pytest` in the terminal
  
Don't forget to start database with `docker-compose up -d`


