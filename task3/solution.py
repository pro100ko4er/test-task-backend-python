import unittest

def merge_intervals(intervals):
    """Объединяет пересекающиеся интервалы."""
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged

def parse_intervals(times):
    """Преобразует список таймстемпов в список пар [start, end]."""
    return [[times[i], times[i + 1]] for i in range(0, len(times), 2)]

def intersect_intervals(intervals1, intervals2):
    print('first interval')
    print(intervals1)
    print('second interval')
    print(intervals2)
    """Возвращает пересечения интервалов двух списков."""
    i, j = 0, 0
    result = []
    while i < len(intervals1) and j < len(intervals2):
        a_start, a_end = intervals1[i]
        b_start, b_end = intervals2[j]
        start = max(a_start, b_start)
        end = min(a_end, b_end)
        if start < end:
            result.append([start, end])
        if a_end < b_end:
            i += 1
        else:
            j += 1
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = parse_intervals(intervals['lesson'])
    pupil = merge_intervals(parse_intervals(intervals['pupil']))
    tutor = merge_intervals(parse_intervals(intervals['tutor']))

    # Пересечение урока с учеником и с учителем

    pupil_present = intersect_intervals(pupil, lesson)
    tutor_present = intersect_intervals(tutor, lesson)

    # Пересечение присутствия ученика и учителя на уроке
    both_present = intersect_intervals(pupil_present, tutor_present)

    # Суммируем общую продолжительность пересечений
    total_time = sum(end - start for start, end in both_present)
    return total_time



tests = [
    {'intervals': {
             'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {
             'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {
             'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'



class TestAppearance(unittest.TestCase):
    def test_case_1(self):
        data = {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        }
        self.assertEqual(appearance(data), 3117)

    def test_case_2(self):
        data = {
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                      1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                      1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                      1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                      1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
                      1594705149, 1594706463]
        }
        self.assertEqual(appearance(data), 3577)

    def test_case_3(self):
        data = {
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
        }
        self.assertEqual(appearance(data), 3565)

    def test_no_overlap(self):
        data = {
            'lesson': [1000, 2000],
            'pupil': [3000, 4000],
            'tutor': [5000, 6000]
        }
        self.assertEqual(appearance(data), 0)

    def test_full_overlap(self):
        data = {
            'lesson': [1000, 2000],
            'pupil': [1000, 2000],
            'tutor': [1000, 2000]
        }
        self.assertEqual(appearance(data), 1000)

    def test_empty_input(self):
        data = {
            'lesson': [1000, 2000],
            'pupil': [],
            'tutor': []
        }
        self.assertEqual(appearance(data), 0)

if __name__ == '__main__':
    unittest.main()