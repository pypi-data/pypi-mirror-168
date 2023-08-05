"""
Summary.

    Local Filesytem Operations

Module Functions:
    - clear_directory:  Cleans all file objects from a directory on local
                        filesystem given as a parameter.

"""
import os
from shutil import rmtree
from libtools import logger



def clear_directory(directory):
    """
        Clear contents of fs directory provided as parameter.
        Will not alter directory name or objects external to
        directory given as a parameter.

    Returns:
        TYPE:  Boolean, Success (dir empty) || Failure (dir not empty)

    """
    try:
        for x in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, x)):
                rmtree(os.path.join(directory, x))
                logger.info('Removed directory %s' % x)
            elif os.path.isfile(os.path.join(directory, x)):
                os.remove(os.path.join(directory, x))
                logger.info('Removed file %s' % x)
    except Exception:
        #logger.warning('%s Directory not found.  Error code %s' % x, sys.exit(exit_codes['E_MISC']['Code']))
        logger.warning('Directory object not found.')
        return False
    return True
