from mininet.topo import Topo

from configparser import ConfigParser

conf = ConfigParser()
conf.read('conf.ini')

protos = "OpenFlow13"

class Topo1( Topo ):
    def build( self ):

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3', protocols=protos )
        rightSwitch = self.addSwitch( 's4', protocols=protos )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )

class Topo2( Topo ):
    def build( self ):

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        s1 = self.addSwitch( 's1', protocols=protos )

        # Add links
        self.addLink( s1, h1 )

class Topo3( Topo ):
    def build( self ):

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1', protocols=protos )

        # Add links
        self.addLink( s1, h1 )
        self.addLink( s1, h2 )


class Topo6( Topo ):
    def build( self ):

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip="10.0.0.1/24" )
        h2 = self.addHost( 'h2', ip="20.0.0.1/24"  )
        s1 = self.addSwitch( 's1', protocols=protos )
        s2 = self.addSwitch( 's2', protocols=protos )

        # Add links
        self.addLink( s1, h1 )
        self.addLink( s1, h2 )
        self.addLink( s1, s2 )
        self.addLink( s1, s2 )

mid_count = int(conf['topo']['mid_count'])
len_mid_count = len(str(mid_count))
class Topo7( Topo ):
    def build( self ):

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip="10.0.0.1/24", defaultRoute='dev h1-eth257' )
        h2 = self.addHost( 'h2', ip="20.0.0.1/24", defaultRoute='dev h2-eth258' )
        sl = self.addSwitch( 'sl', protocols=protos, dpid="101" )
        sr = self.addSwitch( 'sr', protocols=protos, dpid="102" )
        smid = []
        for i in range(mid_count):
            num = (('0' * len_mid_count) + str(i+1))[-len_mid_count:]
            smid.append(self.addSwitch( f'smid{num}', protocols=protos, dpid=num))

        # Add links
        self.addLink( sl, h1, port1=1001, port2=257 )
        self.addLink( sr, h2, port1=1002, port2=258 )
        self.addLink( sl, sr, port1=258, port2=257 )

        for i in range(len(smid)):
            self.addLink(smid[i], sl, port1=257, port2=i+1)
            self.addLink(smid[i], sr, port1=258, port2=i+1)
            for j in range(i+1,len(smid)):
                if i==j:
                    continue
                print(f'linking {i}, {j}')
                self.addLink(smid[i], smid[j], port1=j+1, port2=i+1)
                


class Topo8( Topo ):
    def build( self ):

        # Add hosts and switches
        #h1 = self.addHost( 'h1', ip="10.0.0.1/24", defaultRoute='dev h1-eth257' )
        #h2 = self.addHost( 'h2', ip="20.0.0.1/24", defaultRoute='dev h2-eth258' )
        sl = self.addSwitch( 'sl', protocols=protos, dpid="101" )
        sr = self.addSwitch( 'sr', protocols=protos, dpid="102" )
        smid = []
        for i in range(mid_count):
            num = (('0' * len_mid_count) + str(i+1))[-len_mid_count:]
            smid.append(self.addSwitch( f'smid{num}', protocols=protos, dpid=num))

        # Add links
        #self.addLink( sl, h1, port1=1001, port2=257 )
        #self.addLink( sr, h2, port1=1002, port2=258 )
        self.addLink( sl, sr, port1=258, port2=257 )

        for i in range(len(smid)):
            self.addLink(smid[i], sl, port1=257, port2=i+1)
            self.addLink(smid[i], sr, port1=258, port2=i+1)
            for j in range(i+1,len(smid)):
                if i==j:
                    continue
                print(f'linking {i}, {j}')
                self.addLink(smid[i], smid[j], port1=j+1, port2=i+1)
                


topos = { 'topo1': ( lambda: Topo1() ),
          'topo2': ( lambda: Topo2() ),
          'topo3': ( lambda: Topo3() ),
          'topo6': ( lambda: Topo6() ),
          'topo7': ( lambda: Topo7() ),
          'topo8': ( lambda: Topo8() ) }





