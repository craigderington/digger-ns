from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Input, Button, DataTable
from textual.validation import ValidationResult, Validator
import re
import pydig


class DigResolver:
    def __init__(self):
        self.resolver = pydig.Resolver(
            executable='/usr/bin/dig',
            nameservers=['1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4'],
            additional_args=['+timeout=10', '+short']
        )
        self.record_types = ['A', 'NS', 'CNAME', 'SOA', 'PTR', 'MX', 'TXT',
                             'AAAA', 'DS', 'DNSKEY', 'CDS', 'CDNSKEY', 'CAA']

    def query(self, address: str, record_type: str) -> list:
        try:
            result = self.resolver.query(address, record_type)
            return result if result else []
        except Exception as e:
            print(f"Query error: {e}")
            return []

class DomainOrIPValidator(Validator):
    DOMAIN_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    IP_PATTERN = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    def validate(self, value: str) -> ValidationResult:
        if re.match(self.DOMAIN_PATTERN, value) or re.match(self.IP_PATTERN, value):
            return self.success()
        return self.failure("Invalid domain or IP address")

class MXToolsApp(App):
    CSS_PATH = "../assets/css/buttons.tcss"
    BINDINGS = [("q", "quit", "Quit"), ("?", "help", "Help")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Trtck current sort state
        self._sort_col = None
        self._sort_reverse = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter a domain name or IP address.")
        yield Input(id="input", validators=[DomainOrIPValidator()])
        yield Button("Search", id="search")
        self.results_table = DataTable(zebra_stripes=True)
        # columns keys so we can sort by them
        self.results_table.add_column("Record Type", key="type")
        self.results_table.add_column("Value", key="value")
        yield self.results_table
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#input").focus()
        self.title = "DiggerNS"
        self.sub_title  = "Query the DNS Network by IP or domain name.  Powered by PyDIG"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            address = self.query_one("#input", Input).value.strip()
            if address:
                self.run_query(address)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        address = event.value.strip()
        if address:
            self.run_query(address)

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        col = event.column_key
        if col is None:
            return
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        self.results_table.sort(col, reverse=self._sort_reverse)

    def run_query(self, address: str) -> None:
        try:
            self.results_table.clear()  
        except TypeError:
            pass

        self.results_table.add_row("Status", f"Querying {address}...")
        resolver = DigResolver()
        results = {rt: resolver.query(address, rt) for rt in resolver.record_types}

        try:
            self.results_table.clear()
        except TypeError:
            pass

        any_data = any(results.values())
        if not any_data:
            self.results_table.add_row("Status", f"No records found for {address}")
            return

        for record_type, data in results.items():
            if data:
                for item in data:
                    self.results_table.add_row("type", "value")
        
        try:
            self.results_table.clear()
        except TypeError:
            pass
        for record_type, data in results.items():
            if data:
                for item in data:
                    self.results_table.add_row(record_type, str(item))
            else:
                self.results_table.add_row(record_type, "No records")

        self._sort_col, self._sort_reverse = "type", False
        self.results_table.sort("type", reverse=False)


if __name__ == "__main__":
    app = MXToolsApp()
    app.run()
