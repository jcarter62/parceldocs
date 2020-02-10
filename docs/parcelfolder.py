from appsettings import Settings
import os


class ParcelFolder:

    def __init__(self, parcel: str = '') -> None:
        self.parcel = parcel
        self.path = self.calculate_folder()
        return

    def calculate_folder(self):
        settings = Settings()
        base = settings.get('root_folder')
        parcel_path = self.split_parcel()
        result = os.path.join(base, parcel_path)
        return result

    def split_parcel(self):
        result = ''
        # first remove any spaces
        p = self.parcel.replace(' ', '')
        i = 0
        parts = []
        while i < len(p):
            parts.append(p[i:i+3])
            i += 3
        i = 0
        while i < len(parts):
            result = os.path.join(result, parts[i])
            i += 1
        return result.lower()





