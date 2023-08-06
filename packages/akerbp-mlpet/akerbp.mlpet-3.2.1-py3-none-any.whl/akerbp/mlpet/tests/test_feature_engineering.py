from pandas.testing import assert_frame_equal

from akerbp.mlpet import feature_engineering
from akerbp.mlpet.tests.client import CLIENT, CLIENT_FUNCTIONS
from akerbp.mlpet.tests.data.data import DEPTH_TREND_X, DEPTH_TREND_Y
from akerbp.mlpet.tests.data.data import FORMATION_DF as FORMATION_DF_WITH_SYSTEMS
from akerbp.mlpet.tests.data.data import (
    FORMATION_TOPS_MAPPER,
    TEST_DF,
    VERTICAL_DEPTHS_MAPPER,
    VERTICAL_DF,
)

FORMATION_DF = FORMATION_DF_WITH_SYSTEMS.drop(columns=["SYSTEM"])


def test_add_formations_and_groups_using_mapper():
    df_with_tops = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        formation_tops_mapper=FORMATION_TOPS_MAPPER,
        id_column="well_name",
    )
    # Sorting columns because column order is not so important
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formations_and_groups_using_client():
    df_with_tops = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        client=CLIENT,
    )
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formations_and_groups_using_client_with_systems():
    df_with_tops = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        client=CLIENT,
        add_systems=True,
    )
    assert_frame_equal(
        df_with_tops.sort_index(axis=1), FORMATION_DF_WITH_SYSTEMS.sort_index(axis=1)
    )


def test_add_formations_and_groups_when_no_client_nor_mapping_is_provided():
    _ = feature_engineering.add_formations_and_groups(
        FORMATION_DF[["DEPTH", "well_name"]],
        id_column="well_name",
    )


def test_add_vertical_depths_using_mapper():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        vertical_depths_mapper=VERTICAL_DEPTHS_MAPPER,
        id_column="well_name",
        md_column="DEPTH",
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_using_client():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        md_column="DEPTH",
        client=CLIENT,
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_when_no_client_nor_mapping_is_provided():
    _ = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        md_column="DEPTH",
    )


def test_add_well_metadata():
    metadata = {"30/11-6 S": {"FOO": 0}, "25/7-4 S": {"FOO": 1}}
    df = feature_engineering.add_well_metadata(
        TEST_DF, metadata_dict=metadata, metadata_columns=["FOO"], id_column="well_name"
    )
    assert "FOO" in df.columns.tolist()


def test_add_depth_trend():
    result = feature_engineering.add_depth_trend(
        DEPTH_TREND_X,
        id_column="well",
        env="prod",
        return_file=False,
        return_CI=True,
        client=CLIENT_FUNCTIONS,
        keyword_arguments=dict(
            nan_numerical_value=-9999,
            nan_textual_value="MISSING",
        ),
    )

    assert DEPTH_TREND_Y.equals(result[DEPTH_TREND_Y.columns])
