from django.views import View
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect
from collections import defaultdict
unique_ticket = 0
next_ticket = None


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        service_urls = ['change_oil', 'inflate_tires', 'diagnostic']
        # splitting the url_names and processing them as titles
        service_titles = [" ".join(name.split('_')).capitalize() for name in service_urls]

        services = zip(service_urls, service_titles)
        context = {'services': services}

        return render(request, 'tickets/menu.html', context=context)


class GetTicketView(View):
    # saving the ticket numbers and maintaining the serial

    line_of_cars = defaultdict(list)

    def get(self, request, *args, **kwargs):
        global unique_ticket
        valid_services = ['change_oil', 'inflate_tires', 'diagnostic']
        if kwargs['service'] in valid_services:
            service = kwargs['service'] if kwargs['service'] in valid_services else 0
            unique_ticket += 1
            self.line_of_cars[service].append(unique_ticket)

            # These information should be shown to the clients
            ticket_number = self.line_of_cars[service][-1]
            waiting_time = self.measure_waiting_time(self.line_of_cars, service)

            html_response = f"""
    <div>Your number is {ticket_number}</div>
    <div>Please wait around {waiting_time} minutes</div>
            """
            print(self.line_of_cars['change_oil'], unique_ticket)
            return HttpResponse(html_response)
        else:
            raise Http404

    @staticmethod
    def measure_waiting_time(car_line, service):
        waiting_time = 0
        if service == 'change_oil':
            service_time = 2
            waiting_time = (len(car_line[service]) - 1) * service_time

        elif service == 'inflate_tires':
            service_time = 5
            change_oil_time = len(car_line['change_oil']) * 2
            waiting_time = (len(car_line[service]) - 1) * service_time + change_oil_time

        elif service == 'diagnostic':
            service_time = 30
            change_oil_time = len(car_line['change_oil']) * 2
            inflate_tires_time = len(car_line['inflate_tires']) * 5
            waiting_time = (len(car_line[service]) - 1) * service_time + change_oil_time + inflate_tires_time

        # if statement for preventing negation of values
        return waiting_time if waiting_time > 0 else 0


class ProcessingView(View):

    def get(self, request, *args, **kwargs):
        line_of_cars = GetTicketView.line_of_cars

        change_oil_line = len(line_of_cars['change_oil'])
        inflate_tires_line = len(line_of_cars['inflate_tires'])
        diagnostic_line = len(line_of_cars['diagnostic'])

        context = {'change_oil': change_oil_line,
                   'inflate_tires': inflate_tires_line,
                   'diagnostic': diagnostic_line,
                   }

        return render(request, 'tickets/processing.html', context=context)

    def post(self, request, *args, **kwargs):
        global next_ticket

        # variables related to the waiting cars on the basis of service
        line_of_cars = GetTicketView.line_of_cars
        change_oil_line = line_of_cars['change_oil']
        inflate_tires_line = line_of_cars['inflate_tires']
        diagnostic_line = line_of_cars['diagnostic']

        if len(change_oil_line) >= 1:
            next_ticket = change_oil_line.pop(0)
        elif len(inflate_tires_line) >= 1:
            next_ticket = inflate_tires_line.pop(0)
        elif len(diagnostic_line) >= 1:
            next_ticket = diagnostic_line.pop(0)

        print('--', next_ticket)
        return redirect('processing')


class NextView(View):

    def get(self, request, *args, **kwargs):
        line_of_cars = GetTicketView.line_of_cars
        change_oil_line = line_of_cars['change_oil']
        inflate_tires_line = line_of_cars['inflate_tires']
        diagnostic_line = line_of_cars['diagnostic']
        print(next_ticket)
        return render(request, 'tickets/next.html', context={'next_ticket': next_ticket})