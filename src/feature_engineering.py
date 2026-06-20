import pandas as pd


def add_features(df):
    """
    Add new time-based features to the dataset.
    """

    # Ensure Timestamp is datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Time Features
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Month Name"] = df["Timestamp"].dt.month_name()

    df["Day"] = df["Timestamp"].dt.day
    df["Day Name"] = df["Timestamp"].dt.day_name()

    df["Hour"] = df["Timestamp"].dt.hour
    df["Minute"] = df["Timestamp"].dt.minute

    # Weekend / Weekday
    df["Weekend"] = df["Day Name"].isin(["Saturday", "Sunday"])

    # Season
    def season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    df["Season"] = df["Month"].apply(season)

    return df


if __name__ == "__main__":

    df = pd.read_csv("data/cleaned_ferry_data.csv")

    df = add_features(df)

    df.to_csv("data/ferry_featured.csv", index=False)

    print("✅ Feature Engineering Completed!")
    