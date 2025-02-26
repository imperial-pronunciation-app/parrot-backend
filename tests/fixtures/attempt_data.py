from typing import List

import pytest
from sqlmodel import Session

from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink
from app.models.phoneme import Phoneme
from app.models.user import User


@pytest.fixture
def sample_exercise_attempt(session: Session, sample_exercise: Exercise, sample_user: User) -> ExerciseAttempt:
    """Fixture to create an exercise attempt."""
    attempt = Attempt(user_id=sample_user.id, score=0)
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    exercise_attempt = ExerciseAttempt(id=attempt.id, exercise_id=sample_exercise.id)
    session.add(exercise_attempt)
    session.commit()
    session.refresh(exercise_attempt)
    return exercise_attempt

@pytest.fixture
def sample_phonemes(session: Session) -> List[Phoneme]:
    """Fixture to create sample phonemes."""
    phonemes = [
      Phoneme(ipa="p", respelling="p"),
      Phoneme(ipa="a", respelling="a"),
      Phoneme(ipa="t", respelling="t")
    ]
    session.add_all(phonemes)
    session.commit()
    return phonemes

@pytest.fixture
def sample_attempt_phoneme_links(session: Session, sample_exercise_attempt: ExerciseAttempt, sample_phonemes: List[Phoneme]) -> List[ExerciseAttemptPhonemeLink]:
    """Fixture to create phoneme links for an exercise attempt."""
    phoneme_links = [
      ExerciseAttemptPhonemeLink(exercise_attempt_id=sample_exercise_attempt.id, phoneme_id=sample_phoneme, weight=i)
      for i, sample_phoneme in enumerate(sample_phonemes)
    ]
    session.add_all(phoneme_links)
    session.commit()
    return phoneme_links