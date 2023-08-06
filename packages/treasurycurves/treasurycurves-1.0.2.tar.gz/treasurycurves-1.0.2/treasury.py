"""treasury - carry out various analyses on US Treasury Data"""

import functools
import os
from argparse import ArgumentParser
from datetime import datetime
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

DATE_FMT = "%Y-%m-%d"
COLUMNS = ["1 Yr", "2 Yr", "5 Yr", "10 Yr", "20 Yr", "30 Yr"]


def curves(date=None, allow_missing=False):
    """get treasury curves for today or a specific date"""
    date = datetime.today().strftime(DATE_FMT) if date is None else date
    date = datetime.strptime(date, DATE_FMT)
    dt_str = date.strftime(DATE_FMT)
    dt_range = pd.date_range(end=dt_str, periods=50, freq="12M").shift(date.day, freq="D")

    # gather a big range of dates to filter the curve data
    date_ranges = [dt_range.shift(periods=-delta, freq="D") for delta in range(4)]
    ranges = functools.reduce(lambda r1, r2: r1.append(r2), date_ranges)

    # retrieve curve data, filter with date ranges, and sample by year
    drop_columns = [] if allow_missing else COLUMNS
    curve_data = download().dropna(subset=drop_columns)
    curve_data = curve_data[curve_data.index.isin(ranges)]
    curve_years = curve_data.groupby(curve_data.index.year)
    year_samples = curve_years.apply(lambda year: year.sample(n=1))

    # clean the index
    year_samples.index = year_samples.index.set_names(["Year", "Date"])
    return year_samples.reset_index().set_index(keys="Year")


def plot(raw_curve_data, num_years=10, start_year=None, end_year=None):
    """plot treasury curves over the past num_years. alternatively use start_year, end_year"""
    curve_data = filter_curves(raw_curve_data, num_years, start_year, end_year)
    date = curve_data.Date.max().strftime("%B %d")
    curve_data = curve_data.drop("Date", axis=1)[COLUMNS]

    # format the ploat and the legend to look nice
    plt.close("all")
    start, end = curve_data.index.min(), curve_data.index.max()
    title = f"US Treasury Yields {start}-{end}, {date}"
    chart = curve_data.T.plot(xlabel="Maturity", ylabel="Yield", title=title, figsize=(10, 5))
    chart.legend(bbox_to_anchor=(1.0, 1.0))

    # show the plot and done!
    plt.show()
    return curve_data


def filter_curves(curve_data, num_years=10, start_year=None, end_year=None):
    """filter treasury curve data using year filters"""
    start = curve_data.index.min() if start_year is None else int(start_year)
    end = curve_data.index.max() if end_year is None else int(end_year)
    assert start <= end, "start_year must be earlier than end_year"

    # use start and end year to filter the index
    only_start = start_year is not None and end_year is None
    curves = curve_data.sort_values(by="Date", ascending=only_start)
    curves = curves[(curves.index >= start_year) & (curves.index <= end_year)]

    # bound num years by [1, 10] and get the first num_years rows
    num_years = min(10, max(num_years, 1))
    return curves.head(num_years)


def export(curves_data, file_extension="csv"):
    """export curves data analysis to a desired output format"""
    assert file_extension in {"csv", "xlsx"}, "unsupported extension, use csv or xlsx"
    file_dir = os.path.dirname(os.path.realpath(__file__))
    export_dir = os.path.join(file_dir, "exports")
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # build the filename and save curve data
    date = datetime.today().strftime("%Y%m%d")
    file_name = f"yield_curve_{date}.{file_extension}"
    file_path = os.path.join(export_dir, file_name)
    export_function = pd.DataFrame.to_csv if file_extension == "csv" else pd.DataFrame.to_excel
    export_function(curves_data, file_path)


def download():
    """retrieve all available yield curve data at treasury.gov website"""
    archive_request = requests.get(archive_url())
    archive_data = parse_csv_request(archive_request)
    current_request = requests.get(year_url(datetime.today()))
    current_data = parse_csv_request(current_request)
    all_data = pd.concat([current_data, archive_data]).set_index(keys="Date")
    all_data.index = pd.to_datetime(all_data.index)
    return all_data


def archive_url():
    """the url to the treasury.gov yield curve api"""
    last_year = (datetime.today() - relativedelta(years=1)).strftime("%Y")
    return (
        f"https://home.treasury.gov/system/files/276/yield-curve-rates-1990-{last_year}.csv"
    )


def year_url(date):
    """get csv for a single year"""
    date = date.strftime("%Y")
    return (
        "https://home.treasury.gov/resource-center/data-chart-center/"
        f"interest-rates/daily-treasury-rates.csv/{date}/all?"
        f"type=daily_treasury_yield_curve&field_tdr_date_value={date}&page&_format=csv"
    )


def parse_csv_request(request):
    return pd.read_csv(StringIO(request.text))


def main():
    """carry out all treasury lib api functions according to cli args"""
    parser = ArgumentParser(description="treasury - query and analyze US Treasury yield data")

    # filter arguments
    parser.add_argument("-a", "--allowna", action="store_true", help="Allow NaN values")
    parser.add_argument("-s", "--start", type=int, help="Year to start analysis")
    parser.add_argument("-e", "--end", type=int, help="Year to end analysis")
    parser.add_argument("-d", "--date", type=str, help="Date in YYYY-MM-DD to analyze")
    parser.add_argument("-y", "--years", type=int, default=10, help="Num years before end to analyze")

    # output argument
    parser.add_argument("-p", "--plot", action="store_true", help="Plot yield curves")
    help_msg = "File extension to save data (csv or xlsx), leave empty to avoid saving file"
    parser.add_argument("-o", "--output", type=str, help=help_msg)

    # analyze!
    args = parser.parse_args()
    curve_data = curves(date=args.date, allow_missing=args.allowna)
    if args.plot:
        plot(curve_data, num_years=args.years, start_year=args.start, end_year=args.end)
    if args.output is not None:
        export(curve_data, args.output)

if __name__ == "__main__":
    main()
