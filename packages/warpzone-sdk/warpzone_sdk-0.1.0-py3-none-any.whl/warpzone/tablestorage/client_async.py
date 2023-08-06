""" Module w.r.t. Azure table storage logic."""

import asyncio

from azure.data.tables.aio import TableClient

from warpzone.tablestorage.operations import TableOperations


class WarpzoneTableClientAsync:
    """Class to interact with Azure Table asyncronously."""

    def __init__(self, table_client: TableClient):
        self._table_client = table_client

    @classmethod
    def from_connection_string(cls, conn_str: str, table_name: str):
        table_client = TableClient.from_connection_string(conn_str, table_name)
        return cls(table_client)

    async def execute_table_operations(
        self,
        operations: TableOperations,
    ):
        """Perform table storage operations from a operation set.

        Args:
            operations (TableOperations): Iterable of lists of table operations (dicts)
        """
        tasks = []
        async with self._table_client:
            for batch in operations:
                task = self._table_client.submit_transaction(batch)
                tasks.append(task)

            await asyncio.gather(*tasks)

    async def query(self, query: str) -> list[dict]:
        """Retrieve data from Table Storage using linq query

        Args:
            query (str): Linq query.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        async with self._table_client:
            async_records = self._table_client.query_entities(query)
            records = [entity async for entity in async_records]

        return records
