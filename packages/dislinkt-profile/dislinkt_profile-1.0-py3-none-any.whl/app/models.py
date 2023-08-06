from sqlalchemy import Table, Boolean, Column, ForeignKey, Numeric, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    ime = Column(String)
    prezime = Column(String)
    telefon = Column(String)
    datumRodjenja = Column(Date)
    pol = Column(String)
    role = Column(String(25), nullable=False)
    profile = relationship("Profile", back_populates="user", uselist=False)
    # posts = relationship("Post", back_populates="author")
    # reactions = relationship("Reaction", back_populates="author")


association_table = Table(
    "association",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("profiles.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("profiles.id"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer(), primary_key=True)
    picture = Column(String(80))
    description = Column(String())
    private = Column(Boolean())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    following = relationship("Profile",
                             secondary=association_table,
                             primaryjoin=id==association_table.c.follower_id,
                             secondaryjoin=id==association_table.c.following_id,
                             backref="follower")

    # following koga on prati, follower ko njega prati
    education = relationship("Education", back_populates="profile")



class Education(Base):
    __tablename__ = "education"
    id = Column(Integer(), primary_key=True)
    school = Column(String)
    degree = Column(String)
    start = Column(Date)
    end = Column(Date)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="education")


