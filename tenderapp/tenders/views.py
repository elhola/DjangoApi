import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from .models import Tender

from .forms import LoginForm


class LoginView(View):
    template_name = 'home.html'

    def get(self, request, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tender_list')

        return render(request, self.template_name, {'form': form})


def get_tender_ids():
    api_url = 'https://public.api.openprocurement.org/api/0/tenders?descending=1&limit=10'
    response = requests.get(api_url)
    if response.status_code == 200:
        return [tender['id'] for tender in response.json().get('data', [])]
    return []


def get_tender_data(tender_id):
    api_url = f'https://public.api.openprocurement.org/api/0/tenders/{tender_id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('data', {})
    return {}


class TenderListView(View):
    template_name = 'tender_list.html'

    def get(self, request, *args, **kwargs):
        tender_ids = get_tender_ids()
        tenders = []

        total_amount = 0

        for tender_id in tender_ids:
            tender_data = get_tender_data(tender_id)
            if 'value' in tender_data and 'amount' in tender_data['value']:
                tender = {
                    'tender_id': tender_id,
                    'amount': tender_data['value']['amount'],
                    'description': tender_data.get('description', ''),
                }
                total_amount += tender_data['value']['amount']
                if 'dateModified' in tender_data:
                    tender['date_modified'] = tender_data['dateModified']
                else:
                    tender['date_modified'] = ''
                tenders.append(tender)
                Tender.objects.create(
                    tender_id=tender_id,
                    amount=tender_data['value']['amount'],
                    description=tender_data.get('description', ''),
                    date_modified=tender_data.get('dateModified'),
                )

        context = {'tenders': tenders, 'total_amount': total_amount}
        return render(request, self.template_name, context)
