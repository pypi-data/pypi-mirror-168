from typing import Iterable, Optional, Dict, Union

import numpy as np
import pandas as pd
from cvxopt import matrix, solvers
from sklearn.covariance import empirical_covariance

from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.query.expression.sql_value_type import SqlValType


class QuadraticProgram(BaseProvider):
    """This provider calculates weights for a collection of securities given a table of returns data. It does this by
    solving the following quadratic program

        min_w  \lambda w^T \Sigma w - \mu w

    where \Sigma is the covariance matrix of the returns series, \mu is the mean returns vector, w is the weights
    vector.

    """

    def __init__(self):

        columns = [
            ColumnMeta('Symbol', SqlValType.Text, "Symbol that labels the security (i.e. a stock ticker)"),
            ColumnMeta('Weight', SqlValType.Double, "Weight assigned by the quadratic optimisation."),
        ]
        parameters = [
            ParamMeta(
                'Lam',
                SqlValType.Double,
                "Scaling parameter on the quadratic part of the objective. Sets the tradeoff between risk and returns.",
                is_required=True,
            )
        ]
        table_parameters = [
            TableParam(
                'Returns',
                columns=[
                    ColumnMeta('Symbol', SqlValType.Text),
                    ColumnMeta('Date', SqlValType.Date),
                    ColumnMeta('Price', SqlValType.Double),
                    ColumnMeta('Timedelta', SqlValType.Int),
                    ColumnMeta('Returns', SqlValType.Double)
                ],
                description='A table of returns data to use in the quadratic program.'
            )
        ]

        super().__init__(
            name='Tools.Index.Quadratic.Program',
            columns=columns,
            parameters=parameters,
            table_parameters=table_parameters,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Iterable[Dict[str, Union[str, int, float]]]:

        df = params.get('Returns')
        lam = params.get('Lam')

        if df is None or lam is None:
            raise ValueError('You must specify both the scaling parameter (Lam) and a table of returns (Returns).')

        if df.shape[0] == 0:
            raise ValueError('Input table variable was empty.')

        df['Date'] = pd.to_datetime(df.Date)
        df = df.sort_values('Date')
        df = df.set_index('Date')

        rdf = pd.DataFrame({s: sdf.Returns for s, sdf in df.groupby('Symbol')}).astype(float)

        cov_mat = empirical_covariance(rdf.values)
        avg_ret = rdf.values.mean(axis=0)

        n = len(avg_ret)

        Q = matrix(lam * cov_mat)
        p = matrix(-avg_ret)

        G = matrix(np.vstack([np.diag([1.0] * n), np.diag([-1.0] * n)]))
        h = matrix([1.0] * n + [0.0] * n)

        A = matrix([1.0] * n, (1, n))
        b = matrix(1.0)

        sol = solvers.qp(Q, p, G, h, A, b)

        wdf_qp = pd.DataFrame({
            'Symbol': [c.split('_')[0] for c in rdf.columns],
            'Weight': np.array(sol['x']).flatten()
        }).sort_values(
            'Weight', ascending=False
        ).reset_index(drop=True)

        return map(lambda x: x[1].to_dict(), wdf_qp.iterrows())
