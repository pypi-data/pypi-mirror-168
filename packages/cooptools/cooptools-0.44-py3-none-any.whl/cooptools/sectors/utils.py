from cooptools.common import next_perfect_square_rt
from typing import Tuple
from cooptools.coopEnum import CardinalPosition

def square_sector_def(n_sectors: int) -> (int, int):
    """
    :param n_sectors: the min number of sectors that must be created
    :return: (rows, cols)
    """
    next_sq_rt = next_perfect_square_rt(n_sectors)
    return (next_sq_rt, next_sq_rt)


def rect_sector_attributes(area_rect: Tuple[float, float], sector_def: Tuple[int, int]) -> (float, float, float, float):
    """
    :param area_rect: (width, height)
    :param sector_def: (rows, cols)
    :return: Given the area and the sector def, get the description of the sectors (width, height, width_p, height_p)
    """

    sector_width_p = 1 / sector_def[1]
    sector_height_p = 1 / sector_def[0]

    return (area_rect[0] * sector_width_p, area_rect[1] * sector_height_p, sector_width_p, sector_height_p)

def rect_sector_from_coord(coord: Tuple[float, float], area_rect: Tuple[float, float], sector_def: Tuple[int, int]) -> (float, float):
    """
    :param coord: (x, y)
    :param area_rect: (width, height)
    :param sector_def: (rows, cols)
    :return: The sector the coords are in (row, column)
    """

    if coord is None:
        return None

    # Change the x/y screen coordinates to sectors coordinates
    column = int((coord[0]) // (area_rect[0] / sector_def[1]))
    row = int((coord[1]) // (area_rect[1] / sector_def[0]))

    if 0 <= column < sector_def[1] and \
        0 <= row < sector_def[0]:
        sector_coord = (row, column)
        return sector_coord
    else:
        return None

def rect_sector_indx(sector_def: Tuple[int, int], sector: Tuple[int, int], rows_then_cols: bool = True) -> int:
    """
    :param sector_def: (rows, cols)
    :param sector: (row, column)
    :param rows_then_cols: choose to enumerate rows then columns or vice versa
    :return: Given a definition of a sector layout and the coords of a specific sector, get the index of the sector
    """

    if rows_then_cols:
        return sector[0] * sector_def[1] + sector[1]
    else:
        return sector[1] * sector_def[0] + sector[0]

def coord_of_sector(area_rect: Tuple[float, float], sector_def: Tuple[int, int], sector: Tuple[int, int], cardinality: CardinalPosition):
    """
    :param area_rect: (width, height)
    :param sector_def: (rows, cols)
    :param sector: (row, col)
    :param cardinality: defines what coord is requested for the input
    :return: returns the (x, y) coord of the sector given the input params
    """

    cardinality_switch = {
        cardinality.TOP_LEFT: (0, 0),
        cardinality.TOP_CENTER: (0.5, 0),
        cardinality.TOP_RIGHT: (1, 0),
        cardinality.LEFT_CENTER: (0, 0.5),
        cardinality.CENTER: (0.5, 0.5),
        cardinality.RIGHT_CENTER: (1, 0.5),
        cardinality.BOTTOM_LEFT: (0, 1),
        cardinality.BOTTOM_CENTER: (0.5, 1),
        cardinality.BOTTOM_RIGHT: (1, 1)
    }

    offset = cardinality_switch.get(cardinality, None)
    if offset is None:
        raise NotImplementedError(f"Unhandled cardinality {cardinality}")

    sector_attr = rect_sector_attributes(area_rect, sector_def)

    off_x, off_y = offset
    row_idx = sector[0]
    col_idx = sector[1]
    height = sector_attr[1]
    width = sector_attr[0]

    return (col_idx * width + off_x, row_idx * height + off_y)

if __name__ == "__main__":
    sector_def = square_sector_def(1000) # should yield 3x3
    print (sector_def)

    area_rect = (500, 1000)
    sector_attrs = rect_sector_attributes(area_rect=area_rect, sector_def=sector_def)
    print(sector_attrs)

    coord = (27, 732)
    sec = rect_sector_from_coord(coord=coord, area_rect=area_rect, sector_def=sector_def)
    print(sec)

    idx = rect_sector_indx(sector_def=sector_def, sector=sec)
    print(idx)
    idx2 = rect_sector_indx(sector_def=sector_def, sector=sec, rows_then_cols=False)
    print(idx2)


    for ii in range(3):
        for jj in range(3):
            print(rect_sector_indx(sector_def=sector_def, sector=(ii, jj)))