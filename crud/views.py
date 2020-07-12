from django.shortcuts import render, redirect
from .models import Member, Document, ContactList, CsvUpload,CsvUploadFile
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from crud.forms import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def list(request):
    members_list = Member.objects.all()
    paginator = Paginator(members_list, 5)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'members': members})

@login_required
def create(request):
    if request.method == 'POST':
        member = Member(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            mobile_number=request.POST['mobile_number'],
            description=request.POST['description'],
            location=request.POST['location'],
            date=request.POST['date'],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(), )
        try:
            member.full_clean()
        except ValidationError as e:
            pass
        member.save()
        messages.success(request, 'Member was created successfully!')
        return redirect('/list')
    else:
        return render(request, 'add.html')

@login_required
def edit(request, id):
    members = Member.objects.get(id=id)
    context = {'members': members}
    return render(request, 'edit.html', context)


@login_required
def update(request, id):
    member = Member.objects.get(id=id)
    member.firstname = request.POST['firstname']
    member.lastname = request.POST['lastname']
    member.mobile_number = request.POST['mobile_number'],
    member.description = request.POST['description'],
    member.location = request.POST['location'],
    member.date = request.POST['date'],
    member.save()
    messages.success(request, 'Member was updated successfully!')
    return redirect('/list')

@login_required
def delete(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.error(request, 'Member was deleted successfully!')
    return redirect('/list')


@login_required
def fileupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        document = Document(
            description=request.POST['description'],
            document=myfile.name,
            uploaded_at=datetime.datetime.now(), )
        document.save()
        messages.success(request, 'Member was created successfully!')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return redirect('fileupload')
    else:
        documents = Document.objects.order_by('-uploaded_at')[:3]
        context = {'documents': documents}
    return render(request, 'fileupload.html', context)


@login_required
def ajax(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = ContactList(
                text=request.POST['text'],
                search=request.POST['search'],
                email=request.POST['email'],
                telephone=request.POST['telephone'],
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            data.save()
            astr = "<html><b> you sent an ajax post request </b> <br> returned data: %s</html>" % data
            return JsonResponse({'data': 'success'})
    else:
        ajax_list = ContactList.objects.order_by('-created_at')
        context = {'ajax_list': ajax_list}
    return render(request, 'ajax.html', {'ajax_list': ajax_list})


@csrf_protect
def getajax(request):
    if request.method == 'GET':
        if request.is_ajax():
            data = ContactList.objects.order_by('-created_at').first()
            created = data.created_at.strftime('%m-%d-%Y %H:%M:%S')
            datas = {"id": data.id, "text": data.text, "search": data.search, "email": data.email,
                     "telephone": data.telephone, "created_at": created}
            return JsonResponse(datas)
    else:
        return JsonResponse({'data': 'failure'})


@csrf_protect
def ajax_delete(request):
    if request.method == 'GET':
        if request.is_ajax():
            id = request.GET['id']
            ajax = ContactList.objects.get(id=id)
            ajax.delete()
            return JsonResponse({'data': 'success'})
    else:
        return JsonResponse({'data': 'failure'})


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                is_staff=True,
                is_active=True,
                is_superuser=True,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'success.html')

@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.error(request, 'User was deleted successfully!')
    return redirect('/users')

@login_required
def upload_csv(request):
    if 'GET' == request.method:
        # csv_list = CsvUpload.objects.all()
        # paginator = Paginator(csv_list, 7)
        # page = request.GET.get('page')
        # try:
        #     csvdata = paginator.page(page)
        # except PageNotAnInteger:
        #     csvdata = paginator.page(1)
        # except EmptyPage:
        #     csvdata = paginator.page(paginator.num_pages)
        # return render(request, 'upload_csv.html', {'csvdata': csvdata})
        csvdata = CsvUpload.objects.all()
        context = {'csvdata': csvdata}
        return render(request, 'upload_csv.html', context)
    try:
        csv_file = request.FILES["csv_file"]

        if len(csv_file) == 0:
            messages.error(request, 'Empty File')
            return render(request, 'upload_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return render(request, 'upload_csv.html')

        if csv_file.multiple_chunks():
            messages.error(request, 'Uploaded file is too big (%.5f MB).' % (csv_file.size / (10000 * 10000),))
            return render(request, 'upload_csv.html')

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        for index, line in enumerate(lines):
            fields = line.split(",")
            if index == 0:
                if (fields[0] == 'name') \
                        and (fields[1] == 'end_date') \
                        and (fields[2] == 'affectedtoday') \
                        and (fields[3] == 'todayRecovered') \
                        and (fields[4] == 'todayDeaths') \
                        and (fields[5] == 'todayTests') \
                        and (fields[6] == 'totalPositive') \
                        and (fields[7] == 'totalRecovered') \
                        and (fields[8] == 'totalDeaths') \
                        and (fields[9] == 'totalTests') \
                        and (fields[10] == 'start_date'):
                    pass
                else:
                    messages.error(request, 'File is not Correct Headers')
                    return render(request, 'upload_csv.html')
                    break
            else:
                print(index)
                if (len(fields[0]) != 0) \
                        and (len(fields[1]) != 0) \
                        and (len(fields[2]) != 0) \
                        and (len(fields[3]) != 0) \
                        and (len(fields[4]) != 0) \
                        and (len(fields[5]) != 0) \
                        and (len(fields[6]) != 0) \
                        and (len(fields[7]) != 0) \
                        and (len(fields[8]) != 0) \
                        and (len(fields[9]) != 0)\
                        and (len(fields[10]) != 0):
                    data = CsvUpload(
                        name=fields[0],
                        end_date=datetime.datetime.now(),
                        affectedtoday=fields[2],
                        todayRecovered=fields[3],
                        todayDeaths=fields[4],
                        todayTests=fields[5],
                        totalPositive=fields[6],
                        totalRecovered=fields[7],
                        totalDeaths=fields[8],
                        totalTests=fields[9],
                        start_date=fields[10]
                    )
                    data.save()
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect('/upload/csv/')

    except Exception as e:
        # messages.error(request, "Unable to upload file. " + e)
        return redirect('/upload/csv/')


@login_required
def changePassword(request):
    print('changepasword')
    return render(request, 'change_password.html')


@login_required
def deleteFiles(request, id):
    file = Document.objects.get(id=id)
    file.delete()
    messages.error(request, 'User was deleted successfully!')
    return redirect('/fileupload')

@login_required
def upload_csv_file(request):
    if 'GET' == request.method:
        # csv_list = CsvUpload.objects.all()
        # paginator = Paginator(csv_list, 7)
        # page = request.GET.get('page')
        # try:
        #     csvdata = paginator.page(page)
        # except PageNotAnInteger:
        #     csvdata = paginator.page(1)
        # except EmptyPage:
        #     csvdata = paginator.page(paginator.num_pages)
        # return render(request, 'upload_csv.html', {'csvdata': csvdata})
        csvdatafield = CsvUploadFile.objects.all()
        context = {'csvdatafield': csvdatafield}
        return render(request, 'Csv/upload_csv.html', context)
    try:
        csv_file_district = request.FILES["csv_file_district"]

        if len(csv_file_district) == 0:
            messages.error(request, 'Empty File')
            return render(request, 'Csv/upload_csv.html')

        if not csv_file_district.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return render(request, 'Csv/upload_csv.html')

        if csv_file_district.multiple_chunks():
            messages.error(request, 'Uploaded file is too big (%.5f MB).' % (csv_file_district.size / (100000 * 100000),))
            return render(request, 'Csv/upload_csv.html')

        file_data = csv_file_district.read().decode("utf-8")

        lines = file_data.split("\n")
        for index, line in enumerate(lines):
            fields = line.split(",")
            if index == 0:
                if (fields[0] == 'start_date') \
                        and (fields[1] == 'Bagerhat') \
                        and (fields[2] == 'Bandarban') \
                        and (fields[3] == 'Barguna') \
                        and (fields[4] == 'Barisal') \
                        and (fields[5] == 'Bhola') \
                        and (fields[6] == 'Bogra') \
                        and (fields[7] == 'Brahmanbaria') \
                        and (fields[8] == 'Chandpur') \
                        and (fields[9] == 'Chittagong') \
                        and (fields[10] == 'Chuadanga') \
                        and (fields[11] == 'Comilla') \
                        and (fields[12] == 'CoxsBazar') \
                        and (fields[13] == 'Dhaka') \
                        and (fields[14] == 'Dinajpur') \
                        and (fields[15] == 'Faridpur') \
                        and (fields[16] == 'Feni') \
                        and (fields[17] == 'Gaibandha') \
                        and (fields[18] == 'Gazipur') \
                        and (fields[19] == 'Gopalganj') \
                        and (fields[20] == 'Habiganj') \
                        and (fields[21] == 'Jaipurhat') \
                        and (fields[22] == 'Jamalpur') \
                        and (fields[23] == 'Jessore') \
                        and (fields[24] == 'Jhalakati') \
                        and (fields[25] == 'Jhenaidah') \
                        and (fields[26] == 'Khagrachari') \
                        and (fields[27] == 'Khulna') \
                        and (fields[28] == 'Kishoreganj') \
                        and (fields[29] == 'Kurigram') \
                        and (fields[30] == 'Kushtia') \
                        and (fields[31] == 'Lakshmipur') \
                        and (fields[32] == 'Lalmonirhat') \
                        and (fields[33] == 'Madaripur') \
                        and (fields[34] == 'Magura') \
                        and (fields[35] == 'Manikganj') \
                        and (fields[36] == 'Meherpur') \
                        and (fields[37] == 'Moulvibazar') \
                        and (fields[38] == 'Munshiganj') \
                        and (fields[39] == 'Mymensingh') \
                        and (fields[40] == 'Naogaon') \
                        and (fields[41] == 'Narail') \
                        and (fields[42] == 'Narayanganj') \
                        and (fields[43] == 'Narsingdi') \
                        and (fields[44] == 'Natore') \
                        and (fields[45] == 'Nawabganj') \
                        and (fields[46] == 'Netrakona') \
                        and (fields[47] == 'Nilphamari') \
                        and (fields[48] == 'Noakhali') \
                        and (fields[49] == 'Pabna') \
                        and (fields[50] == 'Panchagarh') \
                        and (fields[51] == 'ParbattyaChattagram') \
                        and (fields[52] == 'Patuakhali') \
                        and (fields[53] == 'Pirojpur') \
                        and (fields[54] == 'Rajbari') \
                        and (fields[55] == 'Rajshahi') \
                        and (fields[56] == 'Rangpur') \
                        and (fields[57] == 'Satkhira') \
                        and (fields[58] == 'Shariatpur') \
                        and (fields[59] == 'Sherpur') \
                        and (fields[60] == 'Sirajganj') \
                        and (fields[61] == 'Sunamganj') \
                        and (fields[62] == 'Sylhet') \
                        and (fields[63] == 'Tangail') \
                        and (fields[64] == 'Thakurgaon') \
                        and (fields[65] == 'SylhetDivision') \
                        and (fields[66] == 'RangpurDivision') \
                        and (fields[67] == 'RajshahiDivision') \
                        and (fields[68] == 'MymensinghDivision') \
                        and (fields[69] == 'KhulnaDivision') \
                        and (fields[70] == 'DhakaDivision') \
                        and (fields[71] == 'ChittagongDivision') \
                        and (fields[72] == 'BarisalDivision'):
                    pass
                else:
                    messages.error(request, 'File is not Correct Headers')
                    return render(request, 'Csv/upload_csv.html')
                    break
            else:
                print(index)
                if (len(fields[0]) != 0) \
                        and (len(fields[1]) != 0) \
                        and (len(fields[2]) != 0) \
                        and (len(fields[3]) != 0) \
                        and (len(fields[4]) != 0) \
                        and (len(fields[5]) != 0) \
                        and (len(fields[6]) != 0) \
                        and (len(fields[7]) != 0) \
                        and (len(fields[8]) != 0) \
                        and (len(fields[9]) != 0)\
                        and (len(fields[10]) != 0)\
                        and (len(fields[11]) != 0)\
                        and (len(fields[12]) != 0)\
                        and (len(fields[13]) != 0)\
                        and (len(fields[14]) != 0)\
                        and (len(fields[15]) != 0)\
                        and (len(fields[16]) != 0)\
                        and (len(fields[17]) != 0)\
                        and (len(fields[18]) != 0)\
                        and (len(fields[19]) != 0)\
                        and (len(fields[20]) != 0)\
                        and (len(fields[21]) != 0)\
                        and (len(fields[22]) != 0)\
                        and (len(fields[23]) != 0)\
                        and (len(fields[24]) != 0)\
                        and (len(fields[25]) != 0)\
                        and (len(fields[26]) != 0)\
                        and (len(fields[27]) != 0)\
                        and (len(fields[28]) != 0)\
                        and (len(fields[29]) != 0)\
                        and (len(fields[30]) != 0)\
                        and (len(fields[31]) != 0)\
                        and (len(fields[32]) != 0)\
                        and (len(fields[33]) != 0)\
                        and (len(fields[34]) != 0)\
                        and (len(fields[35]) != 0)\
                        and (len(fields[36]) != 0)\
                        and (len(fields[37]) != 0)\
                        and (len(fields[38]) != 0)\
                        and (len(fields[39]) != 0)\
                        and (len(fields[40]) != 0)\
                        and (len(fields[41]) != 0)\
                        and (len(fields[42]) != 0)\
                        and (len(fields[43]) != 0)\
                        and (len(fields[44]) != 0)\
                        and (len(fields[45]) != 0)\
                        and (len(fields[46]) != 0)\
                        and (len(fields[47]) != 0)\
                        and (len(fields[48]) != 0)\
                        and (len(fields[49]) != 0)\
                        and (len(fields[50]) != 0)\
                        and (len(fields[51]) != 0)\
                        and (len(fields[52]) != 0)\
                        and (len(fields[53]) != 0)\
                        and (len(fields[54]) != 0)\
                        and (len(fields[55]) != 0)\
                        and (len(fields[56]) != 0)\
                        and (len(fields[57]) != 0)\
                        and (len(fields[58]) != 0)\
                        and (len(fields[59]) != 0)\
                        and (len(fields[60]) != 0)\
                        and (len(fields[61]) != 0)\
                        and (len(fields[62]) != 0)\
                        and (len(fields[63]) != 0)\
                        and (len(fields[64]) != 0)\
                        and (len(fields[65]) != 0)\
                        and (len(fields[66]) != 0)\
                        and (len(fields[67]) != 0)\
                        and (len(fields[68]) != 0)\
                        and (len(fields[69]) != 0)\
                        and (len(fields[70]) != 0)\
                        and (len(fields[71]) != 0)\
                        and (len(fields[72]) != 0):
                    data = CsvUploadFile(
                        start_date=fields[0],
                        Bagerhat=fields[1],
                        Bandarban=fields[2],
                        Barguna=fields[3],
                        Barisal=fields[4],
                        Bhola=fields[5],
                        Bogra=fields[6],
                        Brahmanbaria=fields[7],
                        Chandpur=fields[8],
                        Chittagong=fields[9],
                        Chuadanga=fields[10],
                        Comilla=fields[11],
                        CoxsBazar=fields[12],
                        Dhaka=fields[13],
                        Dinajpur=fields[14],
                        Faridpur=fields[15],
                        Feni=fields[16],
                        Gaibandha=fields[17],
                        Gazipur=fields[18],
                        Gopalganj=fields[19],
                        Habiganj=fields[20],
                        Jaipurhat=fields[21],
                        Jamalpur=fields[22],
                        Jessore=fields[23],
                        Jhalakati=fields[24],
                        Jhenaidah=fields[25],
                        Khagrachari=fields[26],
                        Khulna=fields[27],
                        Kishoreganj=fields[28],
                        Kurigram=fields[29],
                        Kushtia=fields[30],
                        Lakshmipur=fields[31],
                        Lalmonirhat=fields[32],
                        Madaripur=fields[33],
                        Magura=fields[34],
                        Manikganj=fields[35],
                        Meherpur=fields[36],
                        Moulvibazar=fields[37],
                        Munshiganj=fields[38],
                        Mymensingh=fields[39],
                        Naogaon=fields[40],
                        Narail=fields[41],
                        Narayanganj=fields[42],
                        Narsingdi=fields[43],
                        Natore=fields[44],
                        Nawabganj=fields[45],
                        Netrakona=fields[46],
                        Nilphamari=fields[47],
                        Noakhali=fields[48],
                        Pabna=fields[49],
                        Panchagarh=fields[50],
                        ParbattyaChattagram=fields[51],
                        Patuakhali=fields[52],
                        Pirojpur=fields[53],
                        Rajbari=fields[54],
                        Rajshahi=fields[55],
                        Rangpur=fields[56],
                        Satkhira=fields[57],
                        Shariatpur=fields[58],
                        Sherpur=fields[59],
                        Sirajganj=fields[60],
                        Sunamganj=fields[61],
                        Sylhet=fields[62],
                        Tangail=fields[63],
                        Thakurgaon=fields[64],
                        SylhetDivision=fields[65],
                        RangpurDivision=fields[66],
                        RajshahiDivision=fields[67],
                        MymensinghDivision=fields[68],
                        KhulnaDivision=fields[69],
                        DhakaDivision=fields[70],
                        ChittagongDivision=fields[71],
                        BarisalDivision=fields[72],
                    )
                    data.save()
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect('/upload/csvfile/')

    except Exception as e:
        # messages.error(request, "Unable to upload file. " + e)
        return redirect('/upload/csvfile/')
