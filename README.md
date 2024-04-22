# PyChat Command-line Application

This application is a basic implementation of a reliable UDP protocol for a chat application that supports sending and receiving text messages and sending and receiving files using TCP.

## Prerequisites

- Python 3.x
- Access to a terminal or command prompt

## Setup

To run this application, you will need two instances of the program running simultaneously to simulate the sender and receiver.

## Running the Application

1. Open two terminal windows (Terminal A and Terminal B) for the sender and receiver, respectively.

2. In Terminal A, navigate to the directory where the chat application files are located and run: server.py

3. In Terminal B, navigate to the directory where the chat application files are located and run: client.py

4. Once both instances of the application are running, use the prompts to send messages or files.

## Features

- Send and receive messages in real-time.
- Send files with the `$SEND <file-path>` command.
- Exit the chat with the `exit` command.

## Troubleshooting

If you encounter any issues with sending or receiving messages, ensure that the ports defined in the script are open and not blocked by any firewall or network configuration.

## Contact

For any additional questions or feedback, please contact Bader Berro at bader.berro@lau.edu.
