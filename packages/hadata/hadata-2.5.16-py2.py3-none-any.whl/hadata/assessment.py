from datetime import datetime

from mongoengine import Document, StringField, ObjectIdField, DateTimeField, IntField, FloatField, BooleanField


class MongoUserAssessment(Document):
    meta = {'collection': 'user_assessment', 'indexes': [
        {'fields': ('user_id', 'assessment_id'), 'unique': True}
    ]}
    enabled = BooleanField(required=True, default=True)
    score = IntField(required=True, default=0)
    status = StringField(required=True)
    user_id = StringField(required=True)
    assessment_id = StringField(required=True)
    start_time = DateTimeField(required=False)
    end_time = DateTimeField(required=False)
    marked = BooleanField(required=True, default=False)


class MongoAssessments(Document):
    meta = {'collection': 'assessments'}
    assessment_type = StringField(required=True)
    assessment_title = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    is_active = BooleanField(required=True, default=False)
    description = StringField(required=True)
    organization_id = StringField(required=True)
    user_id = StringField(required=False)
    creation_date_time = DateTimeField(required=False)

    def get_profile(self):
        if self.assessment_type == "candidate":
            return 4
        elif self.assessment_type == "employee":
            return 3
        else:
            return 0


class MongoAssessmentsQuestionAnswer(Document):
    meta = {'collection': 'assessments_question_answer'}
    assessment_id = StringField(required=True)
    question_answer_id = StringField(required=True)
    sort_order = IntField(required=True)


class MongoAssessmentsSettings(Document):
    meta = {'collection': 'assessments_settings'}
    assessment_id = StringField(required=True)
    show_score = BooleanField(required=True, default=True)
    shuffle_questions = BooleanField(required=True, default=True)
    enable_copy = BooleanField(required=True, default=True)
    attempt_count = IntField(required=True, default=0)
    custom_message = StringField(required=True)
