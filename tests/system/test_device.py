from datetime import datetime
import json
from six import text_type

import ubersmith
import ubersmith.api
import ubersmith.device


def setup_module():
    ubersmith.init(**{
        'base_url': u'',
        'username': u'',
        'password': u'',
    })


def teardown_module():
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_connection_list(response):
    resp_json = {
        'status': True,
        'error_code': None,
        'error_message': u'',
        'data': {
            '60': {
                u'connection_id': u'3',
                u'connection_type_id': u'1',
                u'type_name': u'Unknown',
                u'connection_class_id': u'10000',
                u'name': u'',
                u'status': u'1',
                u'client_id': u'1',
                u'service_id': u'0',
                u'desserv': None,
                u'servtype': None,
                u'src_device_id': u'20003',
                u'src_dev_desc': u'SWITCH_DESC',
                u'src_label': u'SWITCH_LABEL',
                u'src_interface_id': u'11',
                u'src_interface_name': u'GigabitEthernet0/1',
                u'src_node_type_id': u'0',
                u'src_node_type_code': None,
                u'dst_device_id': u'20002',
                u'dst_dev_desc': u'server1.test',
                u'dst_label': u'server1.test',
                u'dst_interface_id': u'1',
                u'dst_interface_name': u'eth0',
                u'dst_node_type_id': u'0',
                u'dst_node_type_code': None,
                u'num_links': u'1',
                u'start_ts': u'1415390350',
                u'end_ts': u'0',
                u'created_ts': u'1415390350',
                u'created_by': u'admin',
                u'updated_ts': u'0',
                u'updated_by': u'',
                u'description': u''
            }
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {
        60: {
            u'connection_id': 3,
            u'connection_type_id': 1,
            u'type_name': 'Unknown',
            u'connection_class_id': 10000,
            u'name': '',
            u'status': 1,
            u'client_id': 1,
            u'service_id': 0,
            u'desserv': None,
            u'servtype': None,
            u'src_device_id': 20003,
            u'src_dev_desc': u'SWITCH_DESC',
            u'src_label': u'SWITCH_LABEL',
            u'src_interface_id': 11,
            u'src_interface_name': u'GigabitEthernet0/1',
            u'src_node_type_id': 0,
            u'src_node_type_code': None,
            u'dst_device_id': 20002,
            u'dst_dev_desc': u'server1.test',
            u'dst_label': u'server1.test',
            u'dst_interface_id': 1,
            u'dst_interface_name': u'eth0',
            u'dst_node_type_id': 0,
            u'dst_node_type_code': None,
            u'num_links': 1,
            u'start_ts': datetime.fromtimestamp(float('1415390350')),
            u'end_ts': datetime.fromtimestamp(float('0')),
            u'created_ts': datetime.fromtimestamp(float('1415390350')),
            u'created_by': u'admin',
            u'updated_ts': datetime.fromtimestamp(float('0')),
            u'updated_by': u'',
            u'description': u''
        }
    }
    assert dict(ubersmith.device.connection_list(device_id=60)) == expected
