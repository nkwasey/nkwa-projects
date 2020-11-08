__author__ = "Nana Ekow NKwa Sey"


from math import radians, cos, sin, asin, sqrt
import pandas as pd


# Finding coordinates within a certain radius
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    val = c * r
    return val


def search_byDate(date, df, output):
    # output = []
    fireData = df
    df['acq_date'] = pd.to_datetime(fireData['acq_date'])
    found_fires = fireData[fireData['acq_date'] == date]
    # print(found_fires)
    fire_info = []
    for index, row in found_fires.iterrows():
        message = dict(lat=row['latitude'], lon=row['longitude'], date=row['acq_date'].strftime('%m/%d/%Y'),
                       ToD=row['acq_time'], brightness=row['brightness'],
                       satellite=row['satellite'], instrument=row['instrument'])

        fire_info.append(message)
    output.append({"Count(s)": len(fire_info)})
    output.append({"fire(s)": fire_info})
    return output


# search_byDate("1/1/2020")
