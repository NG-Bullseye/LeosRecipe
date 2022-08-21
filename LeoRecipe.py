import random
import time

import numpy as np
import numpy
from opcua import Client, ua
from tqdm import tqdm
import logging

import ProcessParameterInFlowRegimes

logging.getLogger('opcua').setLevel(logging.CRITICAL)


TIME_DELAY = 0.5
RECONNECT_REQUIRED = True


class BioReactor:
    def __init__(self):
        self.opcua_client = Client('opc.tcp://10.6.51.40:4840/', timeout=10)
        self.opcua_client.set_user('admin')
        self.opcua_client.set_password('wago')
        self._reconnect()
        self.calibrate_vessel()
        self.start_pressure_release()
        self.start_pressure_seal()
        self.start_aerate()

    def _reconnect(self):
        if RECONNECT_REQUIRED:
            self.disconnect()
            time.sleep(TIME_DELAY)
            self.opcua_client.connect()
            time.sleep(TIME_DELAY)
            print('-- Bioreactor: Connected to OPC UA --')

    def disconnect(self):
        if RECONNECT_REQUIRED:
            try:
                self.opcua_client.disconnect()
                time.sleep(TIME_DELAY)
                print('-- Bioreactor: Disconnected from OPC UA --')
            except:
                pass

    def start_pressure_seal(self):
        self._reconnect()
        print('-- Bioreactor: Start pressurize seal service --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_SEAL_1.CP_PRESSEAL_SP.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        pressure = ua.Variant(2.2, ua.VariantType.Float)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_SEAL_1.CP_PRESSEAL_SP.VOp').set_value(
            pressure)
        time.sleep(TIME_DELAY)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_SEAL_1.ServiceControl.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_SEAL_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def start_pressure_release(self):
        self._reconnect()
        print('-- Bioreactor: Start pressure release service --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_RELEASE_1.ServiceControl.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.PRESSURE_RELEASE_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def start_aerate(self):
        self._reconnect()
        print('-- Bioreactor: Start aerate service --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AIR_1.ServiceControl.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AIR_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def calibrate_vessel(self):
        self._reconnect()
        print('-- Bioreactor: Calibrate weight cells --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.TARE_1.CP_TARE_SP.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        weight = ua.Variant(30, ua.VariantType.Float)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.TARE_1.CP_TARE_SP.VOp').set_value(
            weight)
        time.sleep(TIME_DELAY)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.TARE_1.ServiceControl.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.TARE_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(10)
        command = ua.Variant(2, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.TARE_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def set_rpm(self, rpm):
        self._reconnect()
        print(f'-- Bioreactor: Set rpm to {rpm} --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.CP_AGIT_SETPOINT_RPM.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        rpm = ua.Variant(rpm, ua.VariantType.Float)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.CP_AGIT_SETPOINT_RPM.VOp').set_value(
            rpm)
        time.sleep(TIME_DELAY)

    def set_service_offline(self):
        self._reconnect()
        print('-- Bioreactor: Set service stir to offline mode --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.ServiceControl.StateOffOp').set_value(
            True)
        time.sleep(TIME_DELAY)

    def set_service_operator(self):
        self._reconnect()
        print('-- Bioreactor: Set service stir to operator mode --')
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.ServiceControl.StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)

    def start_service(self):
        self._reconnect()
        print('-- Bioreactor: Start service stir --')
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def complete_service(self):
        self._reconnect()
        print('-- Bioreactor: Complete service stir --')
        command = ua.Variant(1024, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def reset_service(self):
        self._reconnect()
        print('-- Bioreactor: Reset service stir --')
        command = ua.Variant(2, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=4;s=|var|WAGO 750-8212 PFC200 G2 2ETH RS.Application.Services.AGIT_1.ServiceControl.CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)


class GasControl:
    def __init__(self):
        self.opcua_client = Client('opc.tcp://10.6.51.201:4840/', timeout=10)
        self.opcua_client.set_user('')
        self.opcua_client.set_password('')
        self.opcua_client.connect()
        self._reconnect()

    def _reconnect(self):
        if RECONNECT_REQUIRED:
            self.disconnect()
            time.sleep(TIME_DELAY)
            self.opcua_client.connect()
            time.sleep(TIME_DELAY)
            print('-- Bioreactor: Connected to OPC UA --')

    def disconnect(self):
        if RECONNECT_REQUIRED:
            try:
                self.opcua_client.disconnect()
                time.sleep(TIME_DELAY)
                print('-- Bioreactor: Disconnected from OPC UA --')
            except:
                pass

    def set_flow_rate(self, flow_rate):
        self._reconnect()
        print(f'-- Gas control: Set gas flow to {flow_rate} --')
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeed_Continuous_SetVolumeflow_StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)
        flow_rate = ua.Variant(flow_rate, ua.VariantType.Float)
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeed_Continuous_SetVolumeflow_VOp').set_value(
            flow_rate)
        time.sleep(TIME_DELAY)

    def set_service_offline(self):
        self._reconnect()
        print('-- Gas control: Set service to offline mode --')
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeedControl_StateOffOp').set_value(
            True)
        time.sleep(TIME_DELAY)

    def set_service_operator(self):
        self._reconnect()
        print('-- Gas control: Set service to operator mode --')
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeedControl_StateOpOp').set_value(
            True)
        time.sleep(TIME_DELAY)

    def start_service(self):
        self._reconnect()
        print('-- Gas control: Start service --')
        command = ua.Variant(4, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeedControl_CommandOp').set_value(
            command)
        time.sleep(2)

    def complete_service(self):
        self._reconnect()
        print('-- Gas control: Complete service --')
        command = ua.Variant(1024, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeedControl_CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)

    def reset_service(self):
        self._reconnect()
        print('-- Gas control: Reset service --')
        command = ua.Variant(2, ua.VariantType.UInt32)
        self.opcua_client.get_node(
            'ns=2;s=Volumeflow_basedGasFeedControl_CommandOp').set_value(
            command)
        time.sleep(TIME_DELAY)


print(f'====Initialisation====')
gc = GasControl()
br = BioReactor()



experiments = [
    {'gas_flow': 50, 'rpm': 200}, #loaded
  ]

#funktion zur abbildung von rpm und gasflow nach flow regime siehe Corina Kröger gleichung
# parameter dynamisch mit random faktor ändern aber so dass das flowregime stabil bleibt. Erste und letzte bilder entfernnen.
# extra perioden für übergangsregime einführen

exp_no = 0
picturesPersecond = 4
picturesTaken = 0
amountOfPicutures = 4

while amountOfPicutures <= picturesTaken: # repeats until the amount of pictures where taken. 
    print(f'====RESTART EXPERIMENTS====')

    for exp in ProcessParameterInFlowRegimes.getExperiments()[0]:#0:Dispersded, 1:Transistion, 2:Loaded, 3:Flooded
        exp_no += 1
        print(f'====Experiment {exp}====')

        # Stirring control
        br.complete_service()
        br.reset_service()
        br.set_service_offline()

        rpm = exp['rpm']
        br.set_rpm(rpm)
        br.set_service_operator()
        br.start_service()

        # Gas control
        gc.complete_service()
        gc.reset_service()
        gc.set_service_offline()
        gas_flow = exp['gas_flow']
        gc.set_flow_rate(gas_flow)
        gc.set_service_operator()
        gc.start_service()

        # Execution
        exp_duration = 1 #in sekunden

        for i in tqdm(range(0, int(exp_duration)), desc=f"Experiment execution: {exp_no}/{len(experiments)}"):
            time.sleep(1)

        # Disconnect
        gc.disconnect()
        br.disconnect()
        picturesTaken = picturesTaken + picturesPersecond*exp_duration
