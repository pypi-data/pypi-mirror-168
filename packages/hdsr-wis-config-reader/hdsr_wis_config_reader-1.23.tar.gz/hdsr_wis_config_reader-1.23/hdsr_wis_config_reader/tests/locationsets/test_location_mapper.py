from hdsr_wis_config_reader.idmappings.custom_dataframe import IdMappingDataframe
from hdsr_wis_config_reader.location_sets.location_mapper import LocationMapper
from hdsr_wis_config_reader.tests.fixtures import df_idmap
from hdsr_wis_config_reader.tests.fixtures import gdf_sub_loc
from hdsr_wis_config_reader.tests.fixtures import path_idmap_xml
from hdsr_wis_config_reader.tests.fixtures import path_sub_loc_csv

import geopandas as gpd
import pytest


# silence flake8
path_idmap_xml = path_idmap_xml
path_sub_loc_csv = path_sub_loc_csv
df_idmap = df_idmap
gdf_sub_loc = gdf_sub_loc


def test_mapper_ok_init(path_idmap_xml, path_sub_loc_csv, gdf_sub_loc, df_idmap):
    # scenario 1: paths, no dataframes
    mapper1 = LocationMapper(path_sub_loc_csv=path_sub_loc_csv, path_idmap_xml=path_idmap_xml)
    assert isinstance(mapper1.df_idmap, IdMappingDataframe)

    # scenario 2: no paths, dataframes
    mapper2 = LocationMapper(gdf_sub_loc=gdf_sub_loc, df_idmap=df_idmap)
    assert isinstance(mapper2.gdf_sub_loc, gpd.GeoDataFrame)

    # scenario 3: path and dataframe
    mapper3 = LocationMapper(path_sub_loc_csv=path_sub_loc_csv, df_idmap=df_idmap)
    assert isinstance(mapper3.gdf_sub_loc, gpd.GeoDataFrame)


def test_mapper_wrong_init(path_idmap_xml, path_sub_loc_csv, gdf_sub_loc, df_idmap):
    with pytest.raises(AssertionError):
        LocationMapper()

    with pytest.raises(AssertionError):
        LocationMapper(path_sub_loc_csv=path_sub_loc_csv, gdf_sub_loc=gdf_sub_loc)

    with pytest.raises(AssertionError):
        LocationMapper(path_idmap_xml=path_idmap_xml, df_idmap=df_idmap)


def test_upwards(path_idmap_xml, path_sub_loc_csv, gdf_sub_loc, df_idmap):
    """"upwards: sub -> hoofd -> complex"""
    mapper = LocationMapper(path_sub_loc_csv=path_sub_loc_csv, path_idmap_xml=path_idmap_xml)

    with pytest.raises(AssertionError):
        # either use ex_loc + ex_par OR int_loc
        mapper.sub_to_hoofd(ex_loc="4335", ex_par="ES2", int_loc="KW432224")

    assert mapper.sub_to_hoofd(int_loc="KW432211") == "KW432210"
    assert mapper.sub_to_hoofd(int_loc="KW432224") == "KW432220"
    assert mapper.sub_to_hoofd(ex_loc="4335", ex_par="ES2") == "KW433510"
    assert mapper.sub_to_hoofd(ex_loc="4335", ex_par="Q1") == "KW433520"

    assert mapper.hoofd_to_complex(int_loc="KW432210") == "4322"

    assert mapper.sub_to_complex(int_loc="KW432211") == "4322"
    assert mapper.sub_to_complex(int_loc="KW432224") == "4322"
    assert mapper.sub_to_complex(ex_loc="4335", ex_par="ES2") == "4335"
    assert mapper.sub_to_complex(ex_loc="4335", ex_par="Q1") == "4335"

    # test x8xx locations
    assert mapper.sub_to_hoofd(ex_loc="1811", ex_par="ES2") == "KW108420"
    assert mapper.sub_to_complex(ex_loc="1811", ex_par="ES2") == "1084"


def test_downwards(path_idmap_xml, path_sub_loc_csv, gdf_sub_loc, df_idmap):
    """"downwards: complex -> hoofd -> sub"""
    mapper = LocationMapper(path_sub_loc_csv=path_sub_loc_csv, path_idmap_xml=path_idmap_xml)

    # test a split caw_complex that holds a x8xx notation (team CAW exports this the correct way)
    assert mapper.complex_to_hoofd(caw_complex="4322") == ["KW432210", "KW432220"]
    assert mapper.complex_to_hoofd(caw_complex="4804") == ["KW432210", "KW432220"]
    is_split, is_split_correctly = mapper.is_complex_split_correctly(caw_complex="4322")
    assert is_split and is_split_correctly
    is_split, is_split_correctly = mapper.is_complex_split_correctly(caw_complex="4804")
    assert is_split and is_split_correctly
    # test a split caw_complex without a x8xx notation (team CAW exports this the incorrect way)
    assert mapper.complex_to_hoofd(caw_complex="2182") == ["KW218220", "KW218230"]
    is_split, is_split_correctly = mapper.is_complex_split_correctly(caw_complex="2182")
    assert is_split and not is_split_correctly

    # test split caw_complex that holds a x8xx notation (team CAW exports this the correct way)
    assert mapper.hoofd_to_sub(int_loc="KW432210") == ["KW432211", "KW432212"]
    # test a split caw_complex without a x8xx notation (team CAW exports this the incorrect way)
    assert mapper.hoofd_to_sub(int_loc="KW218220") == ["KW218221"]
    assert mapper.hoofd_to_sub(int_loc="KW218230") == ["KW218231"]

    # test a split caw_complex that holds a x8xx notation (team CAW exports this the correct way)
    expected_subs = ["KW432211", "KW432212", "KW432221", "KW432222", "KW432223", "KW432224", "KW432225", "KW432226"]
    assert mapper.complex_to_sub(caw_complex="4322") == expected_subs
    assert mapper.complex_to_sub(caw_complex="4804") == expected_subs

    # test a split caw_complex without a x8xx notation (team CAW exports this the incorrect way)
    assert mapper.complex_to_sub(caw_complex="2182") == ["KW218221", "KW218231"]

    # TODO: caw_complex is 1e 4 cijfers na KW, dus bijv. 2106 moet ook linken aan 106:
    #  <map externalLocation="106" externalParameter="HO2" internalLocation="KW210611" internalParameter="H.G.0"/>
    #  is_split, is_split_correctly = mapper.is_complex_split_correctly(caw_complex="2106")
    #  assert is_split and not is_split_correctly
    #  --
    #  error: caw_complex (ex_loc) 3243 not in idmapping
    #  caw_complex heeft geen 1 op 1 relatie met ex_loc. Je kan beter uitgaan van eerste 4 cijfers achter KW

    # fix bug "caw_complex (ex_loc) 2106 not in idmapping"
    assert mapper.hoofd_to_complex(int_loc="KW210610") == "2106"
    assert mapper.complex_to_hoofd(caw_complex="2106") == ["KW210610", "KW210620"]
