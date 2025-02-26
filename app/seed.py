import json
from typing import List, TypedDict

from fastapi_users.password import PasswordHelper
from sqlmodel import Session, SQLModel, text

from app.database import engine
from app.models.attempt import Attempt  # noqa: F401
from app.models.basic_lesson import BasicLesson  # noqa: F401
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt  # noqa: F401
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink  # noqa: F401
from app.models.leaderboard_user_link import LeaderboardUserLink, League  # noqa: F401
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.recap_lesson import RecapLesson  # noqa: F401
from app.models.recording import Recording  # noqa: F401
from app.models.unit import Unit
from app.models.user import User
from app.models.word import Word
from app.models.word_of_day import WordOfDay
from app.models.word_of_day_attempt import WordOfDayAttempt  # noqa: F401
from app.models.word_phoneme_link import WordPhonemeLink
from app.redis import LRedis


password_helper = PasswordHelper()

with open("app/resources/phoneme_respellings.json") as f:
    ipa_to_respelling = json.load(f)


class WordEntry(TypedDict):
    word: str
    phonemes: List[str]


word_data = json.load(open("app/resources/word_data.json"))


def seed(session: Session) -> None:
    print("👤 Inserting Users...")
    users = [
        User(email="john.doe@example.com", hashed_password=password_helper.hash("password")),
        User(email="emma.smith@example.com", hashed_password=password_helper.hash("password")),
        User(email="liam.johnson@example.com", hashed_password=password_helper.hash("password")),
        User(email="olivia.brown@example.com", hashed_password=password_helper.hash("password")),
        User(email="noah.williams@example.com", hashed_password=password_helper.hash("password")),
        User(email="ava.jones@example.com", hashed_password=password_helper.hash("password")),
        User(email="sophia.miller@example.com", hashed_password=password_helper.hash("password")),
        User(email="mason.davis@example.com", hashed_password=password_helper.hash("password")),
        User(email="isabella.garcia@example.com", hashed_password=password_helper.hash("password")),
        User(email="logan.martinez@example.com", hashed_password=password_helper.hash("password")),
        User(email="lucas.anderson@example.com", hashed_password=password_helper.hash("password")),
        User(email="mia.thomas@example.com", hashed_password=password_helper.hash("password")),
        User(email="harper.taylor@example.com", hashed_password=password_helper.hash("password")),
        User(email="elijah.moore@example.com", hashed_password=password_helper.hash("password")),
        User(email="amelia.white@example.com", hashed_password=password_helper.hash("password")),
        User(email="james.harris@example.com", hashed_password=password_helper.hash("password")),
        User(email="charlotte.clark@example.com", hashed_password=password_helper.hash("password")),
        User(email="benjamin.lewis@example.com", hashed_password=password_helper.hash("password")),
        User(email="henry.walker@example.com", hashed_password=password_helper.hash("password")),
        User(email="evelyn.hall@example.com", hashed_password=password_helper.hash("password")),
    ]
    session.add_all(users)
    session.commit()

    print("🏆 Inserting Leaderboard...")
    xps = [1200, 1650, 3280, 4090, 4650, 6400, 7250, 8630, 9480, 9610] * 2
    leagues = [League.BRONZE] * 10 + [League.SILVER] * 10
    leaderboard_users = [
        LeaderboardUserLink(user_id=user.id, xp=xp, league=league) for user, xp, league in zip(users, xps, leagues)
    ]
    session.add_all(leaderboard_users)
    session.commit()
    LRedis.clear()
    LRedis.create_entries_from_users(League.BRONZE, leaderboard_users[:10])
    LRedis.create_entries_from_users(League.SILVER, leaderboard_users[10:])

    print("📝 Inserting Words...")
    words = {w["word"]: Word(text=w["word"]) for w in word_data}
    session.add_all(words.values())
    session.commit()

    print("🔤 Inserting Phonemes...")
    phonemes = {ipa: Phoneme(ipa=ipa, respelling=respelling) for ipa, respelling in ipa_to_respelling.items()}
    session.add_all(phonemes.values())
    session.commit()

    print("🔗 Linking Words and Phonemes...")

    word_phoneme_links = []
    for word_entry in word_data:
        word_obj = words[word_entry["word"]]
        for index, ipa in enumerate(word_entry["phonemes"]):
            # This is helpful incase when we add new words, we don't have the
            # phoneme in the database and need to add them
            try:
                word_phoneme_links.append(
                    WordPhonemeLink(word_id=word_obj.id, phoneme_id=phonemes[ipa].id, index=index)
                )
            except Exception as e:
                print(f"Error, when inserting {ipa} for {word_obj}: {e}")
    session.add_all(word_phoneme_links)
    session.commit()

    print("📅 Inserting Word of the Day...")
    word = words["software"]
    word_of_day = WordOfDay(word_id=word.id)
    word.word_of_day_last_used = word_of_day.date
    session.add(word_of_day)
    session.commit()

    print("📚 Inserting Units with Lessons...")
    lessons = [
        Lesson(title="Listening Discrimination Pairs", exercises=[
            Exercise(index=0, word_id=words["cat"].id),
            Exercise(index=1, word_id=words["cut"].id),
            Exercise(index=2, word_id=words["hat"].id),
            Exercise(index=3, word_id=words["hut"].id),
            Exercise(index=4, word_id=words["bat"].id),
            Exercise(index=5, word_id=words["bet"].id),
            Exercise(index=6, word_id=words["pan"].id),
            Exercise(index=7, word_id=words["pen"].id),
        ]),
        Lesson(title="Repetition Practice Words", exercises=[
            Exercise(index=0, word_id=words["man"].id),
            Exercise(index=1, word_id=words["bag"].id),
            Exercise(index=2, word_id=words["cap"].id),
            Exercise(index=3, word_id=words["sat"].id),
            Exercise(index=4, word_id=words["dad"].id),
            Exercise(index=5, word_id=words["jam"].id),
            Exercise(index=6, word_id=words["map"].id),
            Exercise(index=7, word_id=words["nap"].id),
        ]),
        Lesson(title="Sound Isolation Words", exercises=[
            Exercise(index=0, word_id=words["pat"].id),
            Exercise(index=1, word_id=words["pot"].id),
            Exercise(index=2, word_id=words["pig"].id),
            Exercise(index=3, word_id=words["pan"].id),
            Exercise(index=4, word_id=words["pen"].id),
            Exercise(index=5, word_id=words["pop"].id),
            Exercise(index=6, word_id=words["pet"].id),
            Exercise(index=7, word_id=words["pit"].id),
        ]),
        Lesson(title="Repetition Practice Words", exercises=[
            Exercise(index=0, word_id=words["pen"].id),
            Exercise(index=1, word_id=words["pin"].id),
            Exercise(index=2, word_id=words["pack"].id),
            Exercise(index=3, word_id=words["puff"].id),
            Exercise(index=4, word_id=words["pit"].id),
            Exercise(index=5, word_id=words["pair"].id),
            Exercise(index=6, word_id=words["page"].id),
            Exercise(index=7, word_id=words["pine"].id),
        ]),
        Lesson(title="Listening Discrimination Pairs", exercises=[
            Exercise(index=0, word_id=words["see"].id),
            Exercise(index=1, word_id=words["sit"].id),
            Exercise(index=2, word_id=words["feel"].id),
            Exercise(index=3, word_id=words["fill"].id),
            Exercise(index=4, word_id=words["sheep"].id),
            Exercise(index=5, word_id=words["ship"].id),
            Exercise(index=6, word_id=words["heel"].id),
            Exercise(index=7, word_id=words["hill"].id),
        ]),
        Lesson(title="Repetition Practice Words", exercises=[
            Exercise(index=0, word_id=words["tree"].id),
            Exercise(index=1, word_id=words["keep"].id),
            Exercise(index=2, word_id=words["tea"].id),
            Exercise(index=3, word_id=words["free"].id),
            Exercise(index=4, word_id=words["pea"].id),
            Exercise(index=5, word_id=words["neat"].id),
            Exercise(index=6, word_id=words["green"].id),
            Exercise(index=7, word_id=words["heat"].id),
        ]),
        Lesson(title="Programming Terms", exercises=[
            Exercise(index=0, word_id=words["compilers"].id),
            Exercise(index=1, word_id=words["hardware"].id),
            Exercise(index=2, word_id=words["software"].id)
        ]),
        Lesson(title="Computer Accessories", exercises=[
            Exercise(index=0, word_id=words["keyboard"].id),
            Exercise(index=1, word_id=words["mouse"].id),
            Exercise(index=2, word_id=words["computer"].id)
        ]),
        Lesson(title="Short Lesson", exercises=[
            Exercise(index=0, word_id=words["parrot"].id)
        ])
    ]
    
    session.add_all(lessons)
    session.commit()
    
    basic_lessons = [
        BasicLesson(id=lessons[0].id, index=0),
        BasicLesson(id=lessons[1].id, index=1),
        BasicLesson(id=lessons[2].id, index=0),
        BasicLesson(id=lessons[3].id, index=1),
        BasicLesson(id=lessons[4].id, index=0),
        BasicLesson(id=lessons[5].id, index=1),
        BasicLesson(id=lessons[6].id, index=0),
        BasicLesson(id=lessons[7].id, index=1),
        BasicLesson(id=lessons[8].id, index=0),
    ]
    
    session.add_all(lessons)
    session.commit()

    units = [
        Unit(
            name="Short Vowel Sound",
            description="Focus on /æ/",
            order=1,
            lessons=[
                basic_lessons[0],
                basic_lessons[1]
            ]
        ),
        Unit(
            name="Consonant Sound",
            description="Focus on /p/",
            order=2,
            lessons=[
                basic_lessons[2],
                basic_lessons[3]
            ]
        ),
        Unit(
            name="Long Vowel Sound",
            description="Focus on /iː/",
            order=3,
            lessons=[
                basic_lessons[4],
                basic_lessons[5]
            ]
        ),
        Unit(
            name="Advanced Topics",
            description="More complex topics",
            order=4,
            lessons=[
                basic_lessons[6],
                basic_lessons[7]
            ]
        ),
        Unit(
            name="Short Unit",
            description="Short unit",
            order=5,
            lessons=[
                basic_lessons[8]
            ]
        )
    ]
    session.add_all(basic_lessons)
    session.add_all(basic_lessons)
    session.add_all(units)
    session.commit()

    print("🎉✅ Database seeding completed successfully!")


# To seed inside a container
# docker exec -it <container_id> python -m app.seed
if __name__ == "__main__":
    print("🔄 Resetting database schema...")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    SQLModel.metadata.create_all(engine)
    seed(Session(engine))
