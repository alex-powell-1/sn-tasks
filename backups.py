import errno
import shutil
from datetime import datetime

import creds
from error_handler import ScheduledTasksErrorHandler as error_handler


def offsite_backups():
    error_handler.logger.info(f'Offsite Backups: Starting at {datetime.now():%H:%M:%S}')

    backups = {
        'configuration': {
            'src': creds.Backups.Config.source,
            'dst': f'{creds.Backups.Config.destination}_{datetime.now():%m_%d_%y}',
        }
    }

    for backup in backups:
        error_handler.logger.info(f'Starting Backup for {backup}')
        try:
            # For Folders
            shutil.copytree(backups[backup]['src'], backups[backup]['dst'])
        except OSError as exc:
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                # For Files
                shutil.copy(backups[backup]['src'], backups[backup]['dst'])
            else:
                error_handler.error_handler.add_error_v(error=f'OSError: {exc}', origin='offsite_backups OSError')
        except Exception as err:
            error_handler.error_handler.add_error_v(error=f'Error: {err}', origin='offsite_backups Exception')
            continue
        else:
            error_handler.logger.success(f'Finished Backup for {backup}')

    error_handler.logger.info(f'Offsite Backups: Finished at {datetime.now():%H:%M:%S}')
