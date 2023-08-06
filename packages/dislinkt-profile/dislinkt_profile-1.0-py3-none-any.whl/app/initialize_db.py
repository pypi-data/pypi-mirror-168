from sqlalchemy.sql import text
from database import engine

with engine.connect() as con:
    profiles = ({"id": 1, "picture": "sunce.jpg", "description": "opis profila", "private": 0, "user_id": 1},
                {"id": 2, "picture": "sunce.jpg", "description": "opis profila 2", "private": 0, "user_id": 2},
             )

    statement_profiles = text("""INSERT INTO profiles(id, picture, description, private, user_id)
     VALUES(:id, :picture, :description, :private, :user_id)""")

    followers = ({"follower_id": 1, "following_id": 2},
                 {"follower_id": 2, "following_id": 1},
                )

    statement_followers = text("""INSERT INTO association(follower_id, following_id)
         VALUES(:follower_id, :following_id)""")

    for line in profiles:
        con.execute(statement_profiles, **line)

    for line in followers:
        con.execute(statement_followers, **line)

    # for line in users:
        #  con.execute(statement, **line) korisnici su dodati rucno
