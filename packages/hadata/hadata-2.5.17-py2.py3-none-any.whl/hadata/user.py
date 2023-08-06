from mongoengine import Document, EmailField, StringField, ObjectIdField, DateTimeField, IntField, FloatField, \
    BooleanField, ListField


class MongoUser(Document):
    meta = {'collection': 'user'}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    organization_id = StringField(required=True)
    profile_type = IntField(required=True)
    is_verified = BooleanField(required=True, default=False)

    def ids(self):
        return str(self.id)


class MongoPasswordHistory(Document):
    meta = {'collection': 'password_history'}
    user_id = StringField(required=True)
    password = StringField(required=True, min_length=8)


class MongoUserProfile(Document):
    meta = {'collection': 'user_profile'}
    user_id = StringField(required=True, unique=True)
    role = StringField()
    focus_area = StringField()
    projects = ListField(StringField())


class MongoUserAssessmentsQuestionAnswerStatusHistory(Document):
    meta = {'collection': 'user_assessment_question_answer_status_history'}
    user_assessment_question_answer_id = StringField(required=True)
    status = StringField(required=True)
    created_datetime = DateTimeField(required=True)


class MongoUserObjectives(Document):
    meta = {'collection': 'user_objectives'}
    user_id = StringField(required=True, unique=True)
    sample_field = StringField()



