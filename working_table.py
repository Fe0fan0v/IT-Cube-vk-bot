class Table:
    def __init__(self, file_id):
        self.file_id = file_id
        self.data = {}
        import requests
        import csv
        import io

        url = f'https://docs.google.com/spreadsheets/d/{self.file_id}/export?format=csv'
        r = requests.get(url)
        sio = io.StringIO(r.content.decode('utf-8'), newline=None)
        reader = list(csv.reader(sio, dialect=csv.excel))

        for row in reader[1:]:
            self.data[row[1].strip()] = []

        for row in reader[1:]:
            for i, cell in enumerate(row[4:]):
                if cell != '':
                    self.data[row[1].strip()].append(f'{reader[0][4 + i].strip()}: {cell.strip()}'.replace("\n", ""))
