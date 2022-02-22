from django.shortcuts import render
from django.contrib import messages
from interest.forms import InterestForm
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.


@login_required
def interest(request):
    form = InterestForm()
    if request.method == 'POST':

        amount = int(request.POST['amount'])  # Getting amount from UI
        rate = int(request.POST['rate'])     # Getting rate from UI

        startDate = request.POST['Start_Date']   # Getting Start Date from UI
        endDate = request.POST['Current_Date']   # Getting End Date from UI

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

        interest = ((totalYears * 12 + remainingMonths) * rate * amount) / \
            100  # Total Interest for Total Months

        totalMonths = (totalYears * 12 + remainingMonths)

        # Absolute Interest for all Days
        absoluteInterest = (
            (totalYears * 12 + remainingMonths + (remainingDays / 30)) * rate * amount) / 100

        fifthMultiplierDay = (remainingDays // 5) * 5
        fifthMultiplierInterest = interest + \
            ((fifthMultiplierDay / 30) * rate * amount) / 100

        messages.success(
            request, f'You have to pay {absoluteInterest} Rupees!!')

        interestDict = {'totalYears': totalYears, 'totalMonths': totalMonths, 'remainingMonths': remainingMonths, 'remainingDays': remainingDays,
                        'interest': interest, 'absoluteInterest': absoluteInterest, 'fifthMultiplierInterest': fifthMultiplierInterest, 'fifthMultiplierDay': fifthMultiplierDay}

        return render(request, 'interestForm.html', {'form': form, 'interestDict': interestDict})

    return render(request, 'interestForm.html', {'form': form})
