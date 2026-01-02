# Generated manually for transcription support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_create_credit_packages'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(
                choices=[
                    ('separation', 'Audio Separation'),
                    ('transcription', 'Transcription'),
                    ('lyrics_pipeline', 'Lyrics Generation')
                ],
                default='separation',
                help_text='Type of processing job',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='transcription_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('basic', 'Basic Text'),
                    ('timestamped', 'Timestamped JSON'),
                    ('subtitles', 'Subtitles (SRT/VTT)'),
                    ('lyrics', 'Lyrics (LRC)')
                ],
                help_text='Type of transcription to perform',
                max_length=20,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='transcription_format',
            field=models.CharField(
                blank=True,
                choices=[
                    ('txt', 'Plain Text'),
                    ('json', 'JSON with Timestamps'),
                    ('srt', 'SubRip Subtitles'),
                    ('vtt', 'WebVTT Subtitles'),
                    ('lrc', 'LRC Lyrics')
                ],
                help_text='Output format for transcription',
                max_length=10,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='language',
            field=models.CharField(
                blank=True,
                help_text='Language code for transcription (e.g., en, es)',
                max_length=10,
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='job',
            name='model',
            field=models.CharField(
                blank=True,
                choices=[
                    ('htdemucs', 'HT Demucs (4 stems)'),
                    ('htdemucs_ft', 'HT Demucs Fine-tuned (4 stems)'),
                    ('htdemucs_6s', 'HT Demucs 6-stem'),
                    ('hdemucs_mmi', 'Hybrid Demucs MMI')
                ],
                help_text='Demucs model for separation jobs',
                max_length=50,
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='job',
            name='output_format',
            field=models.CharField(
                choices=[
                    ('mp3', 'MP3 (Smaller files)'),
                    ('wav', 'WAV (Lossless quality)')
                ],
                default='mp3',
                help_text='Output audio format for separation',
                max_length=10
            ),
        ),
    ]
