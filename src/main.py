import serial
import time
import Connector


# Main program
def main():
    con = Connector.Connector()

    if con.connected:
        try:
            while True:
                # Here you can add your logic to decide which command to send
                # Example: forward for 2 seconds, then stop
                con.forward()
                time.sleep(2)
                con.backward()
                time.sleep(2)

        except KeyboardInterrupt:
            print("Ah!")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    main()