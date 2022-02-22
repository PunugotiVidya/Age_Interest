from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import InterestStorageModel
from .forms import StorageCreationForm
from datetime import date
import datetime
from django.views.generic import(
    ListView,
    CreateView,
    DeleteView
)

# Create your views here.

# logic for finding the interest for current date is in below....


class Interest():
    def __init__(self, amount, rate, startDate):
        self.amount = amount
        self.rate = rate
        self.startDate = startDate

    def findInterest(self):
        print("--------------Inside findInterest--------------")
        print(self.amount, self.rate)
        # Birth date of the person.
        (stYear, stMonth, stDay) = (self.startDate.year,
                                    self.startDate.month, self.startDate.day)

        # Date for which needs to calculate.
        (endYear, endMonth, endDay) = (
            date.today().year, date.today().month, date.today().day)
        endDate = datetime.date(endYear, endMonth, endDay)

        ''' Setting of variables '''
        totalYears = 0
        remainingMonths = 0
        remainingDays = 0

        sDate = datetime.date(stYear, stMonth, stDay)
        eDate = datetime.date(endYear, endMonth, endDay)

        if eDate < sDate:
            messages.error(
                request, f'End Date({eDate.strftime("%d/%m/%Y")}) cannot be less than Start Date({sDate.strftime("%d/%m/%Y")})!!!')
            return render(request, 'ageForm.html', context={'form': form})

        '''----------------------------- Age Calculation Logic Below--------------------------------------'''
        for year in range(stYear + 1, endYear):   # Calculating Total Years Excluding starting year and Current Year.
            totalYears += 1

        if stYear == endYear:  # if both starting year and ending year is same ==> month calculation
            if stMonth == endMonth:
                remainingDays = endDay - stDay
            else:
                for mnth in range(stMonth + 1, endMonth):
                    remainingMonths += 1
                if endDay >= stDay:
                    remainingMonths += 1
                    remainingDays = endDay - stDay
                else:
                    calRemainingDays = ((30 - stDay) + endDay)
                    remainingMonths += calRemainingDays // 30
                    remainingDays = calRemainingDays - \
                        (calRemainingDays // 30) * 30

        else:
            # if not same remaining month calculation
            for mnth in range(stMonth + 1, 13):
                remainingMonths += 1
            for mnth in range(1, endMonth):
                remainingMonths += 1

            if endDay >= stDay:
                remainingMonths += 1
                remainingDays = endDay - stDay
            else:
                calRemainingDays = ((30 - stDay) + endDay)
                remainingMonths += calRemainingDays // 30
                remainingDays = calRemainingDays - \
                    (calRemainingDays // 30) * 30

        interest = ((totalYears * 12 + remainingMonths) * self.rate * self.amount) / \
            100  # Total Interest for Total Months

        totalMonths = (totalYears * 12 + remainingMonths)

        # Absolute Interest for all Days
        absoluteInterest = (
            (totalYears * 12 + remainingMonths + (remainingDays / 30)) * self.rate * self.amount) / 100

        fifthMultiplierDay = (remainingDays // 5) * 5
        fifthMultiplierInterest = interest + \
            ((fifthMultiplierDay / 30) * self.rate * self.amount) / 100

        # The below will returns absolute Interest of the given start Date and self.amount.
        return round(absoluteInterest, 2)

@login_required
def storageList(request):
    for object_data in InterestStorageModel.objects.all():
        interest = Interest(object_data.amount,
                            object_data.rate, object_data.startDate)
        finalInterest = interest.findInterest()
        object_data.presentinterest = finalInterest
        object_data.save()
        print("finalInterest = ", finalInterest)
        print("object_data = ", object_data.presentinterest)

    # querySet which give the details for only logged in User
    queryset = InterestStorageModel.objects.filter(
        givenPerson=request.user).order_by('-startDate')
    return render(request, 'intereststorage_list.html', {'posts': queryset})


class StorageCreateView(LoginRequiredMixin, CreateView):
    model = InterestStorageModel
    form_class = StorageCreationForm
    template_name = 'intereststorage_form.html'

    def form_valid(self, form):
        form.instance.givenPerson = self.request.user
        return super().form_valid(form)


class LenderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = InterestStorageModel
    template_name = 'lender_confirm_delete.html'
    success_url = '/listInterests/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.givenPerson:
            return True
        return False


# User Lender List View


@login_required
def lenderStorageListView(request, takenperson):
    queryset = InterestStorageModel.objects.filter(
        takenPerson=takenperson)
    # template_name = 'lender_interests.html'
    return render(request, 'lender_interests.html', {'posts': queryset})

# class LenderStorageListView(ListView):
#     model = InterestStorageModel
#     template_name = 'lender_interests.html'
#     context_object_name = 'posts'

#     def get_queryset(self, **kwargs):
#         # user = get_object_or_404(User, username=self.kwargs.get('takenperson'))
#         print("person name: ", self.kwargs.get('takenperson'))
#         print("Filter Object ", InterestStorageModel.objects.filter(
#             takenPerson='kiran').first().takenPerson)
#         return InterestStorageModel.objects.filter(takenPerson=self.kwargs.get('takenperson'))



# class StorageList(LoginRequiredMixin, ListView):
#     # Will update the interest for all the objects of the InterestModel.
#     for object_data in InterestStorageModel.objects.all():
#         interest = Interest(object_data.amount,
#                             object_data.rate, object_data.startDate)
#         finalInterest = interest.findInterest()
#         print("finalInterest = ", finalInterest)
#         object_data.presentinterest = finalInterest
#         print("object_data = ", object_data.presentinterest)
#         object_data.save()
#     print("----OutSide of for loop----")

#     model = InterestStorageModel
#     template_name = 'intereststorage_list.html'
#     context_object_name = 'posts'

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.givenPerson:
#             return True
#         return False
#     # paginate_by = 5  # pagination
