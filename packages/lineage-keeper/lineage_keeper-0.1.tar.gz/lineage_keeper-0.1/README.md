# Lineage Keeper

A lightweight lineage tool based on Spark and Delta Lake

## Instalation

```
pip install lineage-keeper
```

## Basic use

```
from lineage_keeper import load_listener, LineageViewer
load_listener(spark)

df1 = spark.read.table("db.table_1")
df2 = spark.read.table("db.table_2")

df_join = df1.join(df2, "key")

df_join.write.saveAsTable("db.join_tables")

LineageViewer(spark).viewer()
```

## Limitations

- Its necessary to use tables sintax to read data
    - `spark.read.table("db.table")`
    - `spark.sql("SELECT * FROM db.table")`
- To use `load_listener` to automatically input lineage information is necessary to use `df.write.saveAsTable("db.table")` otherwise need to call `LineageListener(spark).listener(df, "db.table")`

## Functionalities

By default Lineage Keeper use "default._service_table_lineage_keeper" as a service table.

If wanted its possible to use a different service table.

### Listener function

After initiate the Listener we can give a DataFrame and a target table name to be add on the service table

```
LineageListener(spark).listener(df, "target_db.target_table")
```

### load listener 

Change df.write.saveAsTable to use the listerner when called

```
load_listener(spark)
```

### Lineage graph viewer

Generate a static HTML with the lineage graph

```
LineageViewer(spark).viewer()
```

### Lineage graph writer

Save a static HTML with the lineage graph on disk

```
LineageViewer(spark).save_graph(path)
```


## Google Colab Sample

[Sample using Lineage Keeper](https://colab.research.google.com/drive/19ZnFMPIxxwGWpQbj9x92CRnzUfzaTyaR?usp=sharing)

![Graph_Sample](.attachment/graph_sample.png)