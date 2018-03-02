# TRANSLATE SPECIES

translate species name into Chinese


## Data

> The most comprehensive species name (Binomial nomenclature) to Chinese translation mapping table

> 全世界最全的拉丁物种>>中文名对照表

## clean data

**download link**:
[tsv格式下载](https://github.com/yech1990/translate_species/blob/master/data/all.species.tsv?raw=true)

### data source

- http://www.zoology.csdb.cn/
- https://species.wikimedia.org
- ...

## Command Line Usage

- translate a list of species name (Fault-tolerant)

```bash
# put your species names in file, one name in one line
./query_all.py ./test/test.input.list
```


## TODO

- [ ] single name string as command line input
