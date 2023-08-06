import datetime as dt
import json
from typing import Optional, Dict, Union, Iterable

from lumipy import provider as lp
from lumipy.provider import ColumnMeta, ParamMeta
from lumipy.provider.metadata import TableParam
from lumipy.query.expression.sql_value_type import SqlValType


class ParameterAndLimitTestProvider(lp.BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('Name', SqlValType.Text),
            ColumnMeta('StrValue', SqlValType.Text),
            ColumnMeta('Type', SqlValType.Text),
        ]
        params = [
            ParamMeta('Param1', data_type=SqlValType.Int, default_value=0),
            ParamMeta('Param2', data_type=SqlValType.Text, default_value='ABC'),
            ParamMeta('Param3', data_type=SqlValType.Double, default_value=3.1415),
            ParamMeta('Param4', data_type=SqlValType.Date, default_value=dt.datetime(2022, 1, 1, 13, 15, 2)),
            ParamMeta('Param5', data_type=SqlValType.DateTime, is_required=True),
            ParamMeta('Param6', data_type=SqlValType.Boolean, default_value=False),
        ]
        super().__init__('test.pyprovider.params_and_limit', columns=columns, parameters=params)

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Iterable[Dict[str, Union[str, int, float]]]:

        for k, v in params.items():
            yield {
                'Name': k,
                'StrValue': str(v),
                'Type': type(v).__name__,
            }

        yield {'Name': 'limit', 'StrValue': str(limit), 'Type': type(limit).__name__}


class TableParameterTestProvider(lp.BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('TableVarColName', SqlValType.Text),
            ColumnMeta('TableVarColType', SqlValType.Text),
            ColumnMeta('TableVarNumCols', SqlValType.Int),
            ColumnMeta('TableVarNumRows', SqlValType.Int),
        ]
        table_params = [
            TableParam('TestTable')
        ]
        super().__init__('test.pyprovider.tablevar', columns=columns, table_parameters=table_params)

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Iterable[Dict[str, Union[str, int, float]]]:

        df = params['TestTable']

        for n, t in df.dtypes.items():
            yield {
                'TableVarColName': n,
                'TableVarColType': t.name,
                'TableVarNumCols': df.shape[1],
                'TableVarNumRows': df.shape[0],
            }


class FilteringTestProvider(lp.BaseProvider):

    def __init__(self):

        super().__init__(
            'test.pyprovider.filter',
            columns=[
                ColumnMeta('NodeId', SqlValType.Int),
                ColumnMeta('OpName', SqlValType.Text),
                ColumnMeta('Input', SqlValType.Text),
            ]
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Iterable[Dict[str, Union[str, int, float]]]:

        flattened = []

        def flatten(fobj):

            op_name, op_args = fobj['OP'], fobj['EX']
            flattened.append({
                'OpName': op_name,
                'Input': json.dumps(op_args)
            })

            if op_name.endswith('Value'):
                return
            else:
                [flatten(op_arg) for op_arg in op_args]

        flatten(data_filter)

        return [{**d, **{'NodeId': i}} for i, d in enumerate(flattened)]
