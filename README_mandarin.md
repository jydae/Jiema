## Jiema Decoder

一个用 Python 编写的多编码解码器，旨在以 CSV 格式高效报告。<br>
支持二进制、摩尔斯、十六进制、Base64、Base32、URL 编码和 Unicode 转义。

<br>
<p align="center"><img src='img.png' align="top" height="170px"></p>

### 使用方法
---

1. **运行脚本**
```bash
python3 jiema_decoder.py
```
要运行脚本，请导航到脚本所在的目录并执行该命令。

2. **输入字符串**
```bash
:
```
当提示时，输入您想要解码的字符串。脚本将识别编码格式并显示解码结果。


```bash
:T2gsIG1vb2R5IGJsdWUuCg==

[02:48:30] [BASE64] [T2gsIG1vb2R5IGJsdWUuCg==] 解码: Oh, moody blue.
```

3. **特殊命令**
   - 输入 `csv` 将结果保存为 CSV 文件。
   - 输入 `txt` 将结果保存为文本文件。
   - 输入 `file` 从指定文件中解码字符串。
<br>
<br>

4. **文件解码**

如果您选择从文件中解码，系统会提示您输入文件的名称或路径（例如，`encodings.txt`）。
脚本将读取文件中的每一行并尝试分别解码它们。

### 依赖

```
pip install colorama
```

