# Generated by Django 4.2.11 on 2024-06-13 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mathesar', '0006_mathesar_databases_to_model'),
    ]

    operations = [
        migrations.RenameModel(old_name='Database', new_name='Connection'),
        migrations.AlterField(
            model_name='databaserole',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesar.connection'),
        ),
        migrations.AlterField(
            model_name='schemarole',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesar.schema'),
        ),
        migrations.AlterField(
            model_name='tablesettings',
            name='column_order',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.RenameModel(old_name='UIQuery', new_name='Exploration'),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('host', models.CharField(max_length=255)),
                ('port', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='server',
            constraint=models.UniqueConstraint(fields=('host', 'port'), name='unique_server'),
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='databases', to='mathesar.server')),
            ],
        ),
        migrations.AddConstraint(
            model_name='database',
            constraint=models.UniqueConstraint(fields=('name', 'server'), name='unique_database'),
        ),
        migrations.AddConstraint(
            model_name='database',
            constraint=models.UniqueConstraint(fields=('id', 'server'), name='database_id_server_index'),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('password', encrypted_fields.fields.EncryptedCharField(max_length=255)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='mathesar.server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='role',
            constraint=models.UniqueConstraint(fields=('name', 'server'), name='unique_role'),
        ),
        migrations.AddConstraint(
            model_name='role',
            constraint=models.UniqueConstraint(fields=('id', 'server'), name='role_id_server_index'),
        ),
        migrations.CreateModel(
            name='UserDatabaseRoleMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesar.database')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesar.role')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesar.server')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userdatabaserolemap',
            constraint=models.UniqueConstraint(fields=('user', 'database'), name='user_one_role_per_database'),
        ),
        migrations.RunSQL(
            sql="""
            ALTER TABLE mathesar_userdatabaserolemap
            ADD CONSTRAINT userdatabaserolemap_database_server_integrity
              FOREIGN KEY (database_id, server_id)
              REFERENCES mathesar_database(id, server_id);
            """,
            reverse_sql="""
            ALTER TABLE mathesar_userdatabaserolemap
            DROP CONSTRAINT userdatabaserolemap_database_server_integrity;
            """
        ),
        migrations.RunSQL(
            sql="""
            ALTER TABLE mathesar_userdatabaserolemap
            ADD CONSTRAINT userdatabaserolemap_role_server_integrity
              FOREIGN KEY (role_id, server_id)
              REFERENCES mathesar_role(id, server_id);
            """,
            reverse_sql="""
            ALTER TABLE mathesar_userdatabaserolemap
            DROP CONSTRAINT userdatabaserolemap_role_server_integrity;
            """
        ),
    ]
