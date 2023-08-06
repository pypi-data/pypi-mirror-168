"""
|  Wrapper for pyreadstat to easily read, create and adjust .sav files.
|  
|  **Requirements:**
|       `pyreadstat 1.1.6 <https://ofajardo.github.io/pyreadstat_documentation/_build/html/index.html>`_
|       pandas
|  
|  **Installation:**
|       ``pip install prs-meta``
|
|  **Usage:**
|       ``from prs.meta import Meta``
|
|  The Meta object has the following attributes:
|    ``df``: pandas DataFrame  
|    ``meta``: original meta object from pyreadstat (if provided)
|    ``names``: list of column names
|    ``labels``: dict of column names mapped to column labels
|    ``value_labels``: dict of column names mapped to value labels
|    ``types``: dict of column names mapped to their type in SPSS format
|    ``measures``: dict of column names mapped to their measure (nominal, ordinal, scale)
|    ``missing``: dict of column names mapped to their missing ranges
"""


import pyreadstat as prs
import pandas as pd
import os


class Meta:
    """
    Wrapper for pyreadstat to easily read, create and adjust .sav files.

    :param path: path to an SPSS file. The DataFrame and meta data object will be constructed from this file, if provided.
    :type path: str, optional
    :param df: pandas DataFrame. The DataFrame will be used to construct the meta data, if only a DataFrame is provided
    :type df: DataFrame, optional
    :param meta: pyreadstat meta data object from SPSS file
    :type meta: object, optional
    :example (from path):
        >>> m = Meta("path_to_file.sav")
        >>> print(m.names)
        ['list', 'of', 'column', 'names']

    :example (df only):
        >>> df = pd.DataFrame({'col1': [1,2,3], 'col2': ['hi','hi','hi']})
        >>> m = Meta(df)
        >>> print(m.types['col2'])
        A2

    :example (df + meta):
        >>> m = Meta(df, meta)
        >>> print(m.names)
        ['list', 'of', 'column', 'names']

    """
    def __init__(self, *args):
        self.args = args
        self._build()

    
    def _build(self):
        """
        Builds class instance from file, DataFrame, or both a DataFrame and meta data object
        """
        if len(self.args) == 1:
            if isinstance(self.args[0], pd.DataFrame) and not self.args[0].empty:
                self._from_df()
            if isinstance(self.args[0], str):
                self._from_file()
        elif len(self.args) == 2:
            if isinstance(self.args[0], pd.DataFrame) and isinstance(self.args[1], object):
                self._from_df()
        else:
            raise ValueError("cannot load or build object from given parameters")


    def _from_file(self):
        if not os.path.exists(str(self.args[0])):
            raise IOError(f"'{str(self.args[0])}' does not exist.")
        # Read from file:
        try:
            self.df, self.meta = prs.read_sav(str(self.args[0]))
            self._get()
        except Exception as e:
            raise FileNotFoundError(f"unable to readfile: {e}")

    
    def _from_df(self):
        # Read from dataframe
        if isinstance(self.args[0], pd.DataFrame) and not self.args[0].empty and len(self.args) == 1:
            self.df = self.args[0]
            self._set()
        # Read from dataframe + meta data
        elif isinstance(self.args[0], pd.DataFrame) and not self.args[0].empty and len(self.args) == 2:
            self.df = self.args[0]
            self.meta = self.args[1]
            self._get()

    
    def _get(self):
        """ 
        Get meta data from class parameter
        """
        self.names = self.meta.column_names
        self.labels = self.meta.column_names_to_labels
        self.value_labels = self.meta.variable_value_labels
        self.types = self._fix_empty_cols(self.meta.original_variable_types, self.value_labels)
        self.measures = self.meta.variable_measure
        self.missing = self.meta.missing_ranges


    def _set(self): 
        """
        Build meta data from DataFrame
        """ 
        self.names = []
        self.labels = {}
        self.value_labels = {}
        self.types = {}
        self.measures = {}
        self.missing = {}
        for col in self.df.columns:
            self.new(col)


    def _check_col(self, col_name: str):
        """
        Checks input type of col_name and whether the column exists
        :param col_name: column name
        """
        if not isinstance(col_name, str):
            raise TypeError(f"parameter 'col_name' should be a string, but the given object is of type {type(col_name)}")
        if not col_name in self.df.columns:
            raise KeyError(f"'{col_name}' does not exist in DataFrame")
        if col_name not in self.names:
            self.names.append(col_name)


    def _fix_empty_cols(self, original_variable_types: dict[str,str], variable_value_labels: dict, default='F1.0') -> list:
        """
        Patching an issue where empty columns of undefined type may result in an error when writing to file

        :param original_variable_types: variable types as defined by pyreadstat
        :param variable_value_labels: variable value labels as defined by pyreadstat
        :param default: datatype of empty columns, default = 'F1.0' (integer)
        :type default: str, optional
        """
        empty_cols = [col for col in self.names if self.df[col].isnull().all()]
        for col in empty_cols:
            if variable_value_labels[col] == {}:
                original_variable_types[col] = default
        return original_variable_types


    def add_column_label(self, col_name: str, col_label: str) -> None:
        """
        Adds column names to meta data

        :param col_name: column name
        :param col_label: column label
        :example:
            >>> m.add_column_label("my_column", "This is my column")
            >>> print(m.labels["my_column"])
            This is my column

        """
        self._check_col(col_name)
        if not isinstance(col_label, str):
            raise TypeError("col_label (param 2) should be a string")
        self.labels[col_name] = col_label


    def add_value_labels(self, col_name: str, val_label: dict[int, str]) -> None:
        """
        Adds a column's value labels to meta data

        :param col_name: column name
        :param val_label: values mapped to labels
        :example:
            >>> labels = {0: 'Not selected', 1: 'Selected'}
            >>> m.add_value_labels('my_column', labels)
            >>> print(m.value_labels['my_column'])
            {0: 'Not selected', 1: 'Selected'}

        """
        self._check_col(col_name)
        if not isinstance(val_label, dict):
            raise TypeError("val_lables (param 2) should be a dict")
        self.value_labels[col_name] = val_label


    def add_type(self, col_name: str, col_type: str='int', decimals: int=0) -> None:
        """
        Adds a column's type to meta data

        :param col_name: column name
        :param col_type: any of *str*, *int*, *float*. default = *int*
        :type col_type: str, optional
        :param decimals: the number of decimals that numeric values should display, default = 0
        :type decimals: int, optional
        :example:
            >>> m.df['my_column'] = [12.3311, 15.2224, 9.8832]          
            >>> m.add_type('my_column', 'float', decimals=3)
            >>> print(m.types['my_column'])
            F6.3

        """
        self._check_col(col_name)
        if not isinstance(col_type, str):
            raise TypeError("col_type should be defined as a string - e.g.: 'int'")
        if not isinstance(decimals, int):
            raise TypeError("decimals (param 3) should be an integer")

        max_width = max([len(a) for a in self.df[col_name].astype('str')])
        pref = max([len(str(c).split('.')[0]) for c in self.df[col_name]])

        if col_type == 'str':
            self.types[col_name] = f'A{max_width}'

        elif col_type == 'int':
            if self.df[col_name].dtype == 'object':
                self.types[col_name] = f'A{pref}'
            else:
                self.types[col_name] = f'F{pref}.0'

        elif col_type == 'float':
            if self._should_be_int(self.df[col_name]):
                self.types[col_name] = f'F{pref}.0'
                return
            dec = max([len(str(c).split('.')[-1]) for c in self.df[col_name]])
            if decimals == 0:
                self.types[col_name] = f'F{pref}.{dec}'
            else:

                if max_width <= decimals:
                    raise ValueError(f"'decimals' ({decimals}) cannot be larger than width ({max_width})")
                self.types[col_name] = f'F{pref}.{decimals}'
        else:
            raise ValueError(f"{col_type} is not a valid argument. Use any of 'str', 'int', 'float'")


    @staticmethod
    def _should_be_int(column: pd.Series) -> bool:
        """
        Checks if a column of floats should be integers
        :param column: target column
        """
        if all([str(c).split('.')[-1] == "0" for c in column]):
            return True
        return False


    def add_measure(self, col_name: str, measure: str) -> None:
        """
        Adds the 'measure' of a column to meta data

        :param col_name: column name
        :param measure: any of *nominal*, *ordinal*, *scale*
        :example:
            >>> m.add_measure('my_column', 'nominal')
            >>> print(m.measures['my_column'])
            nominal

        """
        self._check_col(col_name)
        if not isinstance(measure, str):
            raise TypeError("measures (param 2) should be a string")
        if measure.lower() in ["nominal", "ordinal", "scale"]:
            self.measures[col_name] = measure
        else:
            raise ValueError(f"'{measure}' is not a valid argument, use any of 'nominal', 'ordinal', 'scale'")


    def new(self, col_name: str, col_type: str='int') -> None:
        """ 
        Add a new column to the meta data
        
        :param col_name: column name
        :param col_type: any of *int*, *str*, *float*. default = *int*
        :type col_type: str, optional
        :example:
            >>> m.new('my_column')
            >>> m.types['my_column']
            F1.0
            >>> m.measures['my_column']
            nominal

        """
        self._check_col(col_name)   
        t = self.df[col_name].dtype
        self.add_column_label(col_name, col_name)
        if col_type == 'str' or self.df[col_name].dtype == 'object':
            self.add_type(col_name, 'str')
            self.add_measure(col_name, 'nominal')
        elif col_type == 'int' and str(self.df[col_name].dtype).startswith('int'):  
            self.add_type(col_name, 'int')
            if self.df[col_name].max() > 50:
                self.add_measure(col_name, 'scale')
            else:
                self.add_measure(col_name, 'nominal')
        elif col_type == 'float' or str(self.df[col_name].dtype).startswith('float'):
            self.add_type(col_name, 'float')
            self.add_measure(col_name, 'scale')


    def view(self, col_name: str=None):
        """
        |  Prints meta data for given column.
        |  Will print meta data for all columns in df if none are specified
        
        :param col_name: column name
        :type col_name: str, optional
        :example:
            >>> m.df['my_column] = [1,2,3]
            >>> m.new('my_column')
            >>> m.view('my_column')
            my_column
            type: numeric (F1.0)
            measure: nominal
            label: my_column
            value labels: undefined
            missing ranges: undefined

        """
        if col_name:
            self._print(col_name)
        else:
            x = self.names
            if len(x)>100:
                x = x[:100]
            for col in x:
                print(50*'=')
                self._print(col)


    def _print(self, col_name):
        self._check_col(col_name)
        print(col_name)
        if not col_name in list(self.types.keys()):
            print('type: undefined')
        elif self.types[col_name].startswith('F'):
            print(f'type: numeric ({self.types[col_name]})')
        elif self.types[col_name].startswith('A'):
            print(f'type: string ({self.types[col_name]})')

        if not col_name in list(self.measures.keys()):
            print('measure: undefined')
        else:
            print(f'measure: {self.measures[col_name]}')

        if not col_name in list(self.labels.keys()):
            print('label: undefined')
        else:
            print(f'label: {self.labels[col_name]}')

        if not col_name in list(self.value_labels.keys()):
            print('value labels: undefined')
        else:
            print(f'value labels: {self.value_labels[col_name]}')

        if not col_name in list(self.missing.keys()):
            print('missing ranges: undefined')
        else:
            print(f'missing ranges: {self.missing[col_name]}')


    def purge(self, col_name: str, target='meta') -> None:
        """ 
        Deletes a column's meta data

        :param col_name: column name
        :param target: will also delete column from df if target == 'all'
        :type target: str, optional
        :example:
            >>> m.purge('my_column')
            >>> m.view('my_column')
            my_column
            type: undefined
            measure: undefined
            label: undefined
            value labels: undefined
            missing ranges: undefined            
            
        """
        if col_name in self.names:
            self.names.remove(col_name)
        if col_name in list(self.types.keys()):
            del self.types[col_name]
        if col_name in list(self.measures.keys()):
            del self.measures[col_name]
        if col_name in list(self.missing.keys()):
            del self.missing[col_name]
        if col_name in list(self.value_labels.keys()):
            del self.value_labels[col_name]
        if col_name in list(self.labels.keys()):
            del self.labels[col_name]
        if target == 'all':
            self.df.drop(col_name, axis='columns', inplace=True)


    def write_to_file(self, filename: str="output.sav", with_open=False) -> None:
        """
        Writes the DataFrame and meta data to an SPSS file

        :param filename: name of the new file
        :type filename: str, optional
        :param with_open: if set to True, will open the SPSS file after writing (Windows only)
        :type with_open: bool, optional

        """
        if not isinstance(filename, str):
            raise TypeError("filename (param 1) should be a string")
        if not filename.endswith('.sav'):
            filename = filename + '.sav'
        if os.path.exists(filename):
                raise IOError(f"'{filename}' already exists.")
        try:
            prs.write_sav(self.df, 
                        filename, 
                        column_labels=self.labels,
                        variable_value_labels=self.value_labels,
                        missing_ranges=self.missing,
                        variable_measure=self.measures,
                        variable_format=self.types
                        )
            if with_open == True:
                try:
                    os.startfile(filename)
                except:
                    raise KeyError(f"cannot open {filename}")

        except Exception as e:
           print(f'unable to write to file: {e}')
        
