from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("agencies", "0002_agency_onboarding_kyc")]
    operations = [migrations.AddField(model_name="agencymodel", name="seat_limit", field=models.PositiveIntegerField(default=3))]
