import os
from icmplib import ping
import requests
from sms_engine import SMSEngine
import creds
from datetime import datetime
from error_handler import ScheduledTasksErrorHandler as error_handler

hosts = ['https://www.google.com/', '1.1.1.1', '8.8.8.8']


def check_for_connection(hostname: str):
    host = ping(hostname, count=5, interval=0.2)
    if host.packets_sent == host.packets_received:
        error_handler.logger.info(f'{hostname} is connected.')
    else:
        error_handler.logger.warn(f'{hostname} is not connected.')
    return host.packets_sent == host.packets_received


def restart_server_if_disconnected():
    error_handler.logger.info(f'Business Automation Health Check: Starting at {datetime.now():%H:%M:%S}')
    if not check_for_connection(hosts[0]) and check_for_connection(hosts[1]) and check_for_connection(hosts[2]):
        error_handler.logger.warn('No Internet Connection. Rebooting.')
        os.system('shutdown -t 2 -r -f')
    else:
        error_handler.logger.info('Server is connected to internet. Will continue.')
        error_handler.logger.info(f'Business Automation Health Check: Completed at {datetime.now():%H:%M:%S}')


def health_check():
    url = f'{creds.API.endpoint}'
    response = requests.get(url=url)
    if response.status_code != 200:
        error_handler.logger.warn(f'HTTP Server is not running. Restart the server: {creds.API.server_name}')
        SMSEngine.send_text(
            origin='SERVER',
            campaign='Health Check',
            to_phone=creds.Company.network_notification_phone,
            message=f'{creds.API.endpoint} is not running. Restart the server.',
        )
    else:
        error_handler.logger.info(f'HTTP Server is running: {creds.API.server_name}')


if __name__ == '__main__':
    health_check()
