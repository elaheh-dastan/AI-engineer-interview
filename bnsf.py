# Assume data:
# name,job
# Tony Sullivan,Office manager
# Mary Henry,Film editor
# John Doe,Dancer
# Jane Smith,Dancer
# Alex Ray,Pilot

class SparkTask:
    def __init__(self, spark_session):
        self.job_counts_dict = None
        self.sc = spark_session.sparkContext
        self.spark = spark_session

    def group_sort(self, input_path):
        # Read CSV as text file
        rdd = self.sc.textFile(input_path)

        # Extract the header
        # header = "name,job"
        header = rdd.first()

        # Remove header and split CSV lines
        # [
        #   "Tony Sullivan,Office manager",
        #   "Mary Henry,Film editor",
        #   "John Doe,Dancer",
        #   "Jane Smith,Dancer",
        #   "Alex Ray,Pilot"
        # ]
        rdd = rdd.filter(lambda row: row != header)
        # [
        #     ["Tony Sullivan", "Office manager"],
        #     ["Mary Henry", "Film editor"],
        #     ["John Doe", "Dancer"],
        #     ["Jane Smith", "Dancer"],
        #     ["Alex Ray", "Pilot"]
        #   ]
        rdd = rdd.map(lambda row: row.split(","))



        # Extract job column (second column)
        # [
        #     ("Office manager", 1),
        #     ("Film editor", 1),
        #     ("Dancer", 1),
        #     ("Dancer", 1),
        #     ("Pilot", 1)
        #   ]
        job_rdd = rdd.map(lambda cols: (cols[1].strip(), 1))

        # Count jobs
        # [
        #     ("Office manager", 1),
        #     ("Film editor", 1),
        #     ("Dancer", 2),
        #     ("Pilot", 1)
        # ]
        counts_rdd = job_rdd.reduceByKey(lambda a, b: a + b)

        # Sort by: (count ascending, job name ascending)
        # [
        #     ("Film editor", 1),
        #     ("Office manager", 1),
        #     ("Pilot", 1),
        #     ("Dancer", 2)
        # ]

        sorted_rdd = counts_rdd.sortBy(lambda x: (x[1], x[0]))

        # Convert to Python dict
        result = dict(sorted_rdd.collect())
        return result
