from random import choice
from typing import Dict

from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.recap_lesson import RecapLesson
from app.models.unit import Unit
from app.models.user import User
from app.schemas.unit import UnitPublicWithLessons
from app.services.basic_lesson import BasicLessonService
from app.services.lesson import LessonService
from app.services.recap_lesson import RecapLessonService


class UnitService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_public_with_lessons(self, unit: Unit, user: User) -> UnitPublicWithLessons:
        basic_lesson_service = BasicLessonService(self._uow)
        recap_lesson_service = RecapLessonService(self._uow)
        recap_lesson = self._uow.recap_lessons.find_recap_by_user_id_and_unit_id(user.id, unit.id)

        is_locked = not (unit.index == 0 or self._is_completed_by(self._uow.units.for_language(unit.language_id)[unit.index - 1], user))

        return UnitPublicWithLessons(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            lessons=[basic_lesson_service.to_response(lesson, user) for lesson in unit.lessons] if not is_locked else None,
            recap_lesson=recap_lesson_service.to_response(recap_lesson, user) if recap_lesson else None,
            is_completed=self._is_completed_by(unit, user),
            is_locked=is_locked
        )
    
    def basic_lessons_completed_by(self, unit: Unit, user: User) -> bool:
        lesson_service = LessonService(self._uow)
        return all(lesson_service._is_completed_by(self._uow.lessons.get_by_id(basic_lesson.id), user) for basic_lesson in unit.lessons)

    def _is_completed_by(self, unit: Unit, user: User) -> bool:
        lesson_service = LessonService(self._uow)
        recap_lesson = self._uow.recap_lessons.find_recap_by_user_id_and_unit_id(user.id, unit.id)
        return self.basic_lessons_completed_by(unit, user) and recap_lesson is not None and lesson_service._is_completed_by(self._uow.lessons.get_by_id(recap_lesson.id), user)
        

    def generate_recap_lesson(self, unit: Unit, user: User) -> None:
        # Precondition: all exercises in the unit have been attempted at least once
        """
            For each BasicLesson in the Unit, for each Exercise in the BasicLesson, for each ExerciseAttempt for the Exercise, retrieve the phoneme performance

            Collate performance across the entire unit
        """
        # 1. For each BasicLesson in the Unit, for each Exercise in the BasicLesson, for each exercise attempt, join with phonemes
        # on the exercise attempt phoneme link table, and return the phoneme and weight
        phoneme_difficulties: Dict[int, float] = {}
        for basic_lesson in unit.lessons:
            lesson = self._uow.lessons.get_by_id(basic_lesson.id)
            for exercise in lesson.exercises:
                exercise_attempts = self._uow.exercise_attempts.find_by_user_id_and_exercise_id(user.id, exercise.id)
                for attempt in exercise_attempts:
                    aligned = self._uow.exercise_attempts.get_aligned_phonemes(attempt)
                    for expected, actual in aligned:
                        # Scoring:
                        # Got a phoneme wrong - +1
                        # Added a phoneme - +0.5
                        # Got a phoneme right - -1
                        if expected:
                            score = 1 if expected == actual else -1
                            phoneme_difficulties[expected.id] = phoneme_difficulties.get(expected.id, 0) + score
                        if not expected and actual:
                            phoneme_difficulties[actual.id] = phoneme_difficulties.get(actual.id, 0) + 0.5
        
        worst_phonemes = sorted(phoneme_difficulties.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 2. For each phoneme, find a word containing that phoneme
        # Restrict to the same language as the unit
        words = []
        for phoneme_id, _ in worst_phonemes:
            phoneme = self._uow.phonemes.get_by_id(phoneme_id)
            if phoneme.words:
                word_options = [word for word in phoneme.words if word.language_id == unit.language_id]
                if word_options:
                    words.append(choice(word_options))
        
        # 3. Create a RecapLesson, containing exercises for each of those words
        lesson = self._uow.lessons.upsert(Lesson(
            title=f"Recap of {unit.name}",
            exercises=[Exercise(index=i, word_id=word.id) for i, word in enumerate(words)],
        ))
        self._uow.recap_lessons.upsert(RecapLesson(
            id=lesson.id,
            unit_id=unit.id,
            user_id=user.id
        ))
        self._uow.commit()
