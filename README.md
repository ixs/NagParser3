# NagParser

## Functionality
NagParser is a Python library for parsing Nagios runtime data from ``status.dat`` and
``objects.cache`` files and presenting it as easy-to-use Python objects. It enables you to
build custom monitoring dashboards, reporting tools, and automation scripts that integrate
with your Nagios infrastructure.

## History
NagParser was originally a small subset of a larger project and was written to parse Nagios status data for integration
into a real-time Operations Dashboard. While the dashboard itself is proprietary, this parser has been extracted and
released for the Nagios community to use in your own projects.

Although some rough edges remain as it is refactored into a standalone project, the core code is stable and is executed
hundreds of thousands of times per week in a large-scale Nagios environment.

**This code is provided under GPLv3 (see `LICENSE.txt`).**

If you make improvements, please consider contributing them back via a pull request.  
For questions, see `AUTHORS.txt` for contact information.

---

## Installation

### Production Use
_No external dependencies - relies only on Python's standard library:_

```bash
pip install NagParser
```

### Development
_Includes testing tools:_

```bash
pip install -e ".[dev]"
```

---

## Documentation

Current documentation can be found at:  
<https://ixs.github.io/NagParser3/>

