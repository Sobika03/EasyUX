from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from openui.models import Person
from slack_integration.views import send_slack_message
from .models import Person
from django.http import HttpResponse
from django.conf import settings
from django.core.management import call_command
import os
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from authentication.models import Organization

def get_org_name_from_email(email):
    try:
        domain = email.split('@')[1]  # organization.com
        org_name = domain.split('.')[0]  # organization
        return org_name
    except IndexError:
        return None
 
# Create your views here.
def sample(request):
    aa = send_slack_message("testchennel", "Hello from Django!")
    print("Message sent to Slack channel.", aa)
    return render(request,'sample.html')
 
def tabulator_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get pagination parameters from Tabulator
        page = int(request.GET.get('page', 1))  # Default to page 1
        size = int(request.GET.get('size', 10))  # Default page size is 10
 
        # Ensure page value is within valid range
        total_items = Person.objects.count()
        max_page = (total_items + size - 1) // size  # Calculate maximum page number
        page = max(1, min(page, max_page))  # Clamp page value between 1 and max_page
       
        # Fetch and paginate data
        queryset = Person.objects.all().order_by('id')  # Ensure ordered results
        paginator = Paginator(queryset, size)  # Paginate the queryset
 
        data = list(paginator.get_page(page).object_list.values())  # Convert to list of dicts
 
        return JsonResponse({
            "page": page,  # Send the actual page number
            "size": size,  # Send the actual page size
            "last_page": paginator.num_pages,  # Send the total number of pages
            "data": data  # Paginated data
        })
 
    return render(request, 'table.html')



def backup_data(request):
    return render(request, 'backup.html')




def list_backup_files(request):
    fixtures_dir = os.path.join(settings.BASE_DIR, 'attendance', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)
    files = [f for f in os.listdir(fixtures_dir) if f.endswith('.json')]
    return render(request, 'backup.html', {'files': files})


@csrf_exempt
def dump_data_to_json(request):
    if request.method == "POST":
        fixtures_dir = os.path.join(settings.BASE_DIR, 'attendance', 'fixtures')
        os.makedirs(fixtures_dir, exist_ok=True)

        filename = f"data_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = os.path.join(fixtures_dir, filename)

        with open(file_path, 'w') as f:
            call_command('dumpdata', indent=4, stdout=f)

        return JsonResponse({"message": "Backup created successfully", "filename": filename})
    return JsonResponse({"error": "Invalid request"}, status=400)

def download_dumped_data(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'attendance', 'fixtures', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("File not found.", status=404)



def delete_backup_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'attendance', 'fixtures', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('backup-page')       

    
def dashboard_view(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    org_id = user.organization_id

    if org_id:
        try:
            # Fetch the organization using the org_name
            organization = Organization.objects.get(pk=org_id)
        except Organization.DoesNotExist:
            # Handle the case where the organization does not exist
            return render(request, 'dashboard.html', {'message': 'Superuser'})
        context = {
            'organization': organization
        }
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'dashboard.html', {'message': 'Superuser'})
