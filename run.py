from project import app, db, bcrypt
from project.models import User

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if len(db.session.execute(db.select(User)).scalars().all()) == 0:
            admin = User(username='admin', email='admin@mail.ru', password=bcrypt.generate_password_hash(input('Enter admin password: ')))
            db.session.add(admin)
            db.session.commit()

    app.run()