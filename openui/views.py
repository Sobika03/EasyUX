from django.shortcuts import render

from openui.models import Person
from slack_integration.views import send_slack_message

# # Create your views here.
def sample(request):
    aa = send_slack_message("testchennel", "Hello from Django!")
    print("Message sent to Slack channel.", aa)
    return render(request,'sample.html')

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Person  # Import your model

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
            "page": 10,
            "size": 10,
            
            "data": data,
            "last_page": paginator.num_pages  # Send total pages for Tabulator
        }, safe=False)

    return render(request, 'table.html')
