# Author: Stephane CREMEL <stephane.cremel@gmail.com>
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



import os
import subprocess

import sickbeard

from sickbeard import logger
from sickbeard import encodingKludge as ek
from sickbeard.exceptions import ex
from email.mime.text import MIMEText
import smtplib

class MailNotifier:

    def test_notify(self, mail_from=None, mail_to=None, mail_server=None, mail_ssl=None, mail_username=None, mail_password=None):
        return self._notifyMail("This is a test notification from SickBeard", "SickBeard message", mail_from, mail_to,mail_server,mail_ssl,mail_username,mail_password)

    def notify_snatch(self, ep_name):
        if sickbeard.MAIL_NOTIFY_ONSNATCH:
            logger.log("Notification MAIL SNATCH", logger.DEBUG)
            message = str(ep_name)
            return self._notifyMail("SickBeard Snatch", message, None, None, None, None, None, None)
        else:
            return

    def notify_download(self, ep_name):
        
        if not sickbeard.USE_MAIL:
            return False
        
        logger.log("Notification MAIL DOWNLOAD", logger.DEBUG)
        message = str(ep_name)
        return self._notifyMail("SickBeard Download", message, None, None, None, None, None, None)
    
    def notify_subtitle_download(self, ep_name, lang):
        pass


    def _notifyMail(self, title, message, mail_from=None, mail_to=None, mail_server=None, mail_ssl=None, mail_username=None, mail_password=None):
        
        if not sickbeard.USE_MAIL:
            logger.log("Notification for Mail not enabled, skipping this notification", logger.DEBUG)
            return False

        logger.log("Sending notification Mail", logger.DEBUG)
        
        if not mail_from:
            mail_from = sickbeard.MAIL_FROM
        if not mail_to:
            mail_to = sickbeard.MAIL_TO
        if not mail_ssl:
            mail_ssl = sickbeard.MAIL_SSL
        if not mail_server:
            mail_server = sickbeard.MAIL_SERVER
        if not mail_username:
            mail_username = sickbeard.MAIL_USERNAME
        if not mail_password:
            mail_password = sickbeard.MAIL_PASSWORD                    

        if mail_ssl :
            mailserver = smtplib.SMTP_SSL(mail_server)
        else:
            mailserver = smtplib.SMTP(mail_server)
       
        if len(mail_username) > 0:
            mailserver.login(mail_username, mail_password)
        
        message = MIMEText(message)
        message['Subject'] = title
        message['From'] = mail_from
        message['To'] = mail_to
        
        mailserver.sendmail(mail_from,mail_to,message.as_string())
        
        return True

notifier = MailNotifier
