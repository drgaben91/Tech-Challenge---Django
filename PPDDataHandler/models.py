from time import strptime

from django.db import models


# Create your models here.

class PPDRecord(models.Model):
    DETACHED = 'D'
    SEMI_DETACHED = 'S'
    TERRACED = 'T'
    FLATS = 'F'
    OTHER = 'O'
    PROPERTY_TYPE_CHOICES = (
        (DETACHED, 'Detached'),
        (SEMI_DETACHED, 'Semi-detached'),
        (TERRACED, 'Terraced'),
        (FLATS, 'Flats/Maisonettes'),
        (OTHER, 'Other'),
    )
    NEWLY_BUILT = 'Y'
    ESTABLISHED = 'N'
    OLD_NEW_CHOICES = (
        (NEWLY_BUILT, 'a newly built property'),
        (ESTABLISHED, 'an established residential building'),
    )
    FREEHOLD = 'F'
    LEASEHOLD = 'L'
    DURATION_CHOICES = (
        (FREEHOLD, 'Freehold'),
        (LEASEHOLD, 'Leasehold'),
    )
    STANDARD_PRICE_ENTRY = 'A'
    ADDITIONAL_PRICE_ENTRY = 'B'
    PPD_CATEGORY_TYPE_CHOICES = (
        (STANDARD_PRICE_ENTRY, 'Standard Price Paid entry, includes single residential property sold for value.'),
        (ADDITIONAL_PRICE_ENTRY,
         ' Additional Price Paid entry including transfers under a power of sale/repossessions, buy-to-lets (where they can be identified by a Mortgage) and transfers to non-private individuals.'),
    )
    ADDITION = 'A'
    CHANGE = 'C'
    DELETE = 'D'
    RECORD_STATUS_CHOICES = (
        (ADDITION, 'Addition'),
        (CHANGE, 'Change'),
        (DELETE, 'Delete'),
    )
    transaction_unique_id = models.Field(max_length=50)
    price = models.FloatField('Price')
    date_of_transfer = models.DateTimeField('Date of Transfer')
    postcode = models.CharField(max_length=50, verbose_name='Postcode')
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES, default=OTHER)
    old_new = models.CharField(max_length=1, choices=OLD_NEW_CHOICES)
    duration = models.CharField(max_length=1, choices=DURATION_CHOICES)
    paon = models.CharField(max_length=100, verbose_name='Primary Addressable Object Name')
    saon = models.CharField(max_length=100, verbose_name='Secondary Addressable Object Name')
    street = models.CharField(max_length=100, verbose_name='Street')
    locality = models.CharField(max_length=100, verbose_name='Locality')
    town_city = models.CharField(max_length=100, verbose_name='Town/City')
    district = models.CharField(max_length=100, verbose_name='District')
    county = models.CharField(max_length=100, verbose_name='County')
    ppd_category_type = models.CharField(max_length=1, choices=PPD_CATEGORY_TYPE_CHOICES)
    record_status = models.CharField(null=True, max_length=1, choices=RECORD_STATUS_CHOICES, blank=True)

    def parse_from_csv_row(row_data):
        """
        Method to create record objects from CSV lines. Built the way so it can accept CSV-s from https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
        :return: PPDRecord
        """
        """
        16 when its a monthly data row, last data indicates, wether the record is added/deleted/modified         
        """
        if len(row_data) == 16:
            return PPDRecord(
                transaction_unique_id=row_data['transaction_unique_id'],
                price=float(row_data['price']),
                date_of_transfer=row_data['date_of_transfer'],
                postcode=row_data['postcode'],
                property_type=row_data['property_type'],
                old_new=row_data['old_new'],
                duration=row_data['duration'],
                paon=row_data['paon'],
                saon=row_data['saon'],
                street=row_data['street'],
                locality=row_data['locality'],
                town_city=row_data['town_city'],
                district=row_data['district'],
                county=row_data['county'],
                ppd_category_type=row_data['ppd_category_type'],
                record_status=row_data['record_status']
            )
        if len(row_data) < 16 or row_data is None:
            raise Exception('Insufficient data to create Record object')


def __str__(self):
    return "ID: " + str(self.id) + ", Tr. unique ID: " + self.transaction_unique_id + ", Price: " + str(
        self.price) + ", Tr. date: " + str(self.date_of_transfer)


PPDRecord.parse_from_csv_row = staticmethod(PPDRecord.parse_from_csv_row)
