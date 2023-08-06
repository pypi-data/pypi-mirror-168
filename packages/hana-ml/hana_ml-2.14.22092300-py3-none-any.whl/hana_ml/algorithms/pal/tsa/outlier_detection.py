"""
This module contains Python wrapper for PAL time series outlier detection algorithm.

The following function is available:

    * ：class：`OutlierDetectionTS`
"""
#pylint:disable=line-too-long, too-many-arguments, too-few-public-methods
#pylint: disable=invalid-name, unused-argument, too-many-locals, too-many-statements
#pylint: disable=attribute-defined-outside-init, unused-variable
#pylint: disable=too-many-branches, c-extension-no-member, consider-using-f-string
import logging
import uuid
import warnings

try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from hana_ml.dataframe import quotename
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    ParameterTable,
    pal_param_register,
    try_drop
)
from hana_ml.algorithms.pal.tsa.arima import _convert_index_from_timestamp_to_int, _is_index_int

from hana_ml.algorithms.pal.sqlgen import trace_sql
logger = logging.getLogger(__name__)

class OutlierDetectionTS(PALBase):#pylint:disable=too-many-instance-attributes
    r"""
    Python class for outlier detection in time-series. It is a wrapper of PAL procedure
    **PAL_OUTLIER_DETECTION_FOR_TIME_SERIES**.

    ParameterTable
    --------------
    window_size : int, optional
        Odd number, the window size for median filter, not less than 3.

        Defaults to 3.

    outlier_method : str, optional

        The method for calculate the outlier score from residual.

          - 'z1' : Z1 score.
          - 'z2' : Z2 score.
          - 'iqr' : IQR score.
          - 'mad' : MAD score.

        Defaults to 'z1'.

    threshold : float, optional
        The threshold for outlier score. If the absolute value of outlier score is beyond the
        threshold, we consider the corresponding data point as an outlier.

        Defaults to 3.

    detect_seasonality : bool, optional
        When calculating the residual,

        - False: Does not consider the seasonal decomposition.
        - True: Considers the seasonal decomposition.

        Defaults to False.

    alpha : float, optional
        The criterion for the autocorrelation coefficient. The value range is (0, 1).

        A larger value indicates a stricter requirement for seasonality.

        Only valid when ``detect_seasonality`` is True.

        Defaults to 0.2.

    periods : int, optional
        When this parameter is not specified, the algorithm will search the seasonal period.
        When this parameter is specified between 2 and half of the series length, autocorrelation value
        is calculated for this number of periods and the result is compared to ``alpha`` parameter.
        If correlation value is equal to or higher than ``alpha``, decomposition is executed with the value of ``periods``.
        Otherwise, the residual is calculated without decomposition. For other value of parameter ``periods``,
        the residual is also calculated without decomposition.

        No Default value.

    thread_ratio : float, optional
        The ratio of available threads.

          - 0: single thread.
          - 0~1: percentage.
          - Others: heuristically determined.

        Only valid when ``detect_seasonality`` is True.

        Defaults to -1.

    Attributes
    ----------
    stats_ : DataFrame
        Data statistics related to time-series outlier detection, structured as follows:
            - STAT_NAME : Name of statistics.
            - STAT_VALUE : Value of statistics.

    metrics_ : DataFrame
        Relevent metrics for time-series outlier detection, structured as follows:
            - NAME : Metric name.
            - VALUE : Metric value.


    Examples
    --------
    Time series DataFrame df:

    >>> df.collect().head()
        ID  RAW_DATA
    0    1       2.0
    1    2       2.5
    2    3       3.2
    3    4       2.8
    ......
    14  15       5.3
    15  16      10.0
    16  17       4.6
    17  18       4.4
    18  19       4.8
    19  20       5.1

    Initialize the class:

    >>> tsod = OutlierDetectionTS(detect_seasonality=False,
                                  outlier_method='z1',
                                  window_size=3,
                                  threshold=3.0)
    >>> res = tsod.fit_predict(data=df,
                               key='ID',
                               endog='RAW_DATA')


    Outputs and attributes:

    >>> res.collect()
        TIMESTAMP  RAW_DATA  RESIDUAL  OUTLIER_SCORE  IS_OUTLIER
    0           1       2.0       0.0      -0.297850           0
    1           2       2.5       0.0      -0.297850           0
    2           3       3.2       0.4      -0.010766           0
    ......
    13         14       5.1       0.0      -0.297850           0
    14         15       5.3       0.0      -0.297850           0
    15         16      10.0       4.7       3.075387           1
    16         17       4.6       0.0      -0.297850           0
    17         18       4.4      -0.2      -0.441392           0
    18         19       4.8       0.0      -0.297850           0
    19         20       5.1       0.0      -0.297850           0

    >>> tsod.stats_.collect()
                STAT_NAME STAT_VALUE
    0  DETECT_SEASONALITY          0
    1          OutlierNum          1
    2                Mean      0.415
    3  Standard Deviation    1.39332
    4          HandleZero          0

    """
    method_map = {'z1':0, 'z2':1, 'iqr':2, 'mad':3}
    def __init__(self,
                 window_size=None,
                 detect_seasonality=None,
                 alpha=None,
                 periods=None,
                 outlier_method=None,
                 threshold=None):
        if not hasattr(self, 'hanaml_parameters'):
            setattr(self, 'hanaml_parameters', pal_param_register())
        super().__init__()
        self.window_size = self._arg('window_size', window_size, int)
        self.detect_seasonality = self._arg('detect_seasonality', detect_seasonality, bool)
        self.alpha = self._arg('alpha', alpha, float)
        self.periods = self._arg('periods', periods, int)
        self.outlier_method = self._arg('outlier_method', outlier_method, self.method_map)
        self.threshold = self._arg('threshold', threshold, float)
        self.op_name = 'Outlier'
        stats_ = None
        metrics_ = None
        self.is_index_int = None

    @trace_sql
    def fit_predict(self, data, key=None, endog=None):
        r"""
        Detection of outliers in time-series data.

        Parameters
        ----------

        data : DataFrame

            Input data containing the target time-series.

            ``data`` should have at least two columns: one is ID column,
            the other is raw data.

        key : str, optional
            Specifies the ID column, in this case the column that shows the order
            of time-series.

            It is recommended that you always specifies this column manually.

            Defaults to the first column of data if the index column of data is not provided.
            Otherwise, defaults to the index column of data.

        endog : str, optional
            Specifies the column that contains the values of time-series to be tested.

            Defaults to the first non-key column.

        Returns
        -------
        DataFrame
            Outlier detection result, structured as follows:
                - TIMESTAMP : ID of data.
                - RAW_DATA : Original value.
                - RESIDUAL : Residual.
                - OUTLIER_SCORE : Outlier score.
                - IS_OUTLIER : 0: normal, 1: outlier.

        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        conn = data.connection_context
        key = self._arg('key', key, str)
        endog = self._arg('endog', endog, str)
        if not self._disable_hana_execution:
            cols = data.columns
            if len(cols) < 2:
                msg = ("Input data should contain at least 2 columns: " +
                       "one for ID, another for raw data.")
                logger.error(msg)
                raise ValueError(msg)
            if key is not None and key not in cols:
                msg = ('Please select key from name of columns!')
                logger.error(msg)
                raise ValueError(msg)
            index = data.index
            if index is not None:
                if key is None:
                    if not isinstance(index, str):
                        key = cols[0]
                        warn_msg = ("The index of data is not a single column and key is None, " +
                        "so the first column of data is used as key!")
                        warnings.warn(message=warn_msg)
                    else:
                        key = index
                else:
                    if key != index:
                        warn_msg = "Discrepancy between the designated key column '{}' ".format(key) +\
                        "and the designated index column '{}'.".format(index)
                        warnings.warn(message=warn_msg)
            else:
                if key is None:
                    key = cols[0]
            cols.remove(key)
            if endog is not None:
                if endog not in cols:
                    msg = 'Please select endog from name of columns!'
                    logger.error(msg)
                    raise ValueError(msg)
            else:
                endog = cols[0]
            data_ = data[[key] + [endog]]
            self.is_index_int = _is_index_int(data_, key)
            if not self.is_index_int:
                max_ = data.select(key).max()
                min_ = data.select(key).min()
                delta = (max_ - min_) / (data.count() - 1)
                timedelta = delta.total_seconds()
                forecast_start = min_
                data_ = _convert_index_from_timestamp_to_int(data_, key)
        else:
            data_ = data
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['RESTULT', 'STATS', 'METRICS']
        outputs = ['#PAL_TS_OUTLIER_{}_TBL_{}_{}'.format(name, self.id, unique_id) for name in outputs]
        res_tbl, stats_tbl, metrics_tbl = outputs
        param_rows = [('WINDOW_SIZE', self.window_size, None, None),
                      ('DETECT_SEASONALITY', self.detect_seasonality, None, None),
                      ('ALPHA', None, self.alpha, None),
                      ('PERIODS', self.periods, None, None),
                      ('OUTLIER_METHOD', self.outlier_method, None, None),
                      ('THRESHOLD', None, self.threshold, None)]
        try:
            if check_pal_function_exist(conn, '%OUTLIERDETECTIONFORTIMESERIES%', like=True):
                self._call_pal_auto(conn,
                                    'PAL_OUTLIER_DETECTION_FOR_TIME_SERIES',
                                    data_,
                                    ParameterTable().with_data(param_rows),
                                    *outputs)
            else:
                msg = 'The version of your SAP HANA does not support the outlier detection for time series!'
                logger.error(msg)
                raise ValueError(msg)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, outputs)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, outputs)
        self.stats_ = conn.table(stats_tbl)
        self.metrics_ = conn.table(metrics_tbl)
        if not self._disable_hana_execution:
            if not self.is_index_int:
                columns = conn.table(res_tbl).columns
                return conn.sql("""
                                SELECT ADD_SECONDS('{0}', ({1} - 1) * {2}) AS {8},
                                {3},
                                {4},
                                {5},
                                {6}
                                FROM {7}
                                """.format(forecast_start,
                                           quotename(columns[0]),
                                           timedelta,
                                           quotename(columns[1]),
                                           quotename(columns[2]),
                                           quotename(columns[3]),
                                           quotename(columns[4]),
                                           res_tbl,
                                           quotename(key)))
        return conn.table(res_tbl)
