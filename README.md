# LaunchDarkly
1 - Install Python (if not already installed)<br />
2 - Install Flask (if not already installed)<br />
	&emsp;a - Install pip (if not already installed)<br />
	&emsp;b - run 'pip install flask' (https://stackoverflow.com/questions/17917254/how-to-install-flask-on-windows or https://pypi.org/project/Flask/ for reference)<br />
3 - Install the Launch Darkly python SDK (if not already installed)<br />
	&emsp;a - Run 'pip install launchdarkly-server-sdk' (https://docs.launchdarkly.com/sdk/server-side/python)<br />
4 - In the LD folder edit app.py<br />
	&emsp;a - Locate line #17 - this contains the SDK key, which will need to be replaced with your SDK key<br />
	&emsp;b - Your SDK key is located in the Projects tab of your Account settings page (https://docs.launchdarkly.com/sdk/server-side/python)<br />
	&emsp;c - Note whether you used the 'Production' or 'Test' SDK key<br />
5 - Create a Kill switch feature flag in the environment you linked to with your SDK key in step 4c<br />
	&emsp;a. Ensure that the Feature Flag key is Clear_List<br />
6 - In the LD folder run 'python app.py' to ensure that you can connect to LaunchDarkly, and that a user context 'Brian' is created in LaunchDarkly<br />
	&emsp;a. Close the application (in Windows ctrl-c in the command prompt); we will finish configuring LaunchDarkly before testing it<br />
7 - In LaunchDarkly create a Segment<br />
	&emsp;a. Segment name: North American Users<br />
	&emsp;b. Segment targeting: user: Brian<br />
	&emsp;c. Segment Description: Users in the USA, Canada, and Mexico<br />
	&emsp;d. Segment Tags: Regions<br />
8 - In LaunchDarkly modify the Clear_List feature flag as follows<br />
	&emsp;a. Settings Tab (gear to the upper right in the new interface):<br />
		&emsp;&emsp;1. Name: Clear_List<br />
		&emsp;&emsp;2. Description: This flag controls the 'Clear List' button functionality<br />
		&emsp;&emsp;3. Tags: functionality<br />
	&emsp;b. Variations Editor (in the right side menu in the new interface):<br />
		&emsp;&emsp;1. Variation 1 Name: Clear List On<br />
		&emsp;&emsp;2. Variation 1 Description: The clear list button is functional<br />
		&emsp;&emsp;3. Variation 2 Name: Clear List Off<br />
		&emsp;&emsp;4. Variation 2 Name: The clear list button is non-functional<br />
	&emsp;c. Rules Section - Add Rule button (in the main Flags / Clear_List section in the new interface)<br />
		&emsp;&emsp;1. Name: Geographic Targeting<br />
		&emsp;&emsp;2. Context Operator: is in<br />
		&emsp;&emsp;3. Context Segments: North American Users<br />
		&emsp;&emsp;4. Serve Rollout: Clear List On<br />
	&emsp;c. Targeting Section (under the on/off toggle in the new interface)<br />
		&emsp;&emsp;1 - When Targeting is Off: Clear List Off<br />
		&emsp;&emsp;2 - Ensure that the Default Rule is to Serve 'Clear List On' when targeting is On and contexts don't match any targeting rules<br />
9 - Running the application<br />
	&emsp;a. In the LD folder run python app.py<br />
	&emsp;b. Open a browser and navigate to http://127.0.0.1:5000/<br />
	&emsp;c. If the Clear_List feature flag is On in LaunchedDarkly then the 'Clear List' button in the application will be functional<br />
	&emsp;d. If the ClearList feature flag is Off in LaunchedDarkly then the 'Clear List' button in the application will not be functional<br />
10 - Assignment details<br />
	&emsp;Part 1 - Feature Flag: This is the flag created in step 5.  It can be toggled on or off via the on/off toggle in Flags/Clear_List<br />
        &emsp;Part 1 - Instant Release/Rollbacks: The listener is enabled in the code and functional<br />
        &emsp;Part 1 - Remediate: This can be done in the <br />
	&emsp;Part 2 - Feature Flag: This is the same feature flag as in part 1, above<br />
 	&emsp;Part 2 - Context Attribute: The user attribute was created in the code, and we then associate it with a segment in step 7.b<br />
   	&emsp;Part 2 - Target: Step 8.c adds targeting is against all users (Brian) in the North American segment.  By default the rule is 'on'.  This can be modified to show alternate behavior by changing Step 8.c.4 to 'Clear List Off' to demonstrate that behavior.  Alternatively, instead of creating a geographic targeting rule in 8.c. an 'individual target' rule can be created.  If doing so, assign user brian to either the 'clear list on' or 'clear list off' section, to have the default behavior against user brian be either having the rule on or off.<br />
