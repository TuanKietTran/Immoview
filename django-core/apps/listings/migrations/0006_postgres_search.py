from django.db import migrations


def enable_extensions(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")


def disable_extensions(apps, schema_editor):
    # Extensions are shared database infrastructure; do not drop them on rollback.
    pass


class Migration(migrations.Migration):
    dependencies = [("listings", "0005_duplicate_fraud_fields")]
    operations = [migrations.RunPython(enable_extensions, disable_extensions)]
