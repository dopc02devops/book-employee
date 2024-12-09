from context import Context


def delete_dax_table(dyn_resource=None):
    """
    Deletes the demonstration table.
    :param dyn_resource: Either a Boto3 or DAX resource.
    """
    table_name = Context.dynamodb_table
    all_tables = []
    if dyn_resource is None:
        dynamodb = Context.dynamodb_local
        for table in dynamodb.tables.all():
            all_tables.append(table.name)
        if table_name not in all_tables:
            print(f"Table does not exist")
            return False

    table = dynamodb.Table(table_name)
    table.delete()

    print(f"Deleting {table.name}...")
    table.wait_until_not_exists()
    print(f"Deleting {table.name} complete")