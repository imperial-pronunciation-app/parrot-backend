# test the attempt service and router

"""Service tests
"""

import os

import responses

from app.crud.unit_of_work import UnitOfWork
from app.routers.attempts import AttemptService
from tests.factories.word import WordFactory


@responses.activate
def test_successful_request(uow: UnitOfWork, make_word: WordFactory) -> None:
    """Test that a successful request returns a 200 status code"""
    word = make_word()
    test_wav_filename = "tests/assets/software.wav"
    phonemes = [phoneme.ipa for phoneme in word.phonemes]

    rsp = responses.Response(
        method="POST",
        url=f"{os.environ.get('MODEL_API_URL', '')}/api/v1/eng/infer_word_phonemes",
        json={"success": True, "phonemes": phonemes, "words": [word.text]},
    )
    responses.add(rsp)

    model_response = AttemptService(uow).dispatch_to_model(test_wav_filename, word.language)
    assert model_response.phonemes == phonemes
    assert model_response.words == [word.text]

@responses.activate
def test_unsuccessful_request(uow: UnitOfWork, make_word: WordFactory) -> None:
    """Test that a request with unsuccesfull inference returns a 200 status code"""
    word = make_word()
    test_wav_filename = "tests/assets/software.wav"

    rsp = responses.Response(
        method="POST",
        url=f"{os.environ.get('MODEL_API_URL', '')}/api/v1/eng/infer_word_phonemes",
        json={"success": False, "phonemes": [], "words": []},
    )
    responses.add(rsp)

    model_response = AttemptService(uow).dispatch_to_model(test_wav_filename, word.language)
    assert not model_response.success

