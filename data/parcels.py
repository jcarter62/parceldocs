import pyodbc
from appsettings import Settings
import copy


class Parcels:

    def __init__(self, page_size=10, page=1):
        self.settings = Settings()
        self.parcels = []
        self.parcels_flt = []
        self.active = '1'
        self.page_size = page_size
        self.page = page
        self.load_parcels()

    def _conn_str_(self, ):
        server = self.settings.get('sqlserver')
        database = self.settings.get('sqldb')
        driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
        return driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;'

    #
    # load self.parcels with data
    #
    def load_parcels(self):
        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = 'select parcel_id from parcel where isactive=%s order by parcel_id;' % self.active
        try:
            for row in cursor.execute(cmd):
                parcel_record = self._extract_row(row)
                result.append(parcel_record['parcel_id'])
        except Exception as e:
            print(str(e))

        pagedata = []
        # skip
        index_low = (self.page - 1) * self.page_size
        index_hi = self.page * self.page_size
        i = 0
        while i < len(result):
            if (i > index_low) and (i <= index_hi):
                pagedata.append(result[i])
            i += 1

        self.parcels = copy.deepcopy(pagedata)

        return

    #
    # apply filter to self.parcels, and store in parcels_flt
    #
    def filter_parcels(self, partial:str = ''):
        self.parcels_flt = []
        token = partial.lower()
        for p in self.parcels:
            if token in p['parcel_id']:
                self.parcels_flt.append(p)

    def _extract_row(self, row):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r

