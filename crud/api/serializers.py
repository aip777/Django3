from  rest_framework import serializers

from crud.models import CsvUpload

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvUpload
        fields = [
            'id',
            'start_date',
            'affectedtoday',
            'todayRecovered',
            'todayDeaths',
            'todayTests',
            'totalPositive',
            'totalRecovered',
            'totalDeaths',
            'totalTests',

        ]
        # read_only_fields = ['user']
        # def validate_content(self, value):
        #     if len(value) > 10000:
        #         raise serializers.ValidationError("This is wayy too long.")
        #     return value

        def validate(self, data):
            name = data.get("name", None)
            if name == "":
                name = None
            description = data.get("description", None)
            if name is None and description is None:
                raise serializers.ValidationError("title or image is required.")
            return data




