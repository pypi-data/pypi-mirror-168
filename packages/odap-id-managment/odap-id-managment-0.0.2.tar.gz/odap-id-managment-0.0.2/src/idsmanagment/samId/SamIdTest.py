import unittest
from pyspark.sql import functions as f
from pyspark.sql import types as t
from pyfonycore.bootstrap import bootstrapped_container
from idsmanagment.samId.SamId import SamId
from pysparkbundle.test.PySparkTestCase import PySparkTestCase


class SamIdTest(PySparkTestCase):
    def setUp(self) -> None:
        self.__container = bootstrapped_container.init("test")
        self.__sam_id = self.__container.get(SamId)

    def test_ids_managment(self):
        input_schema = t.StructType([
            t.StructField("id_value", t.IntegerType(), True),
            t.StructField("id_type", t.StringType(), True),
            t.StructField("client_id", t.IntegerType(), True),
            t.StructField("timestamp", t.StringType(), True),
        ])

        input_date_format = "d/M/yyyy H:mm"

        input_data = [
            (1, "ga_id", 1, "1/1/2017 01:00"), #1-B
            (1, "ga_id", 5, "2/1/2017 16:00"),
            (1, "ga_id", 6, "3/1/2017 11:00"),
            (1, "ga_id", 6, "4/1/2017 12:00"),  #3-B-c
            (1, "ga_id", None, "2/1/2017 17:00"),
            
            (2, "ga_id", 2, "1/1/2017 13:00"), #1-B
            (2, "ga_id", 5, "2/1/2017 18:00"),
            (2, "ga_id", 2, "3/1/2017 22:00"),  #3-B-b
            
            (3, "ga_id", 3, "1/1/2017 21:00"), #1-A
            
            (4, "ga_id", 4, "1/1/2017 23:00"), #1-A
            (4, "ga_id", 4, "4/1/2017 07:00"),
            
            (5, "ga_id", None, "6/1/2017 05:00"), #1-A #3-A-a
            
            (6, "ga_id", None, "1/1/2017 04:00"), #1-A #3-A-a
            
            (7, "ga_id", None, "1/1/2017 05:30"), #1-A
            (7, "ga_id", 5, "2/1/2017 03:00"),  #3-B-d
            (7, "ga_id", None, "3/1/2017 02:00"),
            
            (8, "ga_id", None, "5/1/2017 08:00"), #1-A #3-A-b
            
            (9, "ga_id", 1, "6/1/2017 7:00"), #1-A #3-B-a
        
            (10, "ga_id", 8, "7/1/2017 08:00"),  # test 1 09/22: 10 <-> 8 od 4/1/2017 
            (10, "ga_id", 3, "6/1/2017 20:00"),
            (10, "ga_id", None, "4/1/2017 04:30"),  
            
            (11, "ga_id", 7, "9/1/2017 02:00"),  # test 2 09/22:  11 <-> 7 od 2/1/2017 
            (11, "ga_id", None, "5/1/2017 23:00"),
            (11, "ga_id", 22, "2/1/2017 01:50"),  
            
            (12, "ga_id", None, "2/1/2017 07:00"), # test 3 09/22: 12 <-> 23 od 4/1/2017
            (12, "ga_id", 3, "2/1/2017 16:00"),
            (12, "ga_id", 8, "5/1/2017 17:00"),
            (12, "ga_id", 23, "4/1/2017 12:00"),  
            (12, "ga_id", 23, "7/1/2017 18:00")
        ]

        input_dataframe = self.spark.createDataFrame(input_data, input_schema).withColumn("timestamp", f.to_timestamp(f.col("timestamp"), input_date_format))
        
        #output dataframe before SamID
        output_schema = t.StructType([
            t.StructField("id_value", t.IntegerType(), True),
            t.StructField("id_type", t.StringType(), True),
            t.StructField("person_id", t.IntegerType(), True),
            t.StructField("timestamp_valid_from", t.StringType(), True),
            t.StructField("timestamp_valid_to", t.StringType(), True)
        ])

        output_date_format = "d/M/yyyy H:mm"

        output_data = [
            (1, "ga_id", 1, "1/1/2017 0:00", None),  #3-B-c
            (2, "ga_id", 2, "1/1/2017 0:00", None),  #3-B-b
            (3, "ga_id", 3, "1/1/2017 0:00", None),
            (4, "ga_id", 4, "1/1/2017 0:00", None),
            (4, "ga_id", 7, "15/1/2016 05:00", "23/10/2016 22:00"),  #test uzavrety vztah
            
            (5, "ga_id", None, "3/1/2017 0:00", None), #3-A-a
            (6, "ga_id", 6, "1/1/2017 0:00", None), #3-A-a
            (9, "ga_id", None, "2/1/2017 0:00", None), #3-B-a
        
            (12, "ga_id", 9, "31/12/2016 3:00", None)
        ]

        output_dataframe_before_sam_id = (self.spark
            .createDataFrame(output_data, output_schema)
            .withColumn("timestamp_valid_to", f.to_timestamp(f.col("timestamp_valid_to"), output_date_format))
            .withColumn("timestamp_valid_from", f.to_timestamp(f.col("timestamp_valid_from"), output_date_format))
        )
        
        expected_output_schema = t.StructType([
            t.StructField("id_value", t.IntegerType(), True),
            t.StructField("id_type", t.StringType(), True),
            t.StructField("person_id", t.IntegerType(), True),
            t.StructField("timestamp_valid_from", t.StringType(), True),
            t.StructField("timestamp_valid_to", t.StringType(), True)
        ])

        expected_output_date_format = "d/M/yyyy H:mm"

        expected_output_data = [
            (1, "ga_id", 1, "1/1/2017 0:00", "3/1/2017 11:00"),
            (1, "ga_id", 6, "3/1/2017 11:00", None),
            (2, "ga_id", 2, "1/1/2017 0:00", None),
            (3, "ga_id", 3, "1/1/2017 0:00", None),
            (4, "ga_id", 7, "15/1/2016 05:00", "23/10/2016 22:00"),   #test uzavrety vztah
            (4, "ga_id", 4, "1/1/2017 0:00", None),
            
            (5, "ga_id", None, "3/1/2017 0:00", None), 
            (6, "ga_id", 6, "1/1/2017 0:00", None), 
            (7, "ga_id", 5, "1/1/2017 05:30", None),
            (8, "ga_id", None, "5/1/2017 08:00", None),
            (9, "ga_id", 1, "2/1/2017 0:00", None),
            
            (10, "ga_id", 8, "4/1/2017 04:30", None),
            (11, "ga_id", 7, "2/1/2017 01:50", None),
            (12, "ga_id", 9, "31/12/2016 3:00", "4/1/2017 12:00"),
            (12, "ga_id", 23, "4/1/2017 12:00", None)
        ]

        expected_output_dataframe = (self.spark
            .createDataFrame(expected_output_data, expected_output_schema)
            .withColumn("timestamp_valid_to", f.to_timestamp(f.col("timestamp_valid_to"), expected_output_date_format))
            .withColumn("timestamp_valid_from", f.to_timestamp(f.col("timestamp_valid_from"), expected_output_date_format))
        )
        
        output_after_sam_id_df = self.__sam_id.ids_mng(input_dataframe, output_dataframe_before_sam_id)
        
        self.compare_dataframes(expected_output_dataframe, output_after_sam_id_df, ["id_value"])

if __name__ == "__main__":
    unittest.main()
