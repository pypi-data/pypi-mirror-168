# Lineage Keeper

A lightweight lineage tool based on Spark and Delta Lake

<img src="https://raw.githubusercontent.com/otacilio-psf/lineage-keeper/main/.attachment/architecture.drawio.png" alt="Architecture" height="150"/>

## Table of contents

  * [Instalation](#instalation)
  * [Basic use](#basic-use)
  * [Functionalities](#functionalities)
    + [Listener function](#listener-function)
    + [load listener](#load-listener)
    + [Lineage graph viewer](#lineage-graph-viewer)
    + [Lineage graph writer](#lineage-graph-writer)
  * [Limitations](#limitations)
  * [Demo Notebook](#demo-notebook)

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

## Functionalities

By default Lineage Keeper use "default._service_table_lineage_keeper" as a service table.

If wanted its possible to use a different service table.

### Listener function

Manually input lineage information on the service table

LineageListener : spark sesison
listener : source DataFrame, target table

```
ll = LineageListener(spark)
ll.listener(df, "target_db.target_table")
```

### load listener 

Change df.write.saveAsTable to automatically input lineage information on the service table

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

## Limitations

- Its necessary to use tables sintax to read data
    - `spark.read.table("db.table")`
    - `spark.sql("SELECT * FROM db.table")`
- To use `load_listener` to  is necessary to use `df.write.saveAsTable("db.table")` otherwise need to call `LineageListener(spark).listener(df, "db.table")`

## Demo Notebook

[Sample using Lineage Keeper](https://colab.research.google.com/drive/19ZnFMPIxxwGWpQbj9x92CRnzUfzaTyaR?usp=sharing)

<img src="https://raw.githubusercontent.com/otacilio-psf/lineage-keeper/main/.attachment/graph_sample.png" alt="Graph_Sample" height="300"/>