from typing import Union, Optional, Dict, List

import numpy as np

root_datatypes = ["bool", "Bool_t", "Byte_t", "char", "char*", "Char_t", 
                  "double", "Double32_t", "Double_t", "float",
                  "Float16_t", "Float_t", "int", "Int_t", 
                  "long", "long long", "Long_t", "Long64_t",
                  "short", "Short_t", "Size_t", "UChar_t",
                  "UInt_t", "ULong64_t", "ULong_t",
                  "unsigned", "unsigned char", "unsigned int",
                  "unsigned long", "unsigned long long",
                  "unsigned short", "UShort_t"]

uproot_datatypes = ["double", "float", "int", "int64_t", "char*", "int32_t", "uint64_t"]

def get_default_library():
    try:
        import uproot
        has_uproot = True
        from packaging import version
        uproot_version = uproot.__version__
        if version.parse(uproot_version) < version.parse("4.2.0"):
            print("WARNING: uproot version too old (<4.2.0), will switch to using ROOT instead")
            has_uproot = False
    except ImportError:
        has_uproot = False
    if has_uproot:
        return "uproot"
    return "root"

def array2root(array_data:Dict[str, np.ndarray], fname:str, tree_name:str,
               library:str="auto", multithread:bool=True):
    if library.lower() == "auto":
        library = get_default_library()
    if library == "root":
        from quickstats.interface.root.helper import RMultithreadEnv
        from quickstats.interface.cppyy.vectorize import np_type_str_maps
        with RMultithreadEnv(multithread):
            columns = list(array_data.keys())
            snapshot_templates = []
            for column in columns:
                template_type = np_type_str_maps.get(array_data[column].dtype, None)
                if template_type is None:
                    raise ValueError(f"unsupported array type \"{array_data[column].dtype}\""
                                     f" from the column \"{column}\"")
                if template_type == "bool":
                    template_type = "int"
                    array_data[column] = array_data[column].astype("int32")
                snapshot_templates.append(template_type)
            snapshot_templates = tuple(snapshot_templates)
            import ROOT
            df = ROOT.RDF.MakeNumpyDataFrame(array_data)
            df.Snapshot.__getitem__(snapshot_templates)(tree_name, fname, columns)
    elif library == "uproot":
        import uproot
        from packaging import version
        uproot_version = uproot.__version__
        if version.parse(uproot_version) < version.parse("4.2.0"):
            raise RuntimeError("uproot version too old (<4.2.0)")
        file = uproot.recreate(fname)
        file[tree_name] = array_data
        file.close()
    else:
        raise RuntimeError(f'unknown library "{library}" for root data conversion')            
        
numpy2root = array2root

def dataframe2numpy(df:"pandas.DataFrame", columns:Optional[List[str]]=None):
    if columns is not None:
        arrays = dict(zip(columns, df[columns].to_numpy().T))
    else:
        arrays = dict(zip(df.columns.values, df.to_numpy().T))
    for column in arrays:
        arrays[column] = arrays[column].astype(df[column].dtype)
    return arrays 


def dataframe2root(df:"pandas.DataFrame", fname:str, tree_name:str,
                   columns:Optional[List[str]]=None,
                   library:str="auto", multithread:bool=True):
    array_data = dataframe2numpy(df, columns)
    array2root(array_data, fname, tree_name, library=library,
               multithread=multithread)
    
def uproot_get_standard_columns(uproot_tree):
    typenames = uproot_tree.typenames()
    columns = list(typenames.keys())
    column_types = list(typenames.values())
    return np.array(columns)[np.where(np.isin(column_types, uproot_datatypes))]
    
def root2numpy(filename:Union[str, List[str]], treename:str, columns:List[str]=None,
               cut:Optional[str]=None, remove_non_standard_types:bool=True, library:str="auto"):
    if library.lower() == "auto":
        library = get_default_library()
    if library.lower() == "root":
        import ROOT
        rdf = ROOT.RDataFrame(treename, filename)
        if cut is not None:
            rdf = rdf.Filter(cut)
        if (columns is None) and (not remove_non_standard_types):
            return rdf.AsNumpy()
        else:
            from quickstats.interface.cppyy.vectorize import as_np_array
            all_columns = as_np_array(rdf.GetColumnNames())
            if columns is not None:
                columns = np.array(columns)
                missing_columns = np.setdiff1d(columns, all_columns)
                if len(missing_columns) > 0:
                    raise RuntimeError(f'missing column(s): {", ".join(missing_columns)}')
            else:
                columns = all_columns
            if remove_non_standard_types:
                column_types = np.array([rdf.GetColumnType(column) for column in columns])
                columns = columns[np.where(np.isin(column_types, root_datatypes))]
            return rdf.AsNumpy(list(columns))
    elif library.lower() == "uproot":
        import uproot
        if isinstance(filename, str):
            f = uproot.open(filename)
            t = f[treename]
            if remove_non_standard_types:
                standard_columns = uproot_get_standard_columns(t)
                if columns is None:
                    columns = standard_columns
                else:
                    columns = [column for column in columns if column in standard_columns]
            return f[treename].arrays(columns, library="numpy", cut=cut)
        else:
            # iterate over multiple files
            files = {f:treename for f in filename}
            if remove_non_standard_types:
                filter_typename = list(uproot_datatypes)
            else:
                filter_typename = None
            result = {}
            for batch in uproot.iterate(files, expressions=columns,
                                        filter_typename=filter_typename,
                                        cut=cut, library="numpy"):
                for column in batch:
                    if column not in result:
                        result[column] = batch[column]
                    else:
                        result[column] = np.concatenate([result[column], batch[column]])
            return result
    else:
        raise RuntimeError(f'unknown library "{library}" for root data conversion')
        
def root2dataframe(filename:Union[str, List[str]], treename:str, columns:List[str]=None,
                   cut:Optional[str]=None, remove_non_standard_types:bool=True, library:str="auto"):
    if library.lower() == "auto":
        library = get_default_library()
    if library.lower() == "root":
        numpy_data = root2numpy(filename, treename, columns=columns, cut=cut,
                                remove_non_standard_types=remove_non_standard_types)
        import pandas as pd
        return pd.DataFrame(numpy_data)
    elif library.lower() == "uproot":
        import uproot
        if isinstance(filename, str):
            f = uproot.open(filename)
            t = f[treename]
            if remove_non_standard_types:
                standard_columns = uproot_get_standard_columns(t)
                if columns is None:
                    columns = standard_columns
                else:
                    columns = [column for column in columns if column in standard_columns]
            return f[treename].arrays(columns, library="pandas")
        else:
            import pandas as pd
            # iterate over multiple files
            files = {f:treename for f in filename}
            if remove_non_standard_types:
                filter_typename = list(uproot_datatypes)
            else:
                filter_typename = None
            result = None
            for batch in uproot.iterate(files, expressions=columns,
                                        filter_typename=filter_typename,
                                        cut=cut, library="pandas"):
                if result is None:
                    result = batch
                else:
                    result = pd.concat([result, batch])
            return result

def root2rdataset(filename:Union[str, List[str], "quickstats.PathManager"], treename:str,
                  observable:Union[str, dict, "ROOT.RooRealVar",
                                   "quickstats.interface.root.RooRealVar"],
                  weight_name:Optional[str]=None,
                  dataset_name:str="obsData"):
    from quickstats.components.modelling import TreeDataSource
    source = TreeDataSource(treename, filename, observable, weight_name)
    dataset = source.construct_dataset(dataset_name)
    return dataset

def rdataset2numpy(dataset:"ROOT.RooDataSet"):
    from quickstats.interface.root import RooDataSet
    return RooDataSet.to_numpy(dataset)

def rdataset2dataframe(dataset:"ROOT.RooDataSet"):
    from quickstats.interface.root import RooDataSet
    return RooDataSet.to_pandas(dataset)

def rdataset2hist(dataset:"ROOT.RooDataSet"):
    pass

def root2hist(filename:Union[str, List[str]], treename:str,
              column:str, bins:int=10, range:List[float]=None, weight_column:Optional[str]=None):
    pass