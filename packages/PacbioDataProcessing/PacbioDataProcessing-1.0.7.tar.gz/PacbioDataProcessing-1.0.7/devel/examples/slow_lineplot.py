#######################################################################
#
# Copyright (C) 2022 David Palao
#
# This file is part of PacBioDataProcessing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import numpy as np
import seaborn as sns
from pandas import DataFrame
from matplotlib import pyplot as plt


N = 1000000
x = np.random.randint(0, high=10000000000, size=N)
y = np.random.random(N)
df = DataFrame({"x": x, "y": y})

print(f"Using seaborn-{sns.__version__}:")

plot = sns.lineplot(data=df, x="x", y="y", ci=None)


# $ time python devel/examples/slow_lineplot.py
# Using seaborn-0.12.0:
# /home/palao/programming/PacbioDataProcessing/devel/examples/slow_lineplot.py:35: FutureWarning:

# The `ci` parameter is deprecated. Use `errorbar=None` for the same effect.

#   plot = sns.lineplot(

# real    7m9,201s
# user    7m7,049s
# sys     0m2,920s

# $ time python devel/examples/slow_lineplot.py
# Using seaborn-0.11.2:

# real    0m3,046s
# user    0m3,302s
# sys     0m1,603s
