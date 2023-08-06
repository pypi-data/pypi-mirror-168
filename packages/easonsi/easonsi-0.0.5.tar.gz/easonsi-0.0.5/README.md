# 个人 package 尝试

## 打包上传

```sh
# 打包所需.
python3 -m pip install --upgrade pip build twine
```

记得每次需要上传不同名字的包, 因此需要修改版本号; `dist` 中的旧版本如果服务器上已有将不会上传到 pypi.

```sh
# Generating distribution archives
python3 -m build
# Uploading the distribution archives
python3 -m twine upload --repository pypi dist/*
```

安装

```sh
pip install dist/easonshi[version]
pip install -U easonsi -i https://pypi.python.org/simple
```
