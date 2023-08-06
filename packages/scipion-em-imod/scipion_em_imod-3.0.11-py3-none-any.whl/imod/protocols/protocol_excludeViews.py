# **************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csic.es) [1]
# *
# * [1] Centro Nacional de Biotecnologia, CSIC, Spain
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import math
import imod.utils as utils
from pyworkflow import BETA
import pyworkflow.protocol.params as params
import pyworkflow.utils.path as path
from pyworkflow.object import Set
import tomo.objects as tomoObj
from pwem.emlib.image import ImageHandler
from imod import Plugin
from imod.protocols.protocol_base import ProtImodBase


class ProtImodExcludeViews(ProtImodBase):
    """
    Compute the interpolated tilt-series from its transform matrix.
    More info:
        https://bio3d.colorado.edu/imod/doc/man/excludeviews.html
    """

    _label = 'Exclude views'
    _devStatus = BETA

    excludeViewsInfoMatrix = []

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        form.addSection('Input')
        form.addParam('inputSetOfTiltSeries',
                      params.PointerParam,
                      pointerClass='SetOfTiltSeries',
                      important=True,
                      label='Input set of tilt-series')

        form.addParam('excludeViewsFile',
                      params.FileParam,
                      label='Exclude views file',
                      help='File containing the views to be excluded for each tilt-series belonging to the set.\n\n'
                           'The format of the text file must be two columns, the first one being the tilt series ID of '
                           'the series from which the views will be excluded and the second the views to exclude, '
                           'numbered from 1. The syntax for this exclude list is a comma separated list of ranges with '
                           'no espaces between them (e.g., 1,4-5,60-70). \n\n'
                           'An example of this file comes as follows:\n'
                           'stack1 1,4-6,8,44-47\n'
                           'stack2 3,10-12,24\n'
                           '...')

    # -------------------------- INSERT steps functions ---------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.retrieveInputInformation)

        for ts in self.inputSetOfTiltSeries.get():
            self._insertFunctionStep(self.excludeViewsStep, ts.getObjId())
            self._insertFunctionStep(self.generateOutputStackStep, ts.getObjId())
        self._insertFunctionStep(self.closeOutputSetsStep)

    # --------------------------- STEPS functions ----------------------------
    def retrieveInputInformation(self):
        self.excludeViewsInfoMatrix = utils.readExcludeViewsFile(self.excludeViewsFile.get())

    def excludeViewsStep(self, tsObjId):
        ts = self.inputSetOfTiltSeries.get()[tsObjId]
        tsId = ts.getTsId()

        extraPrefix = self._getExtraPath(tsId)
        path.makePath(extraPrefix)

        firstItem = ts.getFirstItem()
        outputFileName = os.path.join(extraPrefix, firstItem.parseFileName())

        path.copyFile(firstItem.getFileName(), outputFileName)

        position = self.checkPositionTiltSeriesInList(tsId)

        if position != -1:
            paramsAlignment = {
                'stackName': outputFileName,
                'viewsToExclude': self.excludeViewsInfoMatrix[position][1],
            }

            argsAlignment = "-StackName %(stackName)s " \
                            "-ViewsToExclude %(viewsToExclude)s "

            Plugin.runImod(self, 'excludeviews', argsAlignment % paramsAlignment)

    def generateOutputStackStep(self, tsObjId):
        output = self.getOutputSetOfTiltSeries(self.inputSetOfTiltSeries.get())

        ts = self.inputSetOfTiltSeries.get()[tsObjId]
        tsId = ts.getTsId()

        extraPrefix = self._getExtraPath(tsId)

        newTs = tomoObj.TiltSeries(tsId=tsId)
        newTs.copyInfo(ts)
        output.append(newTs)

        position = self.checkPositionTiltSeriesInList(tsId)

        if position != -1:
            excludedViews = self.excludeViewsInfoMatrix[position][1]
            excludedViewsAsList = self.makeExclusionPatternAsList(excludedViews)

        else:
            excludedViewsAsList = []

        for index, tiltImage in enumerate(ts):
            if (index + 1) not in excludedViewsAsList:
                newTi = tomoObj.TiltImage()
                newTi.copyInfo(tiltImage, copyId=True, copyTM=True)
                newTi.setAcquisition(tiltImage.getAcquisition())
                newTi.setLocation(index, (os.path.join(extraPrefix, tiltImage.parseFileName())))
                newTs.append(newTi)

        newTs.write(properties=False)

        output.update(newTs)
        output.updateDim()
        output.write()
        self._store()

    def closeOutputSetsStep(self):
        self.TiltSeries.setStreamState(Set.STREAM_CLOSED)
        self.TiltSeries.write()
        self._store()

    # --------------------------- UTILS functions ----------------------------
    def checkPositionTiltSeriesInList(self, tsId):
        for counter, tsExcludeInfo in enumerate(self.excludeViewsInfoMatrix):

            if tsId == tsExcludeInfo[0]:
                return counter

        return -1

    def makeExclusionPatternAsList(self, excludedViews):
        excludedViewsAsList = []

        vector = excludedViews.split(',')

        for element in vector:
            elementVector = element.split('-')

            if len(elementVector) > 1:
                for i in range(int(elementVector[0]), int(elementVector[1])  + 1):
                    excludedViewsAsList.append(int(i))
            else:
                excludedViewsAsList.append(int(elementVector[0]))

        return excludedViewsAsList

    # --------------------------- INFO functions ----------------------------
    def _summary(self):
        summary = []
        if self.TiltSeries:
            summary.append("Excluded views:\n")

            for tsIn, tsOut in zip(self.inputSetOfTiltSeries.get(), self.TiltSeries):
                summary.append("Tilt-series ID: %s.   Size: %d ----> %d."
                               % (tsIn.getTsId(),
                                  tsIn.getSize(),
                                  tsOut.getSize()))
        else:
            summary.append("Output classes not ready yet.")

        return summary

    def _methods(self):
        methods = []
        if self.TiltSeries:
            methods.append("Excluded views:\n")

            for tsIn, tsOut in zip(self.inputSetOfTiltSeries.get(), self.TiltSeries):
                methods.append("Tilt-series ID: %s.   Size: %d ----> %d."
                               % (tsIn.getTsId(),
                                  tsIn.getSize(),
                                  tsOut.getSize()))
        else:
            methods.append("Output classes not ready yet.")

        return methods
