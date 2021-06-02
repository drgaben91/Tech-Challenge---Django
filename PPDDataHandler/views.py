from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from csv import DictReader

from .bulk_create_manager import BulkCreateManager
from .serializers import PPDRecordSelializer
from .models import PPDRecord

CHUNK_SIZE = 10000


class PPDRecordViewSet(ModelViewSet):
    serializer_class = PPDRecordSelializer
    queryset = PPDRecord.objects.all()
    lookup_field = 'transaction_unique_id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'date_of_transfer': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAdminUser])
    def import_csv(self, request, *args):
        import_models_from_csv("PPDDataHandler/input_files/" + request.GET['filename'])
        return self.list(self, request)

    @action(methods=['delete'], detail=False, permission_classes=[permissions.IsAdminUser])
    def delete_all(self, request):
        PPDRecord.objects.all().delete()
        return self.list(self, request)


def import_models_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = DictReader(csvfile, fieldnames=PPDRecordSelializer.Meta.FIELDS)
        bulk_mgr = BulkCreateManager(chunk_size=CHUNK_SIZE)
        counter = 0;
        for row in reader:
            try:
                existing_record_id = PPDRecord.objects.get(
                    transaction_unique_id=row['transaction_unique_id']).id
                try:
                    record = PPDRecord.parse_from_csv_row(row)
                    record.id = existing_record_id
                    counter += 1
                    bulk_mgr.add(record)
                except Exception as e:
                    print("Exception: {0}".format(e) + str(row))
            except PPDRecord.DoesNotExist:
                try:
                    record = PPDRecord.parse_from_csv_row(row)
                    counter += 1
                    bulk_mgr.add(record)
                except Exception as e:
                    print("Exception: {0}".format(e) + str(row))
            if counter % CHUNK_SIZE == 0: print("Added the " + str(counter) + "th record")
        bulk_mgr.done()
