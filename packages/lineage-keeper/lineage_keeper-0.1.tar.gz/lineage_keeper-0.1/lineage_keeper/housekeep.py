# Databricks notebook source
from datetime import datetime, timedelta
class HouseKeep():

    def __init__(self, spark):
        self._spark = spark
        
    def optimize(self, service_table_name="default._service_table_lineage_keeper"):
        try:
            self._spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false")
        except: pass
        
        try:
            self._spark.sql(f"OPTIMIZE {service_table_name}")
            self._spark.sql(f"VACUUM {service_table_name} RETAIN 0 HOURS")
        except Exception as e:
            raise e
            
    def clean_history(self, retention_threshold_days=30, service_table_name="default._service_table_lineage_keeper"):
        retention_threshold_date = (datetime.now() - timedelta(days = retention_threshold_days)).strftime("%Y-%m-%dT%H:%M:%S+%f")
        self._spark.sql(f"DELETE FROM {service_table_name} WHERE load_datetime <= '{retention_threshold_date}'")
    