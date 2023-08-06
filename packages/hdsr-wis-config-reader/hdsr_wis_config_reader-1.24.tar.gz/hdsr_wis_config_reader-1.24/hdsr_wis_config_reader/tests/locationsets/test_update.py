from hdsr_wis_config_reader.location_sets.columns import LocSetSharedCols
from hdsr_wis_config_reader.tests.fixtures import loc_sets

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8
loc_sets = loc_sets


def test_original_cannot_be_updated(loc_sets):

    assert not loc_sets.hoofd_loc.is_geo_df_updated_updated

    row_idx = 0
    assert not loc_sets.hoofd_loc.geo_df_original.empty
    old_value = loc_sets.hoofd_loc.geo_df_original.loc[row_idx][LocSetSharedCols.loc_id]
    new_value = f"{old_value}_updated"

    # update copy with .loc does not work
    df = loc_sets.hoofd_loc.geo_df_original
    df.loc[row_idx][LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_original.loc[row_idx][LocSetSharedCols.loc_id] == old_value

    # update copy with .at is not allowed
    df = loc_sets.hoofd_loc.geo_df_original
    try:
        df.at[row_idx, LocSetSharedCols.loc_id] = new_value
    except NotImplementedError as err:
        assert str(err) == ".geo_df_original cannot be updated. Please update .geo_df_updated"

    # update non-copy with .loc does not work
    loc_sets.hoofd_loc.geo_df_original.loc[row_idx][LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_original.loc[row_idx][LocSetSharedCols.loc_id] == old_value

    # update non-copy with .at is not allowed
    try:
        loc_sets.hoofd_loc.geo_df_original.at[row_idx, LocSetSharedCols.loc_id] = new_value
    except NotImplementedError as err:
        assert str(err) == ".geo_df_original cannot be updated. Please update .geo_df_updated"

    assert not loc_sets.hoofd_loc.is_geo_df_updated_updated


def test_updated_can_be_updated(loc_sets):

    assert not loc_sets.hoofd_loc.is_geo_df_updated_updated

    row_idx = 0
    assert not loc_sets.hoofd_loc.geo_df_updated.empty
    old_value = loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id]
    new_value = f"{old_value}_updated"

    # update copy with .loc does not work
    df = loc_sets.hoofd_loc.geo_df_updated
    df.loc[row_idx][LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id] == old_value

    # update copy with .at is allowed and works
    df = loc_sets.hoofd_loc.geo_df_updated
    df.at[row_idx, LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id] == new_value
    assert loc_sets.hoofd_loc.is_geo_df_updated_updated
    # reset for rest of tests
    df.at[row_idx, LocSetSharedCols.loc_id] = old_value

    assert not loc_sets.hoofd_loc.is_geo_df_updated_updated

    # update non-copy with .loc does not work
    loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id] == old_value

    # update non-copy with .at is allowed and works
    loc_sets.hoofd_loc.geo_df_updated.at[row_idx, LocSetSharedCols.loc_id] = new_value
    assert loc_sets.hoofd_loc.geo_df_updated.loc[row_idx][LocSetSharedCols.loc_id] == new_value

    assert loc_sets.hoofd_loc.is_geo_df_updated_updated
