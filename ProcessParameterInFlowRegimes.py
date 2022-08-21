import random
import numpy as np
import math
import matplotlib.pyplot as plt


marginDispToTrans = 0
marginTransToLoad = 0
marginLoadToFloo = 0

DispToTransX = [0.002, 0.053]  # Fl
DispToTransY = [0.2, 1]  # Fr
TransToLoadX = [0.002, 0.053]  # Fl
TransToLoadY = [0.1, 0.5]  # Fr
LoadToFloodX = [0.025, 0.31]  # Fl
LoadToFloodY = [0.04, 0.5]  # Fr
g = 9.81  # erbeschleunigung
D = 0.1  # meter reaktor durchmesser innen
floLoaX = [0.025, 0.1, 0.31]  # Fl
floLoaY = [0.04, 0.16, 0.5]  # Fr
loadDispX = [0.002, 0.01, 0.053]  # Fl
loadDispY = [0.2, 0.4, 1]  # Fr

maximum = {
    "vs": 150,
    "rpm": 1000,
    "Fr": 2,  # np.power(1000 * 60, 2) * D / g,
    "Fl": 1  # 150 / (1000 * np.power(D, 3) * 60000)
}
minimum = {
    "vs": 10,
    "rpm": 100,
    "Fr": 0.04,  # np.power(100*60, 2)*D/g,
    "Fl": 0.002  # 10/(100*np.power(D, 3)*60000)
}
maximumDisp = {
    "vs": 150,
    "rpm": 1000,
    "FrChart": 2,  # np.power(1000 * 60, 2) * D / g,
    "FlChart": 1,  # 150 / (1000 * np.power(D, 3) * 60000)
    "FrConst": np.power(1000 / 60, 2) * D / g,
    "FlConst": 150 / ((100 / 60 * np.power(D, 3)) * 60000),
    "FrBig": 1000,
    "FlBig": 1000}
minimumDisp = {
    "vs": 10,
    "rpm": 100,
    "FrChart": 0.2,  # np.power(100*60, 2)*D/g,
    "FlChart": 0.002,  # 10/(100*np.power(D, 3)*60000)
    "FrConst": np.power(100 / 60, 2) * D / g,
    "FlConst": 10 / ((1000 / 60 * np.power(D, 3) * 60000))
}
def getFrOfDispToTransFromFlValentin(Fl, margin=0):
    xp = [math.log10(0.002), math.log10(0.1)]
    yp = [math.log10(0.2), math.log10(0.4)]
    if type(Fl) == float:
        return math.pow(10, np.interp(Fl, xp, yp))
    else:
        return [math.pow(10, np.interp(fl_value, xp, yp)) for fl_value in Fl]

def getRpm(Fr):
    return np.sqrt(Fr * g / D) * 60  # N*60=rpm

def getGasflow(Fl, Fr):
    k = Fl * np.sqrt(Fr * g / D) * D * D * D * 60000
    return k  # VS= Q*60000

def getmUndn(x1, x2, y1, y2):
    m = -np.log10(y1) / (np.log10(x2) - np.log10(x1))
    n = np.log10(y2 / np.power(x2, m))
    return m, n

def getFrOfDispToTransFromFl(Fl, margin=marginDispToTrans):
    m, n = getmUndn(DispToTransX[0], DispToTransX[1], DispToTransY[0], DispToTransY[1])
    fr = np.power(10, n) * np.power(Fl - margin, m)
    return fr

def getFrOfTransToLoadFromFl(FlTransToLoad, margin=marginTransToLoad):
    m, n = getmUndn(TransToLoadX[0], TransToLoadX[1], TransToLoadY[0], TransToLoadY[1])
    fr = np.power(10, n) * np.power(FlTransToLoad - margin, m)
    return fr

def getFrOfLoadToFloodFromFl(FlLoadToFlood, margin=marginLoadToFloo):
    m, n = getmUndn(LoadToFloodX[0], LoadToFloodX[1], LoadToFloodY[0], LoadToFloodY[1])
    fr = np.power(10, n) * np.power(FlLoadToFlood - margin, m)
    return fr

def getFrFromRpm(rpm):
    return np.power(rpm / 60, 2) * D / g

def getVsFromRpmOnDispersedKurv(rpm):
    m, n = getmUndn(DispToTransX[0], DispToTransX[1], DispToTransY[0], DispToTransY[1])
    return getGasflow(np.power(getFrFromRpm(rpm) / np.power(10, n), 1 / m), getFrFromRpm(rpm))

def seperationLineDispRpmToVs(rpm):
    m, n = getmUndn(DispToTransX[0], DispToTransX[1], DispToTransY[0], DispToTransY[1])
    return np.power((np.power(rpm, 2) * D) / (3600 * g * np.power(10, n)), 1 / m) * rpm

def getRandomExperimentInDispersedState():
    while True:
        rpm = random.uniform(minimum.get("rpm"), maximum.get("rpm"))
        vs = random.uniform(minimum.get("vs"), maximum.get("vs"))
        vsSeperationLine = seperationLineDispRpmToVs(rpm)
        if vs >= vsSeperationLine:
            continue
        return rpm, vs

def seperationLineDispToTransRpmToVs(rpm, marginDispToTrans):
    m, n = getmUndn(DispToTransX[0], DispToTransX[1], DispToTransY[0], DispToTransY[1])
    return np.power((np.power(rpm, 2) * D) / (3600 * g * np.power(10, n)), 1 / m) * rpm
    pass

def getRandomExperimentInTransState():
    while True:
        rpm = random.uniform(minimum.get("rpm"), maximum.get("rpm"))
        vs = random.uniform(minimum.get("vs"), maximum.get("vs"))
        DispToTrans = seperationLineDispToTransRpmToVs(rpm, marginDispToTrans)
        TransToLoad = seperationLineTransToLoadRpmToVs(rpm, marginTransToLoad)

        if vs >= TransToLoad:  # Rechts von der Linie
            continue
        if vs < DispToTrans:  # Links von der Linie
            continue
        return rpm, vs

def seperationLineTransToLoadRpmToVs(rpm, marginTransToLoad):
    m, n = getmUndn(TransToLoadX[0], TransToLoadX[1], TransToLoadY[0], TransToLoadY[1])
    return np.power((np.power(rpm, 2) * D) / (3600 * g * np.power(10, n)), 1 / m) * rpm

def seperationLineLoadToFlooRpmToVs(rpm, marginLoadToFloo):
    m, n = getmUndn(LoadToFloodX[0], LoadToFloodX[1], LoadToFloodY[0], LoadToFloodY[1])
    return np.power((np.power(rpm, 2) * D) / (3600 * g * np.power(10, n)), 1 / m) * rpm

def getRandomExperimentInLoadState():
    while True:
        rpm = random.uniform(minimum.get("rpm"), maximum.get("rpm"))
        vs = random.uniform(minimum.get("vs"), maximum.get("vs"))
        TransToLoad = seperationLineTransToLoadRpmToVs(rpm, marginTransToLoad)
        LoadToFloo = seperationLineLoadToFlooRpmToVs(rpm, marginLoadToFloo)
        if vs >= LoadToFloo:
            continue
        if vs <= TransToLoad:
            continue
        return rpm, vs
def getRandomExperimentInFloodState():
    while True:
        rpm = random.uniform(minimum.get("rpm"), maximum.get("rpm"))
        vs = random.uniform(minimum.get("vs"), maximum.get("vs"))
        LoadToFloo = seperationLineLoadToFlooRpmToVs(rpm, marginLoadToFloo)

        if vs <= LoadToFloo:
            continue
        return rpm, vs
def getExperiments(amountOfPicuturesPerRegime = 100):
    picturesTaken = 0

    XDisp = []
    YDisp = []
    XTrans = []
    YTrans = []
    XLoad = []
    YLoad = []
    XFlood = []
    YFlood = []
    while amountOfPicuturesPerRegime > picturesTaken:
        ExpDisp = getRandomExperimentInDispersedState()
        XDisp.append(ExpDisp[0])  # rpm
        YDisp.append(ExpDisp[1])  # vs

        ExpTrans = getRandomExperimentInTransState()
        XTrans.append(ExpTrans[0])  # rpm
        YTrans.append(ExpTrans[1])  # vs

        ExpLoad = getRandomExperimentInLoadState()
        XLoad.append(ExpLoad[0])  # rpm
        YLoad.append(ExpLoad[1])  # vs

        ExpFlood = getRandomExperimentInFloodState()
        XFlood.append(ExpFlood[0])  # rpm
        YFlood.append(ExpFlood[1])  # vs
        picturesTaken += 1

    experimentsDisp = []
    experimentsTrans = []
    experimentLoad = []
    experimentsFlood = []

    for i in range(0, amountOfPicutures):
        experimentsDisp.append({'gas_flow': XDisp[i], 'rpm': YDisp[i]})
        experimentsTrans.append({'gas_flow': XTrans[i], 'rpm': YTrans[i]})
        experimentLoad.append({'gas_flow': XLoad[i], 'rpm': YLoad[i]})
        experimentsFlood.append({'gas_flow': XFlood[i], 'rpm': YFlood[i]})

    return experimentsDisp,experimentsTrans,experimentLoad,experimentsFlood
