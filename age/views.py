from django.shortcuts import render
from age.forms import AgeForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.


class HomePage(TemplateView):
    template_name = 'home.html'


class AboutPage(TemplateView):   # using Template based views
    template_name = 'about.html'


@login_required
def age(request):
    form = AgeForm()
    if request.method == 'POST':
        startDate = request.POST['Born_DOB']
        endDate = request.POST['Today_Date']

        print('UI Date ', startDate)

        # Birth date of the person.
        (stYear, stMonth, stDay) = map(int, startDate.split('-'))
        startDate = datetime.date(stYear, stMonth, stDay)

        # Date for which needs to calculate.
        (endYear, endMonth, endDay) = map(int, endDate.split('-'))
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

        totalYears += remainingMonths // 12
        remainingMonths = remainingMonths % 12

        ageInYears = totalYears

        messages.success(
            request, f'Hey you have completed {ageInYears} Years , {remainingMonths} Months and {remainingDays} Days!!!')

        ageDict = {'ageInYears': ageInYears, 'ageRunning': ageInYears + 1,
                   'remainingMonths': remainingMonths, 'remainingDays': remainingDays}

        return render(request, 'ageForm.html', {'form': form, 'ageDict': ageDict})

    return render(request, 'ageForm.html', context={'form': form})
