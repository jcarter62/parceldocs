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
        self.parcel = None
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
        self.parcels = copy.deepcopy(result)
        return

    def load_one_parcel(self, parcel_id):
        self.parcel = None
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = """
            select
                p.Parcel_Id, p.Acres, p.IsActive, p.Section, p.Township, p.Range, c.Description as county, p.LegalDesc, isnull(p.Notes,'') as Notes
            from parcel p join code c on p.CountyCode = c.CODE_ID
            where p.Parcel_Id = '%s'
        """ % parcel_id
        try:
            for row in cursor.execute(cmd):
                record = self._extract_row(row)
                self.parcel = {
                    'parcel_id': record['parcel_id'],
                    'acres': record['acres'],
                    'active':  (record['isactive'] == '1'),
                    'section': record['section'],
                    'township': record['township'],
                    'range': record['range'],
                    'legal': record['legaldesc'],
                    'notes': record['notes'],
                    'county': record['county']
                }
        except Exception as e:
            print(str(e))
        return

    #
    # apply filter to self.parcels, and store in parcels_flt
    #
    def filter_parcels(self, partial:str = ''):
        self.parcels_flt = []
        if partial <= '':
            self.parcels_flt = self.parcels
        else:
            token = partial.lower()
            i = 0
            while i < len(self.parcels):
                if token in self.parcels[i].lower():
                    self.parcels_flt.append(self.parcels[i])
                i += 1

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

