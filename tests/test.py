import urllib.error
import urllib.request
import urllib.parse
import json


ENDPOINT = "http://localhost:8000"

EVENTS_PATH = '/events'
EVENTS_MULTI_PATH = '/events/multi'

SENSORS_PATH = '/sensors'
SENSORS_MULTI_PATH = '/sensors/multi'

EVENTSDATA = {
    "name": "events",
    "create": {
        "sensor_id": 123,
        "name": "create_test",
        "temperature": 50,
        "humidity": 99
    },
    "some_event_id": 1,
    "create_multi": {
        "events": [
            {
            "sensor_id": 1,
            "name": "create_multi",
            "temperature": 50,
            "humidity": 100
            },
            {
            "sensor_id": 2,
            "name": "create_multi",
            "temperature": 100,
            "humidity": 50
            },
            {
            "sensor_id": 3,
            "name": "create_multi",
            "temperature": 23,
            "humidity": 32
            },
            {
            "sensor_id": 4,
            "name": "create_multi",
            "temperature": 0,
            "humidity": 100
            }
        ]
    },
    "update": {
        "sensor_id": 321,
        "name": "update_test",
        "temperature": 99,
        "humidity": 50
    },
    "get_all": {
        "page": 1,
        "size": 100
    },
    "filter_by": {
        'temperature': 50,
        "humidity": 50
    },
    "filter_match":[
        {
            "id": 1,
            "sensor_id": 1,
            "name": "string",
            "temperature": 50,
            "humidity": 100
        },
        {
            "id": 2,
            "sensor_id": 2,
            "name": "string",
            "temperature": 100,
            "humidity": 50
        }
    ]

}

SENSORSDATA = {
    "name": "sensors",
    "create": {
        "id": 1,
        "name": "create_test",
        "type": 2
    },
    "create_multi":{
        "sensors": [
            {
                "id": 123,
                "name": "create_multi_test",
                "type": 2
            },
            {
                "id": 133,
                "name": "create_multi_test",
                "type": 3
            },
            {
                "id": 144,
                "name": "create_multi_test",
                "type": 2
            },
            {
                "id": 155,
                "name": "create_multi_test",
                "type": 3
            },
        ]
    },
    "update": {
        "name": "update_test",
        "type": 3
    },
    "get_all": {
        "page": 1,
        "size": 100
    }
}


def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{ENDPOINT}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)
    
def create_assert_message(status: int, func_name:str, method: str=None):
    return f"Expected HTTP status code 200, got {status}" + \
        f"\nFrom {func_name} {method}"

def test_crud(data: dict, append_path: str):

    print(f"start {test_crud.__name__} - {data['name']}")
    # create
    status, response = request(append_path, method='POST', data=data['create'])
    assert status == 200, create_assert_message(status, test_crud.__name__, method='POST')
    print("\tcreate OK")

    if append_path == EVENTS_PATH:
        obj_id = data['some_event_id']
    else:
        obj_id = data['create']['id']

    # get
    status, response = request(append_path + f'/{obj_id}')
    assert status == 200, create_assert_message(status, test_crud.__name__, method='GET')
    print("\tget OK")

    # update
    status, response = request(append_path + f'/{obj_id}', method="PUT", data=data['update'])
    assert status == 200, create_assert_message(status, test_crud.__name__, method='PUT')
    print("\tupdate OK")
    
    # delete
    status, response = request(append_path + f'/{obj_id}', method="DELETE")
    assert status == 200, create_assert_message(status, test_crud.__name__, method='DELETE')
    print("\tdelete OK")


def test_create_multi(data: dict, append_path: str):
    print(f"start {test_create_multi.__name__} {data['name']}")

    status, response = request(append_path, method="POST", data=data['create_multi'])
    assert status == 200, create_assert_message(status, test_create_multi.__name__)
    print("\t OK")


def test_get_all(data: dict, append_path: str):
    print(f"start {test_get_all.__name__} {data['name']}")

    status, response = request(append_path, data=data['get_all'])
    assert status == 200, create_assert_message(status, test_get_all.__name__)
    print("\t OK")


def test_sensors_match():
    print(f"start {test_sensors_match.__name__}")

    status, response = request(SENSORS_PATH + '/multi', method="POST", data=SENSORSDATA['create_multi'])
    assert status == 200, create_assert_message(status, test_sensors_match.__name__, 'POST')
    print("\t multi OK")

    responsed_sensors = []
    for sensor in SENSORSDATA['create_multi']['sensors']:
        status, response = request(SENSORS_PATH+ f"/{sensor['id']}")
        assert status == 200, create_assert_message(status, test_sensors_match.__name__, 'GET')
        responsed_sensors.append(json.loads(response)['result'])

    if responsed_sensors == SENSORSDATA['create_multi']['sensors']:
        print("\t match OK")
    else: 
        print("\t match NOT passed")
   
def test_get_events_by_sensor_id():
    print(f"start {test_get_events_by_sensor_id.__name__}")

    # create
    status, response = request(EVENTS_PATH, method='POST', data=EVENTSDATA['create'])
    assert status == 200, create_assert_message(status, test_crud.__name__, method='POST')
    print("\t create OK")

    # get by sensor id
    status, response = request(EVENTS_PATH + f"/by-sensor-id/{EVENTSDATA['create']['sensor_id']}")
    assert status == 200, create_assert_message(status, test_get_events_by_sensor_id.__name__)
    print("\t get OK")

def test_get_filtered_events():
    print(f"start {test_get_filtered_events.__name__}")

    # get filtered events
    status, response = request(EVENTS_PATH + f"/filter-by/", data=EVENTSDATA['filter_by'])
    assert status == 200, create_assert_message(status, test_get_filtered_events.__name__)
    print('\t OK')

def test_con_endpoint():
    status, response = request('/docs')
    assert status == 200, create_assert_message(status, test_con_endpoint.__name__)

def main():
    test_con_endpoint()
    test_crud(EVENTSDATA, EVENTS_PATH)
    test_crud(SENSORSDATA, SENSORS_PATH)
    test_create_multi(EVENTSDATA, EVENTS_MULTI_PATH)
    test_create_multi(SENSORSDATA, SENSORS_MULTI_PATH)
    test_get_all(EVENTSDATA, EVENTS_PATH)
    test_get_all(SENSORSDATA, SENSORS_PATH)
    test_sensors_match()
    test_get_events_by_sensor_id()
    test_get_filtered_events()

if __name__ == '__main__':
    main()