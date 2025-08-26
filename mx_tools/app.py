from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, RichLog, Label
from textual.validation import Function, ValidationResult
from textual.binding import Binding
import pydig
import re
import asyncio

class DigResolver:
    def __init__(self):
        self.resolver = pydig.Resolver(
            executable="/usr/bin/dig",
            nameservers=["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4"],
            additional_args=["+time=10"]
        )

    async def run_query(self, domain):
        if not domain:
            return None
        record_types = ["A", "NS", "CNAME", "SOA", "PTR", "MX", "TXT", "AAAA", "DS", "DNSKEY", "CDS", "CDNSKEY", "CAA"]
        query_result = []
        for record_type in record_types:
            try:
                res = await asyncio.get_event_loop().run_in_executor(None, lambda: self.resolver.query(domain, record_type))
                query_result.append(res)
            except Exception:
                query_result.append([])
        return query_result, domain

    def results(self, query_result):
        if not query_result:
            return {}
        keys = ["a_rec", "ns_rec", "cn_rec", "soa_rec", "ptr_rec", "mx_rec", "txt_rec", "aaaa_rec", "ds_rec", "dnskey_rec", "cds_rec", "cdnskey_rec", "caa_rec"]
        return {key: res for key, res in zip(keys, query_result) if res}

class MXToolsApp(App):
    CSS_PATH = "../assets/css/buttons.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="question_mark", action="help", description="Show help screen", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter a domain name or IP.")
        yield Input(type="text", validators=[Function(validate_address, "Invalid domain or IP")])
        yield Button(label="Search", variant="primary", tooltip="Click search to run query")
        yield RichLog(id="results")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one(Input)
        value = input_widget.value
        if not validate_address(value):
            self.query_one("#results", RichLog).write("Invalid input. Please enter a valid domain or IP.")
            return
        dig = DigResolver()
        dig_query = await dig.run_query(value)
        domain = dig_query[1]
        dig_results = dig.results(dig_query[0])
        results_log = self.query_one("#results", RichLog)
        results_log.clear()
        for key, value in dig_results.items():
            results_log.write(f"{key.upper()}: {value or 'No records'}")
        input_widget.value = f"{domain}"

    def on_mount(self) -> None:
        self.title = "MX Tools Application"
        self.sub_title = "Query the DNS Network by Domain or IP."

def validate_address(address):
    domain_pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(domain_pattern, address) or re.match(ip_pattern, address))


if __name__ == "__main__":
    app = MXToolsApp()
    app.run()