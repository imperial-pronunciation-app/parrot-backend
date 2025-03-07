from fastapi import APIRouter, Depends, UploadFile

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.attempt import AttemptResponse, ExerciseAttemptResponse
from app.services.attempts import AttemptService
from app.users import current_active_user


router = APIRouter()


@router.post("/api/v1/exercises/{exercise_id}/attempts", response_model=ExerciseAttemptResponse)
async def post_exercise_attempt(
    exercise_id: int,
    audio_file: UploadFile,
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user),
) -> ExerciseAttemptResponse:
    attempt_service = AttemptService(uow)
    resp = await attempt_service.post_exercise_attempt(audio_file, exercise_id, uow, user)
    return resp


@router.post("/api/v1/word_of_day/attempts", response_model=AttemptResponse)
async def post_word_of_day_attempt(
    audio_file: UploadFile,
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user),
) -> AttemptResponse:
    attempt_service = AttemptService(uow)
    word_of_day_id = uow.word_of_day.get_word_of_day(user.language_id).id
    resp = await attempt_service.post_word_of_day_attempt(audio_file, word_of_day_id, uow, user)
    return resp
