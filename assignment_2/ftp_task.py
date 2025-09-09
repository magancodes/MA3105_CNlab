#!/usr/bin/env python3
import os
import ftplib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

FTP_HOST = os.getenv("FTP_HOST", "localhost")
FTP_USER = os.getenv("FTP_USER", "anonymous")
FTP_PASS = os.getenv("FTP_PASS", "")

TEST_UPLOAD_FILE = "upload_test.txt"
TEST_DOWNLOAD_FILE = "download_test.txt"
REMOTE_UPLOAD_NAME = os.getenv("FTP_REMOTE_NAME", "upload_test_remote.txt")

def ftp_operations():
    with ftplib.FTP() as ftp:
        ftp.connect(FTP_HOST, int(os.getenv("FTP_PORT", "21")), timeout=30)
        logging.info("Connected to FTP %s", FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        logging.info("Logged in as %s", FTP_USER)

        with open(TEST_UPLOAD_FILE, "w", encoding="utf-8") as f:
            f.write("CN Lab FTP upload verification text.\n")

        with open(TEST_UPLOAD_FILE, "rb") as f:
            ftp.storbinary(f"STOR {REMOTE_UPLOAD_NAME}", f)
        logging.info("Uploaded %s as %s", TEST_UPLOAD_FILE, REMOTE_UPLOAD_NAME)

        with open(TEST_DOWNLOAD_FILE, "wb") as f:
            ftp.retrbinary(f"RETR {REMOTE_UPLOAD_NAME}", f.write)
        logging.info("Downloaded to %s", TEST_DOWNLOAD_FILE)

        with open(TEST_UPLOAD_FILE, "rb") as f1, open(TEST_DOWNLOAD_FILE, "rb") as f2:
            up = f1.read()
            down = f2.read()
            if up == down:
                logging.info("Verification success: downloaded content matches uploaded content.")
            else:
                logging.error("Verification failed: content mismatch.")

        logging.info("Remote directory listing:")
        ftp.dir()

if __name__ == "__main__":
    try:
        ftp_operations()
    except Exception as e:
        logging.error("FTP operation failed: %s", e)