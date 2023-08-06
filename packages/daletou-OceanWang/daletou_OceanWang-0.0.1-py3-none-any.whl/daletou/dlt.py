from random import sample


def random_dlt(num=1, reds_pre=None, blue_pre=None):
    result = []
    for n in range(num):

        if reds_pre is None:
            reds = sample([n for n in range(1, 36)], 5)
        if blue_pre is None:
            blues = sample([n for n in range(1, 13)], 2)

        reds.sort()
        blues.sort()

        # reds_balls = []
        # blue_balls = []
        # for i in reds:
        #     reds_balls.append(str(i))
        # for i in blues:
        #     blue_balls.append(str(i))

        # reds_balls = [str(i) for i in reds]
        # blue_balls = [str(i) for i in blues]

        reds_balls = map(lambda x: str(x), reds)
        blue_balls = map(lambda x: str(x), blues)

        result.append(' '.join(reds_balls) + ' + ' + ' '.join(blue_balls))

    return '\n'.join(result)


print(random_dlt())