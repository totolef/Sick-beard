# Author: Nic Wolfe <nic@wolfeden.ca>
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

import os.path

import sickbeard

from sickbeard import logger
from sickbeard import encodingKludge as ek
from sickbeard import processTV

class PostProcesser():
    
    def __init__(self, dir):
        self.processorDir = dir

    def run(self):

        if not ek.ek(os.path.isdir, self.processorDir):
            logger.log(u"Automatic post-processing attempted but dir "+self.processorDir+" doesn't exist", logger.ERROR)
            return

        if not ek.ek(os.path.isabs, self.processorDir):
            logger.log(u"Automatic post-processing attempted but dir "+self.processorDir+" is relative (and probably not what you really want to process)", logger.ERROR)
            return

        processTV.processDir(self.processorDir)
