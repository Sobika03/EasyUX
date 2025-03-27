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

def tabulator_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Fetch data from the database
        data = list(Person.objects.values())  # Convert queryset to list of dictionaries
        return JsonResponse(data, safe=False)
    return render(request, 'table.html')