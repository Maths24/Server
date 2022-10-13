from django.shortcuts import render, redirect
from .models import Room
from django.contrib.auth.models import User
from .forms import RoomForm
from lcsupport import LCSupport
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from base import data
from base.dbcontroller import DBController
# Create your views here.

#rooms = [
#    {'id': 1, 'name': 'Lets learn python!'},
#    {'id': 2, 'name': 'Design with me'},
#    {'id': 3, 'name': 'Frontend developer'},
#]

#---------------------HTML---------------------
def landing(request):
    d = data.Data()
    gesamtKundenzahl = gesamtZahlHeute()
    kundenInLaden = kundenzahlInLaden()
    vergleichVorwoche = gesamtKundenzahl - vergleichVorwoche()
    return render(request, 'base/index.html', {'gesamtKundenzahl': gesamtKundenzahl, 'kundenInLaden': kundenInLaden, 'vergleichVorwoche': vergleichVorwoche})

def settings(request):
    return render(request, 'base/settings.html')

def dataanalysis(request):
    d = data.Data()
    return render(request, 'base/datenanalyse.html', {'data':d})

#---------------------API---------------------
def testapi(request):
    data = [['Uhrzeit', 'Kundenzahl Schnitt', 'Kundenzahl'], ['9:00',  1, 1], ['10:00',  2, 3], ['11:00',  19, 16], ['12:00',  67, 89], ['13:00',  50, 45], ['14:00',  50, 0], ['15:00',  36, 0]]
    #data = [['9:00',  1, 1], ['10:00',  2, 3], ['11:00',  17, 16], ['12:00',  7, 89], ['13:00',  0, 45]]

    return JsonResponse(data, safe=False)

#---------------------Datenbankdaten aufbereiten---------------------
def gesamtZahlHeute():
    dbc = DBController()
    #richtige Daten eintragen!!!!

    data = dbc.query("select * from *table_name* where DATE(*datetime_column*) = curdate();")

    gesamtZahlKunden = 0
    letzterWert = 0

    for d in data:
        if (d[0] > letzterWert):
            gesamtZahlKunden += 1
        letzterWert = d[0]

    return gesamtZahlKunden

def kundenzahlInLaden():
    dbc = DBController()
    #richtige Daten eintragen!!!!
    data = dbc.query("select * from *table_name* ORDER BY *id* DESC LIMIT 1;")

    return data[0][0]

def vergleichVorwoche():
    dbc = DBController()
    #richtige Daten eintragen!!!!
    kundenzahlVorwocheData = dbc.query("select * from *table_name* where *datetime_column* between curdate() - interval 7 day + '00:00:00' and curdatetime() - interval 7 day")
    gesamtZahlKundenVorwoche = 0
    letzterWert = 0

    for d in kundenzahlVorwocheData:
        if (d[0] > letzterWert):
            gesamtZahlKundenVorwoche += 1
        letzterWert = d[0]

    return gesamtZahlKundenVorwoche
#---------------------Livecamera---------------------
@gzip.gzip_page
def livecamera(request):
    try:
        cam = LCSupport.cam()
        print("camera started")
        return StreamingHttpResponse(generateFeed(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e: 
        print("Error: Camera did not load")
        print(e)
        pass
    return render(request, 'base/index.html')


#Live camera feed
def generateFeed(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

"""def home(request):
    rooms = Room.objects.all() 
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context) 

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)"""
