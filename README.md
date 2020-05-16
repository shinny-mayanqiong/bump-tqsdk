# bump-tqsdk


## 安装 tqsdkbump 工具到系统

```
cd 当前目录
python setup.py build
python setup.py install
```

## 发布版本之前

```
cd path_to_tqsdk_python
tqsdkbump --tag=x.x.x  # 自动修改版本号，需要手动修改 changelog，然后 提交
```
