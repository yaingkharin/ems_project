# Generated migration to add ticket field back to booking

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_merge_20260314_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='app.ticket'),
        ),
    ]
