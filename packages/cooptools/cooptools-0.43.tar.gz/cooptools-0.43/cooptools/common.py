import math
import uuid
from typing import List, Union, Tuple
import itertools
import datetime

def flattened_list_of_lists(list_of_lists: List[List], unique: bool = False) -> List:
    flat = list(itertools.chain.from_iterable(list_of_lists))

    if unique:
        flat = list(set(flat))

    return flat

def all_indxs_in_lst(lst: List, value) -> List[int]:
    idxs = []
    idx = -1
    while True:
        try:
            idx = lst.index(value, idx + 1)
            idxs.append(idx)
        except ValueError as e:
            break
    return idxs

def next_perfect_square_rt(n: int) -> int:
    int_root_n = int(math.sqrt(n))
    if int_root_n == n:
        return n
    return int_root_n + 1

def last_day_of_month(any_day: datetime.date):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month_first_day = (any_day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month_first_day - datetime.timedelta(days=1)

def try_resolve_guid(id: str) -> Union[str, uuid.UUID]:

    try:
        return uuid.UUID(id)
    except:
        return id

def split_strip(txt: str):
    return [x.strip() for x in txt.split(',')]


if __name__ == "__main__":
    print(next_perfect_square_rt(9))