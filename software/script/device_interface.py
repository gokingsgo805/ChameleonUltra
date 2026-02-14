"""
Device Interface Layer for RFID Fuzzer

Provides abstraction and utilities for device communication during fuzzing campaigns.
Supports device detection, validation, and advanced interaction patterns.
"""

from typing import Optional, Dict, Tuple, Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
import time
import logging

if TYPE_CHECKING:
    from chameleon_enum import MfcKeyType

logger = logging.getLogger(__name__)


class DeviceMode(Enum):
    """Device operational modes"""
    READER = "reader"
    TAG = "tag"
    UNKNOWN = "unknown"


class DeviceStatus(Enum):
    """Device connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    TIMEOUT = "timeout"


class AuthResult(Enum):
    """Authentication attempt results"""
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class DeviceInfo:
    """Device information and capabilities"""
    name: str
    hw_version: str
    fw_version: str
    mode: DeviceMode
    supports_reader_mode: bool
    supports_mifare_classic: bool
    device_id: Optional[str] = None
    max_retries: int = 3
    timeout_ms: int = 1000


@dataclass
class FuzzerSession:
    """Tracks a fuzzing session with device"""
    device_info: DeviceInfo
    start_time: float
    mutation_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    error_count: int = 0
    timeout_count: int = 0
    last_error: Optional[str] = None


class DeviceInterface:
    """
    Abstraction layer for device communication during fuzzing.

    Provides:
    - Device detection and validation
    - Connection management
    - Authentication testing
    - Error handling and recovery
    - Session tracking
    """

    def __init__(self, cmd_instance):
        """
        Initialize device interface

        Args:
            cmd_instance: ChameleonCMD instance for device communication
        """
        self.cmd = cmd_instance
        self.device_info: Optional[DeviceInfo] = None
        self.session: Optional[FuzzerSession] = None
        self.is_connected = False


    def detect_device(self) -> bool:
        """
        Detect and validate device connection

        Returns:
            True if device detected and valid, False otherwise
        """
        try:
            # Check if device communication is available
            if not hasattr(self.cmd, "device") or self.cmd.device is None:
                logger.error("Device communication not initialized")
                return False

            if not self.cmd.device.isOpen():
                logger.error("Device connection closed")
                return False

            # Try to detect device mode
            try:
                is_reader = self.cmd.is_device_reader_mode()
                mode = DeviceMode.READER if is_reader else DeviceMode.TAG
            except Exception as e:
                logger.warning(f"Could not detect device mode: {e}")
                mode = DeviceMode.UNKNOWN

            # Collect device info
            self.device_info = DeviceInfo(
                name="ChameleonUltra",
                hw_version="Unknown",
                fw_version="Unknown",
                mode=mode,
                supports_reader_mode=True,
                supports_mifare_classic=True,
            )

            self.is_connected = True
            logger.info(f"Device detected: {self.device_info.name} (mode: {mode.name})")
            return True

        except Exception as e:
            logger.error(f"Device detection failed: {e}")
            self.is_connected = False
            return False


    def enter_reader_mode(self) -> bool:
        """
        Ensure device is in reader mode for fuzzing

        Returns:
            True if in reader mode, False otherwise
        """
        if not self.is_connected:
            logger.error("Device not connected")
            return False

        try:
            if not self.cmd.is_device_reader_mode():
                logger.info("Switching device to reader mode...")
                self.cmd.set_device_reader_mode(True)
                time.sleep(0.5)  # Wait for mode switch

            self.device_info.mode = DeviceMode.READER
            return True

        except Exception as e:
            logger.error(f"Failed to enter reader mode: {e}")
            return False


    def start_session(self) -> bool:
        """
        Start a fuzzing session with device

        Returns:
            True if session started successfully
        """
        if not self.detect_device():
            logger.error("Device detection failed")
            return False

        if not self.enter_reader_mode():
            logger.error("Could not enter reader mode")
            return False

        self.session = FuzzerSession(
            device_info=self.device_info, start_time=time.time()
        )

        logger.info("Fuzzing session started")
        return True

    def test_authentication(
        self, block: int, key_type: "MfcKeyType", key: bytes, retry_count: int = 1
    ) -> Tuple[AuthResult, Optional[str]]:
        """
        Test authentication with given key

        Args:
            block: Target block number
            key_type: Key type (A or B)
            key: Authentication key (6 bytes)
            retry_count: Number of retries on timeout

        Returns:
            Tuple of (AuthResult, error_message)
        """
        if not self.is_connected:
            return AuthResult.ERROR, "Device not connected"

        if len(key) != 6:
            return AuthResult.ERROR, "Invalid key length"

        for attempt in range(retry_count):
            try:
                result = self.cmd.mf1_auth_one_key_block(block, key_type, key)

                if self.session:
                    self.session.mutation_count += 1

                if result:
                    if self.session:
                        self.session.success_count += 1
                    return AuthResult.SUCCESS, None
                else:
                    if self.session:
                        self.session.failure_count += 1
                    return AuthResult.FAILURE, None

            except TimeoutError:
                if self.session:
                    self.session.timeout_count += 1

                if attempt < retry_count - 1:
                    logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(0.1)
                    continue

                return AuthResult.TIMEOUT, "Authentication timeout"

            except Exception as e:
                error_msg = str(e)
                if self.session:
                    self.session.error_count += 1
                    self.session.last_error = error_msg

                logger.warning(f"Authentication error: {error_msg}")
                return AuthResult.ERROR, error_msg

        return AuthResult.TIMEOUT, "Max retries exceeded"


    def read_block(
        self, block: int, key_type: "MfcKeyType", key: bytes
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Read a MIFARE block

        Args:
            block: Block number to read
            key_type: Key type (A or B)
            key: Authentication key (6 bytes)

        Returns:
            Tuple of (block_data, error_message)
        """
        if not self.is_connected:
            return None, "Device not connected"

        try:
            data = self.cmd.mf1_read_one_block(block, key_type, key)
            return data, None
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Read error: {error_msg}")
            return None, error_msg

    def write_block(
        self, block: int, key_type: "MfcKeyType", key: bytes, data: bytes
    ) -> Tuple[bool, Optional[str]]:
        """
        Write to a MIFARE block

        Args:
            block: Block number to write
            key_type: Key type (A or B)
            key: Authentication key (6 bytes)
            data: Data to write (16 bytes)

        Returns:
            Tuple of (success, error_message)
        """
        if not self.is_connected:
            return False, "Device not connected"

        if len(data) != 16:
            return False, f"Invalid data length: {len(data)} (expected 16)"

        try:
            self.cmd.mf1_write_one_block(block, key_type, key, data)
            return True, None
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Write error: {error_msg}")
            return False, error_msg


    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get current session statistics

        Returns:
            Dictionary with session statistics
        """
        if not self.session:
            return {}

        elapsed = time.time() - self.session.start_time
        total = (
            self.session.success_count
            + self.session.failure_count
            + self.session.error_count
            + self.session.timeout_count
        )

        return {
            "elapsed_seconds": elapsed,
            "total_mutations": self.session.mutation_count,
            "successful_auths": self.session.success_count,
            "failed_auths": self.session.failure_count,
            "errors": self.session.error_count,
            "timeouts": self.session.timeout_count,
            "success_rate": (
                (self.session.success_count / total * 100) if total > 0 else 0
            ),
            "last_error": self.session.last_error,
        }

    def end_session(self) -> Dict[str, Any]:
        """
        End fuzzing session and return final statistics

        Returns:
            Final session statistics
        """
        if self.session:
            stats = self.get_session_stats()
            logger.info(f"Session ended. Stats: {stats}")
            self.session = None
            return stats

        return {}

    def validate_device_health(self) -> bool:
        """
        Validate device is still healthy and responsive

        Returns:
            True if device is healthy
        """
        try:
            result = self.cmd.is_device_reader_mode()
            return result is not None
        except Exception as e:
            logger.error(f"Device health check failed: {e}")
            return False

    def recover_connection(self) -> bool:
        """
        Attempt to recover device connection after error

        Returns:
            True if connection recovered
        """
        logger.info("Attempting to recover device connection...")

        try:
            # Try to re-detect device
            self.is_connected = False
            time.sleep(1)

            if self.detect_device():
                logger.info("Connection recovered")
                return True
            else:
                logger.error("Connection recovery failed")
                return False

        except Exception as e:
            logger.error(f"Recovery failed: {e}")
            return False

