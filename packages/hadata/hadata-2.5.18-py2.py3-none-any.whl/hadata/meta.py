from mongoengine import Document, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class MongoLevel(Document):
    meta = {'collection': 'level'}
    organization_id = StringField()
    level_name = StringField()
    level_description = StringField()


class MongoRoles(Document):
    meta = {'collection': 'roles'}
    role_name = StringField(required=True)
    role_description = StringField(required=False)


class MongoSkill(Document):
    meta = {'collection': 'skill'}
    organization_id = StringField()
    skill_name = StringField(unique=True)
    skill_description = StringField()


class MongoSubskill(Document):
    meta = {'collection': 'subskill'}
    subskill_name = StringField()
    parent_skill_name = StringField()
    parent_skill_id = StringField()
    layer = IntField(required=False)


class MongoTranscriptFilter(Document):
    meta = {'collection': 'transcript_filter', 'indexes': [
        {'fields': ('job_id', 'start_position', 'end_position'), 'unique': True}
    ]}
    start_position = IntField(required=True)
    end_position = IntField(required=True)
    filtered_transcript = StringField(required=True)
    status = StringField(required=True)
    job_id = StringField(required=True)


class MongoRole(Document):
    meta = {'collection': 'role'}
    sample_field = StringField()


class MongoProjects(Document):
    meta = {'collection': 'projects'}
    sample_field = StringField()


class MongoFocusArea(Document):
    meta = {'collection': 'focus_area'}
    sample_field = StringField()


class MongoDiagnostics(Document):
    meta = { 'collection' : 'diagnostic' }
    service = StringField()
    timestamp = FloatField()
    remarks = StringField()