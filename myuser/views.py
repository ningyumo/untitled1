from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import RegisterForm


class MyRegisterForm(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'my_user/register.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password_1']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        return super().form_valid(form)


my_register = MyRegisterForm.as_view()