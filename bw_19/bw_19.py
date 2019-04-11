# keyword parmeter로 선택적 동작 제공
# keyword parameter의 장점


def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6


def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff


weight_diff = 0.5
time_diff = 3
flow_1 = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow_1)


def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


flow_2 = flow_rate(weight_diff, time_diff)
flow_3 = flow_rate(weight_diff, time_diff, period=3600)


def flow_rate_2(weight_diff, time_diff, period=1, units_per_kg: float = 1):
    return ((weight_diff / units_per_kg) / time_diff) * period


pounds_per_hour = flow_rate_2(weight_diff, time_diff, period=3600, units_per_kg=2.2)
print()