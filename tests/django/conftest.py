import django
from django.conf import settings
from django.db import connection, migrations, models
from django.db.migrations.loader import MigrationLoader
import logging
import os

if os.environ.get('ADAPTER') == 'sqlite':
    database = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
elif os.environ.get('ADAPTER') == 'mysql' or os.environ.get('ADAPTER') == 'mariadb':
    database = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tailslide_test'
    }
elif os.environ.get('ADAPTER') == 'sqlserver':
    database = {
        'ENGINE': 'mssql',
        'NAME': 'tailslide_test',
        'USER': 'SA',
        'PASSWORD': 'YourStrong!Passw0rd'
    }
else:
    database = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tailslide_test'
    }

settings.configure(
    DATABASES={
        'default': database
    },
    DEBUG=True
)
django.setup()

logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class User(models.Model):
    visits_count = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    rating = models.FloatField()
    name = models.CharField(max_length=255)
    # created_at = models.DateTimeField()

    class Meta:
        app_label = 'myapp'


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visits_count', models.IntegerField(null=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=5, null=True)),
                ('rating', models.FloatField(null=True)),
                ('name', models.CharField(max_length=255, null=True))
            ]
        )
    ]


# probably a better way to do this
migration = Migration('initial', 'myapp')
loader = MigrationLoader(connection, replace_migrations=False)
loader.graph.add_node(('myapp', migration.name), migration)
sql_statements = loader.collect_sql([(migration, False)])

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS myapp_user")
    cursor.execute('\n'.join(sql_statements))
