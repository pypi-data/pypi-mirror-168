import networkx as nx
from pyvis.network import Network
from pyspark.sql.functions import col, explode, row_number
from pyspark.sql.window import Window

class LineageViewer():

    def __init__(self, spark):
        self._spark = spark
        
    def _graph_generator(self, service_table_name="default._service_table_lineage_keeper", table_name=None):
        df = self._spark.read.table(service_table_name).withColumn("source_tables", explode(col("source_tables")))
        if table_name:
            df = df.filter((col("target_table")==table_name)|(col("source_tables")==table_name))
        window_spec = Window.partitionBy("target_table","source_tables").orderBy(col("load_datetime").desc())
        df = df.withColumn("rn", row_number().over(window_spec)).filter("rn == 1").drop("rn","load_datetime")

        edges = [(r.source_tables, r.target_table) for r in df.collect()]

        g = nx.DiGraph()
        for s_table, t_table in edges:
            g.add_edge(s_table, t_table)

        if not nx.is_directed_acyclic_graph(g):
            raise Exception("Not directed acyclic graph")
        else:
            return g
        

    def viewer(self, service_table_name="default._service_table_lineage_keeper", table_name=None):
        import IPython
        
        g = self._graph_generator(service_table_name, table_name)
        
        net = Network(height='600', width='1000', directed=True)
        net.from_nx(g)    

        IPython.display.display(IPython.display.HTML(net.generate_html()))
        
    def save_graph(self, path, service_table_name="default._service_table_lineage_keeper", table_name=None):
        g = self._graph_generator(service_table_name, table_name)
        
        net = Network(height='600', width='1000', directed=True)
        net.from_nx(g)
        
        net.write_html(path)

