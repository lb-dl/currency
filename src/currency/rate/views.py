import csv
from io import BytesIO

from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View

from rate.models import ContactUs, Feedback, Rate
from rate.utils import display

import xlsxwriter


class RateListView(ListView):
    queryset = Rate.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_count'] = context['object_list'].count()
        return context


class CreateContactUsView(CreateView):
    success_url = reverse_lazy('index')
    model = ContactUs
    fields = ('email', 'subject', 'text')

    def form_valid(self, form):
        contact_data = form.cleaned_data
        email = contact_data['email']
        subject = contact_data['subject']
        text = contact_data['text']
        send_mail(
            subject,
            text,
            'lbdltest77@gmail.com',
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class CreateFeedbackView(CreateView):
    success_url = reverse_lazy('index')
    model = Feedback
    fields = ('raiting', 'text')


class CSVView(View):
    headers = ['id', 'source', 'currency', 'sale', 'buy', 'created']

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        writer.writerow(self.__class__.headers)
        for rate in Rate.objects.all().iterator():
            writer.writerow([display(rate, header) for header in self.__class__.headers])
        return response


class XLSXView(View):
    def get(self, request):
        output = BytesIO()
        # Feed a buffer to workbook
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("rates")
        bold = workbook.add_format({'bold': True})
        headers = ['id', 'source', 'currency', 'buy', 'sale', 'created']
        row = 0
        for i, elem in enumerate(headers):
            worksheet.write(row, i, elem, bold)
        row += 1
        # Fill rows with columns
        for rate in Rate.objects.all().iterator():
            worksheet.write(row, 0, rate.id)
            worksheet.write(row, 1, rate.get_source_display())
            worksheet.write(row, 2, rate.get_currency_display())
            worksheet.write(row, 3, rate.buy)
            worksheet.write(row, 4, rate.sale)
            worksheet.write(row, 5, str(rate.created))
            row += 1
        # Close workbook for building file
        workbook.close()
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return response
