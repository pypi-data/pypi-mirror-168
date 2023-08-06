class SparkMapper(object):
    @staticmethod
    def add_default_fields(field: dict) -> dict:
        """
        Intends to add default spark schema fields in a metadata dict field.

        :param field: the metadata field that will be changed
        :field type: dict

        :return: the changed field
        :rtype: dict
        """
        default_schema_options = {"nullable": True, "metadata": {}}
        field.update(default_schema_options)
        return field

    @staticmethod
    def add_struct_field(field):
        """
        Intends to mutate complex filed types(dictionary) in spark struct field.

        :param field: the metadata field that will be changed
        :field type: dict
        """

        field.pop("type")
        fields = field.pop("fields")
        field.update(
            {
                "type": {
                    "fields": [SparkMapper.add_fields(field=field) for field in fields],
                    "type": "struct",
                },
            }
        )

    @staticmethod
    def add_array_field(field):
        """
        Intends to mutate complex filed types(dictionary) in spark array field.

        :param field: the metadata field that will be changed
        :field type: dict
        """

        field.pop("type")
        element_type = field.pop("elementType")
        if isinstance(element_type, dict):
            if element_type.get("type") == "struct":
                fields = element_type.pop("fields")
                updated_fields = {
                    "fields": [SparkMapper.add_fields(field=field) for field in fields],
                    "type": "struct",
                }
            else:
                updated_fields = SparkMapper.add_fields(field=element_type)
        else:
            updated_fields = SparkMapper.add_fields(field={"type": element_type})
        field.update(
            {
                "type": {
                    "type": "array",
                    "containsNull": True,
                    "elementType": updated_fields,
                },
            }
        )

    @staticmethod
    def add_fields(field):
        """
        Intends to manage the corresponding mutate field method for any field.

        :param field: the metadata field that will be changed
        :field type: dict
        """

        if field.get("type") == "struct":
            SparkMapper.add_struct_field(field=field)
            SparkMapper.add_default_fields(field=field)
        elif field.get("type") == "array":
            SparkMapper.add_array_field(field=field)
            SparkMapper.add_default_fields(field=field)
        else:
            SparkMapper.add_default_fields(field=field)
        return field

    def get_schema_definition(self, metadata: dict) -> dict:
        """
        Intends to map a inputted metadata dict to spark schema.

        :param metadata: the metadata dict
        :field type: dict

        :return: the spark schema
        :rtype: dict
        """
        schema = metadata.get("schema")

        for field in schema:
            SparkMapper.add_fields(field=field)

        spark_schema = {"type": "struct", "fields": schema}
        return spark_schema
