import base64
import copy
import json
import re
from decimal import Decimal

from cerberus import Validator

from one_table.Utils import get_iso_8601_date


class Table(object):
    def __init__(self, params: dict):
        self.params_list = ["name", "schema", "client"]
        for p in self.params_list:
            if p not in params:
                raise Exception(f'Missing {p} property')
        self.debug = params.get('debug', False)
        self.json_api = params.get('jsonApi', False)
        self.table_name = params['name']
        self.schema = params['schema']
        self.models = params['schema']['models']
        self.client = params['client'].Table(params['name'])
        self.pk_key = self.schema['indexes']['primary']['hash']
        self.sk_key = self.schema['indexes']['primary']['sort']
        self.filter_key = "filter"
        self.scan_index_forward = "ScanIndexForward"
        self.id_key = "idKey"
        self.consistent_read_key = "ConsistentRead"
        self.filter_expressions = {
            "eq": "=",
            "neq": "<>"
        }

    def get_client(self):
        return self.client

    def generate_response_json_api(self, raw_response_: dict, _schema: dict, _model: str, _limit: int,
                                   _id_key: str) -> dict:
        if raw_response_['Count'] > 0:
            if self.debug:
                print(raw_response_)
            r = []
            for idx, item in enumerate(raw_response_['Items']):
                r.append(
                    {"id": item.get(_id_key, ""), "type": _model,
                     "attributes": {k: v for k, v in item.items() if k in _schema.keys()}})

            return {
                "data": r,
                "meta": {
                    "nextPage": base64.b64encode(
                        json.dumps(raw_response_.get("LastEvaluatedKey")).encode('utf-8')).decode(
                        'utf-8') if raw_response_.get("LastEvaluatedKey", False) else None,
                    "itemsPerPage": _limit,
                    "count": raw_response_['Count'],
                }
            }
        return {
            "data": [],
            "meta": {
                "nextPage": None,
                "itemsPerPage": _limit,
                "count": 0,
            }
        }

    def generate_response(self, raw_response_: dict, _schema: dict) -> dict:
        if raw_response_['Count'] > 0:
            if self.debug:
                print(raw_response_)
            r = []
            for idx, item in enumerate(raw_response_['Items']):
                r.append({k: v for k, v in item.items() if k in _schema.keys()})
            return {
                "nextKey": base64.b64encode(
                    json.dumps(raw_response_.get("LastEvaluatedKey")).encode('utf-8')).decode(
                    'utf-8') if raw_response_.get("LastEvaluatedKey", False) else None,
                "count": raw_response_['Count'],
                "items": r
            }
        return {
            "nextKey": None,
            "count": raw_response_['Count'],
            "items": []
        }

    def get_model(self, model: str) -> dict:
        return self.models[model]

    def create(self, model: dict, data_: dict) -> dict:
        _schema = copy.deepcopy(self.models[model])
        sk = self.models[model][self.sk_key]['value']
        pk = self.models[model][self.pk_key]['value']
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        v = Validator(_schema)
        v.validate(data_)
        if v.validate(data_):
            data_[self.pk_key] = pk.format(**data_)
            data_[self.sk_key] = sk.format(**data_)
            data_['createdAt'] = get_iso_8601_date()
            data_['updatedAt'] = get_iso_8601_date()
            data_['_type'] = model
            self.client.put_item(Item=data_)
            return {k: v for k, v in data_.items() if k in _schema.keys()}
        else:
            raise Exception(v.errors)

    def update(self, model, data_):
        _schema = copy.deepcopy(self.models[model])
        _data = copy.deepcopy(data_)
        sk = self.models[model][self.sk_key]['value']
        pk = self.models[model][self.pk_key]['value']
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        pk_keys = re.findall(r'\{([A-Za-z0-9_]+)\}', pk)
        sk_keys = re.findall(r'\{([A-Za-z0-9_]+)\}', sk)
        index_keys = pk_keys + sk_keys
        for item in _schema:
            if item in index_keys:
                _schema[item]['required'] = True
            else:
                _schema[item]['required'] = False

        v = Validator(_schema)
        v.validate(data_)
        if v.validate(data_):
            data_key = data_.keys()
            expression_attribute_names = {}
            expression_attribute_values = {}
            update_expression = []
            data_['updated_at'] = get_iso_8601_date()
            for idx, key in enumerate(data_key):
                expression_attribute_names['#k{}'.format(idx)] = key
                expression_attribute_values[':v{}'.format(idx)] = data_[key]
                update_expression.append('#k{} = :v{}'.format(idx, idx))

            pk_key_parsed = pk.format(**data_)
            sk_key_parsed = sk.format(**data_)

            request = {
                'ConditionExpression': '(attribute_exists({})) AND (attribute_exists({}))'.format(self.pk_key,
                                                                                                  self.sk_key),
                'ExpressionAttributeNames': expression_attribute_names,
                'ExpressionAttributeValues': expression_attribute_values,
                'UpdateExpression': 'set {}'.format(', '.join(update_expression)),
                'ReturnValues': 'ALL_NEW',
                'Key': {
                    'pk': pk_key_parsed,
                    'sk': sk_key_parsed
                }
            }
            if self.debug:
                print(request)
            response = self.client.update_item(**request)
            if 'Attributes' in response:
                return {k: v for k, v in response['Attributes'].items() if k in _schema.keys()}
            return response
        else:
            raise Exception(v.errors)

    def counter(self, model, action, query, value=1):
        _schema = copy.deepcopy(self.models[model])
        action = "+" if action == "increment" else "-"
        request = {"Key": {
            self.pk_key: query[self.pk_key],
            self.sk_key: query[self.sk_key],
        },
            "UpdateExpression": "set #att = #att {} :val".format(action),
            "ExpressionAttributeValues": {
                ':val': Decimal(value)
            },
            'ReturnValues': 'ALL_NEW',
            "ExpressionAttributeNames": {
                "#att": query["key"]
            }}
        if self.debug:
            print(request)
        response = self.client.update_item(**request)
        return response.get('Attributes')

    def find(self, model: str, query: dict, limit=100, next_key=None):
        _schema = copy.deepcopy(self.models[model])
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        scan_index_forward = query.get(self.scan_index_forward, True)
        consistent_read_key = query.get(self.consistent_read_key, False)
        filter_exp = {}
        filter_values = {}
        filter_values_operators = ""
        if self.filter_key in query:
            if len(query[self.filter_key]) > 0:
                for index, flt in enumerate(query[self.filter_key]):
                    filter_exp["#n{}".format(index + 2)] = next(iter(flt[next(iter(flt))]))
                    filter_values[":v{}".format(index + 2)] = flt[next(iter(flt))][next(iter(flt[next(iter(flt))]))]
                    operand = " AND " if index > 0 else ""
                    filter_operator = self.filter_expressions[next(iter(flt))]
                    filter_values_operators = filter_values_operators + "{o} #n{idx} {fe} :v{idx}".format(
                        o=operand, fe=filter_operator, idx=index + 2)

        expression_attribute_names = {**{'#n0': self.schema['indexes']['primary']['hash'],
                                         '#n1': self.schema['indexes']['primary']['sort'], }, **filter_exp}
        expression_attribute_values = {**{
            ':v0': '{}'.format(query[self.pk_key]),
            ':v1': '{}'.format(list(query[self.sk_key].values())[0]),

        }, **filter_values}

        request = {
            'ExpressionAttributeNames': expression_attribute_names,
            'ExpressionAttributeValues': expression_attribute_values,
            'KeyConditionExpression': '#n0 = :v0 AND {}(#n1, :v1)'.format(list(query[self.sk_key].keys())[0]),
            "ConsistentRead": consistent_read_key,
            "ScanIndexForward": scan_index_forward,
            "Limit": limit,
        }
        if self.filter_key in query:
            if len(query[self.filter_key]) > 0:
                request["FilterExpression"] = filter_values_operators.strip()

        if next_key:
            request['ExclusiveStartKey'] = json.loads(base64.b64decode(next_key))

        _schema["createdAt"] = ""
        _schema["updatedAt"] = ""
        if self.debug:
            print(request)
        response = self.client.query(**request)
        id_key = query.get(self.id_key, "id")
        if self.json_api:
            return self.generate_response_json_api(response, _schema, model, limit, id_key)
        else:
            return self.generate_response(response, _schema)

    def delete(self, query: dict):
        pk = self.schema['indexes']['primary']['hash']
        sk = self.schema['indexes']['primary']['sort']
        self.client.delete_item(
            Key={
                pk: query[self.pk_key],
                sk: query[self.sk_key],
            }
        )

    def find_by_sort_key(self, model: str, query: dict, limit=100, next_key=None):
        print("Deprecated. Please use find() instead.")
        return self.find(model, query, limit, next_key)

    def find_by_sort_key_filter(self, model: str, query: dict, limit=100, next_key=None):
        print("Deprecated. Please use find() instead.")
        return self.find(model, query, limit, next_key)
