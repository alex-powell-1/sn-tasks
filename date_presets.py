from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Dates:
    def __init__(self):
        self.now = datetime.now()
        self.minute = self.now.minute
        self.hour = self.now.hour
        self.day = self.now.day
        self.month = self.now.month
        self.year = self.now.year

        self.today = date.today()
        self.yesterday = self.today + relativedelta(days=-1)
        self.two_weeks_ago = self.today + relativedelta(weeks=-2)
        self.two_day_ago = self.today + relativedelta(days=-2)
        self.three_day_ago = self.today + relativedelta(days=-3)
        self.one_week_ago = self.today + relativedelta(weeks=-1)
        self.one_month_ago = self.today + relativedelta(months=-1)

        # Month
        self.month_start = datetime(year=self.today.year, month=self.today.month, day=1)
        self.month_end = self.month_start + relativedelta(months=+1, days=-1)
        # Last Month
        self.last_month_start = self.month_start + relativedelta(months=-1)
        self.last_month_end = self.month_start + relativedelta(days=-1)

        self.six_months_ago = self.today + relativedelta(months=-6)

        # Year
        self.one_year_ago = self.today + relativedelta(years=-1)
        self.two_years_ago = self.today + relativedelta(years=-2)
        self.month_start_last_year = self.month_start + relativedelta(years=-1)

        self.year_start = datetime(self.today.year, 1, 1)
        self.year_end = datetime(self.today.year, 12, 31)

        self.last_year_start = self.year_start + relativedelta(years=-1)
        self.last_year_end = self.year_end + relativedelta(years=-1)

        # ---- Last Week Report ---- #
        # Sunday Values
        if datetime.today().isoweekday() == 7:
            self.last_week_day_offset_start = -7
            self.last_week_day_offset_end = -1

        # All Other Days - else block will output Sunday - Saturday of previous week
        else:
            self.last_week_day_offset_start = -7 - (datetime.today().isoweekday())
            self.last_week_day_offset_end = -1 - (datetime.today().isoweekday())

        self.last_week_start = self.today + relativedelta(days=self.last_week_day_offset_start)
        self.last_week_end = self.today + relativedelta(days=self.last_week_day_offset_end)
        # ------------------------- #

        # Revenue Report
        # The revenue report will generate revenue data for the past number of weeks and years specified
        self.weeks_to_show = 6
        self.years_to_show = 3

        # Forecasting
        # This report will look at top revenue items during this season of last year (as defined by forecast days)
        # Example: If today is 1/1/24 and forecast days is 45, it will show top earners for 1/1/23 - 2/15/23
        self.forecast_days = 45
        self.low_stock_window = 90
        self.last_year_forecast = self.today + relativedelta(years=-1, days=self.forecast_days)
        self.last_year_low_stock_window = self.today + relativedelta(years=-1, days=self.low_stock_window)

        self.date_format = '%x'

        # SMS Related Dates
        # For regular Coupon
        self.coupon_expiration_day_3 = self.today + relativedelta(weeks=+2, days=-3)
        # For Birthday Coupon - Expires 10th day of following month
        self.birthday_coupon_expiration_day = self.month_start + relativedelta(months=+1, days=+9)

        # Reporting Periods
        self.reporting_periods = {
            'yesterday': {'start': self.yesterday, 'end': self.yesterday},
            'last_week': {'start': self.last_week_start, 'end': self.last_week_end},
        }
