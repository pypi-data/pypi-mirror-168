from hdsr_pygithub import GithubFileDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.utils import PdReadFlexibleCsv
from pathlib import Path

import datetime
import pandas as pd  # noqa pandas comes with geopandas
import pytest


def test_multi_separators_1():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_1.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=None,
        )


def test_multi_separators_2():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_2.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=None,
        )


def test_too_many_cells():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_too_many_cells.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=None,
        )


def test_too_little_cells():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_too_little_cells.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=None,
        )


def test_no_error_without_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error.csv"
    assert csv_path.is_file()
    reader = PdReadFlexibleCsv(path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=None,)
    assert isinstance(reader.df, pd.DataFrame)
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_string_dtype(reader.df["start"])
    assert pd.api.types.is_string_dtype(reader.df["end"])


def test_no_error_with_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error.csv"
    assert csv_path.is_file()
    reader = PdReadFlexibleCsv(
        path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=["start", "end"],
    )
    assert isinstance(reader.df, pd.DataFrame)
    assert pd.api.types.is_string_dtype(reader.df["series"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["start"])
    assert pd.api.types.is_datetime64_any_dtype(reader.df["end"])


def test_multi_separators_2_with_dates():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "error_multi_separators_2.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "end"], parse_dates=["start", "end"],
        )


def test_no_error_but_wrong_expected_columns():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error.csv"
    assert csv_path.is_file()
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=csv_path, sep=",", expected_columns=["series", "start", "column_does_not_exist"], parse_dates=None,
        )


def test_github_file():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "no_error.csv"
    assert csv_path.is_file()

    github_downloader = GithubFileDownloader(
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 10),
        target_file=constants.GITHUB_STARTENDDATE_CAW_OPPERVLAKTEWATER_SHORT,
        branch_name=constants.GITHUB_STARTENDDATE_BRANCH_NAME,
        repo_name=constants.GITHUB_STARTENDDATE_REPO_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )

    assert isinstance(github_downloader.get_download_url(), str)
    reader = PdReadFlexibleCsv(
        path=github_downloader.get_download_url(),
        sep=",",
        expected_columns=["series", "start", "end"],
        parse_dates=["start", "end"],
    )
    assert isinstance(reader.df, pd.DataFrame)

    assert isinstance(github_downloader.target_file, Path)
    with pytest.raises(AssertionError):
        PdReadFlexibleCsv(
            path=github_downloader.target_file,
            sep=",",
            expected_columns=["series", "start", "end"],
            parse_dates=["start", "end"],
        )


def test_no_utf8():
    csv_path = constants.TEST_DIR_PD_FLEX_READ_CSV / "parameters_no_utf8_but_ansi.csv"
    assert csv_path.is_file()
    df = PdReadFlexibleCsv(path=csv_path).df
    assert isinstance(df, pd.DataFrame)
