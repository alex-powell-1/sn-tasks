import json
import os
import re
import time
import creds
from datetime import datetime, timezone, timedelta
from email.utils import formatdate
import base64
from error_handler import ScheduledTasksErrorHandler
from PIL import Image, ImageOps, ImageDraw, ImageFont
import pytz
from traceback import format_exc as tb
import secrets
import string


def timer(func):
    def wrapper(*args, eh=ScheduledTasksErrorHandler, operation='', **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_taken = time.time() - start_time
        if operation:
            operation = f'{operation}: '

        eh.logger.info(f'{operation}Time taken: {time_taken // 60} minutes, {round(time_taken % 60, 2)} seconds.')
        return result

    return wrapper


def convert_path_to_raw(path):
    """Converts a path to a raw string for use in Windows file paths."""
    return r'{}'.format(path.replace('/', '\\'))


@timer
def generate_random_code(length):
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(length))
    return res


class PhoneNumber:
    def __init__(self, phone_number: str):
        self.raw = phone_number
        if not PhoneNumber.is_valid(self.raw):
            raise ValueError(f'Invalid phone number format. Input: {phone_number}')
        self.stripped = PhoneNumber.strip_number(phone_number)
        self.area_code = self.stripped[0:3]
        self.exchange = self.stripped[3:6]
        self.subscriber_number = self.stripped[6:]

    def __str__(self):
        return f'({self.area_code}) {self.exchange}-{self.subscriber_number}'

    @staticmethod
    def is_valid(phone_number) -> bool:
        """Validates a phone number using regex."""
        pattern = r'(\+\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        if re.match(pattern, phone_number):
            return True

    @staticmethod
    def strip_number(phone_number: str):
        return (
            (phone_number)
            .replace('+1', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
            .replace(' ', '')
            .replace('_', '')
        )

    def to_cp(self):
        return f'{self.area_code}-{self.exchange}-{self.subscriber_number}'

    def to_twilio(self):
        return f'+1{self.area_code}{self.exchange}{self.subscriber_number}'


class Date:
    """Used to parse and convert date strings."""

    formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z']

    def __init__(self, date_string: str, format: str = None):
        self.date_string = date_string

        self.dt: datetime = None
        self.format: str = format

        if format is None:
            for format in Date.formats:
                try:
                    self.dt = datetime.strptime(date_string, format)
                    self.format = format
                    break
                except ValueError:
                    continue
        else:
            try:
                self.dt = datetime.strptime(date_string, format)
            except ValueError:
                raise ValueError(f'Invalid date format: {format}')

    def __str__(self):
        return self.date_string

    # self.tz = self.dt.tzinfo
    @property
    def tz(self):
        return self.dt.tzinfo

    # self.local_dt = self.dt.astimezone(tz=None)
    @property
    def local_dt(self):
        return self.dt.astimezone(tz=None)

    # self.utc_dt = self.dt.astimezone(tz=timezone.utc)
    @property
    def utc_dt(self):
        return self.dt.astimezone(tz=timezone.utc)


class EmailAddress:
    @staticmethod
    def is_valid(email: str) -> bool:
        """Validates an email address using regex."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if re.match(pattern, email):
            return True
        return False


def parse_custom_url(string: str):
    """Uses regular expression to parse a string into a URL-friendly format."""
    return '-'.join(str(re.sub('[^A-Za-z0-9 ]+', '', string)).lower().split(' '))


def get_filesize(filepath):
    try:
        file_size = os.path.getsize(filepath)
    except FileNotFoundError:
        return None
    else:
        return file_size


def scrub(string: str):
    """Sanitize a string for use in filenames."""
    return re.sub('[^A-Za-z0-9 ]+', '', string)


def convert_to_rfc2822(date: datetime):
    return formatdate(int(date.timestamp()))


def convert_to_iso8601(date: datetime, add_tz=True):
    return date.isoformat()


def convert_to_utc(date: datetime):
    return date.astimezone().isoformat()


def local_to_utc(local_dt: datetime):
    return local_dt.astimezone(tz=timezone.utc)


def utc_to_local(utc_dt: datetime):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def convert_utc_to_local(utc_dt: datetime):
    """Used in preorder"""
    """
    Convert a UTC datetime to local time.

    :param utc_dt: The UTC datetime object.
    :param local_tz: The local timezone as a string (e.g., 'America/New_York').
    :return: The local datetime object.
    """
    try:
        # Define the UTC timezone
        # utc = pytz.utc

        # utc_dt = utc.localize(utc_dt)

        # Define the local timezone
        local_timezone = pytz.timezone('America/New_York')

        # Convert the datetime to the local timezone
        local_dt = utc_dt.astimezone(local_timezone)

        # Remove the timezone information
        local_naive_dt = local_dt.replace(tzinfo=None)

        return local_naive_dt

    except Exception as e:
        print(e)
        return None


def make_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')


def country_to_country_code(country):
    country_codes = {'United States': 'US', 'Canada': 'CA', 'Mexico': 'MX', 'United Kingdom': 'GB'}

    return country_codes[country] if country in country_codes else country


def convert_timezone(timestamp, from_zone, to_zone):
    """Convert from UTC to Local Time"""
    start_time = timestamp.replace(tzinfo=from_zone)
    result_time = start_time.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
    return result_time


def pretty_print(response):
    """Takes in a JSON object and returns an indented"""
    print(json.dumps(response, indent=4))


def encode_base64(input_string):
    # Ensure the string is in bytes, then encode it
    encoded_string = base64.b64encode(input_string.encode())
    # Convert the bytes back into a string and return it
    return encoded_string.decode()


def combine_images(
    product_image_path,
    barcode_image_path,
    combined_image_path=None,
    padding=100,
    barcode_text=None,
    expires_text=None,
):
    # Open the product and barcode images
    product_image = Image.open(product_image_path)
    barcode_image = Image.open(barcode_image_path)

    # Get the width of the wider image
    target_width = max(product_image.width, barcode_image.width)

    # Scale images to have the same width
    if product_image.width != target_width:
        product_image = product_image.resize(
            (target_width, int(product_image.height * target_width / product_image.width))
        )
    if barcode_image.width != target_width:
        barcode_image = barcode_image.resize(
            (target_width, int(barcode_image.height * target_width / barcode_image.width))
        )

    target_width = target_width + 2 * padding

    # Add padding around the images
    product_image = ImageOps.expand(product_image, border=padding, fill='white')
    barcode_image = ImageOps.expand(barcode_image, border=padding, fill='white')

    # Calculate combined height with margin between images
    combined_height = product_image.height + barcode_image.height

    global curr_height
    curr_height = combined_height

    def add_text(text, size):
        size *= 2

        def textsize(text, font):
            im = Image.new(mode='P', size=(0, 0))
            draw = ImageDraw.Draw(im)
            _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
            return width, height

        # Add small centered text under the barcode
        # draw = ImageDraw.Draw(combined_image)
        font = ImageFont.load_default()
        font = font.font_variant(size=size)
        text = text  # Replace with desired text
        text_width, text_height = textsize(text, font=font)
        text_x = (target_width - text_width) // 2

        global curr_height
        text_y = curr_height
        curr_height = curr_height + text_height + (padding // 2)

        def draw_text(fill='black'):
            draw = ImageDraw.Draw(combined_image)
            draw.text((text_x, text_y), text, font=font, fill=fill)

        return draw_text

    if barcode_text is not None:
        draw_code_text = add_text(barcode_text, size=64)

    if expires_text is not None:
        draw_expires_text = add_text(expires_text, size=50)

    # Create a new image for combined output
    combined_image = Image.new('RGB', (target_width, curr_height + padding // 2), 'white')

    # Paste product image and barcode image into the combined image
    combined_image.paste(product_image, (0, 0))
    combined_image.paste(barcode_image, (0, product_image.height))

    if barcode_text is not None:
        draw_code_text()

    if expires_text is not None:
        draw_expires_text()

    if combined_image_path is not None:
        combined_image.save(combined_image_path)

    return combined_image


def delete_old_files(directory=None, days=14, eh=ScheduledTasksErrorHandler):
    """Delete files older than a specified number of days. If no directory is specified, all directories in the Logs
    class will be checked."""
    cut_off_dt = datetime.now() - timedelta(days=days)

    def delete_helper(directory):
        for f in os.listdir(directory):
            last_modified_dt = datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, f)))
            if last_modified_dt < cut_off_dt and f.endswith('.log'):
                try:
                    os.remove(os.path.join(directory, f))
                    pass
                except Exception as e:
                    eh.error_handler.add_error(
                        f'Error deleting file.{e}', origin='delete_old_files', traceback=tb()
                    )
                else:
                    eh.logger.info(f'Deleted file: {directory}/{f}')

    if directory is None:
        for x in creds.Logs.__dict__:
            if not x.startswith('__'):
                delete_helper(creds.Logs.__dict__[x])
    else:
        delete_helper(directory)


states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
if '__main__' == __name__:
    print(generate_random_code(8))
