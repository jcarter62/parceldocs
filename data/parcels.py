import pyodbc
from appsettings import Settings
import copy

class Parcels:

    def __init__(self):
        self.settings = Settings()
        self.parcels = []
        self.parcels_flt = []
        self.active = '1'
        pass

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
                result.append(self._extract_row(row))
            self.parcels = copy.deepcopy(result)
        except Exception as e:
            print(str(e))
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

