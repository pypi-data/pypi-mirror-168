# metadownload
此脚本为下载NCBI中biosample相关字段信息的python脚本


## Installation
```
pip3 install metadownload
```

## Dependency
- [E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK179288/)

**you should add E-utilities in your PATH**

E-utilities install:

```
sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"

sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
```

## Usage

```
usage: download_biosample.py -list <biosample_acc_list> -outdir <output>

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

optional arguments:
  -h, --help      show this help message and exit
  -list LIST      <file>: biosample_acc_list, one accession per line
  -outdir OUTDIR  <path>: output directory name
  -v, --version   Display version
```

## Output

You will get text file contains metainfo for each biosample accession named with the accession number and a csv format summary file
