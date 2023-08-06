import datetime
import json

from hadata.meta import MongoDiagnostics
from hautils.logger import logger


def get_diagnostic_record(service):
    return MongoDiagnostics.objects(service=service).order_by('-timestamp').first()


def add_diagnostic_record(service, remark):
    diagnostic = MongoDiagnostics.objects(service=service).first()
    if diagnostic is not None:
        logger.info("diagnostic record found %s" % (json.dumps(diagnostic.to_json())))
        diagnostic.timestamp = datetime.datetime.now().timestamp()
        diagnostic.remarks = json.dumps(remark)
        diagnostic.save()
    else:
        diagnostic = MongoDiagnostics(service=service)
        logger.info("creating new diagnostic record")
        diagnostic.timestamp = datetime.datetime.now().timestamp()
        diagnostic.remarks = json.dumps(remark)
        diagnostic.save()
    return diagnostic.id
