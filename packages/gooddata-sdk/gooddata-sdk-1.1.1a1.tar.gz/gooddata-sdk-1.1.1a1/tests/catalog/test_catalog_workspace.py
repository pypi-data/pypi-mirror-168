# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

from tests_support.vcrpy_utils import get_vcr

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk import (
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
    CatalogWorkspace,
    GoodDataApiClient,
    GoodDataSdk,
)
from gooddata_sdk.utils import recreate_directory

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspaces"


def _empty_workspaces(sdk: GoodDataSdk) -> None:
    empty_workspaces_e = CatalogDeclarativeWorkspaces.from_api({"workspaces": [], "workspace_data_filters": []})
    sdk.catalog_workspace.put_declarative_workspaces(empty_workspaces_e)
    empty_workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
    assert empty_workspaces_e == empty_workspaces_o
    assert empty_workspaces_e.to_dict(camel_case=True) == empty_workspaces_o.to_dict(camel_case=True)


def _empty_workspace(sdk: GoodDataSdk, workspace_id: str) -> None:
    empty_workspace_e = CatalogDeclarativeWorkspaceModel()
    sdk.catalog_workspace.put_declarative_workspace(workspace_id=workspace_id, workspace=empty_workspace_e)
    empty_workspace_o = sdk.catalog_workspace.get_declarative_workspace(workspace_id=workspace_id)
    assert len(empty_workspace_o.ldm.datasets) == 0
    assert len(empty_workspace_o.ldm.date_instances) == 0
    assert len(empty_workspace_o.analytics.analytical_dashboards) == 0
    assert len(empty_workspace_o.analytics.dashboard_plugins) == 0
    assert len(empty_workspace_o.analytics.filter_contexts) == 0
    assert len(empty_workspace_o.analytics.metrics) == 0
    assert len(empty_workspace_o.analytics.visualization_objects) == 0


def _empty_workspace_data_filters(sdk: GoodDataSdk) -> None:
    empty_workspace_data_filters_e = CatalogDeclarativeWorkspaceDataFilters.from_dict(
        {"workspace_data_filters": []}, camel_case=False
    )
    sdk.catalog_workspace.put_declarative_workspace_data_filters(empty_workspace_data_filters_e)
    empty_workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    assert empty_workspace_data_filters_e == empty_workspace_data_filters_o
    assert empty_workspace_data_filters_e.to_dict(camel_case=True) == empty_workspace_data_filters_o.to_dict(
        camel_case=True
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspaces.yaml"))
def test_load_and_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    with open(_current_dir / "expected" / "declarative_workspaces.json") as f:
        data = json.load(f)
        workspaces_e = CatalogDeclarativeWorkspaces.from_dict(data)

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.load_and_put_declarative_workspaces(path)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)
    finally:
        sdk.catalog_workspace.put_declarative_workspaces(workspaces_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspaces.yaml"))
def test_store_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()
    sdk.catalog_workspace.store_declarative_workspaces(path)
    workspaces_o = sdk.catalog_workspace.load_declarative_workspaces(path)

    assert workspaces_e == workspaces_o
    assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspaces.yaml"))
def test_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.put_declarative_workspaces(workspaces_e)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)
    finally:
        with open(path) as f:
            data = json.load(f)
        workspaces_o = CatalogDeclarativeWorkspaces.from_dict(data)
        sdk.catalog_workspace.put_declarative_workspaces(workspaces_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces_snake_case.yaml"))
def test_get_declarative_workspaces_snake_case(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces_snake_case.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data, camel_case=False)

    assert workspaces_o == expected_o
    assert workspaces_o.to_dict(camel_case=False) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces.yaml"))
def test_get_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data)

    assert workspaces_o == expected_o
    assert workspaces_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_declarative_workspaces.yaml"))
def test_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    assert len(workspaces_o.workspaces) == 3
    assert len(workspaces_o.workspace_data_filters) == 2
    assert [workspace.id for workspace in workspaces_o.workspaces] == ["demo", "demo_west", "demo_west_california"]
    assert workspaces_o.to_dict(camel_case=True) == layout_api.get_workspaces_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_invalid.yaml"))
def test_update_workspace_invalid(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_new_name = "Test"
    workspace_new_parent = "new_parent"

    workspace = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace.id in [w.id for w in workspaces]
    assert workspace_new_parent not in [w.id for w in workspaces]
    assert workspace.parent_id is not None

    try:
        sdk.catalog_workspace.create_or_update(CatalogWorkspace(workspace.id, workspace_new_name, workspace_new_parent))
    except ValueError:
        # Update workspace parent is not allowed.
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace == workspace_o


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_valid.yaml"))
def test_update_workspace_valid(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_new_name = "Test"

    # Original workspace
    workspace = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    # New workspace
    new_workspace = CatalogWorkspace(workspace.id, workspace_new_name, workspace.parent_id)

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace.id in [w.id for w in workspaces]
    assert workspace.parent_id is not None

    try:
        # Updating only name.
        sdk.catalog_workspace.create_or_update(new_workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace_o == new_workspace
    finally:
        # Clean up. Revert changes.
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace_o == workspace


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_workspace.yaml"))
def test_delete_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "demo_west_california"

    workspace = sdk.catalog_workspace.get_workspace(workspace_id)
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.delete_workspace(workspace_id)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 2
        assert workspace_id not in [w.id for w in workspaces]
    finally:
        # Clean up. Create deleted workspace.
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3
        assert workspace_id in [w.id for w in workspaces]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_non_existing_workspace.yaml"))
def test_delete_non_existing_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "non_existing_workspace"

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id not in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.delete_workspace(workspace_id)
    except ValueError:
        # Trying to delete not existing workspace should not be executed and an exception should be raised.
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_parent_workspace.yaml"))
def test_delete_parent_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3

    try:
        sdk.catalog_workspace.delete_workspace(test_config["workspace"])
    except ValueError:
        # Delete of workspace, which has children should not be executed and an exception should be raised.
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_create_workspace.yaml"))
def test_create_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "test"
    workspace_name = "Test"
    workspace_parent = "demo"

    workspace = CatalogWorkspace(workspace_id, workspace_name, workspace_parent)

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id not in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace_id)
        assert len(workspaces) == 4
        assert workspace_o == workspace
    finally:
        # Clean up. Delete created workspace.
        sdk.catalog_workspace.delete_workspace(workspace_id)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3
        assert workspace_id not in [w.id for w in workspaces]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_workspace.yaml"))
def test_get_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # Check workspace without parent
    workspace_demo = sdk.catalog_workspace.get_workspace(test_config["workspace"])
    assert workspace_demo.id == test_config["workspace"]
    assert workspace_demo.name == test_config["workspace_name"]
    assert workspace_demo.parent_id is None

    # Check workspace with parent
    workspace_with_parent = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    assert workspace_with_parent.id == test_config["workspace_with_parent"]
    assert workspace_with_parent.name == test_config["workspace_with_parent_name"]
    assert workspace_with_parent.parent_id == test_config["workspace"]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_workspace_list.yaml"))
def test_workspace_list(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    ids = ["demo", "demo_west", "demo_west_california"]
    names = ["Demo", "Demo West", "Demo West California"]
    parents = [None, "demo", "demo_west"]

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3

    workspaces_id = [w.id for w in workspaces]
    workspaces_id.sort()
    assert ids == workspaces_id

    workspaces_name = [w.name for w in workspaces]
    workspaces_name.sort()
    assert names == workspaces_name

    workspaces_parent = {w.id: w.parent_id for w in workspaces}
    workspaces_parent_l = [workspaces_parent[workspace_id] for workspace_id in workspaces_id]
    assert parents == workspaces_parent_l


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspace_data_filters.yaml"))
def test_get_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    declarative_workspace_data_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    workspace_data_filters = declarative_workspace_data_filters.workspace_data_filters

    assert len(workspace_data_filters) == 2
    assert set(workspace_data_filter.id for workspace_data_filter in workspace_data_filters) == {
        "wdf__region",
        "wdf__state",
    }

    assert declarative_workspace_data_filters.to_dict(
        camel_case=True
    ) == layout_api.get_workspace_data_filters_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspace_data_filters.yaml"))
def test_store_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    declarative_workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    sdk.catalog_workspace.store_declarative_workspace_data_filters(path)
    declarative_workspace_data_filters_o = sdk.catalog_workspace.load_declarative_workspace_data_filters(path)

    assert declarative_workspace_data_filters_e == declarative_workspace_data_filters_o
    assert declarative_workspace_data_filters_e.to_dict(
        camel_case=True
    ) == declarative_workspace_data_filters_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspace_data_filters.yaml"))
def test_load_and_put_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    expected_json_path = _current_dir / "expected" / "declarative_workspace_data_filters.json"
    workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()

    try:
        _empty_workspace_data_filters(sdk)

        sdk.catalog_workspace.load_and_put_declarative_workspace_data_filters(path)
        workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
        assert workspace_data_filters_e == workspace_data_filters_o
        assert workspace_data_filters_e.to_dict(camel_case=True) == workspace_data_filters_o.to_dict(camel_case=True)
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        workspace_data_filters_o = CatalogDeclarativeWorkspaceDataFilters.from_dict(data, camel_case=True)
        sdk.catalog_workspace.put_declarative_workspace_data_filters(workspace_data_filters_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspace_data_filters.yaml"))
def test_put_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspace_data_filters.json"
    declarative_workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()

    try:
        _empty_workspace_data_filters(sdk)

        sdk.catalog_workspace.put_declarative_workspace_data_filters(declarative_workspace_data_filters_e)
        declarative_workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
        assert declarative_workspace_data_filters_e == declarative_workspace_data_filters_o
        assert declarative_workspace_data_filters_e.to_dict(
            camel_case=True
        ) == declarative_workspace_data_filters_o.to_dict(camel_case=True)
    finally:
        with open(path) as f:
            data = json.load(f)
        declarative_workspace_data_filters_o = CatalogDeclarativeWorkspaceDataFilters.from_dict(data)
        sdk.catalog_workspace.put_declarative_workspace_data_filters(declarative_workspace_data_filters_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspace.yaml"))
def test_get_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    workspace = sdk.catalog_workspace.get_declarative_workspace(test_config["workspace"])

    assert len(workspace.ldm.datasets) == 5
    assert len(workspace.ldm.date_instances) == 1
    assert len(workspace.analytics.analytical_dashboards) == 3
    assert len(workspace.analytics.dashboard_plugins) == 2
    assert len(workspace.analytics.filter_contexts) == 2
    assert len(workspace.analytics.metrics) == 24
    assert len(workspace.analytics.visualization_objects) == 15
    assert workspace.to_dict(camel_case=True) == layout_api.get_workspace_layout(
        workspace_id=test_config["workspace"]
    ).to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspace.yaml"))
def test_put_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    sdk.catalog_workspace.create_or_update(
        workspace=CatalogWorkspace(workspace_id=test_config["workspace_test"], name=test_config["workspace_test"])
    )

    try:
        workspace_e = sdk.catalog_workspace.get_declarative_workspace(test_config["workspace"])
        sdk.catalog_workspace.put_declarative_workspace(
            workspace_id=test_config["workspace_test"], workspace=workspace_e
        )
        workspace_o = sdk.catalog_workspace.get_declarative_workspace(test_config["workspace"])
        assert workspace_e == workspace_o
        assert workspace_e.to_dict() == workspace_o.to_dict()
    finally:
        sdk.catalog_workspace.delete_workspace(workspace_id=test_config["workspace_test"])
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspace.yaml"))
def test_store_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    workspaces_e = sdk.catalog_workspace.get_declarative_workspace(workspace_id=test_config["workspace"])
    sdk.catalog_workspace.store_declarative_workspace(workspace_id=test_config["workspace"], layout_root_path=path)
    workspaces_o = sdk.catalog_workspace.load_declarative_workspace(
        workspace_id=test_config["workspace"], layout_root_path=path
    )

    assert workspaces_e == workspaces_o
    assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspace.yaml"))
def test_load_and_put_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    expected_json_path = _current_dir / "expected" / "declarative_workspace.json"
    workspace_e = sdk.catalog_workspace.get_declarative_workspace(workspace_id=test_config["workspace"])

    try:
        _empty_workspace(sdk, workspace_id=test_config["workspace"])

        sdk.catalog_workspace.load_and_put_declarative_workspace(
            workspace_id=test_config["workspace"], layout_root_path=path
        )
        workspace_o = sdk.catalog_workspace.get_declarative_workspace(workspace_id=test_config["workspace"])
        assert workspace_e == workspace_o
        assert workspace_e.to_dict(camel_case=True) == workspace_o.to_dict(camel_case=True)
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        workspace_o = CatalogDeclarativeWorkspaceModel.from_dict(data, camel_case=True)
        sdk.catalog_workspace.put_declarative_workspace(workspace_id=test_config["workspace"], workspace=workspace_o)
