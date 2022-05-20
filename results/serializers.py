from rest_framework import serializers
from django.contrib.auth import get_user_model


#local imports 
from .models import OlympicResults, Olympics, OlympicsSubjects, StudentQuestions, StudentTests, OlympicStudentTests
from tests.serializers import QuestionListSerializer, SubjectSerializer
from users.serializers import UserListSerializer

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','pk')

class PostAnswerSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(required=False, many=False)
    class Meta:
        model = StudentQuestions
        # fields = "__all__"
        exclude = ('test',)

        extra_kwargs = {
            # 'test':{'read_only':True},
            'question':{'read_only':True}
        }

class StudentQuestionDetailSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(required=False, many=False)
    subject = SubjectSerializer(required=False, many=False)
    created_by = StudentSerializer(required=False, many=False)
    modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentQuestions
        # fields = "__all__"
        exclude = ('test',)

        extra_kwargs = {
            # 'test':{'read_only':True},
            'question':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
        }



class TestCreateSerializer(serializers.ModelSerializer):
    questions = PostAnswerSerializer(required=False, many=True)
    # subject = SubjectSerializer(required=False, many=False)
    # created_by = StudentSerializer(required=False, many=False)
    # modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentTests
        fields = "__all__"
    
        extra_kwargs = {
            'all_questions':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
            'date_created':{'read_only':True},
            'date_modified': {'read_only':True},
            'right_answers': {'read_only':True}
        }

class TestResultsSerializer(serializers.ModelSerializer):
    questions = PostAnswerSerializer(required=False, many=True)
    subject = SubjectSerializer(required=False, many=False)
    created_by = StudentSerializer(required=False, many=False)
    modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentTests
        fields = "__all__"
    
        extra_kwargs = {
            'all_questions':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
            'date_created':{'read_only':True},
            'date_modified': {'read_only':True},
            'right_answers': {'read_only':True}
        }

#######  OLYMPICS ###################################

class OlympicSubjectsSerializer(serializers.ModelSerializer):
    # subject = SubjectSerializer(required=False, many=False)
    class Meta:
        model = OlympicsSubjects
        fields = ("id", "subject", "questions_count", "ball")

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
        }

class OlympicSubjectsListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(required=False, many=False)
    class Meta:
        model = OlympicsSubjects
        exclude = ("date_created", "date_modified", )

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
        }



class OlympicResultsSerializer(serializers.ModelSerializer):
    created_by = UserListSerializer(required=False, many=False)
    questions = QuestionListSerializer(required=False, many=True)
    class Meta:
        model = OlympicResults
        fields = "__all__"

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
        }

class OlympicResultsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlympicResults
        exclude = ("questions", "date_created", "date_modified")

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
        }

class OlympicPostSerializer(serializers.ModelSerializer):
    subjects = OlympicSubjectsSerializer(required=False, many=True)
    class Meta:
        model = Olympics
        fields = ("title", "image", "text", "time_start", "time_end", "subjects")



class OlympicSerializer(serializers.ModelSerializer):
    subjects = OlympicSubjectsSerializer(required=False, many=True)
    results = OlympicResultsListSerializer(required=False, many=True)
    created_by = UserListSerializer(required=False, many=False)
    class Meta:
        model = Olympics
        fields = "__all__"

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
            'results':{'read_only':True},             

        }

    def create(self, validated_data):
        if "subjects" in validated_data.keys():
            subjects = validated_data.pop("subjects")
        
        olympic = Olympics.objects.create(**validated_data, created_by=self.context['request'].user)
        if subjects:
            for subject in subjects:
                OlympicsSubjects.objects.create(**subject, olympics=olympic, created_by=self.context['request'].user)
        return olympic


class OlympicDetailSerializer(serializers.ModelSerializer):
    subjects = OlympicSubjectsSerializer(required=False, many=True)
    results = OlympicResultsSerializer(required=False, many=True)
    class Meta:
        model = Olympics
        fields = "__all__"

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},             
            'results':{'read_only':True},
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.save()
        return instance



class OlympicStudentTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlympicStudentTests
        fields = "__all__"

        extra_kwargs = {
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True}, 
            'result': {'read_only':True}
            }