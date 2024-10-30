

from django.shortcuts import render
from django.http import JsonResponse
from .models import SerialKey, Subscription
from .forms import SubscriptionForm
import uuid
from django.utils.dateformat import DateFormat
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_serial_key(request):
    if request.method == "POST":
        serial_key = str(uuid.uuid4())
        SerialKey.objects.create(serial_key=serial_key)
        return JsonResponse({"serial_key": serial_key})



def create_subscription(request):
    if request.method == "POST":
        print(f"Received form data: {request.POST}")
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            serial_key_value = request.POST.get('serial_key').strip()  # Retrieve and strip any extra spaces

            try:
                # Fetch or create the SerialKey instance
                print(f"Attempting to fetch SerialKey for: {serial_key_value}")
                serial_key_obj, created = SerialKey.objects.get_or_create(serial_key=serial_key_value)
                print(f"Fetched SerialKey: {serial_key_obj}")

                # Check for an existing Subscription with this SerialKey
                subscription, created = Subscription.objects.get_or_create(
                    serial_key=serial_key_obj,
                    defaults={
                        'start_date': form.cleaned_data['start_date'],
                        'end_date': form.cleaned_data['end_date']
                    }
                )

                if not created:
                    # Update existing subscription dates if already present
                    subscription.start_date = form.cleaned_data['start_date']
                    subscription.end_date = form.cleaned_data['end_date']
                    subscription.save()
                    status = "updated"
                else:
                    status = "created"

                return JsonResponse({
                    "status": f"Subscription {status}",
                    "serial_key": serial_key_obj.serial_key,
                    "start_date": DateFormat(subscription.start_date).format('Y-m-d H:i'),
                    "end_date": DateFormat(subscription.end_date).format('Y-m-d H:i')
                })

            except SerialKey.DoesNotExist:
                return JsonResponse({"status": "Error", "errors": {"serial_key": ["This serial key does not exist."]}})

        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({"status": "Error", "errors": form.errors})
    else:
        form = SubscriptionForm()

    return render(request, 'create_subscription.html', {'form': form})

@api_view(['POST'])
def verify_serial_key(request):
    serial_number = request.data.get('serial_number')
    if SerialKey.objects.filter(serial_key=serial_number).exists():
        return Response({'valid': True}, status=status.HTTP_200_OK)
    return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def check_subscription(request):
    serial_number = request.data.get('serial_number')
    serial_key = get_object_or_404(SerialKey, serial_key=serial_number)
    
    # Get the latest subscription for the serial key
    subscription = Subscription.objects.filter(serial_key=serial_key).order_by('-end_date').first()
    
    if subscription:
        now = timezone.now()
        if subscription.start_date <= now <= subscription.end_date:
            return Response({
                'valid': True,
                'start_time': subscription.start_date,
                'end_time': subscription.end_date,
                'time_left': (subscription.end_date - now).total_seconds()
            }, status=status.HTTP_200_OK)
        return Response({'valid': False, 'message': 'Subscription expired'}, status=status.HTTP_200_OK)
    
    return Response({'valid': False, 'message': 'No subscription found'}, status=status.HTTP_404_NOT_FOUND)




def main(request):
    return render(request,'main.html')
