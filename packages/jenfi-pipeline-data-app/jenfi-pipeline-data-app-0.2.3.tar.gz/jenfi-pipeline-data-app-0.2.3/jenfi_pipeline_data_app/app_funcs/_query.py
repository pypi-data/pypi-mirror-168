import pandas as pd

# Primary use point for Credit
# Should be able to help take snapshot of data and return the cache as necessary.
def df_query(self, query_str):
    # if self.PYTHON_ENV == "production":
    #     # Make class that hashes query+company_id+credit_app+pipeline+run_number?
    #     # If the hash is the same as previously seen one in S3, download and return
    #     # Else run the query and save the data back up to S3.
    #     pass
    # else:
    #     pass

    return pd.read_sql(query_str, self.db_engine)


def query_one(self, query_str):
    return self.db.execute(query_str).fetchone()


def query_all(self, query_str):
    return self.db.execute(query_str).fetchall()
