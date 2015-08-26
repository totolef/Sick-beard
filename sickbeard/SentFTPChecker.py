# Author: Arnaud Dartois
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.
import time
import os
import sickbeard
import ftplib as ftp
import glob

from sickbeard import logger

class SentFTPChecker():
    def run(self):
        if sickbeard.USE_TORRENT_FTP:
                # upload all torrent file to remote FTP
                logger.log("Sending torrent file to FTP", logger.DEBUG)
                self._sendToFTP("*.torrent", sickbeard.TORRENT_DIR)

    def _sendToFTP(self, filter, dir):
        """
        Send all of the specified filtered files (eg "*.torrent") to the appropriate FTP.

        """
        iCount = self.count_files(dir, filter)
        logger.log(u"Files Found (" + filter + "): " + str(iCount), logger.DEBUG)

        if (iCount>0):
            MyFTP = ftp.FTP()

            logger.log(u"Initializing FTP Session", logger.DEBUG)
            MyFTP.connect(sickbeard.FTP_HOST, sickbeard.FTP_PORT, sickbeard.FTP_TIMEOUT)

            # Connect to the FTP server
            MyFTP.login(sickbeard.FTP_LOGIN, sickbeard.FTP_PASSWORD, '')

            # Assign passive mode
            logger.log(u"Assign Session Passive Mode", logger.DEBUG)
            MyFTP.set_pasv(sickbeard.FTP_PASSIVE)

            # change remote directory
            try:
                logger.log(u"Set Remote Directory : %s" % sickbeard.FTP_DIR, logger.DEBUG)
                MyFTP.cwd(sickbeard.FTP_DIR)
            except Exception, e:
                logger.log(u"Change directory failed :" + e.message, logger.ERROR)

            for fileName in glob.glob(os.path.join(dir,filter)):

                file_handler = open(fileName, 'rb')

                # Send the file
                logger.log(u"Send local file : " + fileName, logger.DEBUG)
                MyFTP.set_debuglevel(1)
                MyFTP.storbinary('STOR %s' % os.path.basename(fileName), file_handler)
                MyFTP.set_debuglevel(0)
                file_handler.close()

                # delete local file after uploading
                logger.log(u"Deleting local file : " + fileName, logger.DEBUG)
                os.remove(fileName)

            # Close FTP session
            logger.log(u"Close FTP Session", logger.DEBUG)
            MyFTP.quit()

            logger.log(u"It's working ... hop a beer !", logger.DEBUG)
        else:
            logger.log(u"No local files found.", logger.DEBUG)

    def count_files(self, path, filter):
        list_dir = []
        list_dir = os.listdir(path)
        count = 0
        for file in glob.glob(os.path.join(path,filter)):
            count += 1
        return count
