# Generated by Django 5.2 on 2025-05-02 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'areas',
            },
        ),
        migrations.CreateModel(
            name='PermissionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'permissions_types',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'projects',
            },
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'roles_types',
            },
        ),
        migrations.CreateModel(
            name='StatusType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'status_types',
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tools',
            },
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'works_groups',
            },
        ),
        migrations.CreateModel(
            name='AreaProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.area')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.project')),
            ],
            options={
                'db_table': 'areas_projects',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('repository_url', models.CharField(max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.project')),
            ],
            options={
                'db_table': 'repositories',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.statustype'),
        ),
        migrations.CreateModel(
            name='ToolProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.project')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.tool')),
            ],
            options={
                'db_table': 'tools_projects',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.roletype')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.user'),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.permissiontype')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.user')),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.workgroup'),
        ),
        migrations.CreateModel(
            name='WorkGroupUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.workgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.user')),
            ],
            options={
                'db_table': 'works_groups_users',
            },
        ),
    ]
