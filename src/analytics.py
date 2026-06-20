import pandas as pd


def calculate_kpis(df):
    """Calculate key performance indicators."""

    total_sales = df["Sales Count"].sum()
    total_redemption = df["Redemption Count"].sum()

    net_passenger = total_sales - total_redemption

    avg_sales = df["Sales Count"].mean()
    avg_redemption = df["Redemption Count"].mean()

    peak_hour = (
        df.groupby("Hour")["Sales Count"]
        .sum()
        .idxmax()
    )

    off_peak_hour = (
        df.groupby("Hour")["Sales Count"]
        .sum()
        .idxmin()
    )

    print("=" * 40)
    print("FERRY ANALYTICS KPI REPORT")
    print("=" * 40)

    print(f"Total Tickets Sold        : {total_sales:,}")
    print(f"Total Tickets Redeemed   : {total_redemption:,}")
    print(f"Net Passenger Movement   : {net_passenger:,}")
    print(f"Average Sales            : {avg_sales:.2f}")
    print(f"Average Redemption       : {avg_redemption:.2f}")
    print(f"Peak Demand Hour         : {peak_hour}:00")
    print(f"Off Peak Hour            : {off_peak_hour}:00")


if __name__ == "__main__":

    df = pd.read_csv("data/ferry_featured.csv")

    calculate_kpis(df)