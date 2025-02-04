# delete_all_todos.py
from app import app, db, Todo

def delete_all_todos():
    with app.app_context():
        # Delete all rows in the Todo table
        db.session.query(Todo).delete()
        db.session.commit()
        print("All rows have been deleted from the Todo table.")

if __name__ == "__main__":
    delete_all_todos()
