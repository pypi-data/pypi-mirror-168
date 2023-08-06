from logging import Logger

from pyspark.sql import SparkSession
from pyspark.sql import functions as f

columns_basic = ["id_value", "id_type", "client_id", "min_date", "max_date"]
columns_not_seen = ["id_value", "id_type", "client_id", "since", "max_date"]

columns_to_drop = ["client_ids", "max_timestamps", "min_timestamps", "num_clients", "num_dates"]

id_value_col = "id_value"
person_id_col = "person_id"
valid_to_col = "timestamp_valid_to"

inner_join_cols = ['id_value', 'max_date']
full_join_cols = ["id_value", "timestamp_valid_from"]

class SamId:
    def __init__(
        self,
        logger: Logger,
        spark: SparkSession,
    ):
        self.__logger = logger
        self.__spark = spark

    def ids_mng(self, input_df, output_df):
    # transform input_df
        distinct_pairs_df = self._distinct_pairs(input_df)
        sized_input_df = self._pairs_sized(distinct_pairs_df)
    
    # part a)
        no_conflicts_df = self._filter_no_conflicts(sized_input_df)
        no_conflicts_ready_df = self._process_parts(no_conflicts_df, 
                                          distinct_pairs_df, 
                                          inner_join_cols, 
                                          columns_basic)
    
        no_conflicts_null_df = self._divide_no_conflicts_part(self._filter_null_values, 
                                                    no_conflicts_ready_df, 
                                                    person_id_col, 
                                                    columns_basic)
    
        no_conflicts_null_new_df = no_conflicts_null_df.join(output_df, id_value_col, "left_anti")
        
        no_conflicts_one_client_df = self._divide_no_conflicts_part(self._filter_non_null_values, 
                                                            no_conflicts_ready_df, 
                                                            person_id_col, 
                                                            columns_basic)
            
        # part b)
        no_conflicts_2_dates_df = self._filter_no_conflicts_2_dates(sized_input_df)
        
        # part c) 
        conflicts_non_null_df = self._filter_conflicts_non_null(sized_input_df)
        conflicts_non_null_ready_df = self._process_parts(conflicts_non_null_df, 
                                            distinct_pairs_df, 
                                            inner_join_cols, 
                                            columns_basic)
        
        # part d)
        conflicts_plus_null_sized_df = self._conflicts_null_processed_df(sized_input_df, 
                                                                distinct_pairs_df, 
                                                                inner_join_cols[0], 
                                                                columns_to_drop, 
                                                                columns_basic[2])
        
        conflicts_null_seen_df = self._filter_conflicts_null_seen(conflicts_plus_null_sized_df, output_df)
        conflicts_null_seen_ready_df = self._process_parts(conflicts_null_seen_df, 
                                                    distinct_pairs_df, 
                                                    inner_join_cols, 
                                                    columns_basic)
        
        conflicts_null_not_seen_df = conflicts_plus_null_sized_df.join(output_df, id_value_col, "left_anti")
        conflicts_null_not_seen_ready_df = self._process_parts(conflicts_null_not_seen_df, 
                                                    distinct_pairs_df, 
                                                    inner_join_cols, 
                                                    columns_not_seen)
        
        # add increment parts to output_df
        pairs_united = self._union_all_parts(output_df,
                        no_conflicts_null_new_df,
                        no_conflicts_one_client_df,
                        no_conflicts_2_dates_df,
                        conflicts_non_null_ready_df,
                        conflicts_null_seen_ready_df,
                        conflicts_null_not_seen_ready_df)
        
        pairs_to_update = self._filter_pairs_to_update(pairs_united, 
                                                id_value_col, 
                                                valid_to_col)

        output_ready_df = self._create_output_df(pairs_to_update, pairs_united, full_join_cols)

        return output_ready_df


#functions

# process input_df
    def _distinct_pairs(self, df):
        return (
            df
            .groupBy("id_value", "id_type", "client_id")
            .agg(
                f.min("timestamp").alias("min_date"), 
                f.max("timestamp").alias("max_date"))
        )

    def _pairs_sized(self, df):
        return (
            df
            .groupBy("id_value")
            .agg(
                f.collect_set('max_date').alias('max_timestamps'),
                f.collect_set('min_date').alias('min_timestamps'),
                f.collect_set("client_id").alias("client_ids")
        )
        .withColumn('num_clients', f.size('client_ids'))
        .withColumn('num_dates', f.size('max_timestamps'))
    )

    def _process_parts(self, df, input_df, join_cols, cols):
        df = df.join(input_df, join_cols)
        df = df.select(cols)
        df = self._rename_cols(df, cols)
    
        return df

    # a) 
    def _filter_no_conflicts(self, df):
        return (
            df
            .filter((f.col("num_clients")< 2) & (f.col("num_dates") == 1))
            .withColumn("max_date", f.col("max_timestamps").getItem(0))
            .select("id_value", "max_date")
        )

    def _divide_no_conflicts_part(self, function, df, col, cols):
        df = function(df, col)
        df = self._rename_cols(df, cols)
    
        return df

    # b) 
    def _filter_no_conflicts_2_dates(self, df):
        return (
            df
            .filter((f.col("num_clients")< 2) & (f.col("num_dates") == 2))
            .withColumn("client_id", f.col("client_ids").getItem(0))
            .withColumn("min_date", f.array_min(f.col("min_timestamps")))
            .withColumn("id_type", f.lit("ga_id"))
            .select("id_value", "id_type", "client_id", "min_date")
            .withColumnRenamed("client_id", "person_id")
            .withColumnRenamed("min_date", "timestamp_valid_from")
            .withColumn("timestamp_valid_to", f.lit(None))
        )

    # c)
    def _filter_conflicts_non_null(self, df):
        return (
            df
            .filter((f.col("num_clients")>= 2) & (f.col("num_clients") == f.col("num_dates")))
            .withColumn("max_date", f.array_max(f.col("max_timestamps")))
            .select("id_value", "max_date")
        )    

    # d)
    def _conflicts_null_processed_df(self, df, input_df, join_cols, drop_cols, cols):
        conflicts_plus_null_df = self._filter_conflicts_plus_null(df)
        conflicts_plus_null_joined_df = conflicts_plus_null_df.join(input_df, join_cols)
        conflicts_plus_null_filtered_df = conflicts_plus_null_joined_df.drop(*drop_cols)
        conflicts_plus_null_ready_df = self._filter_non_null_values(conflicts_plus_null_filtered_df, cols)
        conflicts_plus_null_sized_df = self._size_conflicts_plus_null(conflicts_plus_null_ready_df)
        
        return conflicts_plus_null_sized_df

    def _filter_conflicts_plus_null(self, df):
        return (
            df
            .filter((f.col("num_clients")>= 2) & (f.col("num_clients") != f.col("num_dates")))
            .withColumn("since", f.array_min(f.col("min_timestamps")))
        )

    # add increment parts to output_df
    def _union_all_parts(self, output_df, df, df1, df2, df3, df4, df5):
        output_df = df.unionByName(output_df)
        output_df = df1.unionByName(output_df)
        output_df = df2.unionByName(output_df)
        output_df = df3.unionByName(output_df)
        output_df = df4.unionByName(output_df)
        output_df = df5.unionByName(output_df)
        output_df = self._update_pairs_l6(output_df)

        return output_df

    # filter pairs that need to update timestamps cols
    def _filter_pairs_to_update(self, output_df, col1, col2):
        df = self._agg_pairs_l6(output_df)
        df = output_df.join(df, col1, "right")
        df = self._filter_null_values(df, col2)
        df = self._update_person_id_col(df)

        return df

    # process remaining into final output
    def _create_output_df(self, df, output_df, cols):
        df = self._pairs_update_timestamps(df)
        output_df = df.join(output_df, cols, "full")
        output_df = self._update_pairs_l7(output_df)
        df = self._pairs_update_null_solution(df)
        output_df = df.join(output_df, cols, "full")
        output_df = self._update_pairs_l8(output_df)
        output_ready_df = self._create_final_output(output_df)

        return output_ready_df


    def _size_conflicts_plus_null(self, df):
        return (
            df
            .groupBy("id_value", "since")
            .agg(
                f.collect_set('max_date').alias('timestamps')
            )
            .withColumn('num_dates', f.size('timestamps'))
            .withColumn("max_date", f.array_max(f.col("timestamps")))
            .select("id_value", "since", "max_date")
        )

    
    def _filter_conflicts_null_seen(self, df, output_df):
        return df.join(output_df.select("id_value"), ["id_value"])


    def _update_pairs_l6(self, df):
        return (
            df
            .orderBy("timestamp_valid_from")
            .dropDuplicates(["id_value","person_id"])
            .fillna({'person_id':'0'})
        )


    def _agg_pairs_l6(self, df):
        return (
            df
            .filter(f.col("timestamp_valid_to").isNull())
            .groupBy("id_value")
            .agg(f.countDistinct("person_id").alias("no_clients"))
            .filter(f.col("no_clients")==2)
            .select("id_value")
        )


    def _update_person_id_col(self, df): 
        return df.withColumn("person_id", f.when(f.col("person_id") == 0, None).otherwise(f.col("person_id")))

    def _pairs_update_timestamps(self, df):
        return (
            df
            .groupBy("id_value")
            .agg(
                f.countDistinct("person_id").alias("no_clients"),
                f.sort_array(f.collect_set('timestamp_valid_from')).alias("timestamps"))
            .withColumn("timestamp_valid_from", f.col("timestamps").getItem(0))
            .withColumn("max_date", f.col("timestamps").getItem(1))
        )


    def _update_pairs_l7(self, df):
        return (
            df
            .drop("no_clients")
            .withColumn("timestamp_valid_to",
                f.when((f.col("timestamp_valid_to").isNull()) & (f.col("max_date").isNotNull()), f.col("max_date"))
                .otherwise(f.col("timestamp_valid_to")))
        )


    def _pairs_update_null_solution(self, df):
        return (
            df
            .withColumnRenamed("timestamp_valid_from", "since")
            .withColumnRenamed("max_date", "timestamp_valid_from")
            .drop("timestamps")
        )


    def _update_pairs_l8(self, df):     
        return (
            df
            .withColumn("timestamp_valid_from",
                f.when((f.col("no_clients") == 1) & (f.col("since").isNotNull()), f.col("since"))
                .otherwise(f.col("timestamp_valid_from")))
            .withColumn("timestamp_valid_to",
                f.when((f.col("timestamp_valid_to").isNull()) & (f.col("max_date").isNotNull()), f.col("max_date"))
                .otherwise(f.col("timestamp_valid_to")))
        )

    
    def _create_final_output(self, df):
        return (
            df
            .withColumn("drop", 
                    f.when((f.col("person_id") == 0) & (f.col("timestamp_valid_to").isNotNull()), 1)
                    .otherwise(0))
            .withColumn("person_id", f.when(f.col("person_id")==0, None).otherwise(f.col("person_id")))
            .filter(f.col("drop")==0).drop("timestamps", "max_date", "drop")
            .select("id_value", "id_type", "person_id", "timestamp_valid_from", "timestamp_valid_to")
        )

    def _rename_cols(self, df, cols):      
        return (
            df
            .withColumnRenamed(cols[2], "person_id")
            .withColumnRenamed(cols[3], "timestamp_valid_from")
            .withColumnRenamed(cols[4], "timestamp_valid_to")
            .withColumn("timestamp_valid_to", f.lit(None))
        )

    def _filter_non_null_values(self, df, col):
        return (
            df
            .filter(f.col(col).isNotNull())
        )

    def _filter_null_values(self, df, col):
        return (
            df
            .filter(f.col(col).isNull())
        )