from typing import Optional


class MetadataEntity(object):
    """
    This class represents the metadata entity on source tasks.

    :param description: the dataset description
    :type description: string

    :param dataexpert: the dataset expert name
    :type dataexpert: string

    :param schema: the dataset schema
    :type schema: list

    :param classifications: the dataset classification. May be PII or None
    :type classifications: Optional, list

    :param glossary: the glossary word present on the dataset
    :type glossary: Optional, string
    """

    def __init__(
        self,
        description: str,
        dataexpert: str,
        schema: list,
        classifications: Optional[list] = None,
        glossary: Optional[str] = None,
    ):
        self.description = description
        self.dataexpert = dataexpert
        self.schema = schema
        self.classifications = classifications
        self.glossary = glossary

    @staticmethod
    def build(metadata: dict):
        return MetadataEntity(
            description=metadata.get("description"),
            dataexpert=metadata.get("dataexpert"),
            schema=metadata.get("schema"),
        )
