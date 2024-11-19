import heapq
from collections import deque


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_ints = intervals.get('lesson', None)
    pupil_ints = intervals.get('pupil', None)
    tutor_ints = intervals.get('tutor', None)

    if not lesson_ints or not pupil_ints or not tutor_ints \
            or len(lesson_ints) != 2 or len(pupil_ints) % 2 == 1 or len(tutor_ints) % 2 == 1:
        raise ValueError('Invalid intervals')

    def _merge_intersecting_ints(tss: list[int]) -> list[int]:
        res_ints = []
        interval_deque = deque(zip(tss[::2], tss[1::2]))

        while len(interval_deque) >= 2:
            fst, snd = interval_deque.popleft(), interval_deque.popleft()

            if fst[1] < snd[0]:
                res_ints.append(fst)
                interval_deque.appendleft(snd)

            else:
                interval_deque.appendleft((min(fst[0], snd[0]), max(fst[1], snd[1])))

        while len(interval_deque) > 0:
            res_ints.append(interval_deque.popleft())

        return [ts for interval in res_ints for ts in interval]

    pupil_tutor_ints = list(heapq.merge(
        map(lambda ts: (ts, 'pupil'), _merge_intersecting_ints(pupil_ints)),
        map(lambda ts: (ts, 'tutor'), _merge_intersecting_ints(tutor_ints)),
    ))

    both_online_time = 0

    lesson_st = lesson_ints[0]
    pupil_st = None
    tutor_st = None

    i = 0
    while i < len(pupil_tutor_ints) and pupil_tutor_ints[i][0] < lesson_ints[1]:
        if pupil_st is not None and tutor_st is not None:
            both_online_time += pupil_tutor_ints[i][0] - max(pupil_st, tutor_st)
            if pupil_tutor_ints[i][1] == 'pupil':
                pupil_st = None
            else:
                tutor_st = None

        elif pupil_st is None and tutor_st is None:
            if pupil_tutor_ints[i][1] == 'pupil':
                pupil_st = max(pupil_tutor_ints[i][0], lesson_st)
            else:
                tutor_st = max(pupil_tutor_ints[i][0], lesson_st)

        elif pupil_st is not None:
            if pupil_tutor_ints[i][1] == 'pupil':
                pupil_st = None
            else:
                tutor_st = max(pupil_tutor_ints[i][0], lesson_st)

        elif tutor_st is not None:
            if pupil_tutor_ints[i][1] == 'pupil':
                pupil_st = max(pupil_tutor_ints[i][0], lesson_st)
            else:
                tutor_st = None

        i += 1

    if pupil_st is not None and tutor_st is not None:
        both_online_time += lesson_ints[1] - max(pupil_st, tutor_st)

    return both_online_time
