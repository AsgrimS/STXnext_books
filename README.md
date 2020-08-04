# STXnext_books
Recruitment task for STXnext

To update database run `python manage.py update_database`

List of books is under `http://127.0.0.1:8000/api/books/`
You can sort them with query params like: 
  `http://127.0.0.1:8000/api/books/?published_date=2020`
  `http://127.0.0.1:8000/api/books/?sort=published_date`  
  `http://127.0.0.1:8000/api/books/?sort=-published_date`
  `http://127.0.0.1:8000/api/books/?author=J. R. R. Tolkien`
  
To add new books make a POST to `http://127.0.0.1:8000/api/db` with body `{"q":"war"}`
  
Dont forget to start database with `docker-compose up -d`
