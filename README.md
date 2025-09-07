
# DiggerNS

## Overview

![DiggerNS](https://raw.githubusercontent.com/craigderington/digger-ns/1c655a93521e4b9e8d8455dc9080000029aa8796/assets/images/digger-ns.svg)

The MX Tools Application is a sophisticated Textual User Interface (TUI) built with Python, designed to query the DNS network for various record types using the DIG command. This application leverages the power of the Textual framework to provide an interactive, terminal-based experience for users to input domain names or IP addresses and retrieve detailed DNS information. It supports querying multiple DNS record types such as A, NS, CNAME, SOA, PTR, MX, TXT, AAAA, DS, DNSKEY, CDS, CDNSKEY, and CAA.

The application is built for ease of use, featuring input validation for domains and IPs, a search button to initiate queries, and a display area for results. It is ideal for network administrators, developers, and anyone needing quick DNS lookups without leaving the terminal.

## Features

- **User-Friendly Interface**: Powered by Textual, offering a modern TUI with keyboard bindings (e.g., 'q' to quit, '?' for help), headers, footers, and interactive widgets like Input fields and Buttons.
- **DNS Querying**: Utilizes the pydig library to perform DIG-like queries across multiple DNS servers (1.1.1.1, 1.0.0.1, 8.8.8.8, 8.8.4.4) with a 10-second timeout.
- **Record Types Supported**: Automatically queries and retrieves results for A, NS, CNAME, SOA, PTR, MX, TXT, AAAA, DS, DNSKEY, CDS, CDNSKEY, and CAA records.
- **Input Validation**: Validates entered domains or IPs using regular expressions, providing visual feedback (e.g., color changes in the Input field) based on boolean validation results.
- **Asynchronous Operations**: Handles DNS queries asynchronously to prevent UI freezing, ensuring a responsive experience.
- **Results Display**: Outputs query results in a RichLog widget, formatting each record type with its corresponding data or "No records" if empty.
- **Customizable Bindings**: Includes bindings for quitting, help, and potential future expansions like delete or scroll actions.
- **Error Handling**: Gracefully manages invalid inputs and query failures, displaying appropriate messages in the results log.

## Installation

To install and run the MX Tools Application, follow these steps:

1. **Prerequisites**:
   - Python 3.12 or higher.
   - Ensure you have `pip` installed for dependency management.

2. **Install Dependencies**:
   - Install Textual: `pip install textual`
   - Install pydig: `pip install pydig`

3. **Clone or Download the Code**:
   - Download the `app.py` file provided in this project.

4. **Run the Application**:
   - Execute `python app.py` in your terminal.
   - The application will launch in your terminal window, displaying the header, input field, search button, and results area.

Note: The application assumes the DIG executable is available at `/usr/bin/dig`. If your system path differs, modify the `executable` path in the `DigResolver` class accordingly.

## Usage

1. **Launch the App**: Run `python app.py`.
2. **Enter Input**: Type a valid domain name (e.g., `example.com`) or IP address (e.g., `192.168.1.1`) into the Input field. The field will provide visual feedback: red for invalid, blue/green for valid (depending on Textual's default styling).
3. **Validate Input**: The validation uses regex patterns:
   - Domain: Matches standard domain formats like `sub.domain.com`.
   - IP: Matches IPv4 formats like `xxx.xxx.xxx.xxx`.
   - If invalid, the app displays an error in the results log.
4. **Search**: Press the "Search" button or hit Enter to query.
5. **View Results**: Results appear in the RichLog widget below, listed by record type (e.g., A_REC: ['93.184.216.34']).
6. **Keyboard Shortcuts**:
   - `q`: Quit the application.
   - `?`: Show help screen.
   - Additional bindings like `delete` or `j` (down) can be implemented for enhanced navigation.
7. **Exit**: Use the quit binding or close the terminal.

For advanced usage, extend the `record_types` list in `DigResolver` to include more DNS types.

## Dependencies and Credits

This application relies on two key Python libraries:

- **Textual**: A rapid application development framework for creating sophisticated Textual User Interfaces (TUIs) in Python. Textual is developed by Textualize (textualize.io), with primary authorship credited to Will McGugan. It enables the interactive widgets, event handling, and styling used in this app. Textual is licensed under the MIT License. For more details, visit [Textualize Documentation](https://textual.textualize.io/).
  
- **pydig**: A Python library that provides a wrapper for the DIG command-line tool, allowing programmatic DNS queries. pydig is authored and maintained by Shumon Huque (shuque@gmail.com). It was created to perform DNS queries and explore features of the DNS protocol, modeled after ISC BIND's dig tool. pydig supports advanced DNS features like EDNS client subnet, DNS over TLS, and more. It is licensed under the GNU General Public License (GPL). For more information, see the [pydig GitHub Repository](https://github.com/shuque/pydig).

Other standard libraries used include `re` for regex validation, `asyncio` for asynchronous operations, and Textual's built-in widgets.

## Development and Customization

- **Code Structure**:
  - `DigResolver`: Utility class for resolving DNS queries using pydig.
  - `MXToolsApp`: Main App class extending Textual's App, handling composition, events, and bindings.
  - `validate_address`: Function for input validation, returning a ValidationResult for enhanced feedback.
  
- **Extending the App**:
  - Add more record types by updating the `record_types` list.
  - Implement additional bindings (e.g., `action_delete` to clear input).
  - Customize CSS by modifying `assets/css/buttons.tcss` for button styles.
  
- **Troubleshooting**:
  - If validation fails: Ensure the regex patterns match your needs; the boolean return style integrates with Textual's color feedback.
  - DNS Query Issues: Check network connectivity or adjust nameservers in `DigResolver`.
  - UI Freezing: The async `run_query` should prevent this; verify your Python version supports asyncio.

## Contributing

Contributions are welcome! Fork the repository, make changes, and submit a pull request. Focus on improving validation, adding features like export to file, or enhancing error handling.

## License

This MX Tools Application is open-source and released under the MIT License. However, it incorporates libraries with their own licenses:
- Textual: MIT License.
- pydig: GNU General Public License (GPL).

Please respect the licenses of the dependencies when distributing or modifying this application.

## Acknowledgments

Special thanks to Will McGugan and the Textualize team for the Textual framework, and to Shumon Huque for the pydig library, which made this application possible. This project is for educational and practical purposes in DNS querying.