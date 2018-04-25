from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from feriados.models import Feriado
from feriados.serializers import FeriadoSerializer

@csrf_exempt
## GET /api/feriados/
def list(request):
    feriados = Feriado.objects.all()
    serializer = FeriadoSerializer(feriados, many=True)
    return JsonResponse(serializer.data, safe=False)

## GET /api/feriados/<feriado_id>/
def detail(request, feriado_id):
    f = Feriado.objects.get(id=feriado_id)
    serializer = FeriadoSerializer(f)
    return JsonResponse(serializer.data, safe=False)
