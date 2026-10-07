**Diagnosis**
* **Observed Evidence:** DeskSync displays error E104 (connection timeout) and files are not syncing [D-c2f77e01, D-74a8abaf].
* **Possible Cause:** E104 indicates DeskSync could not reach its organization sync service within 30 seconds, which in turn causes sync failures. This may be caused by network connectivity issues, VPN requirements, or blocked access to the organization sync endpoint [D-c2f77e01, D-74a8abaf].

**Troubleshooting Steps**
1. **Confirm internet connection:** Open your organization's portal in a web browser to confirm your internet connection works [D-c2f77e01].
2. **Test the connection:** In DeskSync, open **Settings**, go to **Connection**, and choose **Test connection** [D-c2f77e01].
3. **Check VPN settings:** If you are using a VPN, verify whether your organization requires it for the sync service [D-c2f77e01]. (Do not disable required security software) [D-c2f77e01].
4. **Check sync activity and pause status:** Open the **Sync activity panel** to check if sync is paused. If paused, select **Resume sync** [D-74a8abaf].
5. **Verify file location and storage:** Ensure the unsynced file is inside the workspace folder and not excluded by workspace file filters. Also verify that your workspace has sufficient storage, as insufficient storage stops new uploads [D-74a8abaf].
6. **Consult IT administrator:** If the connection test fails, ask your IT administrator to verify access to the organization sync endpoint [D-c2f77e01].
7. **Collect diagnostics:** Go to **Help**, **Diagnostics**, and select **Export diagnostic report** to collect the connection result for support if needed [D-c2f77e01]. *(Note: Do not delete the local workspace as a troubleshooting shortcut) [D-74a8abaf].*

**Verification Steps**
* Perform a successful connection test in DeskSync Settings followed by a completed file sync to verify recovery [D-c2f77e01].

**Next Action**
* If the error persists after completing the troubleshooting steps, share the exported diagnostic report (with personal filenames or private content removed) along with your DeskSync version, operating system, exact error, and time of failure with your support team [D-47ebc471].