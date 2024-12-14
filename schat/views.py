from datetime import datetime

from axes.helpers import get_client_ip_address
from axes.models import AccessAttempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from schat.forms import MessageForm
from schat.models import Message


# Create your views here.
#@login_required
def chat(request):
    is_locked = False
    client_ip = get_client_ip_address(request)
    form = MessageForm()
    if client_ip:
        attempt = AccessAttempt.objects.filter(ip_address=client_ip).last()
        if attempt and attempt.failures_since_start >= 5:  # Проверяем лимит неудачных попыток
            is_locked = True
    if is_locked:
        return render(request, 'schat/chat.html', {'is_locked': True})

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.login = request.user
            message.message = request.POST.get('message')
            message.save()
        return redirect('/schat/chat')
    mess = Message.objects.select_related('login').order_by('-create_dt')[:5][::-1]
    return render(request, 'schat/chat.html', context={'form': form, 'mess': mess})
