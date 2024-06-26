# SPDX-License-Identifier: Apache-2.0
#
# Copyright (c) 2023 Malik Talha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import configparser

config = configparser.ConfigParser()
config_path = None
logger = None

def set_config_path(path):
    """
    Sets the path to the config file.
    """
    global config_path
    config_path = path

def load_config():
    """
    Loads the config file and initializes the logger.

    Also creates logging directory if it doesn't already exist.
    """
    if config_path is not None:
        global logger
        config.read(config_path)
        
        # create the base log dir if not exists
        if not os.path.exists(get_config_value('BASE_LOG_DIR')):
            os.makedirs(get_config_value('BASE_LOG_DIR'))

        logging.basicConfig(filename=get_config_value('BASE_LOG_DIR')+'whisper_server.log', level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s]: (%(filename)s:%(funcName)s) %(message)s', filemode='a')
        logger = logging.getLogger("agl_whisper_server")
        logger.info("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")

        # remove unwanted third-party loggers
        logging.getLogger("grpc").setLevel(logging.WARNING)

    else:
        raise Exception("Config file path not provided.")

def update_config_value(value, key, group="General"):
    """
    Updates a value in the config file.
    """
    if config_path is None:
        raise Exception("Config file path not set.")
    
    config.set(group, key, value)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def get_config_value(key, group="General"):
    """
    Gets a value from the config file.
    """
    return config.get(group, key)

def get_logger():
    """
    Gets the initialized logger.
    """
    if logger is not None:
        return logger
    
    else:
        logging.basicConfig(level=logging.DEBUG)
        print("[-] Error: Failed to get logger. Logger is not initialized!")
        logging.error("Failed to get logger. Logger is not initialized!")