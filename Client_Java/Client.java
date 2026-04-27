import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * TCP Client for Polyglot Chat Challenge
 * Interoperates with a Python Server using UTF-8 and Ping-Pong flow.
 */
public class Client {
    private static final boolean DEBUG = true; // Optional debug flag

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java Client <HOST_IP> <PORT>");
            return;
        }

        String host = args[0];
        int port = Integer.parseInt(args[1]);

        // Using try-with-resources for graceful closing of the socket and streams
        try (Socket socket = new Socket(host, port);
             // Explicit UTF-8 encoding as required 
             BufferedReader networkIn = new BufferedReader(
                     new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
             BufferedWriter networkOut = new BufferedWriter(
                     new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8));
             BufferedReader consoleIn = new BufferedReader(
                     new InputStreamReader(System.in))) {

            System.out.println("Connected to server at " + host + ":" + port);

            while (true) {
                // 1. Client sends first 
                System.out.print("Client (You): ");
                String messageToSend = consoleIn.readLine();

                if (messageToSend == null) break;

                networkOut.write(messageToSend + "\n");
                networkOut.flush(); // Ensure data is sent immediately

                if (DEBUG) {
                    System.out.println("[DEBUG] Sent: " + messageToSend.getBytes(StandardCharsets.UTF_8).length + " bytes");
                }

                if (messageToSend.equalsIgnoreCase("exit")) {
                    System.out.println("Exit command sent. Closing connection...");
                    break; // 
                }

                // 2. Wait for server response (Ping-Pong flow) [cite: 5, 7]
                System.out.println("Waiting for server...");
                String receivedMessage = networkIn.readLine();

                if (receivedMessage == null || receivedMessage.equalsIgnoreCase("exit")) {
                    String reason = (receivedMessage == null) ? "Server disconnected." : "Server sent exit.";
                    System.out.println(reason);
                    break; // 
                }

                System.out.println("Server: " + receivedMessage);
                if (DEBUG) {
                    System.out.println("[DEBUG] Received: " + receivedMessage.getBytes(StandardCharsets.UTF_8).length + " bytes");
                }
            }

        } catch (UnknownHostException e) {
            System.err.println("Error: Host unreachable (" + host + ")");
        } catch (ConnectException e) {
            System.err.println("Error: Connection refused. Is the server running on port " + port + "?");
        } catch (IOException e) {
            System.err.println("Network error: " + e.getMessage());
        } finally {
            System.out.println("Client terminated.");
        }
    }
}