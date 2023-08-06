from email import header


def test(sample):
    max_score = None
    max_location = None

    def has_value(val):
        return 1 if val == 0 or bool(val) else -1

    sample = [
        [has_value(v) for v in r]
        for r in sample
    ]

    for skip_row in range(10):
        for skip_col in range(5):
            score = sum(
                sum(r[skip_col:])
                for r in sample[skip_row:]
            )
            if max_score is None or max_score < score:
                max_score = score
                max_location = (skip_row, skip_col)

    print(max_location, max_score)

    header_count = 0
    for v in sample[max_location[0]][max_location[1]:]:
        if v == 1:
            header_count += 1
        else:
            break
    
    print(header_count)


if __name__ == '__main__':
    sample = [
        ['Summary of stuff'],
        ['', '', ''],
        ['', 'header', 'a', 'b', 'c', '', 'not a header'],
        ['', 1, 2, 3, 4],
        ['', 1, 2, 3, 4, ''],
        ['', 1, 2, 3, 4, ''],
        ['', 1, 2, 3, 4, ''],
        ['', 1, 2, 3, 4, 'not a good row'],
        ['', 1, 2, 3, 4],
        ['', 1, 2, 3, 4],
        ['', 1, 2, 3, 4],
    ]
    test(sample)

    
