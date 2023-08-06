import pytest
import json
import sklearn
from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectServer

import vetiver

# Load data, model
X_df, y = vetiver.mock.get_mock_data()
model = vetiver.mock.get_mock_model().fit(X_df, y)

RSC_SERVER_URL = "http://localhost:3939"
RSC_KEYS_FNAME = "vetiver/tests/rsconnect_api_keys.json"

pytestmark = pytest.mark.rsc_test  # noqa


def server_from_key(name):
    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return RSConnectServer(RSC_SERVER_URL, api_key)


def rsc_from_key(name):
    with open(RSC_KEYS_FNAME) as f:
        api_key = json.load(f)[name]
        return RsConnectApi(RSC_SERVER_URL, api_key)


def rsc_fs_from_key(name):

    rsc = rsc_from_key(name)

    return RsConnectFs(rsc)


def rsc_delete_user_content(rsc):
    guid = rsc.get_user()["guid"]
    content = rsc.get_content(owner_guid=guid)
    for entry in content:
        rsc.delete_content_item(entry["guid"])


@pytest.fixture(scope="function")
def rsc_short():
    # tears down content after each test
    fs_susan = rsc_fs_from_key("susan")

    # delete any content that might already exist
    rsc_delete_user_content(fs_susan.api)

    yield BoardRsConnect(
        "", fs_susan, allow_pickle_read=True
    )  # fs_susan.ls to list content

    rsc_delete_user_content(fs_susan.api)


def test_board_pin_write(rsc_short):
    v = vetiver.VetiverModel(
        model=model, ptype_data=X_df, model_name="susan/model", versioned=None
    )
    vetiver.vetiver_pin_write(board=rsc_short, model=v)
    assert isinstance(rsc_short.pin_read("susan/model"), sklearn.dummy.DummyRegressor)


@pytest.mark.xfail
def test_deploy(rsc_short):
    v = vetiver.VetiverModel(
        model=model, ptype_data=X_df, model_name="susan/model", versioned=None
    )

    vetiver.vetiver_pin_write(board=rsc_short, model=v)
    connect_server = RSConnectServer(
        url=RSC_SERVER_URL, api_key=server_from_key("susan")
    )
    vetiver.deploy_rsconnect(
        connect_server=connect_server, board=rsc_short, pin_name="susan/model"
    )
    response = vetiver.predict(RSC_SERVER_URL + "/predict", json=X_df)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [44.47, 44.47]}, response.json()
