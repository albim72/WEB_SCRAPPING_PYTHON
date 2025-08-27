import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, sessionmaker



# --- 2) Właściwy engine do bazy z driverem PyMySQL ---
engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:abc123@localhost:3306/{DB_NAME}?charset=utf8mb4",
    echo=True,
    future=True,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=50))
    fullname = sqlalchemy.Column(sqlalchemy.String(length=50))
    nickname = sqlalchemy.Column(sqlalchemy.String(length=50))

    def __repr__(self):
        return f"<User -> name: {self.name}, fullname: {self.fullname}, nickname: {self.nickname}>"

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine, future=True)
session = Session()

session.add_all([
    User(name="Marcin", fullname="Marcin Albiniak", nickname="norman"),
    User(name="Ola", fullname="Ola Krzak", nickname="olka"),
    User(name="Ola", fullname="Ola Nowak", nickname="olka"),
    User(name="Leon", fullname="Leon Zawodowiec", nickname="leos"),
])
session.commit()

print("_" * 50)
for s in session.query(User).all():
    print(s)

print("_" * 50)
for s in session.query(User).filter(User.nickname == "olka"):
    print(s.fullname)
