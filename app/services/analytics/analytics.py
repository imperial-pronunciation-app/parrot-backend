from app.crud.analytics.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def get_chart_data(self) -> dict:
        # Sadly, we can't use the UnitOfWork pattern here, as this service is called from the admin panel
        results = AnalyticsRepository().get_count_of_endpoint_and_response_time()

        endpoints: list[str] = [str(r[0]) for r in results]
        counts: list[int] = [int(r[1]) for r in results]
        avg_times: list[float] = [round(float(r[2]), 2) if r[2] is not None else 0.0 for r in results]

        results_filtered: list[tuple[str, int, float]] = [
            (endpoint, count, avg_time)
            for endpoint, count, avg_time in zip(endpoints, counts, avg_times)
            if "admin" not in endpoint
        ]

        if results_filtered:
            endpoints, counts, avg_times = map(list, zip(*results_filtered))
        else:
            endpoints, counts, avg_times = [], [], []

        chart_data = {
            "labels": endpoints,
            "datasets": [
                {
                    "label": "Number of Calls",
                    "data": counts,
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                    "borderColor": "rgb(75, 192, 192)",
                    "borderWidth": 1,
                },
                {
                    "label": "Avg Response Time (ms)",
                    "data": avg_times,
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "borderWidth": 1,
                    "yAxisID": "response-time",
                },
            ],
        }
        return chart_data

    def get_exercise_analytics(self) -> dict:
        results = AnalyticsRepository().get_exercise_analytics()

        # Filter to only get attempts to exercise endpoints
        results = [r for r in results if r[0].endswith("attempts")]

        results = results = [(x[0].split("/")[-2], x[1]) for x in results]

        endpoints: list[str] = [str(r[0]) for r in results]
        counts: list[int] = [int(r[1]) for r in results]

        return {
            "labels": endpoints,
            "datasets": [
                {
                    "label": "# time exercise was attempted",
                    "data": counts,
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "borderWidth": 1,
                },
            ],
        }

    def get_exercise_difficulty_data(self) -> dict:
        results = AnalyticsRepository().get_exercise_difficulty_analytics()

        exercise_ids: list[str] = [str(r[0]) for r in results]
        avg_scores: list[float] = [round(float(r[1]), 2) if r[1] is not None else 0.0 for r in results]

        # Replace the exercise ids with the actual words
        exercise_words = AnalyticsRepository().get_exercise_words()
        exercise_mapping = {str(exercise_id): word for exercise_id, word in exercise_words}
        exercise_labels = [f"{exercise_id}: {exercise_mapping[exercise_id]}" for exercise_id in exercise_ids]

        return {
            "labels": exercise_labels,
            "datasets": [
                {
                    "label": "Average Score",
                    "data": avg_scores,
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                    "borderColor": "rgb(75, 192, 192)",
                    "borderWidth": 1,
                }
            ],
        }

    def get_phoneme_difficulty_data(self) -> dict:
        # Per phoneme we want 4 different bars, we want:
        # - Correctly identified
        # - Present but incorrect
        # - User didn't say anything
        # - User inserted a phoneme that wasn't present

        results = AnalyticsRepository().get_phoneme_difficulty_analytics()

        phonemes_dict = {}

        for i in range(len(results)):
            expected_phoneme_id, actual_phoneme_id = results[i]

            if expected_phoneme_id not in phonemes_dict and expected_phoneme_id is not None:
                phonemes_dict[expected_phoneme_id] = {
                    "correct": 0,
                    "incorrect": 0,
                    "none": 0,
                    "inserted": 0,
                }

            if expected_phoneme_id is None and actual_phoneme_id is not None:
                # Set actual to inserted
                if actual_phoneme_id not in phonemes_dict:
                    phonemes_dict[actual_phoneme_id] = {
                        "correct": 0,
                        "incorrect": 0,
                        "none": 0,
                        "inserted": 1,
                    }
                else:
                    phonemes_dict[actual_phoneme_id]["inserted"] += 1

            elif expected_phoneme_id == actual_phoneme_id:
                if expected_phoneme_id is not None:
                    phonemes_dict[expected_phoneme_id]["correct"] += 1
            elif actual_phoneme_id is None:
                if expected_phoneme_id is not None:
                    phonemes_dict[expected_phoneme_id]["none"] += 1
            elif expected_phoneme_id != actual_phoneme_id:
                if expected_phoneme_id is not None:
                    phonemes_dict[expected_phoneme_id]["incorrect"] += 1
            else:
                raise ValueError(f"Unexpected case {expected_phoneme_id} {actual_phoneme_id}")

        # Average out the values
        for phoneme_id in phonemes_dict.keys():
            phone = phonemes_dict[phoneme_id]
            total = phone["correct"] + phone["incorrect"] + phone["none"] + phone["inserted"]
            # I want to change the values in place, so I'm disabling the type check here
            phone["correct"] = phone["correct"] / total  # type: ignore
            phone["incorrect"] = phone["incorrect"] / total  # type: ignore
            phone["none"] = phone["none"] / total  # type: ignore
            phone["inserted"] = phone["inserted"] / total  # type: ignore

        phonemes_ids = list(phonemes_dict.keys())
        phonemes_mapping = AnalyticsRepository().get_phoneme_names()
        phonemes = []

        for p in phonemes_ids:
            for phoneme_id, ipa, respelling in phonemes_mapping:
                if p == phoneme_id:
                    phonemes.append(f"{ipa} ({respelling})")

        correct = [phonemes_dict[p]["correct"] for p in phonemes_ids]
        incorrect = [phonemes_dict[p]["incorrect"] for p in phonemes_ids]
        none = [phonemes_dict[p]["none"] for p in phonemes_ids]
        inserted = [phonemes_dict[p]["inserted"] for p in phonemes_ids]

        return {
            "labels": phonemes,
            "datasets": [
                {
                    "label": "Correct",
                    "data": correct,
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                    "borderColor": "rgb(75, 192, 192)",
                    "borderWidth": 1,
                },
                {
                    "label": "Incorrect",
                    "data": incorrect,
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "borderWidth": 1,
                },
                {
                    "label": "None",
                    "data": none,
                    "backgroundColor": "rgba(54, 162, 235, 0.5)",
                    "borderColor": "rgb(54, 162, 235)",
                    "borderWidth": 1,
                },
                {
                    "label": "Inserted",
                    "data": inserted,
                    "backgroundColor": "rgba(255, 206, 86, 0.5)",
                    "borderColor": "rgb(255, 206, 86)",
                    "borderWidth": 1,
                },
            ],
        }
