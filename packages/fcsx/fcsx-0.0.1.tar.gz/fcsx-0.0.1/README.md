# FCSX: FCS for Humans

FCSX is 

* a very simple but fully featured Flow Cytometry Standard (FCS) reader for Python.
* written in Python Standard Library

FCSX supports to

* parse FCS 2.0, 3.0, and 3.1 versions
* create NumPy memory-mapped array for the DATA segment via installing NumPy




## Installation

```bash
pip install fcsx
```

To support NumPy memory mapping (usually faster), please install the extra dependencies as

```bash
pip install fcsx[numpy]
```



## Quick Start

```python
import fcs

f = fcs.read('./FR-FCM-ZZPH/Samusik_all.fcs')
```



## Contributing



## License

FCSX has an BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/fcsx/blob/main/LICENSE) file.