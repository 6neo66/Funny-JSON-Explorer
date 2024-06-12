# Funny-JSON-Explorer
简称为FJE，是一个按照工厂方法、抽象工厂、建造者模式、组合模式的要求使用Python编写的用于可视化JSON文件的命令行界面小工具。

## 领域模型
![image]([Funny JSON Explorer 领域模型.png](https://github.com/6neo66/Funny-JSON-Explorer/blob/main/Funny%20JSON%20Explorer%20%E9%A2%86%E5%9F%9F%E6%A8%A1%E5%9E%8B.png))

## 命令格式
```shell
fje -f <json file> -s <style> -i <icon family>
```
其中json file指定要读取的JSON文件，style指定可视化风格，icon family指定节点图标族。

## 示例
对于项目根目录下的JSON文件example.json：
```json
{
    "oranges": {
        "mandarin": {
            "clementine": null,
            "tangerine": "cheap & juicy!"
        }
    },
    "apples": {
        "gala": null
    }
}
```
若执行命令：
```shell
fje -f example.json -s tree
```
将产生输出：
```
├─ oranges
│  └─ mandarin
│     ├─ clementine
│     └─ tangerine: cheap & juicy!
└─ apples
   └─ gala
```
若执行命令：
```shell
fje -f example.json -s rectangle
```
将产生输出：
```
┌─ oranges ───────────────────────────────┐
│  ├─ mandarin ───────────────────────────┤
│  │  ├─ clementine ──────────────────────┤
│  │  ├─ tangerine: cheap & juicy! ───────┤
├─ apples ────────────────────────────────┤
└──┴─gala ────────────────────────────────┘
```
对于为分支节点指定图标♢、为叶子节点指定图标♤的节点图标族poker-face-icon-family，若执行命令：
若执行命令：
```shell
fje -f example.json -s tree -i poker-face-icon-family
```
将产生输出：
```
├─♢oranges                                 
│  └─♢mandarin                             
│     ├─♤clementine                        
│     └─♤tangerine: cheap & juicy!    
└─♢apples                                  
   └─♤gala
```

## 参考资料
1. unicode制表符与图标：https://unicode.yunser.com/
