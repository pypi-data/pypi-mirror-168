from hdsr_wis_config_reader import IdMappingCollection
from hdsr_wis_config_reader.idmappings.columns import ExLocChoices
from hdsr_wis_config_reader.idmappings.columns import IdMapCols
from hdsr_wis_config_reader.idmappings.columns import IntLocChoices
from hdsr_wis_config_reader.idmappings.custom_dataframe import IdMappingDataframe
from hdsr_wis_config_reader.location_sets.columns import LocSetSharedCols
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import geopandas as gpd
import pandas as pd  # noqa pandas comes with geopandas


class LocationMapper:

    """
    This class enables easy mapping between caw_complex, hoofd_locations and sub_locations.
    ow_locs (Waterlevel measurement_locations) are also hoofd_locations, but we exclude them in this mapper.

    A caw_complex has 1 to 9 hoofd_locations and a hoofd_location has 1 to 9 sub_locations.
        Example: KW123456
            caw_complex = digits 1 till 4 = ‘1234‘
            hoofd_location = digit 5 = '5'
            sub_location = digit 6 = '6'

    A split location is a caw_complex that has >1 hoofd_locations. In that case, team CAW should use a
    ex_loc=x8xx for the other hoofd_locations. For example: KW4315
        - KW43151X is Kockengen stuw (stuw/totaal/vispassage),          CAW exports this as 4803
        - KW43152X is Kockengen pompvijzel (krooshek/pompvijzel/totaal) CAW exports this as 4315
    context: Kockengen stuw and pompvijzel are separated ~100 meters. They share 1 electricity supply (?), so team
    CAW determined them as one location. However, they regulate different water
    levels (twee verschillende peilscheidingen), so in FEWS-WIS we determine them as separate locations.
    Be aware that CAW started using x8xx notations in 2018, but they have not yet fully implemented this.
    """

    def __init__(
        self,
        path_sub_loc_csv: Path = None,
        gdf_sub_loc: gpd.GeoDataFrame = None,
        path_idmap_xml: Path = None,
        df_idmap: IdMappingDataframe = None,
    ):
        self.path_sub_loc_csv = path_sub_loc_csv
        self._gdf_sub_loc = gdf_sub_loc
        self.path_idmap_xml = path_idmap_xml
        self._df_idmap = df_idmap
        self.validate_constructor()

    def validate_constructor(self):
        if self.path_sub_loc_csv:
            assert isinstance(self.path_sub_loc_csv, Path)
            assert self._gdf_sub_loc is None, "use either path_sub_loc_csv or gdf_sub_loc"
        else:
            assert self._gdf_sub_loc is not None, "use either path_sub_loc_csv or gdf_sub_loc"
            assert isinstance(self._gdf_sub_loc, gpd.GeoDataFrame)

        if self.path_idmap_xml:
            assert isinstance(self.path_idmap_xml, Path)
            assert self._df_idmap is None, "use either path_idmap_xml or df_idmap"
        else:
            assert self._df_idmap is not None, "use either path_idmap_xml or df_idmap"
            assert isinstance(self._df_idmap, IdMappingDataframe)

    @property
    def gdf_sub_loc(self) -> gpd.GeoDataFrame:
        if self._gdf_sub_loc is not None:
            return self._gdf_sub_loc
        from hdsr_wis_config_reader import FewsConfigReader  # noqa avoiding circular import

        self._gdf_sub_loc = FewsConfigReader.get_gdf_locset_via_path(file_path=self.path_sub_loc_csv)
        return self._gdf_sub_loc

    @property
    def df_idmap(self) -> IdMappingDataframe:
        if self._df_idmap is not None:
            return self._df_idmap
        self._df_idmap = IdMappingCollection.get_idmap_df_via_path(file_path=self.path_idmap_xml)
        return self._df_idmap

    @staticmethod
    def _validate_caw_complex(caw_complex: str) -> None:
        assert IntLocChoices.is_caw_complex(caw_complex=caw_complex), f"{caw_complex} is not a caw_complex"

    @staticmethod
    def _validate_hoofd(int_loc: str) -> None:
        assert IntLocChoices.is_kw_hoofd(int_loc=int_loc), f"{int_loc} is not a hoofd_loc"

    @staticmethod
    def _validate_sub(ex_loc: str = None, ex_par: str = None, int_loc: str = None) -> None:
        assert bool(ex_loc) == bool(ex_par) != bool(int_loc), "use either ex_loc or int_loc"
        if int_loc:
            assert IntLocChoices.is_kw_sub(int_loc=int_loc), f"{int_loc} is not a sub int_loc"
            assert ex_par is None, "use either ex_loc+ex_par or int_loc"
        elif ex_loc:
            assert IntLocChoices.is_caw_complex(caw_complex=ex_loc), f"{ex_loc} is not a caw_complex"
            assert isinstance(ex_par, str)

    def is_complex_split_correctly(self, caw_complex: str) -> Tuple[bool, Optional[bool]]:
        hoofd_locs = self.complex_to_hoofd(caw_complex=caw_complex)
        is_split = len(hoofd_locs) > 1
        if not is_split:
            is_split_correctly = None
            return is_split, is_split_correctly
        ex_locs = []
        for hoofd_loc in hoofd_locs:
            [ex_locs.append(x) for x in self.df_idmap.get_filtered_df(int_loc=hoofd_loc)[IdMapCols.ex_loc].unique()]
        ex_locs = list(set(ex_locs))
        # _3digit_ex_locs = [x for x in ex_locs if len(x) == 3]
        _4digit_ex_locs = [x for x in ex_locs if len(x) == 4]
        _x8xx_in_4digit_ex_locs = [ExLocChoices._is_split_x8xx(ex_loc=ex_loc) for ex_loc in _4digit_ex_locs]  # noqa
        is_split_correctly = len(_4digit_ex_locs) / 2 == sum(_x8xx_in_4digit_ex_locs)
        return is_split, is_split_correctly

    def complex_to_hoofd(self, caw_complex: str) -> List[str]:
        """Retrieve all related hoofd locations on this caw complex"""
        self._validate_caw_complex(caw_complex=caw_complex)
        df_idmap_filtered_normal = self.df_idmap.get_filtered_df(ex_loc=caw_complex)
        df_idmap_filtered_str = self.df_idmap[self.df_idmap[IdMapCols.int_loc].str.contains(f"KW{caw_complex}")]
        df_merge = pd.concat(objs=[df_idmap_filtered_normal, df_idmap_filtered_str], axis=0)
        if df_merge.empty:
            msg = f"caw_complex {caw_complex} not in idmapping (expected KW{caw_complex} in column {IdMapCols.int_loc}"
            raise AssertionError(msg)
        hoofd_locs = [x for x in df_merge[IdMapCols.int_loc].unique() if IntLocChoices.is_kw_hoofd(int_loc=x)]
        hoofd_locs_less_simple = []
        for hoofd_loc in hoofd_locs:
            _caw_complex = hoofd_loc[0:6]
            all_sub_hoofd_locs = self.df_idmap[self.df_idmap[IdMapCols.int_loc].str.contains(_caw_complex)][
                IdMapCols.int_loc
            ].unique()
            [hoofd_locs_less_simple.append(x) for x in all_sub_hoofd_locs if IntLocChoices.is_kw_hoofd(int_loc=x)]
        hoofd_locs.extend(hoofd_locs_less_simple)
        hoofd_locs = sorted(set(hoofd_locs))
        return hoofd_locs

    def complex_to_sub(self, caw_complex: str) -> List[str]:
        """Retrieve all related sub locations on this caw complex"""
        self._validate_caw_complex(caw_complex=caw_complex)
        hoofd_locs = self.complex_to_hoofd(caw_complex=caw_complex)
        sub_locs = []
        for hoofd_loc in hoofd_locs:
            [sub_locs.append(x) for x in self.hoofd_to_sub(int_loc=hoofd_loc)]
        return sub_locs

    def hoofd_to_complex(self, int_loc: str) -> str:
        # TODO: KW109911 always returns 1099.. while also 099 did exist
        #  	<map externalLocation="099" externalParameter="Q1" internalLocation="KW109911" internalParameter="Q.G.0"/>
        # 	<map externalLocation="1099" externalParameter="Q1" internalLocation="KW109911" internalParameter="Q.G.0"/>
        self._validate_hoofd(int_loc=int_loc)
        caw_complex = f"{int_loc.lstrip('KW')[:-2]}"
        self._validate_caw_complex(caw_complex=caw_complex)
        return caw_complex

    def hoofd_to_sub(self, int_loc: str) -> List[str]:
        self._validate_hoofd(int_loc=int_loc)
        subs = self.gdf_sub_loc[self.gdf_sub_loc["PAR_ID"] == int_loc][LocSetSharedCols.loc_id].unique().tolist()
        assert subs, f"hoofd_loc (int_loc={int_loc}, must have sub_locs (but none found in sub_loc.csv"
        return subs

    def sub_to_complex(self, ex_loc: str = None, ex_par: str = None, int_loc: str = None) -> str:
        self._validate_sub(ex_loc=ex_loc, ex_par=ex_par, int_loc=int_loc)
        hoofd_loc = self.sub_to_hoofd(ex_loc=ex_loc, ex_par=ex_par, int_loc=int_loc)
        return self.hoofd_to_complex(int_loc=hoofd_loc)

    def sub_to_hoofd(self, ex_loc: str = None, ex_par: str = None, int_loc: str = None) -> str:
        """
        Enige plek waar Koppeling subloc en hoofdloc te maken is id_map
        X8xx staat in Idmap
        Van idmap ga subloc
        Laatste cijfer en vervangen door 0
        """
        self._validate_sub(ex_loc=ex_loc, ex_par=ex_par, int_loc=int_loc)
        df_idmap_filtered = self.df_idmap.get_filtered_df(ex_loc=ex_loc, ex_par=ex_par, int_loc=int_loc)
        assert (
            not df_idmap_filtered.empty
        ), f"sub_loc (ex_loc={ex_loc}, ex_par={ex_par}, int_loc={int_loc}) not in idmapping"

        hoofd_locs = []
        for int_loc in df_idmap_filtered[IdMapCols.int_loc].unique():
            if IntLocChoices.is_kw_sub(int_loc=int_loc):
                hoofd_loc = f"{int_loc[:-1]}0"
                hoofd_locs.append(hoofd_loc)
        assert len(set(hoofd_locs)) == 1, f"expected 1 hoofd_loc for be found {hoofd_locs}"
        return hoofd_locs[0]
