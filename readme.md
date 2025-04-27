> 2025/4/27 09:51:37

介绍：通过包装pytest的@pytest.mark.parametrize实现的leetcode刷题debug环境

| 阶段                   | 关键动作                                       |
| ---------------------- | ---------------------------------------------- |
| 1. 启动 Initialization | 初始化内部插件，解析命令行参数                 |
| 2. 收集 Collecting     | 递归扫描符合规则的文件、类、函数，生成测试节点 |
| 3. 配置准备 Setup      | fixture准备、资源分配                          |
| 4. 执行 Running        | 按顺序逐个执行测试函数                         |
| 5. 收尾 Teardown       | 资源释放，输出测试报告                         |

在第3阶段中，会执行参数化（如果用了 `@pytest.mark.parametrize`），我们通过自定义注解简化了测试数据的输入，只需要如下：

```
imoport base
@base.ag_test(cases=[(1, 2)], expected=[4])
def solve1(a, b):
    return a + b
```

##### 关于注解什么时候被解析

1.Python解释器执行到 `def func(): ...` 这行时，首先**创建**一个函数对象 `func`

2.发现这个 `func` 上面有一个 `@decorator`

3.**立即调用** `decorator(func)`

4.`decorator(func)` 返回一个**新的可调用对象**（可以是函数、类、包装器等等）

5.**把新的对象赋值给 `func`**，原来的 `func` 被覆盖掉了！

##### 问题点

* 通过inspect判断包装的是函数/类
* 通过`func.__qualname__`判断是模块函数还是类函数
* 通过`func.__code__.co_varnames`获取包装函数的参数名称
* 通过`--tb=line`简化输出
* 通过`--disable-warnings`忽略警告

##### 解决每次创建新文件，调试leetcode上复制下来的代码不能直接运行，还要先导入本地的包

Builtin与global。builtin是python内置作用域，global是当前模块的全局变量。通过在启动时添加base模块中的函数变量添加到内置作用域，运行结束在移除进行管理

##### 使用builtin管理时pycharm标红

`# noinspection PyUnresolvedReferences`标红行，上一行添加

✅ 所以如果你想**只对当前项目关掉** `Unresolved Reference`，正确做法是：

1. `File → Settings → Editor → Inspections`
2. 右上角找到 `Profile` （下拉）
3. 点 ➕，新建一个 `MyProjectProfile`
4. 在 `MyProjectProfile`里把`Unresolved References`取消勾选
5. 应用
6. 绑定到当前项目

✅ 这样其他项目不受影响，只有当前项目不会检查未解析引用！

打开其他项目可以检查一下是否使用的默认