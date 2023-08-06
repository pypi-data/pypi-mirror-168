from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader import IdMappingCollection
from hdsr_wis_config_reader.idmappings.custom_dataframe import IdMappingDataframe
from hdsr_wis_config_reader.location_sets.collection import LocationSetCollection
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.startenddate import StartEndDateReaderLocal
from pathlib import Path

import geopandas as gpd
import pytest


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def fews_config_local() -> FewsConfigReader:
    # we use config saved in this repo (=static), instead of downloading from repo 'wis_config'
    assert constants.TEST_DIR_WIS_CONFIG.is_dir()
    fews_config = FewsConfigReader(path=constants.TEST_DIR_WIS_CONFIG)
    return fews_config


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def loc_sets() -> LocationSetCollection:
    fews_config = FewsConfigReader(path=constants.TEST_DIR_WIS_CONFIG)
    loc_sets = LocationSetCollection(fews_config=fews_config)
    return loc_sets


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def startenddate_local() -> StartEndDateReaderLocal:
    return StartEndDateReaderLocal(startenddate_csv_path=constants.TEST_PATH_STARTENDDATE_CAW_OPP_SHORT)


@pytest.fixture(scope="session")
def path_idmap_xml() -> Path:
    path_idmap_xml = constants.TEST_DIR_WIS_CONFIG / "IdMapFiles" / "IdOPVLWATER.xml"
    assert path_idmap_xml.is_file()
    return path_idmap_xml


@pytest.fixture(scope="session")
def path_sub_loc_csv() -> Path:
    path_sub_loc_csv = constants.TEST_DIR_WIS_CONFIG / "MapLayerFiles" / "oppvlwater_subloc.csv"
    assert path_sub_loc_csv.is_file()
    return path_sub_loc_csv


@pytest.fixture(scope="session")
def gdf_sub_loc(path_sub_loc_csv) -> gpd.GeoDataFrame:
    return FewsConfigReader.get_gdf_locset_via_path(file_path=path_sub_loc_csv)


@pytest.fixture(scope="session")
def df_idmap(path_idmap_xml) -> IdMappingDataframe:
    return IdMappingCollection.get_idmap_df_via_path(file_path=path_idmap_xml)
