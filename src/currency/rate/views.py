from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from rate.models import ContactUs, Feedback, Rate


class RateListView(ListView):
   queryset = Rate.objects.all()


class CreateContactUsView(CreateView):
   success_url = reverse_lazy('index')
   model = ContactUs
   fields = ('email', 'subject', 'text')

   def form_valid(self, form):
   # I don't understand what to do
      return super().form_valid(form)


class CreateFeedbackView(CreateView):
   success_url = reverse_lazy('index')
   model = Feedback
   fields = ('raiting', 'text')
