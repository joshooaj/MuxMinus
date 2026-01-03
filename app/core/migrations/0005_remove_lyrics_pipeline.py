# Generated manually to remove lyrics_pipeline job type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_transcription_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(
                choices=[
                    ('separation', 'Audio Separation'),
                    ('transcription', 'Transcription'),
                ],
                default='separation',
                help_text='Type of processing job',
                max_length=20
            ),
        ),
    ]
