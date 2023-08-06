"""treasury - carry out various analyses on US Treasury Data"""

import functools
import os
from argparse import ArgumentParser
from calendar import month
from datetime import datetime
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

DATE_FMT = "%Y-%m-%d"
COLUMNS = ["1 Yr", "2 Yr", "5 Yr", "10 Yr", "20 Yr", "30 Yr"]


def curves(date=None, allow_missing=False):
    """get treasury curves for today or a specific date

    :param str date: a datetime str in the format YYYY-MM-DD
    :param bool allow_missing: boolean flag that allows NaN values when True
    """
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


def yearly_curves(year, allow_missing=False):
    """get the yearly curve over months for different treasury durations

    :param int year: the year to analyze
    :param bool allow_missing: boolean flag that allows NaN values when True
    """
    drop_columns = [] if allow_missing else COLUMNS
    curve_data = download_year(year).dropna(subset=drop_columns)

    # now get 1 sample per month for plotting
    curve_months = curve_data.groupby(curve_data.index.month)
    month_samples = curve_months.apply(lambda month: month.sample(n=1))

    # clean the index
    month_samples.index = month_samples.index.set_names(["Month", "Date"])
    month_samples = month_samples.reset_index()
    to_month = lambda m: datetime.strptime(str(m), "%m").strftime("%b")
    month_samples["Month"] = month_samples["Month"].apply(to_month)
    return month_samples.set_index(keys="Month")


def plot(raw_curve_data, num_years=10, start_year=None, end_year=None):
    """plot treasury curves over the past num_years. alternatively use start_year, end_year
    as a range. if start_year equals end_year, plot yearly data over the 12 months

    :param pandas.DataFrame raw_curve_data: treasury curve data with index Year
    :param int num_years: number of years to plot, default is 10
    :param int start_year: first year to begin plotting data
    :param int end_year: last year to consider when plotting
    """
    curve_data = filter_curves(raw_curve_data, num_years, start_year, end_year)
    yearly = start_year == end_year
    date = curve_data.Date.max().strftime("%B") if not yearly else start_year
    curve_data = curve_data.drop("Date", axis=1)[COLUMNS]

    # format the ploat and the legend to look nice
    plt.close("all")
    start, end = ("Jan", "Dec") if yearly else (curve_data.index.min(), curve_data.index.max())
    xlabel, ylabel = ("Maturity", "Yield") if not yearly else ("Month", "Yield")
    title = f"US Treasury Yields {start}-{end}, {date}"
    curve_data = curve_data.T if yearly else curve_data
    chart = curve_data.T.plot(xlabel=xlabel, ylabel=ylabel, title=title, figsize=(10, 5))
    chart.legend(bbox_to_anchor=(1.0, 1.0))

    # show the plot and done!
    plt.show()
    return curve_data


def filter_curves(curve_data, num_years=10, start_year=None, end_year=None):
    """filter treasury curve data using year filters, if start=end don't filter"""
    if start_year is not None and start_year == end_year:
        return curve_data
    start = curve_data.index.min() if start_year is None else int(start_year)
    end = curve_data.index.max() if end_year is None else int(end_year)
    assert start <= end, "start_year must be earlier than end_year"

    # use start and end year to filter the index
    only_start = start_year is not None and end_year is None
    curves = curve_data.sort_values(by="Date", ascending=only_start)
    curves = curves[(curves.index >= start) & (curves.index <= end)]

    # bound num years by [1, 12] and get the first num_years rows
    num_years = min(10, max(num_years, 1))
    return curves.head(num_years)


def export(curves_data, file_extension="csv"):
    """export curves data analysis to a desired output format

    :param pandas.DataFrame curves_data: dataframe containing treasury curve data
    :param str file_extension: the file type to export. can be "csv" or "xlsx"
    """
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


def download_year(year):
    """retrieve all curve data for a year"""
    dt_year = datetime.now().replace(year=year)
    url = year_url(dt_year)
    year_data = parse_csv_request(requests.get(url)).set_index(keys="Date")
    year_data.index = pd.to_datetime(year_data.index)
    return year_data


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
    help_msg = "Year to end analysis. If equal to start, analyze curves for the year"
    parser.add_argument("-e", "--end", type=int, help=help_msg)
    parser.add_argument("-d", "--date", type=str, help="Date in YYYY-MM-DD to analyze")
    parser.add_argument("-y", "--years", type=int, default=10, help="Num years before end to analyze")

    # output argument
    parser.add_argument("-p", "--plot", action="store_true", help="Plot yield curves")
    help_msg = "File extension to save data (csv or xlsx), leave empty to avoid saving file"
    parser.add_argument("-o", "--output", type=str, help=help_msg)
    args = parser.parse_args()

    # if start == end, use yearly curves instead of all data
    if args.start != args.end:
        curve_data = curves(date=args.date, allow_missing=args.allowna)
    else:
        curve_data = yearly_curves(year=args.start, allow_missing=args.allowna)

    # analyze!
    if args.plot:
        plot(curve_data, num_years=args.years, start_year=args.start, end_year=args.end)
    if args.output is not None:
        export(curve_data, args.output)

if __name__ == "__main__":
    main()
