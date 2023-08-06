#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pyspark.ml.param import *
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters
from ai.h2o.sparkling.ml.params.HasIgnoredCols import HasIgnoredCols


class H2OExtendedIsolationForestParams(HasIgnoredCols, Params):

    ##
    # Param definitions
    ##
    ntrees = Param(
        Params._dummy(),
        "ntrees",
        """Number of Extended Isolation Forest trees.""",
        H2OTypeConverters.toInt())

    sampleSize = Param(
        Params._dummy(),
        "sampleSize",
        """Number of randomly sampled observations used to train each Extended Isolation Forest tree.""",
        H2OTypeConverters.toInt())

    extensionLevel = Param(
        Params._dummy(),
        "extensionLevel",
        """Maximum is N - 1 (N = numCols). Minimum is 0. Extended Isolation Forest with extension_Level = 0 behaves like Isolation Forest.""",
        H2OTypeConverters.toInt())

    seed = Param(
        Params._dummy(),
        "seed",
        """Seed for pseudo random number generator (if applicable)""",
        H2OTypeConverters.toInt())

    modelId = Param(
        Params._dummy(),
        "modelId",
        """Destination id for this model; auto-generated if not specified.""",
        H2OTypeConverters.toNullableString())

    categoricalEncoding = Param(
        Params._dummy(),
        "categoricalEncoding",
        """Encoding scheme for categorical features""",
        H2OTypeConverters.toEnumString("hex.Model$Parameters$CategoricalEncodingScheme"))

    ignoreConstCols = Param(
        Params._dummy(),
        "ignoreConstCols",
        """Ignore constant columns.""",
        H2OTypeConverters.toBoolean())

    ##
    # Getters
    ##
    def getNtrees(self):
        return self.getOrDefault(self.ntrees)

    def getSampleSize(self):
        return self.getOrDefault(self.sampleSize)

    def getExtensionLevel(self):
        return self.getOrDefault(self.extensionLevel)

    def getSeed(self):
        return self.getOrDefault(self.seed)

    def getModelId(self):
        return self.getOrDefault(self.modelId)

    def getCategoricalEncoding(self):
        return self.getOrDefault(self.categoricalEncoding)

    def getIgnoreConstCols(self):
        return self.getOrDefault(self.ignoreConstCols)

    ##
    # Setters
    ##
    def setNtrees(self, value):
        return self._set(ntrees=value)

    def setSampleSize(self, value):
        return self._set(sampleSize=value)

    def setExtensionLevel(self, value):
        return self._set(extensionLevel=value)

    def setSeed(self, value):
        return self._set(seed=value)

    def setModelId(self, value):
        return self._set(modelId=value)

    def setCategoricalEncoding(self, value):
        return self._set(categoricalEncoding=value)

    def setIgnoreConstCols(self, value):
        return self._set(ignoreConstCols=value)
