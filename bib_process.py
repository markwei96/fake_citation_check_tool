
class bib_processer:
    def __init__(self, bib_file):
        self.bib_file = bib_file
        self.entries = self.parse_bib_file()

    def parse_bib_file(self):
        entries = []
        with open(self.bib_file, 'r', encoding='utf-8') as file:
            entry = {}
            for line in file:
                line = line.strip()
                if line.startswith('@'):
                    if entry:
                        entries.append(entry)
                        entry = {}
                    entry['type'] = line.split('{')[0][1:].strip()
                    entry['key'] = line.split('{')[1].strip(',').strip()
                elif '=' in line:
                    key, value = line.split('=', 1)
                    entry[key.strip()] = value.strip().strip('"').strip(',')[1:-1]
            if entry:
                entries.append(entry)
        return entries

    def get_entries(self):
        return self.entries