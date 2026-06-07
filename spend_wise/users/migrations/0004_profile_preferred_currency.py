from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_fixed_target_percent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='preferred_currency',
            field=models.CharField(
                choices=[
                    ('EUR', 'Euro (\u20ac)'),
                    ('USD', 'US Dollar ($)'),
                    ('GBP', 'British Pound (\xa3)'),
                ],
                default='EUR',
                max_length=3,
            ),
        ),
    ]
