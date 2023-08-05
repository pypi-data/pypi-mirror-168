from pyspark.sql.dataframe import DataFrame
from pyspark.sql.readwriter import DataFrameWriter
from datetime import datetime

class LineageListener():

    def __init__(self, spark):
        self._spark = spark

    def _get_source_tables(self, df):
        explain_formatted = df._sc._jvm.PythonSQLUtils.explainString(df._jdf.queryExecution(), "formatted")
        explain_formatted_parsed = [i.split(" ")[-1] for i in explain_formatted.split("\n") if ("Scan" in i) and ("(" == i[0])]
        return list(set(explain_formatted_parsed))

    def listener(self, df, target_table_name, service_table="default._service_table_lineage_keeper"):
        source_tables = self._get_source_tables(df)
        schema ='target_table string, source_tables ARRAY<string>, load_datetime string'
        load_time = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S+%f"))
        (
            self._spark.createDataFrame(
                [(target_table_name, source_tables, load_time)], schema
            ).write.mode("append").format("delta")._jwrite.saveAsTable(service_table)
        )

def load_listener(spark, service_table="default._service_table_lineage_keeper"):

    class DataFrameWriterLineage(DataFrameWriter): 

        def __init__(self, df):
            super().__init__(df)

        def saveAsTable(self, name, format=None, mode=None, partitionBy=None, **options):
            """Saves the content of the :class:`DataFrame` as the specified table.
            
            Lineage Keeper listener included

            In the case the table already exists, behavior of this function depends on the
            save mode, specified by the `mode` function (default to throwing an exception).
            When `mode` is `Overwrite`, the schema of the :class:`DataFrame` does not need to be
            the same as that of the existing table.

            * `append`: Append contents of this :class:`DataFrame` to existing data.
            * `overwrite`: Overwrite existing data.
            * `error` or `errorifexists`: Throw an exception if data already exists.
            * `ignore`: Silently ignore this operation if data already exists.

            .. versionadded:: 1.4.0

            Notes
            -----
            When `mode` is `Append`, if there is an existing table, we will use the format and
            options of the existing table. The column order in the schema of the :class:`DataFrame`
            doesn't need to be same as that of the existing table. Unlike
            :meth:`DataFrameWriter.insertInto`, :meth:`DataFrameWriter.saveAsTable` will use the
            column names to find the correct column positions.

            Parameters
            ----------
            name : str
                the table name
            format : str, optional
                the format used to save
            mode : str, optional
                one of `append`, `overwrite`, `error`, `errorifexists`, `ignore` \
                (default: error)
            partitionBy : str or list
                names of partitioning columns
            **options : dict
                all other string options
            """
            
            LineageListener(spark).listener(self._df, name, service_table)
            
            self.mode(mode).options(**options)
            if partitionBy is not None:
                self.partitionBy(partitionBy)
            if format is not None:
                self.format(format)
            self._jwrite.saveAsTable(name)
            
    @property
    def write_lineage(self):
        """
        Interface for saving the content of the non-streaming :class:`DataFrame` out into external
        storage.

        .. versionadded:: 1.4.0

        Returns
        -------
        :class:`DataFrameWriterLineage`
        """
        return DataFrameWriterLineage(self)

    DataFrame.write = write_lineage       

