import zmq
import time


class XPlaneClient:

    def __init__(self, topic, ip="127.0.0.1"):

        # Initialize a zeromq context
        self.context = zmq.Context()
        self.ip = ip
        self.topic = topic

        self.publication_port = 5555
        self.subscription_port = 5555


    def connect(self):
        """
        Connect to the C++ client. Make sure that Xplane and the C++ client are running

        """
        
        # Set up a channel to send work
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(f"tcp://{self.ip}:5555") # Initialization port

        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(f"tcp://{self.ip}:5556")
        self.subscriber.subscribe(self.topic)
        # Give everything a second to spin up and connect
        time.sleep(0.5)

        # Send initial connection string to register to server
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"Connection"])
        time.sleep(0.5)
        response = self.subscriber.recv_multipart()

        self.publication_port = response[1].decode("utf-8")
        self.subscription_port = str(int(self.publication_port) + 1)

        # Rebind the connection for the new ports
        self.publisher.bind(f"tcp://{self.ip}:{self.publication_port}")
        self.subscriber.connect(f"tcp://{self.ip}:{self.subscription_port}")
        print(f"Connected to Xplane Server on ports: {self.subscription_port} and {self.publication_port}")

        # Give everything a second to spin up and connect
        time.sleep(1)

    def disconnect(self):
        # Send disconnection message to server
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"Disconnection", b"0", b"0"])
        response = self.subscriber.recv_multipart()

        if "Received" in response[1].decode("utf-8"):
            self.subscriber.disconnect(f"tcp://{self.ip}:{self.subscription_port}")
            self.publisher.disconnect(f"tcp://{self.ip}:{self.publication_port}")
            return True
        else:
            return False


    def getDataRef(self, dref):
        """
        Get the value of a dataref as a string.

        Args:
            dref (str): dataRef of interest as a string

        Returns:
            str: Value of the dataRef
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"read", bytes(dref, 'utf-8'), b"0"])
        response = self.subscriber.recv_multipart()
        return response[1].decode("utf-8")

    def setDataRef(self, dref, value):
        """
        Set the dataref to the specified value.

        Args:
            dref (str): Dataref of interest
            value (str): Value of the dataref

        Returns:
            bool: True of successfully sent, false otherwise.
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"set", bytes(dref, 'utf-8'), bytes(value, 'utf-8')])
        response = self.subscriber.recv_multipart()
        if "Received" in response[1].decode("utf-8"):
            return True
        else:
            return False

    def sendCommand(self, dref):
        """
        Send command to Xplane.

        Args:
            dref (str): Designated command to be sent

        Returns:
            bool: True of successfully sent, false otherwise.
        """
        self.publisher.send_multipart([bytes(self.topic, 'utf-8'), b"command", bytes(dref, 'utf-8'), b"0"])
        response = self.subscriber.recv_multipart()
        if "Received" in response[1].decode("utf-8"):
            return True
        else:
            return False


