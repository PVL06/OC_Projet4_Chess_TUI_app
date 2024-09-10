from rich.table import Table
from rich import print


class SelectBox:
    def __init__(self, title, items: list, active=False) -> None:
        self.title = title
        self.items = items
        self.active = active
        self.selector = [1] + [0]*(len(items) - 1)
        self.table = self.get_table()

    def get_table(self):
        table = Table(title=self.title, border_style="green" if self.active else "red", expand=True, show_header=False)
        if not self.title:
            table.box = None
        table.add_column(self.title, justify="center")
        for i in range(len(self.items)):
            row_style = ""
            if self.active:
                row_style = 'bold on green' if self.selector[i] == 1 else 'bold black'
            table.add_row(self.items[i], style=row_style)
        return table
    
    def get_values(self):
        if self.items:
            return self.items[self.selector.index(1)]
        return None
    
    def select(self, key):
        index = self.selector.index(1)
        if index < len(self.items) - 1 and key == b's':
            self.selector.pop()
            self.selector.insert(0, 0)
        elif index != 0 and key == b'z':
            self.selector.append(0)
            self.selector.pop(0)
        self.table = self.get_table()
    
    def update(self, data: list):
        self.items = data
        self.table = self.get_table()


class InputBox:
    def __init__(self, fields, active=False) -> None:
        self.fields = fields
        self.active = active
        self.values = [""]*len(fields)
        self.field_index = 0
        self.table = self.create_table()

    def create_table(self):
        table = Table(title="input", border_style="green" if self.active else "red", show_header=False, expand=True)
        table.add_column('Instructions')
        table.add_column('Inputs', width=20)
        for field, input_value in zip(self.fields, self.values):
            table.add_row(field, input_value, style='black on white' if self.fields.index(field) == self.field_index else None)
        return table

    def update(self, key):
        if key == b'\r':
            if self.field_index >= len(self.fields) - 1:
                self.table = None
            else:
                self.field_index += 1
        else:
            if key == b'\x08' and self.values[self.field_index]:
                self.values[self.field_index] = self.values[self.field_index][0:-1]
            else:
                try:
                    self.values[self.field_index] += key.decode("ascii")
                except UnicodeDecodeError:
                    pass #todo check key and find char
                
        if self.table:
            self.table = self.create_table()
        return self.table

    def get_table(self):
        return self.table
    
    def get_values(self):
        return self.values
    
    def toogle(self):
        self.active = False if self.active else True
        self.create_table
        self.table = self.get_table()

if __name__ == "__main__":
    pass