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
9 - Setting up flag triggers<br />
	&emsp;a. Navigate to https://apidocs.launchdarkly.com/tag/Flag-triggers<br />
 	&emsp;b. Scroll down to the 'Create Flag Trigger' section and click 'Try it'.  Fill out the settings as follows:<br />
		&emsp;&emsp;1 - Security.<br />
  			&emsp;&emsp;&emsp;a - An access token must be created.  Go to your LaunchDarkly interface and go into the global settings.  Once there, go to 'Security'.  Scroll down to 'Access Tokens' and click 'Create token.'  Give your token a description and set the role to 'Admin', then click 'save token'.  Once the token is created copy the key, and paste it into the 'Security' section of the 'Create Flag Trigger' API<br />
  		&emsp;&emsp;2 - Body.  Change turnFlagOn to turnFlagOff.<br />
  		&emsp;&emsp;3 - Parameters.  Change turnFlagOn to turnFlagOff.<br />
  			&emsp;&emsp;&emsp;a - projectKey.  Go to your LaunchDarkly interface and go into the global settings.  Once there, go to 'Projects'.  Under your environment name you should see the projectKey.  By default it is 'default'.<br />
  			&emsp;&emsp;&emsp;b - environmentKey.  In the 'Projects' section click on the environment name.  This will take you to the 'Environments' section.  Once there you can see all environments (by default there is Production and Test).  Under each environment name is the environmentKey.  Use the appropriate key, based on which environment you are utilizing.  For example, if using the Production enviornment, by default the environmentKey is 'production'.<br />
  			&emsp;&emsp;&emsp;c - featureFlagKey.  In the main LaunchDarkly dashboard go to 'Flags' and highlight your flag.  A dropdown menu should appear to the right - click on it and select 'Copy Key'.   This is your featureFlagKey.<br />
 	&emsp;c. Click 'Send'.  In the response copy the triggerURL - this is the unguessable URL that can be used to execute the trigger.<br />
10 - Setting up an experiment<br />
	&emsp;a. In the LaunchDarkly interface click on 'Metrics', then 'Create Metric' and fill out the following:<br />
  		&emsp;&emsp;1 - Name:  Testing<br />
  		&emsp;&emsp;2 - Description:  A test page view metric.<br />
  		&emsp;&emsp;3 - Event Information: select Page View'<br />
  		&emsp;&emsp;4 - Target type: Simple match<br />
  		&emsp;&emsp;5 - Target URL: http://127.0.0.1:5000/<br />
  		&emsp;&emsp;6 - Leave all other parameters as the default, and select 'Create metric'<br />
	&emsp;b. In the LaunchDarkly interface click on 'Experiments', then 'Create Experiment' and fill out the following:<br />
  		&emsp;&emsp;1 - Name:  Test<br />
  		&emsp;&emsp;2 - Hypothesis:  Leaving the flag on will result in more page views.<br />
  		&emsp;&emsp;3 - Experiment type: Feature change<br />
  		&emsp;&emsp;4 - Randomization unit: leave as user<br />
  		&emsp;&emsp;5 - Attribute: select 'name'<br />
  		&emsp;&emsp;6 - Select Metrics: Select 'Testing' (the metric created in step 10.a)<br />
  		&emsp;&emsp;7 - Choose flag variations: Select 'Clear_List' (the flag created in step 5.a)<br />
  		&emsp;&emsp;8 - Set audience: Select geographic targeting (the segment created in step 7), and select 'Finish'<br />
11 - Running the application<br />
	&emsp;a. In the LD folder run python app.py<br />
	&emsp;b. Open a browser and navigate to http://127.0.0.1:5000/<br />
	&emsp;c. If the Clear_List feature flag is On in LaunchedDarkly then the 'Clear List' button in the application will be functional<br />
	&emsp;d. If the ClearList feature flag is Off in LaunchedDarkly then the 'Clear List' button in the application will not be functional<br />
12 - Assignment details<br />
	&emsp;Part 1 - Feature Flag: This is the flag created in step 5.  It can be toggled on or off via the on/off toggle in Flags/Clear_List<br />
        &emsp;Part 1 - Instant Release/Rollbacks: The listener is enabled in the code and functional<br />
	&emsp;Part 1 - Remediate: The Trigger created in step 9.c can be executed in a command prompt via the following command: curl -X POST triggerURL -H "Content-Type: application/json" .  Replace triggerURL with the URL generated in step 9.c.<br />
	&emsp;Part 2 - Feature Flag: This is the same feature flag as in part 1, above<br />
 	&emsp;Part 2 - Context Attribute: The user attribute was created in the code, and we then associate it with a segment in step 7.b<br />
   	&emsp;Part 2 - Target: Step 8.c adds targeting is against all users (Brian) in the North American segment.  By default the rule is 'on'.  This can be modified to show alternate behavior by changing Step 8.c.4 to 'Clear List Off' to demonstrate that behavior.  Alternatively, instead of creating a geographic targeting rule in 8.c. an 'individual target' rule can be created.  If doing so, assign user brian to either the 'clear list on' or 'clear list off' section, to have the default behavior against user brian be either having the rule on or off.<br />
	&emsp;Extra Credit - Feature Flag: This is the same feature flag as in part 1, above<br />
 	&emsp;Extra Credit - Metrics: See step 10.a<br />
   	&emsp;Extra Credit - Experiment: See step 10.b<br />
       	&emsp;Extra Credit - Measure: As configured the metric in step 10.a cannot collect data as the target URL (step 10.a.5) is not externally accessible.<br />
