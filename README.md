pip install fastapi sqlalchemy alembic psycopg2-binary passlib[bcrypt]

pip install python-dotenv

pip install jwt

pip install uvicorn

pip install mysqlclient

pip install -r requirements.txt

python -m config.createtables

python -m uvicorn main:app --reload

