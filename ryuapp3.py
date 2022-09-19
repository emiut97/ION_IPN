from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.controller import dpset

from time import sleep
from configparser import ConfigParser


conf = ConfigParser()
conf.read('conf.ini')

_mid_count = int(conf['topo']['mid_count'])

arp = []
arptemp = conf['flows']['arp'].split('_')
for f in arptemp:
    arp.append([int(elem) for elem in f.split(',')])

other = []
othertemp = conf['flows']['other'].split('_')
for f in othertemp:
    other.append([int(elem) for elem in f.split(',')])

class ipn(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        'dpset': dpset.DPSet,
    }

    def __init__(self, *args, **kwargs):
        super(ipn, self).__init__(*args, **kwargs)
        # Store DPSet instance to call its API later in the app
        self.dpset = kwargs['dpset']
        self.smid = []
        self.sl = None
        self.sr = None
        
    def init_dps(self):
        print(f'\n>>> init_dps (STARTED)')
        for f in arp:      
            for idx in range(1,len(f)-1):
                datapath = self.dpset.get(f[idx])
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(in_port=f[idx-1], eth_type=0x0806)
                actions = [parser.OFPActionOutput(f[idx+1])]
                self.add_flow(datapath, 100, match, actions)
        for f in other:
            for idx in range(1,len(f)-1):
                datapath = self.dpset.get(f[idx])
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(in_port=f[idx-1])
                actions = [parser.OFPActionOutput(f[idx+1])]
                self.add_flow(datapath, 10, match, actions)
        print(f'\n>>> init_dps (DONE)')

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        if datapath.id <= 256:
            self.smid.append(datapath)
        elif datapath.id == 257:
            self.sl = datapath
        else:
            self.sr = datapath
        print(f'\n----CONN---->>\t {datapath.id}\n')

        # init dps if all dps are connected
        if len(self.smid) == _mid_count and self.sr is not None and self.sl is not None:
            while len(self.dpset.get_all()) != (len(self.smid) + 2):
                print('Waiting for DPs to register.')
                sleep(1)
            self.init_dps()

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
        actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
        match=match, instructions=inst)
        datapath.send_msg(mod)
