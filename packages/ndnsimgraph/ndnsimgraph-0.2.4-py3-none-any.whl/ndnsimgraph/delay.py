from enum import Enum
from typing import Optional, List
from .common import GraphBase, NodeItem, ExportItem, ExportBase
import numpy as np
import pandas as pd


class DelayType(Enum):
    """
    延迟类型
    https://ndnsim.net/current/metric.html
    """
    # LastDelay means that DelayS and DelayUS represent delay between last Interest sent and Data packet received
    # LastDelay意味着DelayS和DelayUS代表最后发送的兴趣和接收的数据包之间的延迟
    LastDelay = 0
    # FullDelay means that DelayS and DelayUS represent delay between first Interest sent and Data packet received
    # (i.e., includes time of Interest retransmissions)
    # FullDelay是指DelayS和DelayUS代表发送的第一个感兴趣的数据包和接收的数据包之间的延迟
    FullDelay = 1


class DelayTarget(Enum):
    """
    延迟目标
    """
    DelayS = 0  # 按秒统计的延迟
    DelayMS = 1  # 按毫秒统计的延迟
    DelayUS = 2  # 按微秒统计的延迟

    @staticmethod
    def getUnit(delayTargetName: str) -> str:
        value = DelayTarget[delayTargetName].value
        if value == 0:
            return "Second"
        elif value == 1:
            return "Millisecond"
        elif value == 3:
            return "Microsecond"
        else:
            return "unknown"


class DelayItem:
    """
    一个用于描述 ndnsim 延迟采样结果的类
    https://ndnsim.net/current/metric.html#application-level-trace-helper
    """

    def __init__(self, Time: float, Node: str, AppId: int, SeqNo: int, Type: DelayType, DelayS: float,
                 DelayUS: float, RetxCount: int, HopCount: int):
        """
        :param Time:
        :param Node:
        :param AppId:
        :param SeqNo:
        :param Type:
        :param DelayS:
        :param DelayUS:
        :param RetxCount:
        :param HopCount:
        """
        self.Time = Time
        self.Node = Node
        self.AppId = AppId
        self.SeqNo = SeqNo
        self.Type = Type
        self.DelayS = DelayS
        self.DelayUS = DelayUS
        self.RetxCount = RetxCount
        self.HopCount = HopCount

    def getValueByDelayTarget(self, delayTarget: DelayTarget) -> float:
        if delayTarget == DelayTarget.DelayS:
            return self.DelayS
        elif delayTarget == DelayTarget.DelayMS:
            return self.DelayUS / 1000.0
        else:
            return self.DelayUS

    @staticmethod
    def parseLine(line: str):
        # 0.14809	C2	0	1	LastDelay	0.0610684	61068.4	1	3
        values = line.strip().split("\t")
        if len(values) < 9:
            return None
        return DelayItem(
            float(values[0].strip()),
            values[1].strip(),
            int(values[2].strip()),
            int(values[3].strip()),
            DelayType[values[4].strip()],
            float(values[5].strip()),
            float(values[6].strip()),
            int(values[7].strip()),
            int(values[8].strip())
        )


class NodeAppDelay:
    """
    用于描述某个节点上某个App的延迟 => 使用 AppId 来区分同一个节点上的不同App
    """

    def __init__(self, Node: str, AppId: int):
        self.Node = Node
        self.AppId = AppId
        self.typeMap = dict()  # 用于存储不同 Delay Type 的采样记录
        for delayType in DelayType:
            self.typeMap[delayType.name] = []

    def appendItem(self, item: DelayItem):
        """
        新增一条采样记录
        :param item:
        :return:
        """
        # 如果不是当前App的统计记录，忽略
        if item.Node != self.Node or item.AppId != self.AppId:
            return
        self.typeMap[item.Type.name].append(item)

    def _sampling_interval(self, params: dict, start: int = 0, end: int = float("inf"), x_offset: float = 0) -> dict:
        lastCount, res, x_v, y_v, tmp = 0, {}, 0, 0, []
        delayType, samplingInterval, raw = \
            params.get("delayType", DelayType.LastDelay), params.get("samplingInterval", 2), \
            params.get("raw", -1)

        for i in range(len(self.typeMap[DelayType.FullDelay.name])):
            fullItem, lastItem = self.typeMap[DelayType.FullDelay.name][i], \
                                 self.typeMap[DelayType.LastDelay.name][i]
            full, last = fullItem.getValueByDelayTarget(DelayTarget.DelayMS), \
                         lastItem.getValueByDelayTarget(DelayTarget.DelayMS)
            # 过滤重传的包
            if full - last > 10e-6 or last <= start or last > end:
                continue
            item = self.typeMap[delayType.name][i]
            if samplingInterval > 0:
                # 采样
                if raw == 0:
                    # 1. 采样区间内平均
                    if int(item.Time / samplingInterval) != lastCount:
                        lastCount = int(item.Time / samplingInterval)
                        x_v = lastCount * samplingInterval + x_offset
                        y_v = np.average(tmp)
                        tmp = []
                        if y_v > start and y_v <= end:
                            res[x_v] = y_v
                    else:
                        tmp.append(last)
                elif raw > 0:
                    # 2. 按样本数间隔采样
                    if i % samplingInterval == 0:
                        x_v = item.Time
                        y_v = last
                        if y_v > start and y_v <= end:
                            res[x_v] = y_v
                else:
                    # 3. 按时间间隔采样
                    if int(item.Time / samplingInterval) != lastCount:
                        lastCount = int(item.Time / samplingInterval)
                        x_v = lastCount * samplingInterval + x_offset
                        y_v = last
                        if y_v > start and y_v <= end:
                            res[x_v] = y_v
            else:
                # 不采样，使用原始数据
                x_v = item.Time
                y_v = last
                if y_v > start and y_v <= end:
                    res[x_v] = y_v
        return res

    def _sampling(self, params: dict, get_x=True):
        """
        采样
        :param params:
        :return:
        """
        lastCount, x, y = 0, [], []
        delayType, samplingInterval, raw, anomalyIntervalList = \
            params.get("delayType", DelayType.LastDelay), params.get("samplingInterval", 2), \
            params.get("raw", -1), params.get("anomalyIntervalList", [])

        # 1. 首先对全局进行采样
        result = self._sampling_interval(params)

        # 2. 接着对每个异常区间采样
        for idx, interval in enumerate(anomalyIntervalList):
            tmp_result = self._sampling_interval(
                params, interval[0], interval[1],
                samplingInterval * idx + 1 / len(anomalyIntervalList)
            )
            result.update(tmp_result)

        # 3. 按时间排序
        keys = list(result.keys())
        keys.sort()
        x = keys
        if not get_x:
            for k in keys:
                y.append(result[k])

        return x, y

    def getX(self, params: dict):
        """
        获取采样时间列表
        :param delayType:
        :return:
        """
        x, _ = self._sampling(params, True)
        return x

    def getY(self, params: dict):
        """
        获取延迟采样列表
        :param delayType:           延迟类型
        :param delayTarget:         延迟目标
        :param samplingInterval:    采样间隔
        :return:
        """
        _, y = self._sampling(params, False)
        return y


class NodeDelay:
    """
    一个用于描述同一个节点上各个App延迟的类
    """

    def __init__(self, Node: str):
        self.Node = Node
        self.appMap = dict()

    def appendItem(self, item: DelayItem):
        """
        新增一条采样记录
        :param item:
        :return:
        """
        # 如果不是当前节点的采样记录，则忽略
        if item.Node != self.Node:
            return
        if item.AppId not in self.appMap:
            self.appMap[item.AppId] = NodeAppDelay(item.Node, item.AppId)
        self.appMap[item.AppId].appendItem(item)

    def getX(self, AppId: int, params: dict):
        """
        获取某个App的采样时间列表
        :param AppId:
        :param delayType:
        :param samplingInterval:
        :return:
        """
        if AppId not in self.appMap:
            return []
        return self.appMap[AppId].getX(params)

    def getY(self, AppId: int, params: dict):
        """
        获取某个App的延迟采样列表
        :param AppId:
        :param delayType:
        :param delayTarget:
        :param samplingInterval:
        :return:
        """
        if AppId not in self.appMap:
            return []
        return self.appMap[AppId].getY(params)


class Delay:
    """
    一个用于解析 ndnsim 延迟采样结果的类
    """

    def __init__(self):
        self.nodeMap = dict()

    def getByNode(self, node: str) -> Optional[NodeDelay]:
        if node not in self.nodeMap:
            return None
        return self.nodeMap[node]

    @staticmethod
    def parse(inputFile: str):
        """
        传入一个 ndnsim 采集的延迟采样结果文件，从中解析出延迟信息
        :param inputFile:
        :return:
        """
        delay = Delay()
        with open(inputFile, "r") as f:
            # 首先忽略表头
            # Time	Node	AppId	SeqNo	Type	DelayS	DelayUS	RetxCount	HopCount
            f.readline()

            # 从第一行开始解析
            line = f.readline()
            while line:
                if line.strip() != "":
                    item = DelayItem.parseLine(line)
                    if item:
                        if item.Node not in delay.nodeMap:
                            delay.nodeMap[item.Node] = NodeDelay(item.Node)
                        delay.nodeMap[item.Node].appendItem(item)
                line = f.readline()
        return delay


class DelayExtractBase:
    def __init__(self, delay: Delay):
        self.samplingInterval = 1.0
        self.delayType = DelayType.LastDelay
        self.delayTarget = DelayTarget.DelayMS
        self.delay = delay
        self.raw = 0
        # 异常区间
        # 1. 在进行采样时，异常区间列表中的每一个区间单独采样；
        self.anomalyIntervalList: List[tuple] = []

    def setAnomalyInterval(self, intervals: List[tuple]):
        """
        设置异常采样区间
        :param intervals:
        :return:
        """
        self.anomalyIntervalList = intervals
        return self

    def setSamplingInterval(self, samplingInterval: float):
        """
        设置采样间隔 => 如果 samplingInterval = 1.0 表示绘图时，每秒采样一次
        :param samplingInterval:
        :return:
        """
        self.samplingInterval = samplingInterval
        return self

    def setRaw(self, raw: int):
        """
        raw < 0 => 按时间间隔采样
        raw > 0 => 按样本数间隔采样
        raw == 0 => 平均采样
        :param raw:
        :return:
        """
        self.raw = raw
        return self

    def setDelayType(self, delayType: DelayType):
        """
        设置延迟类型
        :param delayType:
        :return:
        """
        self.delayType = delayType
        return self

    def setDelayTarget(self, delayTarget: DelayTarget):
        """
        设置延迟目标
        :param delayTarget:
        :return:
        """
        self.delayTarget = delayTarget
        return self

    def getNode(self, nodeName):
        return self.delay.getByNode(nodeName)

    def getX(self, node: NodeDelay, nodeId):
        return node.getX(nodeId, self.__dict__)

    def getY(self, node: NodeDelay, nodeId):
        return node.getY(nodeId, self.__dict__)

    def getUnit(self):
        return DelayTarget.getUnit(self.delayTarget.name)


class DelayGraph(GraphBase, DelayExtractBase, ExportBase):
    """
    一个用于实现绘制延迟图的类
    """

    def __init__(self, delay: Delay):
        GraphBase.__init__(self)
        DelayExtractBase.__init__(self, delay)
        ExportBase.__init__(self, self.getNode, self.getX, self.getY, self.getUnit)

    def plot(self, nodeName: str, appId: int, *args,
             color: str = "&&",
             linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
             markerfacecolor: str = "none", markersize: float = 6,
             **kwargs):
        node = self.delay.getByNode(nodeName)
        if not node:
            print("not exist node: ", node)
            return self
        if "label" not in kwargs:
            kwargs["label"] = node.Node
        x, y = node.getX(appId, self.__dict__), \
               node.getY(appId, self.__dict__)
        self.select(nodeName, appId, kwargs["label"])
        super().innerPlot(x, y, *args,
                          color=color,
                          linewidth=linewidth,
                          linestyle=linestyle,
                          marker=marker,
                          markerfacecolor=markerfacecolor,
                          markersize=markersize,
                          **kwargs)
        return self

    def plotSum(self, nodeList: [NodeItem], *args,
                color: str = "&&",
                linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
                markerfacecolor: str = "none", markersize: float = 6,
                **kwargs):
        label = None
        if "label" in kwargs:
            label = kwargs["label"]
        self.selectSum(nodeList, label=label)
        super().innerPlotSum(nodeList, self.getNode, self.getX, self.getY, *args,
                             color=color,
                             linewidth=linewidth,
                             linestyle=linestyle,
                             marker=marker,
                             markerfacecolor=markerfacecolor,
                             markersize=markersize,
                             **kwargs)
        return self

    def plotAvg(self, nodeList: [NodeItem], *args,
                color: str = "&&",
                linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
                markerfacecolor: str = "none", markersize: float = 6,
                **kwargs):
        label = None
        if "label" in kwargs:
            label = kwargs["label"]
        self.selectAvg(nodeList, label=label)
        self.innerPlotAvg(nodeList, self.getNode, self.getX, self.getY, *args,
                          color=color,
                          linewidth=linewidth,
                          linestyle=linestyle,
                          marker=marker,
                          markerfacecolor=markerfacecolor,
                          markersize=markersize,
                          **kwargs)
        return self

    def exportExcel(self, savePath: str,
                    xName: str = "Times",
                    yName: str = "Delay",
                    xUnit: str = "Second"):
        """
        导出数据到Excel
        :param savePath:
        :param xName:
        :param yName:
        :param xUnit:
        :return:
        """
        dfResult = None
        for item in self.items:
            contents = [[xName, yName], [xUnit, item.units], ["", item.label]]
            dataMatrix = np.vstack([np.array(item.x).T, np.array(item.y).T])
            for i in range(len(item.x)):
                contents.append(dataMatrix[:, i])
            df = pd.DataFrame(contents)
            if dfResult is None:
                dfResult = df
            else:
                dfResult = pd.concat([dfResult, df], axis=1)
        dfResult.to_excel(savePath, index=False, header=None)
        return self

    def exportGroupExcel(self, savePath: str):
        dfResult = None
        for item in self.items:
            nextCount = int(item.x[0] / self.samplingInterval) * self.samplingInterval + self.samplingInterval
            # 填充没有的时间
            for i in range(int(item.x[0] / self.samplingInterval)):
                res = [[(i + 1) * self.samplingInterval], [item.label], []]
                df = pd.DataFrame(res)
                if dfResult is None:
                    dfResult = df
                else:
                    dfResult = pd.concat([dfResult, df], axis=1)
            tmp = [[nextCount], [item.label], []]
            for i in range(len(item.x)):
                if item.x[i] < nextCount:
                    tmp.append([item.y[i]])
                else:
                    df = pd.DataFrame(tmp)
                    if dfResult is None:
                        dfResult = df
                    else:
                        dfResult = pd.concat([dfResult, df], axis=1)
                    nextCount += self.samplingInterval
                    tmp = [[nextCount], [item.label], [], [item.y[i]]]
            if len(tmp) > 10:
                dfResult = pd.concat([dfResult, pd.DataFrame(tmp)], axis=1)
        dfResult.to_excel(savePath, index=False, header=None)
        return self

    def exportGroupCategoriesExcel(self, savePath: str):
        dfResult = None
        tmp = [['Time', 'Consumer', 'Data'], ['', '', ''], ['', '', '']]
        for item in self.items:
            nextCount = int(item.x[0] / self.samplingInterval) * self.samplingInterval + self.samplingInterval
            # 填充没有的时间
            for i in range(int(item.x[0] / self.samplingInterval)):
                res = [[(i + 1) * self.samplingInterval], [item.label], []]
                tmp.append([self.samplingInterval * (i + 1), item.label, 0])

            for i in range(len(item.x)):
                tmp.append([nextCount, item.label, item.y[i]])
                if item.x[i] < nextCount:
                    continue
                else:
                    nextCount += self.samplingInterval

        pd.DataFrame(tmp).to_excel(savePath, index=False, header=None)
        return self

    @staticmethod
    def parse(inputFile: str):
        return DelayGraph(Delay.parse(inputFile))
