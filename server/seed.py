from app import app
from extensions import db, bcrypt
from models import User, Note
from faker import Faker

fake = Faker()


def seed_data():
    with app.app_context():
        try:
            # Create sample users
            for number in range(1, 6):
                username = f"demo_user{number}"

                user = User.query.filter_by(
                    username=username
                ).first()

                if not user:
                    password_hash = bcrypt.generate_password_hash(
                        "Password123!"
                    ).decode("utf-8")

                    user = User(
                        username=username,
                        password_hash=password_hash
                    )

                    db.session.add(user)
                    db.session.flush()

                # Create sample notes if the user has none
                if not user.notes:
                    for _ in range(3):
                        note = Note(
                            title=fake.sentence(nb_words=4),
                            content=fake.paragraph(),
                            user_id=user.id
                        )

                        db.session.add(note)

            db.session.commit()

            print("Database seeded successfully!")
            print("Created or verified 5 demo users.")
            print("Each demo user has 3 sample notes.")

        except Exception as error:
            db.session.rollback()
            print(f"Seeding failed: {error}")
            raise


if __name__ == "__main__":
    seed_data()