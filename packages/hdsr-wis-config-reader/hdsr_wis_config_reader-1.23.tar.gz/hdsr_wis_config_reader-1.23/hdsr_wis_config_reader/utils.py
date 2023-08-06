from pathlib import Path
from typing import List
from typing import Union

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


class PdReadFlexibleCsv:
    def __init__(
        self,
        path: Union[str, Path],
        sep: str = None,
        expected_columns: List[str] = None,
        parse_dates: List[str] = None,
    ):
        self.path_str = self._get_path(path=path)
        self.date_columns = parse_dates
        self.separators = self._get_separators(sep=sep)
        self.expected_columns = expected_columns
        self.df = self._get_df()
        self.is_http_file = None

    def _get_path(self, path: Union[str, Path]) -> str:
        if isinstance(path, str) and ("http" in path or Path(path).is_file()):
            self.is_http_file = True
            return path
        elif isinstance(path, Path) and path.is_file():
            self.is_http_file = False
            return path.as_posix()
        raise AssertionError(
            "path must be a pathlib.Path (existing file) or a str (an url containing 'http'). "
            "In case you use e.g. GithubFileDownloader, then use get_download_url() instead of target_file"
        )

    def _get_separators(self, sep: str = None) -> List[str]:
        if sep:
            assert isinstance(sep, str), f"sep {sep} must be of type string"
            return [sep]
        if self.date_columns:
            return [None, ";"]
        return [",", ";"]

    @staticmethod
    def _trim_all_string_columns(df):
        """Trim whitespace from ends of each value across all series in dataframe."""
        return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def __check_separators_per_row(self, used_separator: str, df: pd.DataFrame) -> None:
        if self.is_http_file:
            # loop trough csv line by line is not possible with github file (in buffer). Avoid downloading!
            return
        nr_expected_separators_per_row = len(df.columns) - 1
        with open(self.path_str) as tmp_file:
            for index, line in enumerate(tmp_file):
                nr_separators_found = line.count(used_separator)
                if nr_separators_found != nr_expected_separators_per_row:
                    raise AssertionError(
                        f"csv error in {self.path_str} as line nr {index+1} has unexpected nr separators "
                        f"{nr_separators_found} (expected={nr_expected_separators_per_row}"
                    )

    @staticmethod
    def __check_sep_not_in_other_columns(df: pd.DataFrame, used_separator: str, default_error_msg: str) -> None:
        """
        We want to avoid that this:
            col_a,col_b,col_c
            text1,text2,text3
            text1;text2;text3
            text1,text2,text3
        becomes:
            col_a               col_b               col_c
            text1               text2               text3
            text1;text2;text3   None                None
            text1               text2               text3
        """
        has_df_no_nan = df.isnull().sum().sum() == 0
        if has_df_no_nan:
            return

        df_nr_nans_per_row = df.isnull().sum(axis=1)
        df_wrong_rows = df[df_nr_nans_per_row == len(df.columns) - 1]
        if not df_wrong_rows.empty:
            raise AssertionError(f"{default_error_msg}.  df_wrong_rows={df_wrong_rows}")

        all_possible_separators = [",", ";"]
        df_rows_with_nan = df[df_nr_nans_per_row != 0]
        for possible_wrong_separator in all_possible_separators:
            if possible_wrong_separator == used_separator:
                continue
            for col in df_rows_with_nan.columns:
                try:
                    df_wrong_rows = df_rows_with_nan[df_rows_with_nan[col].str.contains(possible_wrong_separator)]
                except Exception:  # noqa
                    continue
                if not df_wrong_rows.empty:
                    row_indices = df_wrong_rows.index.to_list()
                    err = f"row(s) {row_indices} contain empty cell(s) AND a separator other than {used_separator}"
                    raise AssertionError(f"{default_error_msg}, err={err}")

    def _get_df(self) -> pd.DataFrame:
        default_error_msg = (
            f"could not read csv {self.path_str} with separators={self.separators}, "
            f"expected columns={self.expected_columns}"
        )
        for separator in self.separators:
            df = self._csv_to_df(separator=separator)
            if df.empty:
                continue
            if len(df.columns) == 1:
                continue
            if self.expected_columns:
                for expected_column in self.expected_columns:
                    assert (
                        expected_column in df.columns
                    ), f"expected_column {expected_column} must be in {df.columns}, file={self.path_str}"
            df = self._trim_all_string_columns(df=df)
            self.__check_separators_per_row(used_separator=separator, df=df)
            return df
        raise AssertionError(default_error_msg)  # raise since no success

    def _csv_to_df(self, separator: str, encoding: str = None) -> pd.DataFrame:
        encoding = encoding if encoding else "utf-8"
        try:
            df = pd.read_csv(filepath_or_buffer=self.path_str, sep=separator, engine="python", encoding=encoding)
            if self.date_columns:
                # convert 'None' to pd.NaN (we require this for the __check_sep_not_in_other_columns()
                for date_column in self.date_columns:
                    df[date_column] = pd.to_datetime(arg=df[date_column], errors="coerce")
            return df
        except pd.errors.ParserError as err:
            logger.debug(f"could not parse csv {self.path_str} with separator {separator}, err={err}")
            return pd.DataFrame(data=None)
        except UnicodeDecodeError as err:
            with open(self.path_str) as tmp_file:
                df = self._csv_to_df(separator=separator, encoding=tmp_file.encoding)
                if not df.empty:
                    logger.warning(
                        f"found encoding {tmp_file.encoding} (instead of utf-8) for {self.path_str}, err={err}"
                    )
                return df
        except Exception as err:
            raise AssertionError(f"unexpected error when opening {self.path_str}, err={err}")
