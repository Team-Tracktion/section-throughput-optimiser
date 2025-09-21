"""
Helper functions for the IRIS system.
"""

import json
import logging
import logging.config
import os
from datetime import datetime

def setup_logging(log_config='config/logging.conf', default_level=logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_config: Path to logging configuration file
        default_level: Default logging level if config file is not found
        
    Returns:
        Logger instance
    """
    if os.path.exists(log_config):
        try:
            logging.config.fileConfig(log_config)
            logger = logging.getLogger(__name__)
            logger.info("Logging configuration loaded from %s", log_config)
        except Exception as e:
            logging.basicConfig(level=default_level)
            logger = logging.getLogger(__name__)
            logger.warning("Failed to load logging config: %s. Using basic config.", e)
    else:
        logging.basicConfig(level=default_level)
        logger = logging.getLogger(__name__)
        logger.info("Using basic logging configuration")
    
    return logger

def save_results(results, output_file):
    """
    Save optimization results to a JSON file.
    
    Args:
        results: Optimization results dictionary
        output_file: Path to output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Add metadata to results
        results_with_meta = {
            'results': results,
            'generated_at': datetime.now().isoformat(),
            'version': 'IRIS 0.1.0'
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results_with_meta, f, indent=2)
        
        return True
    except Exception as e:
        logging.error("Failed to save results: %s", e)
        return False

def load_config(config_file):
    """
    Load configuration from a JSON file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error("Failed to load config: %s", e)
        raise