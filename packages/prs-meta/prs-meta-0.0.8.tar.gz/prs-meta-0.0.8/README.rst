prs meta
========

A wrapper for pyreadstat to easily read, create, and adjust .sav files


**Documentation**: 
    https://prs-meta.rtfd.io/en/latest/prs.html


**Requirements:**
    1. `pyreadstat 1.1.6 <https://ofajardo.github.io/pyreadstat_documentation/_build/html/index.html>`_
    2. pandas
 

**Installation:**
      ``pip install prs-meta``


**Usage:**
    >>> from prs.meta import Meta
    >>> df = pd.DataFrame({'my_column': [1, 2, 3]})
    >>> m = Meta(df)
    >>> m.view()
    ==================================================
    my_column
    type: numeric (F1.0)
    measure: nominal
    label: my_column
    value labels: undefined
    missing ranges: undefined

  
**The Meta object can have the following attributes:**

    ``df``  A pandas DataFrame

    ``meta``  The original meta object from pyreadstat (if provided) 

    ``names``  A list of column names

    ``labels``  A dict of column names mapped to column labels

    ``value_labels``  A dict of column names mapped to value labels

    ``types``  A dict of column names mapped to their type in SPSS format

    ``measures``  A dict of column names mapped to their measure (nominal, ordinal, scale)

    ``missing``  A dict of column names mapped to their missing ranges


