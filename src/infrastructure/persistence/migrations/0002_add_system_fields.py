# Migration to add missing fields to existing tables
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("persistence", "0001_initial"),
    ]

    operations = [
        # SystemDeptInfo - Add creator and modifier
        migrations.AddField(
            model_name="systemdeptinfo",
            name="creator",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="created_depts",
                db_column="creator_id",
            ),
        ),
        migrations.AddField(
            model_name="systemdeptinfo",
            name="modifier",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="modified_depts",
                db_column="modifier_id",
            ),
        ),

        # SystemMenu - Add creator, modifier, meta
        migrations.AddField(
            model_name="systemmenu",
            name="meta",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.systemmenumeta",
                related_name="menus",
                db_column="meta_id",
            ),
        ),
        migrations.AddField(
            model_name="systemmenu",
            name="creator",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="created_menus",
                db_column="creator_id",
            ),
        ),
        migrations.AddField(
            model_name="systemmenu",
            name="modifier",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="modified_menus",
                db_column="modifier_id",
            ),
        ),

        # SystemOperationLog - Add creator
        migrations.AddField(
            model_name="systemoperationlog",
            name="creator",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="operation_logs",
                db_column="creator_id",
            ),
        ),

        # SystemUserRole - Add creator, modifier
        migrations.AddField(
            model_name="systemuserrole",
            name="creator",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="created_user_roles",
                db_column="creator_id",
            ),
        ),
        migrations.AddField(
            model_name="systemuserrole",
            name="modifier",
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to="persistence.user",
                related_name="modified_user_roles",
                db_column="modifier_id",
            ),
        ),
    ]
