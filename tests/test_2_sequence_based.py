import numpy as np
import pytest

from kipoi_dataloaders.datasets.sequence import SeqStringDataset, SeqDataset, parse_dtype

data_bpath = "tests/data/"

min_set_props = ["output_schema", "type", "defined_as", "info", "args", "dependencies", "postprocessing",
                 "_yaml_path", "source", "source_dir"]


def test_min_props():
    for Dl in [SeqStringDataset, SeqDataset]:
        props = dir(Dl)
        assert all([el in props for el in min_set_props])

        # TODO - check that all arguments are descript in Dl.args_prototype


def test_parse_dtype():
    dtypes = {'int': int, 'string': str, 'float': float, 'bool': bool}
    assert all([parse_dtype(dt) == dtypes[dt] for dt in dtypes.keys()])
    assert all([parse_dtype(dt) == dt for dt in dtypes.values()])
    with pytest.raises(Exception):
        parse_dtype("int8")
    assert parse_dtype(None) is None


def test_fasta_based_dataset():
    # just test the functionality
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta")
    ret_val = dl[0]
    assert isinstance(ret_val["inputs"], np.ndarray)
    assert ret_val["inputs"].shape == (1,)
    # test with set wrong seqlen:
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta", required_seq_len=3)
    with pytest.raises(Exception):
        dl[0]
    # test with short max_seqlen:
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta", max_seq_len=1)
    with pytest.raises(Exception):
        dl[0]
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta", label_dtype="string")
    ret_val = dl[0]
    assert isinstance(ret_val['targets'][0], np.str_)
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta", label_dtype="int")
    ret_val = dl[0]
    assert isinstance(ret_val['targets'][0], np.int_)
    dl = SeqStringDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta", label_dtype="bool")
    ret_val = dl[0]
    assert isinstance(ret_val['targets'][0], np.bool_)


def test_seq_dataset():
    dl = SeqDataset(data_bpath + "sample_intervals.bed", data_bpath + "sample.fasta")
    ret_val = dl[0]
    assert isinstance(ret_val["inputs"], np.ndarray)
    assert ret_val["inputs"].shape == (2, 4)
