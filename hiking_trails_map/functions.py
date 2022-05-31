import pandas as pd
from hiking_trails_api.models import HikingTrails


def make_df():

    hiking_trails = HikingTrails.objects.all()

    #
    # # Make a Dataframe with empty lat & lon collumns
    # df = pd.DataFrame(
    #     {'Lake': 'lake',
    #      })
    #
    # df["latitude"] = ""
    # df["longitude"] = ""
    # df["Directions"] = ""

    return print(hiking_trails)


make_df()

