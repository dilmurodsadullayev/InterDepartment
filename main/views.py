from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Programme, Faculty, ApplicationUser, CustomUser, ApplicationIssue, Application
from .forms import ApplicationCreate, RegistrationForm, ApplicationForm


# Create your views here.

def index_view(request):

    ctx = {

    }

    return render(request, 'main/index.html', ctx)



def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Ma'lumotlaringizni to'g'ri kiriting.")  # Umumiy xato xabari
    else:
        form = RegistrationForm()

    ctx = {
        "form": form
    }

    return render(request, 'registration/signup.html', ctx)

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Foydalanuvchini tizimga kiritamiz
                return redirect('home')  # Bosh sahifaga yo'naltirish
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
    else:
        form = AuthenticationForm()
    return render(request,'registration/signin.html', {'form': form})


def logout_view(request):
    logout(request)  # Foydalanuvchini tizimdan chiqarish
    return redirect('home')



class ApplicationView(View):
    def get(self, request):
        print("FILES:", request.FILES)
        print("POST:", request.POST)
        programmes = Programme.objects.all()

        ctx = {
            "programmes": programmes
        }

        return render(request, 'main/application.html', ctx)

    def post(self, request):
        # print("FILES:", request.FILES)
        # print("POST:", request.POST)
        programmes = Programme.objects.all()
        form = ApplicationCreate(request.POST, request.FILES)

        if form.is_valid():
            # Extract selected programme and faculty
            programme_id = form.cleaned_data['programme']
            faculty_id = form.cleaned_data['faculty']
            try:
                programme = Programme.objects.get(id=int(programme_id.id))
                faculty = Faculty.objects.get(id=int(faculty_id.id))
            except Programme.DoesNotExist:
                # print("Programme does not exist")
                return render(request, 'main/application.html', {'form': form, 'error': 'Programme not found'})
            except Faculty.DoesNotExist:
                # print("Faculty does not exist")
                return render(request, 'main/application.html', {'form': form, 'error': 'Faculty not found'})

            # Create the application object
            application = form.save(commit=False)
            application.programme = programme
            application.faculty = faculty

            application.save()
            ApplicationUser.objects.create(
                user = request.user,
                application = application,

            )

            return redirect('application')

        else:
            # Form is not valid, print form errors for debugging
            pass
            # print("Form errors:", form.errors)

        # In case the form is not valid
        ctx = {
            "programmes": programmes,
            'form': form
        }

        return render(request, 'main/application.html', ctx)

def get_faculties(request):
    programme_id = request.GET.get('programme_id')
    faculties = Faculty.objects.filter(programme_id=programme_id).values('id', 'faculty_name')
    return JsonResponse(list(faculties), safe=False)


def my_application_view(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)
        application_issues = []
        application_datas = ApplicationUser.objects.filter(user=user)

        for application_user in application_datas:
            issues = ApplicationIssue.objects.filter(application_user=application_user).first()
            application_issues.append(
                {
                    "application": application_user,
                    "issues": issues
                }
            )

        print(application_issues)

        ctx = {
            'application_issues':application_issues

        }

        return render(request, 'main/my_application.html', ctx)
    else:
        return HttpResponse("Siz saytga login qilmagansiz")



class ApplicationChangeView(View):
    template_name = 'admin/application_change.html'

    def get(self, request, id):
        # Application modelini olish
        application = get_object_or_404(Application, id=id)
        form = ApplicationForm(instance=application)
        return render(request, self.template_name, {'form': form, 'application': application})

    def post(self, request, id):
        application = get_object_or_404(Application, id=id)
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('admin:main_application_changelist')  # Success page, or redirect to application list
        return render(request, self.template_name, {'form': form, 'application': application})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)