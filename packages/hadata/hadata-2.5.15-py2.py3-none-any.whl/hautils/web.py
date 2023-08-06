import datetime
import traceback

import bson
from fastapi.responses import Response
from hautils.logger import logger
import json
from mongoengine import Document, QuerySet, DateTimeField, ObjectIdField
from pydantic import BaseModel
from fastapi import status

from hautils.slack import slack_notify


def mongo_to_dict(content):
    if not issubclass(type(content), Document) and not issubclass(type(content), dict) and not issubclass(type(content),
                                                                                                          BaseModel):
        logger.warn("unsupported object type %s " % (type(content)))
        raise Exception
    if issubclass(type(content), Document):
        response_object = json.loads(content.to_json())
        # response_object["id"] = str(content.id)
        response_object.pop("_id")
        for field in type(content)._fields.values():
            logger.debug("handling field %s of type %s" % (field.name, type(content[field.name])))
            if isinstance(content[field.name], DateTimeField) and content[field.name] is not None:
                response_object[field.name] = int(content[field.name].timestamp())
            elif isinstance(content[field.name], datetime.datetime) and content[field.name] is not None:
                response_object[field.name] = int(content[field.name].timestamp())
            elif isinstance(content[field.name], bson.objectid.ObjectId) and content[field.name] is not None:
                response_object[field.name] = str(content[field.name])
            elif isinstance(content[field.name], ObjectIdField) and content[field.name] is not None:
                response_object[field.name] = str(content[field.name])
    elif issubclass(type(content), BaseModel):
        response_object = content.dict()
    else:
        logger.debug("format type %s" % (type(content)))
        response_object = content

    return response_object


def json_response(content, http_status=200, pop_fields=list()):
    try:
        if issubclass(type(content), QuerySet) or issubclass(type(content), list):
            response = []
            for doc in content:
                response.append(doc_cleanup(doc, pop_fields))
        else:
            response = doc_cleanup(content, pop_fields)
        logger.debug("json dumping type %s" % (type(response)))
        response = json.dumps(response)
        logger.info("json encode %s" % (response,))
        return Response(content=response, status_code=http_status, media_type="application/json")
    except Exception as e:
        exception_log(e)


def doc_cleanup(doc, pop_fields):
    response = mongo_to_dict(doc)
    for field in pop_fields:
        try:
            response.pop(field)
        except Exception as e:
            logger.error("field %s not in dictionary" % (field,))
    return response


def mongo_to_log(content):
    try:
        return json.dumps(mongo_to_dict(content))
    except Exception as e:
        return ""


def exception_log(e):
    logger.error(e)
    traceback_log = traceback.format_exception(type(e), e, e.__traceback__)
    logger.debug(traceback_log)
    formatted_message = """# Exception 

```
{}}
```
""".format(traceback_log)
    slack_notify(message=formatted_message)
    raise ProcessException(http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, errors={"error": str(type(e))})


class ProcessException(Exception):
    def __init__(self, errors=None, data=None, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        if data is None:
            data = {}
        self.errors = errors
        self.data = data
        self.status = http_status
