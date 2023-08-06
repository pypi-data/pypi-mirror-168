from hdsr_pygithub import GithubDirDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.tests.helpers import _remove_dir_recursively
from pathlib import Path

import datetime
import logging
import pandas as pd  # noqa pandas comes with geopandas
import pytest


# silence flake8
fews_config_local = fews_config_local

logger = logging.getLogger(__name__)


expected_df_parameter_column_names = [
    "DESCRIPTION",
    "GROUP",
    "ID",
    "NAME",
    "PARAMETERTYPE",
    "SHORTNAME",
    "UNIT",
    "USESDATUM",
    "VALUERESOLUTION",
]


@pytest.mark.second_to_last  # run this test second_to_last as it takes long (~3 min)!
def test_local_fews_config(fews_config_local):
    fews_config = fews_config_local
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config_local.get_parameters()
    assert isinstance(df_parameters, pd.DataFrame)
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names


@pytest.mark.last  # run this test last as it takes long (~3 min)!
def test_github_fews_config_prd():
    target_dir = Path("FEWS/Config")
    github_downloader = GithubDirDownloader(
        target_dir=target_dir,
        only_these_extensions=[".csv", ".xml"],
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 2),
        repo_name=constants.GITHUB_WIS_CONFIG_REPO_NAME,
        branch_name=constants.GITHUB_WIS_CONFIG_BRANCH_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )
    download_dir = github_downloader.download_files(use_tmp_dir=True)
    config_dir = download_dir / target_dir
    fews_config = FewsConfigReader(path=config_dir)
    assert fews_config.path == config_dir

    # test FewsConfigReader
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config.get_parameters()
    assert "VALUERESOLUTION" in df_parameters.columns
    assert len(df_parameters) > 100

    # clean up
    _remove_dir_recursively(dir_path=download_dir)
