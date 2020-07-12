from  rest_framework import serializers

from crud.models import CsvUpload, CsvUploadFile

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


class DistrictAndDivision(serializers.ModelSerializer):
    class Meta:
        model = CsvUploadFile
        fields = [
            'id','start_date', 'Bagerhat', 'Bandarban', 'Barguna', 'Barisal', 'Bhola', 'Bogra', 'Brahmanbaria', 'Chandpur', 'Chittagong',
            'Chuadanga', 'Comilla', 'CoxsBazar', 'Dhaka', 'Dinajpur', 'Faridpur', 'Feni', 'Gaibandha', 'Gazipur', 'Gopalganj', 'Habiganj',
            'Jaipurhat', 'Jamalpur', 'Jessore', 'Jhalakati', 'Jhenaidah', 'Khagrachari', 'Khulna', 'Kishoreganj', 'Kurigram', 'Kushtia',
            'Lakshmipur', 'Lalmonirhat', 'Madaripur', 'Magura', 'Manikganj', 'Meherpur', 'Moulvibazar', 'Munshiganj', 'Mymensingh',
            'Naogaon', 'Narail', 'Narayanganj', 'Narsingdi', 'Natore', 'Nawabganj', 'Netrakona', 'Nilphamari', 'Noakhali', 'Pabna',
            'Panchagarh', 'ParbattyaChattagram', 'Patuakhali', 'Pirojpur', 'Rajbari', 'Rajshahi', 'Rangpur', 'Satkhira', 'Shariatpur',
            'Sherpur', 'Sirajganj', 'Sunamganj', 'Sylhet', 'Tangail', 'Thakurgaon', 'SylhetDivision', 'RangpurDivision',
            'RajshahiDivision', 'MymensinghDivision', 'KhulnaDivision', 'DhakaDivision', 'ChittagongDivision', 'BarisalDivision',

        ]



