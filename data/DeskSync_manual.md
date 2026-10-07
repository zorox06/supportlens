# DeskSync product manual

This is sample documentation for the fictional DeskSync desktop collaboration product. Its settings and error codes are for this demonstration only.

## Installation requirements
DeskSync 2.4 requires Windows 11 or macOS 13 or newer, 500 MB of available disk space, and a working internet connection for sign-in. Download the installer from your organization's approved software portal. After installation, launch DeskSync and sign in with your organization account. Administrative privileges may be required by your organization's device policy.

## Error E104 connection timeout
E104 means DeskSync could not reach its organization sync service within 30 seconds. First confirm your internet connection works by opening your organization's portal in the browser. In DeskSync, open Settings, then Connection, and choose Test connection. If you are using a VPN, check whether your organization requires it for the sync service. Do not disable required security software. Ask your IT administrator to verify access to the organization sync endpoint. Use Help, Diagnostics, Export diagnostic report to collect the connection result for support. A successful connection test followed by a completed sync verifies recovery.

## Files are not syncing
Open the Sync activity panel to check whether sync is paused. If it is paused, select Resume sync. Verify that the file is inside the workspace folder and not excluded by the workspace's file filters. A workspace with insufficient storage stops new uploads until the administrator increases capacity or removes unnecessary files according to the retention policy. If E104 appears, use the E104 connection troubleshooting procedure. Do not delete the local workspace as a troubleshooting shortcut.

## Sign-in and two-factor authentication
Use the Forgot password option on the organization sign-in page to begin the approved recovery process. If an authentication code is rejected, check that the device clock is synchronized and try a fresh code. Do not share passwords, authentication codes or recovery codes with support. If the account is locked, contact the organization administrator; DeskSync support cannot unlock organization accounts.

## Diagnostics and support
Diagnostic reports include the application version, operating system, connection test result and error codes. Review a report before sharing and remove personal file names or private content. A support request should include the DeskSync version, operating system, exact error, time of failure, attempted steps and a redacted diagnostic report. Support may request the organization identifier, but never a password or authentication code.
