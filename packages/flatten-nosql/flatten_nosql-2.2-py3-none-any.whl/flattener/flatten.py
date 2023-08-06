"""Flatten NoSQL data to SQL"""

import pandas as pd


class Flattener:
    """Flattener class"""

    _HAS_SUBFIELD_LIST = 1
    _HAS_SUBFIELD_DICT = 2
    _HAS_NO_SUBFIELD = 3
    _HAS_NO_SUBFIELD_BUT_ITERABLE = 4
    _need_flattening = [
        _HAS_SUBFIELD_DICT,
        _HAS_SUBFIELD_LIST,
    ]

    def _check_subfield(self, obj):

        if isinstance(obj, dict):
            return self._HAS_SUBFIELD_DICT
        if isinstance(obj, list):
            if len(obj) < 1:
                return self._HAS_NO_SUBFIELD
            if isinstance(obj[0], dict):
                return self._HAS_SUBFIELD_LIST
            return self._HAS_NO_SUBFIELD_BUT_ITERABLE
        return self._HAS_NO_SUBFIELD

    def _has_subfield(self, obj):

        status = self._check_subfield(obj)
        return status in [self._HAS_SUBFIELD_LIST, self._HAS_SUBFIELD_DICT]

    def _get_types(self, data: pd.DataFrame, check_rows=100):

        types = {}
        rows = data.to_numpy()
        columns = data.columns.tolist()
        for row in rows[:check_rows]:
            for i, cell in enumerate(row):
                tmp = self._check_subfield(cell)
                if columns[i] in types:
                    types[columns[i]] = min(types[columns[i]], tmp)
                else:
                    types[columns[i]] = tmp
        return types

    def _flatten(self, data: pd.DataFrame, depth: int = 0, depth_cur: int = 0, sep: str = "."):
        if isinstance(data, dict):
            data = pd.json_normalize(data)
        elif isinstance(data, pd.DataFrame):
            data = pd.json_normalize(
                data=data.to_dict("records"),
                sep=sep,
            )
        else:
            raise ValueError(
                "Either dictionary (JSON) or dataframe (array of JSON) objects are supported"
            )
        if depth_cur != depth_cur:
            raise ValueError("Current depth has to be an integer")
        if depth != depth:
            raise ValueError("Max depth has to be an integer")
        if not isinstance(depth, int):
            raise ValueError("Max depth has to be an integer")
        if not isinstance(depth_cur, int):
            raise ValueError("Depth has to be an integer")
        if depth <= depth_cur:
            return data
        data["_ID_"] = [i + 1 for i in range(data.shape[0])]
        types = self._get_types(data)
        columns = data.columns.tolist()
        df_flat = data
        num_flat = 0
        for col in columns:
            if types[col] in self._need_flattening:
                records = df_flat.to_dict("records")
                df_flat = df_flat.drop(col, axis=1)
                cur_flat = pd.json_normalize(
                    records,
                    record_path=col,
                    meta="_ID_",
                    record_prefix=col + sep,
                )
                df_flat = pd.merge(
                    left=df_flat,
                    right=cur_flat,
                    left_on=[
                        "_ID_",
                    ],
                    right_on=[
                        "_ID_",
                    ],
                    how="outer",
                )
            else:
                num_flat += 1
        df_flat = df_flat.drop(
            "_ID_",
            axis=1,
        )
        if num_flat == data.shape[1]:
            return df_flat
        else:
            return self.flatten(df_flat, depth, depth_cur + 1)

    def flatten(self, data: pd.DataFrame, depth: int = 0, sep: str = "."):
        """Flatten dataframe `data`.

        :param data: Pandas dataframe containing data to flatten.
        :type data: `pd.DataFrame`
        :param depth: How deep the flattening should be done, defaults to 0
        :type depth: `int`, optional
        :param sep: Separator for flattened columns, defaults to "."
        :type sep: `str`, optional
        :return: Flattened dataframe.
        :rtype: `pd.DataFrame`
        """

        return self._flatten(
            data=data,
            depth=depth,
            depth_cur=0,
            sep=sep,
        )
