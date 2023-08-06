# Author: Salyl Bhagwat, Gammath Works
# Copyright (c) 2021-2022, Salyl Bhagwat, Gammath Works
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = 'Salyl Bhagwat'
__copyright__ = 'Copyright (c) 2021-2022, Salyl Bhagwat, Gammath Works'

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import (mean_squared_error, r2_score, make_scorer)
from sklearn.model_selection import (TimeSeriesSplit, GridSearchCV)
from sklearn.preprocessing import (StandardScaler, minmax_scale)
from sklearn.linear_model import (Lasso, Ridge, BayesianRidge, SGDRegressor)
from sklearn.pipeline import make_pipeline

try:
    from gammath_spot import gammath_mi_scores as gmis
except:
    import gammath_mi_scores as gmis

try:
    from gammath_spot import gammath_lpep as lpep
except:
    import gammath_lpep as lpep

#This is experimental and a WIP.
def get_root_mean_squared_error(y_true, y_pred):
    return (np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred)))

def main():
    tsymbol = sys.argv[1]
    path = Path(f'tickers/{tsymbol}')
    df = pd.read_csv(path / f'{tsymbol}_history.csv')

    gscores = pd.read_csv(path / f'{tsymbol}_micro_gscores.csv', index_col='Unnamed: 0')
    try:
        mi_scores_regr, mi_scores_classif = gmis.get_mi_scores(gscores)
        print(f'Regressor: \n{mi_scores_regr.sort_values()}')
        print(f'Classifier: \n{mi_scores_classif.sort_values()}')
    except:
        print('\nERROR: mi scores for symbol ', tsymbol, ': ', sys.exc_info()[0])

    gscores_scaled = gscores.drop('Date', axis=1).apply(minmax_scale)
    print(gscores_scaled)

#    tss = TimeSeriesSplit(n_splits=249)
#    tss.split(gscores)

    pep = lpep.GPEP()
    pep.get_moving_price_estimated_projection('SP500')

if __name__ == '__main__':
    main()
