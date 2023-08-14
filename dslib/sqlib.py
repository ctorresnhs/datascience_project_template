from pandas import DataFrame

class sqlite_context ():
    def __init__(self, database) -> None:
        self.database = database
    def __enter__(self):
        import sqlite3 as sqlite
        self.conn = sqlite.connect(self.database)
        self.cur = self.conn.cursor()
        return self.conn, self.cur
    def __exit__(self):
        self.conn.close()
def create_db(dbname)-> None:
    import sqlite3 as sq
    dbConn = sq.connect(f'./{dbname}')
    dbConn.close()
def import_from_csv(file,tableName,db,append=False):
    import pandas as pd
    import sqlite3 as sq
    data = pd.read_csv(file)
    dbConn = sq.connect(f'./{db}')
    if append:
        data.to_sql(tableName,dbConn,if_exists='append', index=False)
    else:
        data.to_sql(tableName,dbConn,if_exists='replace', index=False)
    dbConn.close()
def import_from_xls(file,sheet,tableName,db,append=False):
    import pandas as pd
    import sqlite3 as sq
    data = pd.read_excel(file,sheet_name=sheet)
    dbConn = sq.connect(f'./{db}')
    if append:
        data.to_sql(tableName,dbConn,if_exists='append', index=False)
    else:
        data.to_sql(tableName,dbConn,if_exists='replace', index=False)
    dbConn.close()
def import_from_dataframe(dataframe:DataFrame,database:str,table_name:str):
    import pandas as pd
    from pandas import DataFrame
    import sqlite3 as sqlite
    db = sqlite.connect(database)
    dataframe.to_sql(
        name=table_name,
        con=db,
        if_exists='replace',
        index=False
    )
def export_to_csv(db,tableName, folder=None): 
    import csv
    import sqlite3 as sqlite
    conn = sqlite.connect(db)
    cur = conn.cursor()
    data = cur.execute(f"SELECT * FROM {tableName}")
    cols = [description[0] for description in cur.description]
    if folder:
        tableName = folder+'/'+tableName
    with open(f"{tableName}.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(data)
    conn.close()

def execute_query(query_file,db):
    import sqlite3 as sqlite
    with open(query_file,'r') as f:
        query = f.read()
    db = sqlite.connect(db)
    cursor = db.cursor()
    cursor.executescript(query)
    db.close()

def execute_query_direct(query,db):
    import sqlite3 as sqlite
    db = sqlite.connect(db)
    cursor = db.cursor()
    cursor.executescript(query)
    db.close()

def import_bulk(file_name, tbl_name='bulk', db_name=None, max_rows=None, chunk_size=1000, ACH_DATE_filter_as_int=None):
    import pandas as pd
    from pandas import DataFrame
    import sqlite3 as sqlite

    sql_create_table = f"""CREATE TABLE if not exists {tbl_name}(
    QUALITY_SERVICE text,
    NAME text,
    ORG_CODE text,
    ACH_DATE integer,
    IND_CODE text,
    FIELD_NAME text,
    VALUE real,
    DEFAULT_VALUES_USED text,
    SUBMIT_USER_ID text,
    SUBMIT_DATE text,
    SUBMIT_TIME text,
    LAST_SUBMISSION text
    )"""

    cols = [
        'QUALITY_SERVICE',
        "NAME",
        'ORG_CODE',
        'ACH_DATE',
        'IND_CODE',
        'FIELD_NAME',
        "VALUE",
        "DEFAULT_VALUES_USED",
        "SUBMIT_USER_ID",
        "SUBMIT_DATE",
        "SUBMIT_TIME",
        "LAST_SUBMISSION"
    ]


    def yn_converter(x):
        if x == 'Y':
            return 1
        elif x == 'N':
            return 0
        else:
            return x

    db = sqlite.connect(db_name)
    query = db.cursor()
    query.execute(sql_create_table)
    
    chunk:DataFrame  
    for chunk in pd.read_csv(
            filepath_or_buffer=file_name, 
            usecols=cols,
            converters={'VALUE':yn_converter}, 
            chunksize= chunk_size,
            nrows=max_rows):
        #post-processing
        # chunk['SCHEME'] = chunk['QUALITY_SERVICE'].str[:3]
        # chunk['FY'] = chunk['QUALITY_SERVICE'].str[3:]
        # chunk['YM'] = chunk['ACH_DATE'].astype(str).str[0:6]
        # chunk['Y'] = chunk['ACH_DATE'].astype(str).str[:4]
        # chunk['M'] = chunk['ACH_DATE'].astype(str).str[4:6]
        # chunk['ORG_TYPE'] = 'GP'
        # chunk = chunk[chunk['SUBMIT_USER_ID']=='cro-processor']
        # chunk.rename(columns={'FIELD_NAME':'MEASURE'},inplace=True)
        chunk = chunk[chunk['ACH_DATE']==ACH_DATE_filter_as_int] if ACH_DATE_filter_as_int is not None else chunk
        # chunk = chunk[new_cols]
        if len(chunk)>0:
            chunk.to_sql(tbl_name, db, if_exists='append', index=False)
    db.close()