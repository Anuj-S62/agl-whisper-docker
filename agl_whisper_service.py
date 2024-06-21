
import os
import sys

# Get the path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the "generated" folder
generated_dir = os.path.join(current_dir, "generated")
# Add the "generated" folder to sys.path
sys.path.append(generated_dir)

import argparse
from utils.config import set_config_path, load_config, update_config_value, get_config_value, get_logger
from agl_whisper_server import run_server

def print_version():
    print("Automotive Grade Linux (AGL)")
    print(f"Whisper ASR Service v1.0")

def main():
    server_port = ""
    stt_model_path = ""

    parser = argparse.ArgumentParser(description="Automotive Grade Linux (AGL) - Whisper ASR Service")
    parser.add_argument('--version', action='store_true', help='Show version')
    
    subparsers = parser.add_subparsers(dest='subcommand', title='Available Commands')
    subparsers.required = False
    
    # Create subparsers for "run server" and "run client"
    server_parser = subparsers.add_parser('run-server', help='Run the Whisper gRPC Server')
    
    # Add the arguments for the server
    server_parser.add_argument('--default', action='store_true', help='Starts the server based on default config file.')
    server_parser.add_argument('--config', required=False, help='Path to a config file. Server is started based on this config file.')
    server_parser.add_argument('--stt-model-path', required=False, help='Path to the Whisper Speech To Text model')    
    server_parser.add_argument('--server-port', required=False, help='Port of the gRPC server running the Whisper ASR Service.')
    server_parser.add_argument('--log-store-dir', required=False, help='Path to the directory where logs will be stored.')
    args = parser.parse_args()
    
    if args.version:
        print_version()

    elif args.subcommand == 'run-server':
        if not args.default and not args.config:
            if not args.stt_model_path:
                print("Error: The --stt-model-path is missing. Please provide a value. Use --help to see available options.")
                exit(1)
            if not args.server_port:
                print("Error: The --server-port is missing. Please provide a value. Use --help to see available options.")
                exit(1)
            
            # Contruct the default config file path
            config_path = os.path.join(current_dir, "config.ini")

            # Load the config values from the config file
            set_config_path(config_path)
            load_config()

            logger = get_logger()
            logger.info("Starting AGL Whisper ASR Service in server mode using the cli arguments")
            # Update the log store dir in config.ini if provided
            log_dir = args.log_store_dir or get_config_value('BASE_LOG_DIR')
            update_config_value(log_dir, 'BASE_LOG_DIR')

            stt_model_path = args.stt_model_path
            server_port = args.server_port


        elif args.config:
            # Get config file path value 
            cli_config_path = args.config

            # if config file path provided then load the config values from it
            if cli_config_path :
                cli_config_path  = os.path.abspath(cli_config_path) if not os.path.isabs(cli_config_path) else cli_config_path 
                print(f"New config file path provided: {cli_config_path}. Overriding the default config file path.")
                set_config_path(cli_config_path)
                load_config()

                stt_model_path = get_config_value('STT_MODEL_PATH')
                server_port = get_config_value('SERVER_PORT')

                logger = get_logger()
                logger.info(f"Starting AGL Whisper ASR Service in server mode using the provided config file...")
        
        elif args.default:
            # Contruct the default config file path
            config_path = os.path.join(current_dir, "config.ini")

            # Load the config values from the config file
            set_config_path(config_path)
            load_config()

            stt_model_path = get_config_value('STT_MODEL_PATH')
            server_port = get_config_value('SERVER_PORT')

            logger = get_logger()
            logger.info(f"Starting AGL Whisper ASR Service in server mode using the default config file...")

        run_server( server_port, stt_model_path)
    else:
        print_version()
        print("Use --help to see available options.")


if __name__ == '__main__':
    main()