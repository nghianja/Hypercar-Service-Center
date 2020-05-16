from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
}
ticket_number = 0
next_ticket = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html')


class TicketView(View):
    def get(self, request, *args, **kwargs):
        ticket_type = kwargs['ticket_type']
        minutes_to_change_oil = 2 * len(line_of_cars['change_oil'])
        minutes_to_inflate_tires = 5 * len(line_of_cars['inflate_tires'])
        minutes_to_diagnostic = 30 * len(line_of_cars['diagnostic'])
        minutes_to_wait = 0
        if ticket_type == 'change_oil':
            minutes_to_wait = minutes_to_change_oil
        elif ticket_type == 'inflate_tires':
            minutes_to_wait = minutes_to_inflate_tires + minutes_to_change_oil
        elif ticket_type == 'diagnostic':
            minutes_to_wait = minutes_to_diagnostic + minutes_to_inflate_tires + minutes_to_change_oil
        global ticket_number
        ticket_number += 1
        line_of_cars[ticket_type].append(ticket_number)
        return render(request, 'ticket.html',
                      context={
                          "ticket_number": ticket_number,
                          "minutes_to_wait": minutes_to_wait
                      })


class QueueView(View):
    def get(self, request, *args, **kwargs):
        change_oil_qlen = len(line_of_cars['change_oil'])
        inflate_tires_qlen = len(line_of_cars['inflate_tires'])
        diagnostic_qlen = len(line_of_cars['diagnostic'])
        return render(request, 'queue.html',
                      context={
                          "change_oil_qlen": change_oil_qlen,
                          "inflate_tires_qlen": inflate_tires_qlen,
                          "diagnostic_qlen": diagnostic_qlen
                      })

    def post(self, request, *args, **kwargs):
        global next_ticket
        if len(line_of_cars['change_oil']) > 0:
            next_ticket = line_of_cars['change_oil'].pop(0)
        elif len(line_of_cars['inflate_tires']) > 0:
            next_ticket = line_of_cars['inflate_tires'].pop(0)
        elif len(line_of_cars['diagnostic']) > 0:
            next_ticket = line_of_cars['diagnostic'].pop(0)
        else:
            next_ticket = 0
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        # ticket_number = int(kwargs['ticket_number'])
        return render(request, 'next.html',
                      context={
                          "ticket_number": next_ticket
                      })
