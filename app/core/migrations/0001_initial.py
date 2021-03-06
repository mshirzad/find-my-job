# Generated by Django 2.1.15 on 2021-11-08 20:13

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_freelancer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=512)),
                ('address_line2', models.CharField(blank=True, max_length=512)),
                ('city', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('post_code', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(choices=[('Diploma', 'Diploma'), ('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Phd', 'Phd')], max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('faculty', models.CharField(max_length=255)),
                ('start_year', models.IntegerField()),
                ('graduation_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=512)),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('thumbnail', models.ImageField(upload_to=core.models.image_path_generator)),
                ('thumbnail_2', models.ImageField(null=True, upload_to=core.models.image_path_generator)),
                ('thumbnail_3', models.ImageField(null=True, upload_to=core.models.image_path_generator)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('profession', models.CharField(choices=[('Eng', 'Engineer'), ('CS', 'Computer Scientist'), ('Gph Desg', 'Graphic Designer'), ('Web Dev', 'Web Developer'), ('Mobile Dev', 'Mobile App Developer'), ('Programmer', 'Programmer'), ('Acc', 'Accountant'), ('Phy', 'Physician'), ('Tech', 'Technician'), ('Plu', 'Plumber'), ('Elect', 'Electrician'), ('Carp', 'Carpenter'), ('Phot', 'Photographer')], max_length=255)),
                ('ratings', models.FloatField(default=0)),
                ('bio', models.CharField(blank=True, max_length=255)),
                ('profile_photo', models.ImageField(null=True, upload_to=core.models.image_path_generator)),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='core.Address')),
                ('education', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='education', to='core.Education')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gig',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='core.Profile'),
        ),
    ]
